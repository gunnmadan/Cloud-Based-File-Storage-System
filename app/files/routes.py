from flask import Blueprint, request, jsonify, render_template, redirect
from flask_login import login_required, current_user
from ..models import File, FileShare, db
from ..services.google_drive import GoogleDriveService
from datetime import datetime, timedelta
import uuid


files = Blueprint('files', __name__)
drive_service = GoogleDriveService('credentials.json')

@files.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')

    if 'file' not in request.files:
        return render_template('upload.html', error="No file provided")

    file = request.files['file']
    if file.filename == '':
        return render_template('upload.html', error="No file selected")

    try:
        file_content = file.read()
        drive_file_id = drive_service.upload_file(
            file_content,
            file.filename,
            file.content_type
        )

        new_file = File(
            filename=file.filename,
            drive_file_id=drive_file_id,
            mime_type=file.content_type,
            size=len(file_content),
            user_id=current_user.id
        )
        db.session.add(new_file)
        db.session.commit()

        return redirect(url_for('files.list_files'))

    except Exception as e:
        return render_template('upload.html', error=str(e))

@files.route('/download/<int:file_id>', methods=['GET'])
@login_required
def download_file(file_id):
    file = File.query.get_or_404(file_id)
    
    if file.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        file_content = drive_service.download_file(file.drive_file_id)
        return file_content, 200, {
            'Content-Type': file.mime_type,
            'Content-Disposition': f'attachment; filename={file.filename}'
        }
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@files.route('/api/share/<int:file_id>', methods=['POST'])
@files.route('/share/<int:file_id>', methods=['GET', 'POST'])
@login_required
def share_form(file_id):
    file = File.query.get_or_404(file_id)

    if file.user_id != current_user.id:
        return render_template('share.html', file=file, error="Unauthorized")

    if request.method == 'POST':
        email = request.form['email']
        expires = int(request.form.get('expires_in_days', 7))

        existing = FileShare.query.filter_by(file_id=file.id, shared_with_email=email).first()
        if existing:
            return render_template('share.html', file=file, message="Already shared", share_link=existing.share_link)

        try:
            share_link = drive_service.create_share_link(file.drive_file_id)

            new_share = FileShare(
                file_id=file.id,
                shared_with_email=email,
                share_link=share_link,
                expires_at=datetime.utcnow() + timedelta(days=expires)
            )
            db.session.add(new_share)
            db.session.commit()

            return render_template('share.html', file=file, message="File shared!", share_link=share_link)

        except Exception as e:
            return render_template('share.html', file=file, error=str(e))

    return render_template('share.html', file=file)


@files.route('/files', methods=['GET'])
@login_required
def list_files():
    files = File.query.filter_by(user_id=current_user.id).all()
    return render_template('files.html', files=files)

<<<<<<< HEAD
from flask import Blueprint, request, jsonify, render_template, redirect
=======
from flask import Blueprint, request, jsonify
>>>>>>> miracle/main
from flask_login import login_required, current_user
from ..models import File, FileShare, db
from ..services.google_drive import GoogleDriveService
from datetime import datetime, timedelta
import uuid

<<<<<<< HEAD

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
=======
files = Blueprint('files', __name__)
drive_service = GoogleDriveService('credentials.json')

@files.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Upload to Google Drive
>>>>>>> miracle/main
        file_content = file.read()
        drive_file_id = drive_service.upload_file(
            file_content,
            file.filename,
            file.content_type
        )

<<<<<<< HEAD
=======
        # Save file metadata to database
>>>>>>> miracle/main
        new_file = File(
            filename=file.filename,
            drive_file_id=drive_file_id,
            mime_type=file.content_type,
            size=len(file_content),
            user_id=current_user.id
        )
        db.session.add(new_file)
        db.session.commit()

<<<<<<< HEAD
        return redirect(url_for('files.list_files'))

    except Exception as e:
        return render_template('upload.html', error=str(e))
=======
        return jsonify({
            'message': 'File uploaded successfully',
            'file_id': new_file.id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
>>>>>>> miracle/main

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

<<<<<<< HEAD
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

=======
@files.route('/share/<int:file_id>', methods=['POST'])
@login_required
def share_file(file_id):
    file = File.query.get_or_404(file_id)
    
    if file.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    email = data.get('email')
    expires_in_days = data.get('expires_in_days', 7)

    try:
        share_link = drive_service.create_share_link(file.drive_file_id)
        
        file_share = FileShare(
            file_id=file.id,
            shared_with_email=email,
            share_link=share_link,
            expires_at=datetime.utcnow() + timedelta(days=expires_in_days)
        )
        
        db.session.add(file_share)
        db.session.commit()

        return jsonify({
            'message': 'File shared successfully',
            'share_link': share_link
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
>>>>>>> miracle/main

@files.route('/files', methods=['GET'])
@login_required
def list_files():
    files = File.query.filter_by(user_id=current_user.id).all()
<<<<<<< HEAD
    return render_template('files.html', files=files)
=======
    return jsonify([{
        'id': f.id,
        'filename': f.filename,
        'size': f.size,
        'created_at': f.created_at.isoformat(),
        'mime_type': f.mime_type
    } for f in files]), 200
>>>>>>> miracle/main

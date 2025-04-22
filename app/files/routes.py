from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models import File, FileShare, db
from ..services.google_drive import GoogleDriveService
from datetime import datetime, timedelta
import uuid


files = Blueprint('files', __name__)
drive_service = GoogleDriveService('credentials.json')

@files.route('/upload', methods=['POST'])
@login_required
def upload_file():

    print("UPLOAD route HIT!")

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Upload to Google Drive
        file_content = file.read()
        drive_file_id = drive_service.upload_file(
            file_content,
            file.filename,
            file.content_type
        )

        # Save file metadata to database
        new_file = File(
            filename=file.filename,
            drive_file_id=drive_file_id,
            mime_type=file.content_type,
            size=len(file_content),
            user_id=current_user.id
        )
        db.session.add(new_file)
        db.session.commit()

        return jsonify({
            'message': 'File uploaded successfully',
            'file_id': new_file.id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@files.route('/share/<int:file_id>', methods=['POST'])
@login_required 
def share_file(file_id):
    print(" DEBUG: current_user.is_authenticated:", current_user.is_authenticated)
    print("DEBUG: current_user.id:", current_user.get_id())

    file = File.query.get(file_id)
    if not file:
        return jsonify({'error': 'File not found'}), 404

    if not hasattr(current_user, 'id') or current_user.id is None:
        return jsonify({'error': 'Unauthorized'}), 401  
    
    if file.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403 

    data = request.get_json()
    email = data.get('email')
    expires_in_days = data.get('expires_in_days', 7)
    existing_share = FileShare.query.filter_by(file_id=file.id, shared_with_email=email).first()
    if existing_share:
        return jsonify({
            'message': 'File already shared',
            'share_link': existing_share.share_link
        }), 200

    share_link = drive_service.create_share_link(file.drive_file_id)

    duplicate_link = FileShare.query.filter_by(share_link=share_link).first()
    if duplicate_link:
        return jsonify({
            'message': 'File already shared (via reused link)',
            'share_link': duplicate_link.share_link
        }), 200
 
    try:
        
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

@files.route('/files', methods=['GET'])
#@login_required
def list_files():
    files = File.query.filter_by(user_id=1).all()
    return jsonify([{
        'id': f.id,
        'filename': f.filename,
        'size': f.size,
        'created_at': f.created_at.isoformat(),
        'mime_type': f.mime_type
    } for f in files]), 200
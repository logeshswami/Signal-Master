from flask import request , jsonify , Blueprint,send_file
import os
from flask_cors import CORS

download_logs_bp = Blueprint("download_logs",__name__)
CORS(download_logs_bp)
import zipfile
from io import BytesIO



@download_logs_bp.route('/download_logs', methods=['GET'])
def download_logs():
    logs_folder = 'logs'
    # create zip buffer 
    zip_buffer = BytesIO()
    #create zip in ram
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(logs_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, logs_folder))

    # move to start
    zip_buffer.seek(0)
    response = send_file(zip_buffer, as_attachment=True, download_name='traffic_logs.zip')    
    return response



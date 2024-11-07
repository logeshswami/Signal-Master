from flask import request , jsonify , Blueprint
import threading 
from utils.arial_anpr import run_arial_anpr
from flask_cors import CORS
import os

arial_anpr_bp = Blueprint("arial_anpr", __name__)
CORS(arial_anpr_bp)

video_path = os.path.join(os.path.dirname(__file__), '..', 'assets',"traffic_1.mp4")

def start_arial_anpr():
    thread = threading.Thread(target=run_arial_anpr, args=(video_path,))
    thread.start()

@arial_anpr_bp.route("/arial_anpr",methods = ["GET"])
def arial_anpr():
    start_arial_anpr()
    return {"message":" arial anpr executed successfully"}

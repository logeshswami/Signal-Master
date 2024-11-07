from flask import request , jsonify , Blueprint
from utils.anpr import run_anpr
import threading
from flask_cors import CORS
import os

anpr_bp = Blueprint("anpr",__name__)
CORS(anpr_bp)
video_path = os.path.join(os.path.dirname(__file__), '..', 'assets',"demo.mp4")

def start_anpr():
    thread = threading.Thread(target=run_anpr, args=(video_path,))
    thread.start()

@anpr_bp.route("/anpr",methods = ["GET"])
def anpr():
    start_anpr()
    return {"message":"anpr executed successfully"}

from flask import request , jsonify , Blueprint
from utils.vehicle_tracker import track
import threading
from flask_cors import CORS
import os

tracking_bp = Blueprint("vehicle_tracking",__name__)
CORS(tracking_bp)

video_path = os.path.join(os.path.dirname(__file__), '..', 'assets',"traffic.mp4")

def tracking(video_path):
    thread = threading.Thread(target=track, args=(video_path,))
    thread.start()

@tracking_bp.route("/track_vehicle" , methods = ["GET"])
def tracker():
    tracking(video_path=video_path)
    return jsonify({"message" : "tracking done successfully"})
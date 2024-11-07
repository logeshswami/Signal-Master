from flask import request , jsonify , Blueprint
import os
from flask_cors import CORS

shutdown_bp = Blueprint("shutdown",__name__)
CORS(shutdown_bp)

@shutdown_bp.route("/shutdown" , methods = ["GET"])
def shutdown():
    print("controller terminated successfully")
    os._exit(0)
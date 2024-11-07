from flask import Flask
from flask_cors import CORS
import os
from views.traffic_signal_view  import traffic_signal_bp
from views.shutdown_view import shutdown_bp
from views.anpr_view import anpr_bp
from views.vehicle_tracking_view import tracking_bp
from views.arial_anpr_view import arial_anpr_bp
from views.download_logs_view import download_logs_bp

app = Flask(__name__)
CORS(app)

#regestering blueprints for different views  
app.register_blueprint(traffic_signal_bp)
app.register_blueprint(shutdown_bp)
app.register_blueprint(anpr_bp)
app.register_blueprint(tracking_bp)
app.register_blueprint(arial_anpr_bp)
app.register_blueprint(download_logs_bp)


if __name__ == '__main__':
    app.run(debug=True)
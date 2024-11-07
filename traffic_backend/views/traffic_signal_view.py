from flask import request , jsonify , Blueprint
import os
import json
import threading
import time
import math
from utils.calculate_density import calc_density
from utils.logger import start_logger_thread
from flask_cors import CORS

#CREATING BLUE PRINT FOR TRAFFIC SIGNAL
traffic_signal_bp = Blueprint("traffic_signal",__name__)
CORS(traffic_signal_bp)




# Default values of signal times
defaultRed = 150
defaultYellow = 5
defaultGreen = 10
defaultMinimum = 10
defaultMaximum = 70

signals = []
noOfSignals = 4
noOfLanes = 2
currentGreen = 0
nextGreen = (currentGreen+1) % noOfSignals
currentYellow = 0  # yellow on or off
densityScore = 0 

# avg time for vehicle to pass signal
carTime = 2
twoWheelerTime = 1
threeWheelerTime = 2.25
busTime = 2.5
truckTime = 2.5

detectionTime = 7

speeds = {'car': 2.25, 'bus': 1.8, 'truck': 1.8, 'tri-wheeler': 2, 'two-wheeler': 2.5}

resource_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
ip_feed = [resource_dir+r'\traffic.mp4',
           resource_dir+r'\traffic_3.mp4',
           resource_dir+r'\traffic_1.mp4',
           resource_dir+r'\traffic_2.mp4'
           ]
print(ip_feed)

# Get density from the video feed of a particular direction
def get_density(direction):
    densities = calc_density(ip_feed[direction])
    print(f"Detected densities at direction {direction}: {densities}")
    return densities

class TrafficSignal:
    def __init__(self, red, yellow, green, minimum, maximum):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.minimum = minimum
        self.maximum = maximum
        self.totalGreenTime = 0

class TrafficSignalController:
    def __init__(self):
        self.running = False
        self.thread = None
        self.density_logger = None
        self.signal_logger = None

    # Start the traffic signal controller
    def start(self):
        global signals
        for i in range(noOfSignals):
            ts = TrafficSignal(defaultRed, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
            signals.append(ts)
        signals[1].red = 25
        self.running = True
        self.paused = False
        self.thread = threading.Thread(target=self.run_signal_cycle)
        self.density_logger , self.signal_logger = start_logger_thread()
        #logging during start
        self.density_logger.info(f"Signal{currentGreen+1} ,Density: NA, Green Time Set: {defaultGreen} seconds")
        self.signal_logger.info(f"Signal  started ")
        #start the signal thread
        self.thread.start()

    # Stop the traffic signal controller
   
    def stop(self):
        self.paused = True
        self.signal_logger.info(f"Signal {currentGreen+1} stopped")
        print("Traffic signal paused")
    
    def resume(self):
        if self.paused :
            self.paused = False
            self.signal_logger.info(f"Signal {currentGreen+1} resumed")
            print("Traffic signal resumed")
    # Set new green time based on traffic density
    def set_time(self, currentGreen, nextGreen):
        global carTime, twoWheelerTime, busTime, truckTime, threeWheelerTime, defaultMinimum, defaultMaximum,densityScore
        densities = get_density(nextGreen)
        noOfCars = densities['car']
        noOftwoWheeler = densities['two-wheeler']
        noOfBuses = densities['bus']
        noOfTrucks = densities['truck']
        noOfThreeWheeler = densities['tri-wheeler']
        densityScore = ((noOfCars * carTime) +
                               (noOfThreeWheeler * threeWheelerTime) +
                               (noOfBuses * busTime) +
                               (noOfTrucks * truckTime) +
                               (noOftwoWheeler * twoWheelerTime))
        greenTime = math.ceil(densityScore / noOfLanes)

        if greenTime < defaultMinimum:
            greenTime = defaultMinimum
        elif greenTime > defaultMaximum:
            greenTime = defaultMaximum

        print(f"New green time for direction {nextGreen}: {greenTime} seconds")
        signals[nextGreen].green = greenTime
        #logging density and green time status
        self.density_logger.info(f"Signal{nextGreen+1} ,Density: {densities}, Density Score: {densityScore},Green Time Set: {greenTime} seconds")


    # Function to set new current green and green time based on  input
    def set_current_green_time(self,new_green_signal,new_green_time):
        global currentGreen, nextGreen

        if 0 <= new_green_signal < noOfSignals:
            currentGreen = new_green_signal
            signals[currentGreen].green = new_green_time
            print(f"Updated current green signal to {currentGreen} with green time: {new_green_time} seconds")

            # Reset remaining signal times to default for all signals
            for i in range(noOfSignals):
                signals[i].red = defaultRed
                signals[i].yellow = defaultYellow
                if i != currentGreen:
                    signals[i].green = defaultGreen
            
            # Update nextGreen and adjust its red time
            nextGreen = (currentGreen + 1) % noOfSignals
            signals[nextGreen].red = signals[currentGreen].green + signals[currentGreen].yellow
            signals[currentGreen].red = 0
            
            #logging signal status
            self.signal_logger.info(f"Updated current green signal to {currentGreen+1} with green time: {new_green_time} seconds")
        
        else:
            print(f"Invalid signal number. Please enter a value between 0 and {noOfSignals - 1}.")

    # Print the status of the traffic lights
    def print_status(self):
        for i in range(noOfSignals):
            if i == currentGreen:
                if currentYellow == 0:
                    print(f"GREEN TS{i+1} -> r:{signals[i].red}, y:{signals[i].yellow}, g:{signals[i].green}")
                else:
                    print(f"YELLOW TS{i+1} -> r:{signals[i].red}, y:{signals[i].yellow}, g:{signals[i].green}")
            else:
                print(f"   RED TS{i+1} -> r:{signals[i].red}, y:{signals[i].yellow}, g:{signals[i].green}")
        print()

    def get_status(self):
        status ={}
        for i in range(noOfSignals):
            if i == currentGreen:
                if currentYellow == 0:
                    status[f"TS{i+1}"] = (f"GREEN TS{i+1} -> r:{signals[i].red}, y:{signals[i].yellow}, g:{signals[i].green}")
                else:
                    status[f"TS{i+1}"] = (f"YELLOW TS{i+1} -> r:{signals[i].red}, y:{signals[i].yellow}, g:{signals[i].green}")
            else:
                status[f"TS{i+1}"] = (f"RED TS{i+1} -> r:{signals[i].red}, y:{signals[i].yellow}, g:{signals[i].green}")
           
        return status
    
    def send_timing(self):
        status ={}
        for i in range(noOfSignals):
            individual_signal = {}
            if i == currentGreen:
                status["currentGreen"] = i
                status["nextGreen"] = (i+1)%4
                status["densityScore"] = densityScore
                if currentYellow == 0:
                    individual_signal["active_signal"] = "green"
                else:
                    individual_signal["active_signal"] = "yellow"
            else:
                individual_signal["active_signal"] = "red"
            
            individual_signal["timing"] ={"red":signals[i].red , "yellow":signals[i].yellow,"green":signals[i].green}
            status[f"{i}"] = individual_signal
        return status


    # Update the values of the signals
    def update_values(self):
        global currentGreen, currentYellow
        for i in range(noOfSignals):
            if i == currentGreen:
                if currentYellow == 0:
                    signals[i].green -= 1
                    signals[i].totalGreenTime += 1
                else:
                    signals[i].yellow -= 1
            else:
                signals[i].red -= 1

    # Main cycle for managing signal timings
    def run_signal_cycle(self):
        global currentGreen, currentYellow, nextGreen
        while self.running:
            while signals[currentGreen].green > 0 and not self.paused:
                self.print_status()
                self.update_values()

                if signals[currentGreen].green == detectionTime:
                    thread = threading.Thread(target=self.set_time, args=(currentGreen, nextGreen))
                    thread.start()

                time.sleep(1)
            
            if(self.paused):
                while self.paused:
                    time.sleep(1)
                continue

            # Switch to yellow signal
            currentYellow = 1
            while signals[currentGreen].yellow > 0 and not self.paused:
                self.print_status()
                self.update_values()
                time.sleep(1)

            currentYellow = 0
            signals[currentGreen].green = defaultGreen
            signals[currentGreen].yellow = defaultYellow
            signals[currentGreen].red = defaultRed

            currentGreen = nextGreen
            nextGreen = (currentGreen + 1) % noOfSignals
            signals[nextGreen].red = signals[currentGreen].yellow + signals[currentGreen].green
            signals[currentGreen].red = 0

print(__name__)
if __name__ == "views.traffic_signal_view":
   if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
       print("traffic signal started")
       controller = TrafficSignalController()
       controller.start()
       print("traffic signal is runnig")
  

@traffic_signal_bp.route('/traffic_signal/status',methods = ['GET'])
def status():
    status = controller.get_status()
    return jsonify(status)

@traffic_signal_bp.route("/traffic_signal/send_timing",methods = ["POST"])
def send_timing():
    timing = controller.send_timing()
    return jsonify(timing)


@traffic_signal_bp.route("/traffic_signal/stop",methods = ['POST'])
def stop():
    controller.stop()
    return jsonify({"message":"singal stopped successfully"})


@traffic_signal_bp.route("/traffic_signal/resume" , methods = ["POST"])
def resume():
    controller.resume()
    return jsonify({"message":"signal resumed successfully"})

@traffic_signal_bp.route("/traffic_signal/update_signal", methods = ["POST"])
def update_signal():
    data = request.json
    new_green_signal = data["new_green_signal"]
    new_green_time = data["new_green_time"]
    controller.set_current_green_time(new_green_signal=new_green_signal,new_green_time=new_green_time)
    
    return jsonify({"message":"signal updated successfully"})
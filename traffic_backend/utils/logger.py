import os
import logging
import threading
from datetime import datetime
import time

# Logger Config
def setup_density_logger():
    current_time = datetime.now()
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs', current_time.strftime('%Y-%m-%d'), current_time.strftime('%H'))
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger("DensityLogger")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(os.path.join(log_dir, 'density_with_green_time.log'))
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

    logger.addHandler(file_handler)

    return logger

def setup_signal_logger():
  
    current_time = datetime.now()
    # day and hour folder
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs', current_time.strftime('%Y-%m-%d'), current_time.strftime('%H'))
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("SignalLogger")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(os.path.join(log_dir, 'signal_actions.log'))
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    logger.addHandler(file_handler)

    return logger

def setup_anpr_logger():
    current_time = datetime.now()
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs', current_time.strftime('%Y-%m-%d'), current_time.strftime('%H'))
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger("AnprLogger")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(os.path.join(log_dir, 'anpr.log'))
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

    logger.addHandler(file_handler)

    return logger


def check_and_update_loggers(density_logger, signal_logger):
   
    current_hour = datetime.now().strftime("%H")
    current_day = datetime.now().strftime("%Y-%m-%d")
    while True:
        new_hour = datetime.now().strftime("%H")
        new_day = datetime.now().strftime("%Y-%m-%d")
        
        if new_day != current_day or new_hour != current_hour:
            # close handler
            for handler in density_logger.handlers:
                handler.close()
                density_logger.removeHandler(handler)
            for handler in signal_logger.handlers:
                handler.close()
                signal_logger.removeHandler(handler)

            # reinit for new day or hout
            density_logger = setup_density_logger()
            signal_logger = setup_signal_logger()
            current_hour = new_hour
            current_day = new_day

        time.sleep(60)

def start_logger_thread():
    density_logger = setup_density_logger()
    signal_logger = setup_signal_logger()
    
    logger_thread = threading.Thread(target=check_and_update_loggers, args=(density_logger, signal_logger), daemon=True)
    logger_thread.start()
    print("logger created and started successfully")
    return density_logger, signal_logger


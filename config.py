DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "your_password"
}

MODEL_PATHS = {
    "vehicle_model": "final_sql_model_detect/models/vehicle_detect_v1.pt",
    "plate_model": "final_sql_model_detect/models/plate_detection.pt",
    "char_model": "final_sql_model_detect/models/plate_number_det.pt"
}

VIDEO_PATH = "final_sql_model_detect/car_det_test_v2.mp4"
PIPELINE_SCRIPT = "final_sql_model_detect/pipeline_full_det.py"
PID_FILE = "process.pid"

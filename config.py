DB_CONFIG = {
    "host": "localhost",
    "database": "donem_sonu",
    "port": "5433",
    "user": "postgres",
    "password": "220902"
}

MODEL_PATHS = {
    "vehicle_model": "/Users/tunahanbg/Code/vscode_files/db_donem_sonu/final_sql_model_detect/models/vehicle_detect_v1.pt",
    "plate_model": "/Users/tunahanbg/Code/vscode_files/db_donem_sonu/final_sql_model_detect/models/plate_detection.pt",
    "char_model": "/Users/tunahanbg/Code/vscode_files/db_donem_sonu/final_sql_model_detect/models/plate_number_det.pt"
}

VIDEO_PATH = "/Users/tunahanbg/Code/vscode_files/db_donem_sonu/final_sql_model_detect/car_det_test_v2.mp4"
PIPELINE_SCRIPT = "/Users/tunahanbg/Code/vscode_files/db_donem_sonu/final_sql_model_detect/pipeline_full_det.py"
PID_FILE = "process.pid"

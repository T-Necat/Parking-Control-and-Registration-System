# AI-Powered Parking Management System 🚗

Made with Python, PostgreSQL | MIT License

## 🎯 Overview

A comprehensive parking management system that integrates artificial intelligence for vehicle detection with a robust database management interface. The system automates parking operations through real-time vehicle detection, license plate recognition, and intelligent pricing.

![System Demo](path_to_demo_image_or_gif)

## ✨ Key Features

### 🤖 AI Integration
- Real-time vehicle detection using YOLO architecture
- Automatic license plate recognition
- Vehicle type classification
- Integrated DeepSort tracking

### 📊 Management Features
- Multi-level user access control
- Automated entry/exit tracking
- Dynamic pricing based on vehicle type
- Comprehensive reporting system

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 13+
- CUDA-enabled GPU (recommended)
- Windows/Linux OS

### Quick Start

1. Clone the repository
    ```bash
    git clone https://github.com/T-Necat/Parking-Control-and-Registration-System
    cd parking-ai-system
    ```

2. Set up virtual environment
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    ```

3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

4. Configure database
    ```bash
    python create_database.py
    ```

5. Start the application
    ```bash
    streamlit run apps/main_page.py
    ```

## 🗄️ Database Structure

| Table Name       | Description                       |
|------------------|-----------------------------------|
| roles            | User role definitions             |
| users            | User account information          |
| vehicle_type     | Vehicle categories and pricing    |
| vehicles         | Vehicle registration records      |
| parking_records  | Entry/exit transaction logs       |
| system_info      | System configuration data         |

## 💾 Database Setup

### Prerequisites
Ensure that PostgreSQL is installed on your system before proceeding.

### Installation
To set up the database, run the following commands:
```bash
cd db
python setup_database.py
```

This process will:
- Create the database schema
- Add basic roles
- Create default users
- Define vehicle types

## 📁 Project Structure

```
parking-ai-system/
├── apps/
│   ├── login.py
│   └── main_page.py
├── db/
│   ├── database_schema.sql
│   ├── initial_data.sql
│   └── setup_database.py
├── models/
│   ├── vehicle_detect_v1.pt
│   ├── plate_detection.pt
│   └── plate_number_det.pt
├── config.py
├── requirements.txt
└── README.md
```

## 🔐 Default Access Credentials

| Role    | Username | Password   |
|---------|----------|------------|
| Admin   | admin    | admin123   |
| Manager | manager  | manager123 |

## 🚀 Usage

1. Launch the application using the command:
    ```bash
    streamlit run apps/login.py
    ```
2. Log in with provided credentials
3. Access features based on role permissions:
    - Vehicle monitoring
    - User management
    - Report generation
    - System configuration

## 📊 System Architecture

![System Architecture](path_to_architecture_diagram)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

⭐ Star us on GitHub — it motivates us to make great tools for you!
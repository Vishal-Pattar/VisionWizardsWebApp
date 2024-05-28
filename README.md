# Vision Wizards Web App

VisionWizardsWebApp is a web application designed to demonstrate advanced computer vision capabilities. The application provides functionalities such as person detection, video streaming, and user authentication.

## Features

- **Person Detection:** Real-time detection of people in video streams.
- **Video Streaming:** Stream video from different sources with integrated person detection.
- **User Authentication:** Secure login and user management.
- **Notification System:** Get notifications based on detection events.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Required Python packages (listed in `requirements.txt`)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Vishal-Pattar/VisionWizardsWebApp.git
    cd VisionWizardsWebApp
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    streamlit run app.py
    ```

## Usage

Once the application is running, navigate to `http://localhost:8501` in your web browser to access the web interface.

## Live Demo

Check out our live demo [here](https://visionwizardswebapp.onrender.com).

## Screenshots

### Login Page
![image](https://github.com/Vishal-Pattar/VisionWizardsWebApp/assets/104265753/4b087f25-df66-40e2-937c-5e89e86c00be)
![image](https://github.com/Vishal-Pattar/VisionWizardsWebApp/assets/104265753/84ff81ab-7731-4164-b2e7-56ac6c18fac5)

### Settings Page
![image](https://github.com/Vishal-Pattar/VisionWizardsWebApp/assets/104265753/81d660b8-cf21-45c3-a846-8d0974d83c74)
![image](https://github.com/Vishal-Pattar/VisionWizardsWebApp/assets/104265753/f95b7027-3422-4879-aac2-c4751b4f0194)

### Admin Panel
![image](https://github.com/Vishal-Pattar/VisionWizardsWebApp/assets/104265753/9db50e22-aff8-4d53-9c9a-45113592b797)
![image](https://github.com/Vishal-Pattar/VisionWizardsWebApp/assets/104265753/d45a84ab-5486-408d-b145-df7c2d0af51e)

## Project Structure

- `app.py`: Main application file.
- `notification_system.py`: Handles notifications for detection events.
- `person_detector.py`: Core logic for person detection.
- `requirements.txt`: List of required Python packages.
- `settings_manager.py`: Manages application settings.
- `stream_manager.py`: Handles video stream management.
- `user_auth.py`: Manages user authentication and security.
- `video_stream.py`: Integrates video streaming functionality.
- `models/`: Contains machine learning models for detection.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors
- [Vishal Pattar](https://github.com/Vishal-Pattar)
- [Dhanashri Mirajkar](https://github.com/MirajkarD)
- [Bhaskar Dhuri](https://github.com/bhaskardhuri)
- [Tanaya Varpe](https://github.com/TanayaVarpe22)
- [Gauri Raykar](https://github.com/Gauri24R)

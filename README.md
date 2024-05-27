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
<!--
### Home Page
![Home Page](screenshots/home_page.png)

### Person Detection
![Person Detection](screenshots/person_detection.png)

### User Authentication
![User Authentication](screenshots/user_authentication.png)
-->

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
- [Vishal Pattar](https://github.com/Vishal-Pattar).

# Face-Recognition-Attendance-system

## Description
This Face Recognition Attendance System is a Django-based web application that leverages facial recognition technology to automate the process of marking attendance. The system integrates with RetinaFace for accurate face detection and face recognition for recognition the faces. It allows users to upload group photos, detects faces, and records attendance for each individual. The project uses Django models to manage courses, students, and attendance records efficiently.

## Features

- Facial Recognition: Utilizes RetinaFace and Face_Recognition for robust face detection and recognition.
- Attendance Tracking: Marks attendance automatically based on recognized faces.
- Course Management: Organizes students into courses with comprehensive attendance statistics.
- Downloadable Reports: Provides the ability to download attendance sheets for specific dates and courses.
- Responsive Web Interface: A user-friendly web interface for easy interaction.

## Installation

1. Clone the repository:

   ```bash
   git clonehttps://github.com/chiranjivikeshav/Face-Recognition-Attendance-system.git
2. Navigate to the project directory:

   ```bash
   cd Face-Recognition-Attendance-system
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
3. Apply database migrations:

   ```bash
   python manage.py migrate

## Usage

1. Run the development server:

   ```bash
   python manage.py runserver

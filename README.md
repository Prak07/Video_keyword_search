# Subtitle Keyword Search Website

The Subtitle Keyword Search Website is a web application designed to simplify the process of searching specific keywords within video subtitles. This platform allows users to upload video files, search for particular keywords, and provides precise timestamps where the searched subtitles appear. 

## Features

- **Keyword Search**: Search for specific words or phrases within video subtitles.
- **Precise Timestamps**: Get exact timestamps for the occurrences of the searched keywords.
- **Fast Processing**: Optimized backend ensures the search is completed within 1-2 seconds.
- **File Upload**: Securely upload video files to the platform.
- **Cloud Storage**: Videos are stored on Amazon S3 for reliability and scalability.
- **Background Processing**: Uses Celery for task management to handle file processing without delays.

## Technologies Used

### Backend:
- **Python**: For core logic and backend development.
- **Django**: Framework for building the web application.
- **Celery**: For managing asynchronous tasks.
- **Ccextractor**: To extract subtitles from uploaded video files.
- **Amazon DynamoDB**: To store and manage subtitle keywords efficiently.

### Frontend:
- **HTML, CSS, JavaScript**: For building a responsive and user-friendly interface.

### Deployment:
- **Amazon S3**: For storing video files.
- **Amazon EC2**: For hosting the application.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/subtitle-keyword-search.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd subtitle-keyword-search
   ```
3. **Set up a Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: .\env\Scripts\activate
   ```
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Set up Environment Variables**:
   - Configure AWS credentials for S3 and DynamoDB.
   - Add `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION` to the environment.
6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
7. **Access the Website**:
   Open `http://127.0.0.1:8000` in your browser.

## Usage

1. **Upload a Video**: Navigate to the upload page and select a video file.
2. **Enter a Keyword**: Specify the word or phrase you want to search for.
3. **View Results**: Get a list of timestamps where the keyword appears in the subtitles.

## Deployment

The website is deployed at [https://keysearch.symbitt.in](https://keysearch.symbitt.in) for public use.

## Contributions

This project was solely developed by **Me**, who implemented the subtitle extraction, keyword search functionality, backend logic, and deployment.


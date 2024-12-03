# Project Name

A Django-based web application with PostgreSQL, packaged in Docker, and ready for deployment.


## Requirements

Before you start the application, ensure you have the following installed:

- Docker
- Docker Compose
- Python 3.10+

## Environment Setup

1. **Clone the Repository**  
   Clone the project repository to your local machine:
   ```bash
   git clone https://github.com/abhiguptag22/report_generation.git
   cd report_generation
   ```
2. **Configure the Docker Setup**
Go to the app directory:

    cd app
    
3. **Configure docker-compose.yml**
Edit the ```docker-compose.yml``` file to set up the PostgreSQL database connection. Ensure the environment variables are correctly configured for your database.

4. **Build the Docker Containers**
Run the following command to build and start the Docker containers:

    docker-compose up --build

5. **Access the Application**

The Django application will be available at http://localhost:5000.

You can monitor the Celery tasks at http://localhost:5555.

## API Endpoints
The app provides the following APIs which can be tested using POSTMAN:

1. **POST /assignment/html**
Endpoint to enqueue a task for an HTML report.

Body: JSON data containing the event detail of a student.

    { "namespace": "ns_example", "student_id": "00a9a76518624b02b0ed57263606fc26", "events": [ {"type": "saved_code", "created_time": "2024-07-21 03:04:55.939000+00:00", "unit": "17"}, {"type": "saved_code", "created_time": "2024-07-21 03:05:27.027000+00:00", "unit": "17"}, {"type": "submission", "created_time": "2024-07-21 03:06:53.025000+00:00", "unit": "17"}, {"type": "saved_code", "created_time": "2024-07-21 02:25:17.781000+00:00", "unit": "6"}] }
Returns a json response

    {"task_id": "abcdef123456"}

2. **GET /assignment/html/{task_id}**
Endpoint to get the status of the task.

Returns the status of the task. If the task status is success then returns the html file.

Similar endpoints to handle tasks related to PDF generation.



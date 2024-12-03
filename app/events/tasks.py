from celery import shared_task
import hashlib
import uuid
import time
from xhtml2pdf import pisa
from io import BytesIO
import os
from django.conf import settings


def generate_unique_filename(extension=".pdf"):
    # Generate a random UUID and append it to the file name to ensure uniqueness
    base_filename = uuid.uuid4().hex  # Use UUID to generate a unique filename
    storage_path = os.path.join(settings.MEDIA_ROOT, "pdfs")
    file_path = os.path.join(storage_path, f"{base_filename}{extension}")

    # Check if the file already exists and add a counter if necessary
    counter = 1
    while os.path.exists(file_path):
        new_filename = f"{base_filename}_{counter}{extension}"
        file_path = os.path.join(storage_path, new_filename)
        counter += 1

    return file_path

@shared_task(bind=True, max_retries=5, default_retry_delay=30)  # Retry up to 5 times, 30 seconds between retries
def process_task(self, data, pdf=False):
    # Simulate processing time
    time.sleep(10)
    student_id = data.get("student_id", "N/A")
    events = data.get("events", [])
    sorted_events = sorted(events, key=lambda x: int(x["unit"]))
    unit_alias = {unit: f"Q{idx+1}" for idx, unit in enumerate(sorted(set(int(e["unit"]) for e in sorted_events)))}
    event_order = " -> ".join(unit_alias[int(event["unit"])] for event in events)
    # Construct HTML string
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Task Result</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                color: #333;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                text-align: center;
                color: #4CAF50;
            }}
            .content {{
                font-size: 18px;
                line-height: 1.6;
            }}
            .highlight {{
                font-weight: bold;
                color: #4CAF50;
            }}
        </style>
    </head>
    <body>

        <div class="container">
            <h1>Task Result</h1>
            <div class="content">
                <p><span class="highlight">Student ID:</span> {student_id}</p>
                <p><span class="highlight">Event Order:</span> {event_order}</p>
            </div>
        </div>

    </body>
    </html>
    """
    if pdf:
        storage_path = os.path.join(settings.MEDIA_ROOT, "pdfs")
        os.makedirs(storage_path, exist_ok=True)  # Ensure the directory exists
        
        # Generate a unique filename internally
        file_path = generate_unique_filename(extension=".pdf")

        # Convert HTML to PDF and save
        with open(file_path, "wb") as pdf_file:
            pdf_status = pisa.CreatePDF(BytesIO(html.encode("utf-8")), dest=pdf_file)

        # Return the file path if successful
        if not pdf_status.err:
            return file_path
        else:
            raise ValueError("PDF generation failed.")

    return html

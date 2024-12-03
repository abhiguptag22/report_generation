import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from celery.result import AsyncResult
from .models import Task
from .tasks import process_task
from django.http import FileResponse, Http404, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.html import escape
from json.decoder import JSONDecodeError


@api_view(['POST'])
def gen_html(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = request.data
            if 'student_id' not in data or 'events' not in data:
                return JsonResponse({
                    "error": "Invalid input. 'student_id' and 'events' keys are required.",
                    "status": "error"
                }, status=400)
            # Trigger the Celery task
            task = process_task.delay(data)

            # Save task info to the database
            Task.objects.create(task_id=task.id, status='PENDING', task_type='html')

            # Return a success response with the task ID
            return JsonResponse({"task_id": task.id, "status": "Task created successfully"}, status=201)

        except JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON format.",
                "status": "error"
            }, status=400)
        except Exception as e:
            # Handle errors
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"error": "Invalid request method. Use POST to generate html report."}, status=405)

@api_view(['POST'])
def gen_pdf(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = request.data
            if 'student_id' not in data or 'events' not in data:
                return JsonResponse({
                    "error": "Invalid input. 'student_id' and 'events' keys are required.",
                    "status": "error"
                }, status=400)

            # Trigger the Celery task
            task = process_task.delay(data, pdf=True)

            # Save task info in the database
            Task.objects.create(task_id=task.id, status='PENDING', task_type='pdf')

            # Return the task ID in the response
            return JsonResponse({"task_id": task.id, "status": "Task created successfully"}, status=201)

        except JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON format.",
                "status": "error"
            }, status=400)
            
        except Exception as e:
            # Handle errors 
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"error": "Invalid request method. Use POST to generate pdf report."}, status=405)


def homepage(request):
    tasks = Task.objects.all()
    return render(request, 'events/homepage.html', {'tasks': tasks})

@api_view(['GET'])
def task_details(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, task_id=task_id)
        result = AsyncResult(task_id)

        # Check if the requested URL matches the task type
        if "html" in request.path and task.task_type == "pdf":
            return JsonResponse({
                "error": "Task is of type PDF. Please use the PDF endpoint.",
                "status": "error"
            }, status=400)

        if "pdf" in request.path and task.task_type == "html":
            return JsonResponse({
                "error": "Task is of type HTML. Please use the HTML endpoint.",
                "status": "error"
            }, status=400)


        # Handle task states
        if result.state in ['PENDING', 'STARTED']:
            return JsonResponse({"status": "Task still processing"})

        elif result.state == 'FAILURE':
            task.status = 'FAILED'
            task.save()
            return JsonResponse({"status": "Task Failed"})

        elif result.state == 'SUCCESS':
            task.status = 'COMPLETED'
            task.result = result.result
            task.save()

            # If the task generates a file, include the download link
            if task.task_type == 'pdf' and task.result:
                file_path = task.result
                download_url = f"{request.build_absolute_uri()}?download=true"  # Build download link
                if 'download' in request.GET:
                    try:
                        return FileResponse(
                            open(file_path, 'rb'),
                            content_type='application/pdf',
                            as_attachment=True,
                            filename="Event Order.pdf"
                        )
                    except FileNotFoundError:
                        raise Http404("The requested PDF file was not found.")

                return JsonResponse({
                    "status": "Task Completed",
                    "message": "Your task has been completed successfully.",
                    "download_url": download_url
                })

            return HttpResponse(task.result, content_type="text/html")


        # Default response for unknown states
        return JsonResponse({"status": "Unknown task state"})
    return JsonResponse({"error": "POST method now allowed."}, status=405)


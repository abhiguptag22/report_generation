from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('assignment/html/', views.gen_html, name='generate_html'),
    path('assignment/pdf/', views.gen_pdf, name='generate_pdf'),
    path('assignment/html/<str:task_id>/', views.task_details, name='task_detail_html'),
    path('assignment/pdf/<str:task_id>/', views.task_details, name='task_details_pdf'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


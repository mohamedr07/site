from django.urls import path, re_path
from .views import CvUploadView

urlpatterns = [
    re_path(r'^upload/(?P<filename>[^/]+)$', CvUploadView.as_view()),
]
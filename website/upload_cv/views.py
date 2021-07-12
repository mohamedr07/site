from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from googleapiclient.http import MediaIoBaseUpload
from rest_framework import status
from .google import Create_Service
import io


class CvUploadView(APIView):

    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):

        file_obj = request.data['file']

        client_secret_file = 'website/client2.json'
        api_name = 'drive'
        api_version = 'v3'
        scopes = ['https://www.googleapis.com/auth/drive']

        service = Create_Service(client_secret_file, api_name, api_version, scopes)
        folder_id = '15FHUf7XEQjtqroQPxc87ibuwklG1ZbfS'
        
        cv = io.BytesIO(file_obj.read())

        service.files().create(
            body = {
            'name': file_obj.name,
            'parents': [folder_id]
            },
            media_body = MediaIoBaseUpload(cv, mimetype = 'application/pdf'),
            fields = 'id'
        ).execute() 

        return Response(status=status.HTTP_202_ACCEPTED)
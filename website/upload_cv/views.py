from rest_framework.response import Response
from rest_framework.views import APIView
from googleapiclient.http import MediaIoBaseUpload
from rest_framework import status
from .google import Create_Service
import io, os


class CvUploadView(APIView):


    def put(self, request, format=None):
        
        file_obj = request.data['file']
        file_name, file_ext = os.path.splitext(file_obj.name)

        file_types = {
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.pdf': 'application/pdf'
            }

        allowed_file_type = False
        mime_type = ''

        for key, value in file_types.items():
            print(file_ext)
            print(key)
            print(value)
            print('...............')
            if file_ext == key:
                allowed_file_type = True
                mime_type = value

        if allowed_file_type == False:
            return Response("Error: File type not allowed")

        print(allowed_file_type)
        # print(mime_type)

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
            media_body = MediaIoBaseUpload(cv, mimetype = mime_type),
            fields = 'id'
        ).execute() 

        return Response(status=status.HTTP_202_ACCEPTED)
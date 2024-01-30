import io
from typing import Any, Dict

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from .serializers import FileSerializer


class CreateGoogleDocView(APIView):
    """
    API view для создания документа Google Docs с заданным названием и содержимым.
    """

    def post(self, request: Request) -> Response:
        """
        ::param
        - request (Request): Запрос Django REST Framework.

        ::return
        - Response: Ответ с информацией о созданном документе.
        """
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            data = serializer.validated_data['data']
            folder_id = '1zIEZ37lTH6FPg_JzOnkwgekpKLZFdvI1'

            try:
                credentials = Credentials.from_service_account_file('client_secrets.json')
                service = build('drive', 'v3', credentials=credentials)

                file_metadata: Dict[str, Any] = {
                    'name': name,
                    'mimeType': 'application/vnd.google-apps.document',
                    'parents': [folder_id]
                }
                byte_stream = io.BytesIO(data.encode('utf-8'))
                media = MediaIoBaseUpload(byte_stream, mimetype='text/plain', resumable=True)
                file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

                return Response({"message": "Документ создан", "file_id": file.get('id')})

            except HttpError as error:
                return Response({"error": "Ошибка при создании документа: " + str(error)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


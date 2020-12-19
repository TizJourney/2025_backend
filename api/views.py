from rest_framework import (decorators, response, serializers, status)
from .serializers import VerifyOutputSerializer
from rest_framework.decorators import api_view

@api_view(('GET',))
def verify(request):
    query = request.GET.get('query', '')
    if not query:
        query = 'Тестовая цитата'

    output_data = VerifyOutputSerializer(data={
        'query': query,
        'score': 0,
    })
    output_data.is_valid(raise_exception=True)

    return response.Response(output_data.data, status=status.HTTP_200_OK)



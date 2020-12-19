from rest_framework import (decorators, response, serializers, status)
from .serializers import VerifyOutputSerializer

@decorators.api_view(['GET'])
def verify(request):
    print("Здеся")

    query = request.data.get('query', '')

    output_data = VerifyOutputSerializer(data={
        'query': query,
        'score': 0,
    })

    return response.Response(output_data.data, status=status.HTTP_200_OK)


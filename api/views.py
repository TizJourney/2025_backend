from rest_framework import (decorators, response, serializers, status)
from .serializers import VerifyOutputSerializer, VerifyInputSerializer
from rest_framework.decorators import api_view

@api_view(('GET',))
def verify(request):

    input_data = VerifyInputSerializer(data=request.GET)
    input_data.is_valid(raise_exception=True)

    print(input_data.validated_data)

    output_data = VerifyOutputSerializer(data={
        'query': input_data.validated_data['query'],
        'score': 0,
    })
    output_data.is_valid(raise_exception=True)

    return response.Response(output_data.data, status=status.HTTP_200_OK)



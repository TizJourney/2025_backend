from rest_framework import (decorators, response, serializers, status)
from .serializers import VerifyOutputSerializer, VerifyInputSerializer
from rest_framework.decorators import api_view
from pymystem3 import Mystem
import re

stemmer = Mystem()

def lemmatize(text):
    lemm_list = stemmer.lemmatize(text)
    lemm_text = ''.join(lemm_list).strip('\n')
        
    return lemm_text


def clean(text):
    return ' '.join(re.sub(r'[^а-яё ]', ' ', text.lower()).split())    


@api_view(('GET',))
def verify(request):

    input_data = VerifyInputSerializer(data=request.GET)
    input_data.is_valid(raise_exception=True)

    query = input_data.validated_data['query']
    converted_query = lemmatize(clean(query))


    output_data = VerifyOutputSerializer(data={
        'query': query,
        'converted_query': converted_query,
        'score': 0,
    })
    output_data.is_valid(raise_exception=True)

    return response.Response(output_data.data, status=status.HTTP_200_OK)



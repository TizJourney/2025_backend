from rest_framework import (decorators, response, serializers, status)
from .serializers import VerifyOutputSerializer, VerifyInputSerializer, CitateSerializer
from rest_framework.decorators import api_view
from pymystem3 import Mystem
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from sklearn.metrics.pairwise import cosine_similarity

from .models import Citate


nltk.download('stopwords')

class QueryConverter:
    def __init__(self):
        self.stemmer = Mystem()
        self.stop_words = set(nltk.corpus.stopwords.words('russian'))

    def lemmatize(self, text):
        lemm_list = self.stemmer.lemmatize(text)
        lemm_text = ''.join(lemm_list).strip('\n')

        return lemm_text

    def clean(self, text):
        return ' '.join(re.sub(r'[^а-яё ]', ' ', text.lower()).split())

    def query_transform(self, text):
        return self.lemmatize(self.clean(text))

    def find_similar(self, text, number=10):
        lemmed_text = self.query_transform(text)

        start_of_text = ' '.join(lemmed_text.split(' ')[:3])

        candidate_objects = Citate.objects.prefetch_related('poem').filter(lemmed_line__icontains=start_of_text)
        self.tf_idf = TfidfVectorizer(stop_words=self.stop_words)
        lemmed_class_lines = [item.lemmed_line for item in candidate_objects]
        if not lemmed_class_lines:
            return []

        self.tf_idf_data = self.tf_idf.fit_transform(lemmed_class_lines)

        vectorized_text = self.tf_idf.transform([lemmed_text])

        cosine_similarities = cosine_similarity(
            vectorized_text,  self.tf_idf_data).flatten()
        related_product_indices = cosine_similarities.argsort()[:-number:-1]

        results = []
        for index in related_product_indices:
            slow_index = int(index)
            item = CitateSerializer(instance=candidate_objects[slow_index], context={'score' : cosine_similarities[index]*100})

            results.append(item.data)
        return results


@api_view(('GET',))
def verify(request):

    input_data = VerifyInputSerializer(data=request.GET)
    input_data.is_valid(raise_exception=True)

    query = input_data.validated_data['query']
    citate_number = input_data.validated_data['number']
    
    convert_instance = QueryConverter()
    similar_lines = convert_instance.find_similar(query, citate_number)

    best_score = max(item['score'] for item in similar_lines) if similar_lines else 0
    output_data = {
        'query': query,
        'similar': similar_lines,
        'score': best_score,
    }
    return response.Response(output_data, status=status.HTTP_200_OK)

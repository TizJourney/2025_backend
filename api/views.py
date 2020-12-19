from rest_framework import (decorators, response, serializers, status)
from .serializers import VerifyOutputSerializer, VerifyInputSerializer
from rest_framework.decorators import api_view
from pymystem3 import Mystem
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from sklearn.metrics.pairwise import cosine_similarity

from .models import Poem, Citate


# nltk.download('stopwords')


# class QueryConverter:
#     def __init__(self):
#         self.stemmer = Mystem()
#         self.citate_corpus = pd.read_csv('./data/text_corpus.csv')
#         self.citate_corpus.dropna(inplace=True)

#         stop_words = set(nltk.corpus.stopwords.words('russian'))

#         self.tf_idf = TfidfVectorizer(stop_words=stop_words)

#         self.tf_idf_data = self.tf_idf.fit_transform(
#             self.citate_corpus['lemmed_line']
#         )

#     def lemmatize(self, text):
#         lemm_list = self.stemmer.lemmatize(text)
#         lemm_text = ''.join(lemm_list).strip('\n')

#         return lemm_text

#     def clean(self, text):
#         return ' '.join(re.sub(r'[^а-яё ]', ' ', text.lower()).split())

#     def query_transform(self, text):
#         lemmed_text = self.lemmatize(self.clean(text))
#         print(lemmed_text)
#         vectorized_text = self.tf_idf.transform([lemmed_text])
#         return vectorized_text

#     def find_similar(self, text, number=10):
#         vectorized_text = self.query_transform(text)

#         cosine_similarities = cosine_similarity(
#             vectorized_text,  self.tf_idf_data).flatten()
#         related_product_indices = cosine_similarities.argsort()[:-number:-1]
#         return [
#             {
#                 'citate': self.citate_corpus.iloc[index]['line'],
#                 'author': self.citate_corpus.iloc[index]['author'],
#                 'title': self.citate_corpus.iloc[index]['name'],
#                 'score':  int(cosine_similarities[index]*100)
#             }
#             for index in related_product_indices
#         ]


# convert_instance = QueryConverter()


@api_view(('GET',))
def verify(request):

    input_data = VerifyInputSerializer(data=request.GET)
    input_data.is_valid(raise_exception=True)

    query = input_data.validated_data['query']
    citate_number = input_data.validated_data['number']
    similar_lines = []
    # convert_instance.find_similar(query, citate_number)

    best_score = max(item['score'] for item in similar_lines) or 0
    output_data = VerifyOutputSerializer(data={
        'query': query,
        'similar': similar_lines,
        'score': best_score,
    })
    output_data.is_valid(raise_exception=True)
    return response.Response(output_data.data, status=status.HTTP_200_OK)


@api_view(('GET',))
def init(request):
    csv_text_data = pd.read_csv('./data/poem.csv')
    data = csv_text_data.to_dict(orient='records')
    def cleaned_row(row):
        cleaned = row
        cleaned['date_to'] = int(row['date_to']) if not np.isnan(
            row['date_to']) else None
        cleaned['date_from'] = int(row['date_from']) if not np.isnan(
            row['date_from']) else None
        return cleaned

    bulk_data = [Poem(**cleaned_row(row)) for row in data]
    items = Poem.objects.bulk_create(
        bulk_data, batch_size=None, ignore_conflicts=True)

    del csv_text_data
    del data

    citate_text_data = pd.read_csv('./data/citate.csv')
    data = citate_text_data.to_dict(orient='records')
    def prepare_citate(row):
        changed = row
        changed['poem_id'] = row['poem']
        del changed['poem']
        return changed

    bulk_data = [Citate(**prepare_citate(row)) for row in data]
    citate_items = Citate.objects.bulk_create(
        bulk_data, batch_size=None, ignore_conflicts=True)

    items = []


    return response.Response(f'Создано {len(items)} записей и {len(citate_items)} цитат', status=status.HTTP_200_OK)

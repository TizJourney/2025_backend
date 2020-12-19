from rest_framework import (decorators, response, serializers, status)
from .serializers import VerifyOutputSerializer, VerifyInputSerializer
from rest_framework.decorators import api_view
from pymystem3 import Mystem
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from sklearn.metrics.pairwise import cosine_similarity


nltk.download('stopwords')


class QueryConverter:
    def __init__(self):
        self.stemmer = Mystem()
        self.citate_corpus = pd.read_csv('./data/text_corpus.csv')
        self.citate_corpus.dropna(inplace=True)

        stop_words = set(nltk.corpus.stopwords.words('russian'))

        self.tf_idf = TfidfVectorizer(stop_words=stop_words)

        self.tf_idf_data = self.tf_idf.fit_transform(
            self.citate_corpus['lemmed_line'])

    def lemmatize(self, text):
        lemm_list = self.stemmer.lemmatize(text)
        lemm_text = ''.join(lemm_list).strip('\n')

        return lemm_text

    def clean(self, text):
        return ' '.join(re.sub(r'[^а-яё ]', ' ', text.lower()).split())

    def query_transform(self, text):
        lemmed_text = self.lemmatize(self.clean(text))
        vectorized_text = self.tf_idf.transform([lemmed_text])
        return vectorized_text

    def find_similar(self, text):
        vectorized_text = self.query_transform(text)
        cosine_similarities = cosine_similarity(
            vectorized_text,  self.tf_idf_data).flatten()
        related_product_indices = cosine_similarities.argsort()[:-4:-1]
        return [
            {
                'citate': self.citate_corpus.loc[index]['line'],
                'score':  int(cosine_similarities[index]*100)
            }
            for index in related_product_indices
        ]


convert_instance = QueryConverter()


@api_view(('GET',))
def verify(request):

    input_data = VerifyInputSerializer(data=request.GET)
    input_data.is_valid(raise_exception=True)

    query = input_data.validated_data['query']

    similar_lines = convert_instance.find_similar(query)


    best_score = max(item['score'] for item in similar_lines) or 0
    output_data = VerifyOutputSerializer(data={
        'query': query,
        'similar': similar_lines,
        'score': best_score,
    })
    output_data.is_valid(raise_exception=True)

    print(output_data.data)

    return response.Response(output_data.data, status=status.HTTP_200_OK)

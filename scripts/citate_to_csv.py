import codecs
import json
import pandas as pd



def main():
    citate_data = pd.read_csv('../data/text_corpus.csv')

    cleaned_citate_data = citate_data.loc[:, ['line', 'lemmed_line']]
    cleaned_citate_data['poem'] = citate_data['index']

    bad_indexes = cleaned_citate_data.query('poem == "index"').index
    cleaned_citate_data.drop(bad_indexes, inplace=True)

    cleaned_citate_data.to_csv('citate.csv', index_label='id')


if __name__ == "__main__":
    main()
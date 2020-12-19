import codecs
import json
import pandas as pd



def main():
    f = codecs.open('text_corpus.json', 'r', 'utf-8' )
    data = json.load(f)
    f.close()    
    print(f'Всего данных: {len(data)}')
    fields_data = [item['fields'] for item in data]
    text_data = pd.DataFrame(
        data=fields_data,
        columns=['author', 'date_from', 'text', 'date_to', 'name']
        )

    text_data.to_csv('poem.csv', index_label='id')

    csv_text_data = pd.read_csv('poem.csv')
    print(f'Всего данных после перезагрузки: {len(csv_text_data)}')

if __name__ == "__main__":
    main()
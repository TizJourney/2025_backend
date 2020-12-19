import pandas as pd
from api.models import Citate

def run():
    citate_text_data = pd.read_csv('./data/citate.csv')
    data = citate_text_data.to_dict(orient='records')
    def prepare_citate(row):
        changed = row
        changed['poem_id'] = row['poem']
        del changed['poem']
        return changed

    bulk_data = [Citate(**prepare_citate(row)) for row in data]
    citate_items = Citate.objects.bulk_create(
        bulk_data, batch_size=100, ignore_conflicts=True)
    print(f'Inserted {len(citate_items)} citates')    


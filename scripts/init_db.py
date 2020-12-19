import pandas as pd
import numpy as np
from api.models import Poem, Citate

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
print(f'Inserted {len(items)} poems')

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
print(f'Inserted {len(citate_items)} citates')    


import pandas as pd
import numpy as np
from api.models import Poem, Citate

def run():
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

    print(f'Inserted {len(items)} poems')



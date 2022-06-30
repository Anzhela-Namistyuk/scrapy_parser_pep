import csv
from collections import Counter
import datetime as dt
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:

    def open_spider(self, spider):
        self.count_status = Counter()

    def process_item(self, item, spider):
        status = item['status']
        self.count_status[status] += 1
        return item

    def close_spider(self, spider):
        date_now = dt.datetime.now()
        date_str = date_now.strftime('%Y-%m-%d_%H-%M-%S')
        results_dir = BASE_DIR / 'results'
        filename = results_dir / f'status_summary_{date_str}.csv'
        total = sum(self.count_status.values())
        with open(filename, mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            writer = csv.writer(f)
            writer.writerows(self.count_status.items())
            f.write(f'Total,{total}\n')

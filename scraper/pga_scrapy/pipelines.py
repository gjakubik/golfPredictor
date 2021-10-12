# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
import os
import re


PWD = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PWD, "..", "..", "data")


def get_valid_filename(s):
    """A little helper function to strip out illegal characters for filenames"""
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


class PgaScrapyPipeline:
    """Scrapy Pipeline class to handle the parsed stat pages"""

    def process_item(self, item, spider):
        year = item.pop('year')

        year_dir = os.path.join(DATA_DIR, year)

        if not os.path.exists(year_dir):
            os.makedirs(year_dir, exist_ok=True)

        stat_group = get_valid_filename(item.pop("stat_group"))
        stat_name = get_valid_filename(item.pop("stat_name"))
        df = pd.read_html(str(item.pop("stat_table")))[0]

        saved_file_name = os.path.join(year_dir, stat_group + "_" + stat_name + '.csv')

        df.to_csv(saved_file_name, index=False)

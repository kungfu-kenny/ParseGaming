# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import json
from uuid import uuid4
from itemadapter import ItemAdapter

from config import DICT_ITEM_FILE

class ParsegamingPipeline:
    def process_item(self, item, spider):
        file_path = DICT_ITEM_FILE[item.name_item]

        #TODO change it here after the adding database modules
        if not os.path.exists(file_path):
            list_id = []
            file_used = []
        else:
            with open(file_path, 'r') as file_old:
                file_used = json.load(file_old)
                list_id = [i['id'] for i in file_used]
        if not item['id'] in list_id:
            dct = dict(item)
            dct["uuid"] = str(uuid4())
            file_used.append(dct)
            with open(file_path, 'w') as file_new:
                file_new.write(
                    json.dumps(
                        file_used, 
                        indent=4
                    )
                )
        return item

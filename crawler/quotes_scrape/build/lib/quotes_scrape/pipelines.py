# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from quotes_scrape.config import *
from quotes_scrape.items import QuotesScrapeItem
import pymysql
import re

class QuotesScrapePipeline(object):
    data_insert_cnt = 0

    def __init__(self):

        try:
            con = pymysql.connect(db_host, db_user, db_password)
            self.cursor = con.cursor()
            self.cursor.execute(
                'CREATE DATABASE IF NOT EXISTS ' + db_name + ' CHARACTER SET utf8 COLLATE utf8_general_ci;')
            self.con = pymysql.connect(db_host, db_user, db_password, db_name, local_infile=1)
            self.cursor = self.con.cursor()

            try:
                create_table = "CREATE TABLE IF NOT EXISTS " + db_data_table + """ (
                                                                                    job_id varchar(250) default null,
                                                                                    quote_text longtext default null,
                                                                                    quote_author longtext default null,
                                                                                    quote_tags longtext default null,
                                                                                    input varchar(250) default null
                                                                                    );"""
                self.cursor.execute(create_table)
            except Exception as e:
                print("Can't create log table :" + str(e))

        except Exception as e:
            print(e)

    def normalize_text(self, text):
        if (type(text)) == str:
            text = re.sub('<[^<]+?>', '', str(text))
            text = re.sub('\s+', ' ', re.sub('\t|\n|\r', ' ', str(text))).strip()
        return text

    def process_item(self, item, spider):
        if isinstance(item, QuotesScrapeItem):
            try:
                field_list = []
                value_list = []
                for field in item:
                    field_list.append((field))
                    value_list.append(str(item[field]).replace("'", "’"))
                value_list = list(map(self.normalize_text, value_list))
                values = "','".join(value_list)
                fields = ','.join(field_list)
                insert_db = "insert into " + db_data_table + "( " + fields + " ) values ( '" + values + "' )"
                self.cursor.execute(insert_db)
                self.con.commit()
                self.data_insert_cnt += 1
                print(f"\rData Inserted...{self.data_insert_cnt}", end='')
            except Exception as e:
                print(e)
        return item

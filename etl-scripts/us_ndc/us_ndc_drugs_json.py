import time
import wget
import psycopg2
import os
from zipfile import ZipFile
import json

from dotenv import load_dotenv
load_dotenv()

# Downloading first file which contain drugs main informations
data_url = 'https://download.open.fda.gov/drug/ndc/drug-ndc-0001-of-0001.json.zip'
data_zip_filename = 'drug-ndc-0001-of-0001.json.zip'
data_filename = 'drug-ndc-0001-of-0001.json'
data_zip = wget.download(data_url, data_zip_filename)

with ZipFile(data_zip, 'r') as zipObj:
    zipObj.extractall()

with open(data_filename, 'r') as data_json:
    data = json.load(data_json)

    try:
        connection = psycopg2.connect('')
        connection.autocommit = True
        cursor = connection.cursor()

        insert_sql = '''
           INSERT INTO "us_ndc"."us_drug_ndc_json" ("drug")
                 VALUES(%s);
        '''

        drugs_count = data['meta']['results']['total']
        i = 1

        for drug in data['results']:
            cursor.execute(insert_sql, (json.dumps(drug),))
            print(str(i) + '/' + str(drugs_count))
            i += 1

    except (Exception, psycopg2.Error) as error:
        if (connection):
            print("Failed to insert record into mobile table", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

os.remove(data_filename)
os.remove(data_zip_filename)

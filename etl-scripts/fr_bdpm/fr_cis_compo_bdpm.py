import wget
import csv
import codecs
import psycopg2
import os

from dotenv import load_dotenv
load_dotenv()

# Downloading first file which contain drugs main informations
data_url = 'http://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_COMPO_bdpm.txt'
data_filename = 'CIS__COMPO_bdpm.txt'
wget.download(data_url, data_filename)

with codecs.open(data_filename, 'rU', 'windows-1254') as data_txt:
    data = csv.reader(data_txt, delimiter='\t')

    try:
        connection = psycopg2.connect('')
        connection.autocommit = True
        cursor = connection.cursor()

        insert_sql = '''
           INSERT INTO fr_bdpm.cis_compo_bdpm
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        '''

        i = 1
        for row in data:
            cursor.execute(insert_sql, row[:-1])
            print(str(i))
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

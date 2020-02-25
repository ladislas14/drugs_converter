import wget
import pandas as pd
import codecs
import datetime

class ETL_france:

    def extract_data(self):
        # Downloading first file which contain drugs main informations
        data_presentation_url = 'http://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_bdpm.txt'
        #data_presentation_filename = './files/france/CIS_bdpm_' + str(int(datetime.datetime.now().timestamp())) + '.txt'
        data_presentation_filename = './files/france/CIS_bdpm_1582624968.txt'
        #wget.download(data_presentation_url, data_presentation_filename)


        # Opening file using the good encoding
        data_presentatioon_doc = codecs.open(data_presentation_filename, 'rU', 'windows-1254')

        # Opening data with pandas, dropping useless columns and setting columns name
        df = pd.read_csv(data_presentatioon_doc, sep='\t', header=None)
        df.drop(columns=[4,5,7,8,9,11], inplace=True)
        df.columns = ['CIS', 'generic_name', 'dosage_form', 'route', 'commercialized', 'brand_name']
        df.set_index('CIS')

        # Downloading second file which contain composition informations
        data_composition_url = 'http://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_COMPO_bdpm.txt'
        #data_composition_filename = './files/france/CIS_COMPO_bdpm_' + str(int(datetime.datetime.now().timestamp())) + '.txt'
        data_composition_filename = './files/france/CIS_COMPO_bdpm_1582624979.txt'
        #wget.download(data_composition_url, data_composition_filename)

        # Opening file using the good encoding
        data_composition_doc = codecs.open(data_composition_filename, 'rU', 'windows-1254')

        # Opening data with pandas, dropping useless columns and setting columns name
        df_composition = pd.read_csv(data_composition_doc, sep='\t', header=None)
        df_composition.drop(columns=[2, 6, 7, 8], inplace=True)
        df_composition.columns = ['CIS', 'pharmaceutical_element', 'active_susbtance_name', 'active_susbtance_strength', 'active_susbtance_strength_reference']
        df_composition.set_index('CIS')
        
        # Joining both dataset on CIS
        print(df_composition.loc['60009573'])
        

    def checking_data_timestamp(self):
        #TODO
        pass


etl_france = ETL_france()
etl_france.extract_data()

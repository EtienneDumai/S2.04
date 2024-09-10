import pandas as pd
import os
import numpy as np
os.chdir('C:\\Cours\\1EreAnnee\\2EmeSemestre\\S2.04\\Fichiers CSV-20240213')
reviews=pd.read_table('reviews.csv',sep=";", index_col=0, encoding='ANSI')
hotes=pd.read_table('hotes.csv',sep=";", index_col=0, encoding='ANSI')
logements=pd.read_table('logements.csv',sep=";", index_col=0, encoding='ANSI')   
capb_communes=pd.read_table('capb-communes-poles.csv',sep=";", index_col=0, encoding='ANSI')

import pandas as pd

"""read in desinv historical data, create ISOz"""

def pull():
    LOC = '/Users/ewanog/Google Drive/SoHSS/Report/Docs/Datasets/desinv.csv'
    desinv = pd.read_csv(LOC)
    desinv.columns = ['div_' + v.lower().replace(' ', '_') for v in desinv.columns]
    desinv['div_uid'] = desinv['div_country_code'] + desinv['div_year'].map(str)

    return desinv

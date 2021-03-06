print('running')

import pandas as pd

from fts_pull import fts
from rw_pull import rw
import sc_pull
import desinv_pull
import dash_pull
import hno_pull
from hcr_pull import hcr

def get_rw(sc):
    r = rw(year = 2005, sc = sc)
    r = r.master_pull()

    rw_cnt = pd.DataFrame(r['rw.uid'].value_counts()).reset_index()
    rw_cnt.columns = ['rw.uid', 'rw.cnt']

    return rw_cnt

def get_fts(sc):
    """get a sc specific dataset and also all sector dataset (incl shelter)"""
    return fts(sc = sc, all_sector=True).get_flow_bdown()

def get_desinv():
    return desinv_pull.pull()

def get_dash():
    return dash_pull.pull()

def get_hno():
    return hno_pull.pull()

def get_hcr():
    r = hcr()
    org = r.group('ref_org_id', 'ref_org_iso3', 'org_')
    dest = r.group('ref_dest_uid', 'ref_dest_iso3', 'dest_')

    return {'org' : org, 'dest' : dest}

def main():
    #get dataz
    sc = sc_pull.pull()

    rw = get_rw(sc = sc)
    fts = get_fts(sc = sc)
    div = get_desinv()
    dash = get_dash()
    hno = get_hno()
    hcr = get_hcr()

    merge_d = { 'rw' : 'rw.uid',
                'fts' : 'sc_fts.uid',
                'div': 'div_uid',
                'dash' : 'dash_uid',
                'hno' : 'hno_uid',
                'hcr_org' : 'org_ref_org_id',
                'hcr_dest': 'ref_ref_dest_uid'
            }

    #merge
    print('merge rw')
    sc = sc.merge(rw, left_on='sc.uid', right_on='rw.uid', how='left')
    print(len(sc))

    print('merge fts')
    sc = sc.merge(fts, left_on='sc.uid', right_on='fts.uid', how='left')
    print(len(sc))

    print('merge div')
    sc = sc.merge(div, left_on='sc.uid', right_on='div_uid', how='left')
    print(len(sc))

    print('merge dash')
    sc = sc.merge(dash, left_on='sc.uid', right_on='dash_uid', how='left')
    print(len(sc))

    print('merge hno')
    sc = sc.merge(hno, left_on='sc.uid', right_on='hno_uid', how='left')
    print(len(sc))

    print('merge hcr_org')
    sc = sc.merge(hcr['org'], left_on='sc.uid', right_on='org_ref_org_id', how='left')
    print(len(sc))

    print('merge hcr_dest')
    sc = sc.merge(hcr['dest'], left_on='sc.uid', right_on='dest_ref_dest_uid', how='left')
    print(len(sc))

    #TODO: wtf? type error for right join
    # #merge
    # for k,v in merge_d.items():
    #     df = globals()[k]
    #     print(type(df))
    #     sc = sc.merge(df, left_on='sc.uid', right_on=v, how='left')
    #
    # #drop
    # for v in merge_d.values():
    #     sc.drop(v, axis=1, inplace=True)

    sc.to_csv('../d0cz/old_out.csv')

main()

# #merge rw
#
#
# #merge fts
# sc = sc.merge(fts, left_on = 'sc.uid', right_on = 'fts.uid', how = 'left')
#
# #merge div
# sc = sc.merge(div, left_on = 'sc.uid', right_on = 'div_uid', how = 'left')
#
# merge dash


# #drop cols
#
# sc.drop('fts.uid', axis = 1)
# sc.drop('div_uid', axis = 1)
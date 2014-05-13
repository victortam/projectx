import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import or_, and_
from sqlalchemy import func
#from sqlalchemy import create_engine
#engine = create_engine('sqlite:///:memory:', echo=True)
#conn = engine.connect()
from dteam.schemas import bi, bizdw, bizdw_v6
from pprint import *
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import random

from datetime import datetime, timedelta

from dteam import datastores
ds = datastores.bi()

MOD_SIZE = 1000

    #s = select([t.c.pk_event_id]).\
    #where(and_(t.c.created >= '2014-03-19', t.c.created <= '2014-03-20'))


def group_by_date_and_count():

    q = select([func.count(s.c.pk_event_id)]).\
        group_by(func.DATE(s.c.created))
    
    case_chunks = []
    for i, row in enumerate(conn.execute(q)):
        if i and i % MOD_SIZE == 0:
            yield case_chunks
            case_chunks = []
        case_chunks.append(row[0])
    yield case_chunks

def group_by_minute_and_count(s,conn):
#def group_by_minute_and_count():


    yes = datetime.now() - timedelta(days=1)
    yes = yes.strftime('%Y-%m-%d')

    tmr = datetime.now() + timedelta(days=1)
    tmr = tmr.strftime('%Y-%m-%d')

    print(yes)

    #q = select([func.count(s.c.pk_event_id), func.MINUTE(s.c.pk_event_id)]).\
    #    where(and_(s.c.created >= '2014-04-01', s.c.created < '2014-04-02')).\
    #    group_by(func.DATE(s.c.created),func.HOUR(s.c.created),func.MINUTE(s.c.created))






    q = select([func.count(s.c.pk_event_id), func.DATE(s.c.created), func.HOUR(s.c.created), func.MINUTE(s.c.created)]).\
        where(and_(s.c.created >= yes, s.c.created < tmr)).\
        group_by(func.DATE(s.c.created), func.HOUR(s.c.created), func.MINUTE(s.c.created))






    #result of query can only be called once so save it to raw
    raw = []
    for i in conn.execute(q):
        raw.append(i)    
    
    
    
    #create a list of lists for all returned columns from select statement
    all_col_list = []
    c = 0
    while c < 4:
        curr_col = []
        for i in raw:
            curr_col.append(i[c])
        all_col_list.append(curr_col)    
        c += 1
    
    #populate a pandas dataframe with the values
    df = pd.DataFrame(all_col_list[0],columns=["sub_count"])
    df['date'] = all_col_list[1]
    df['hour'] = all_col_list[2]
    df['minute'] = all_col_list[3]
    
    df = df.set_index(pd.to_datetime(df.date.astype(str) + 'T' + df.hour.astype(str) + ':' + df.minute.astype(str)))
    df = df['sub_count']
    df = df.resample('T')  
    df = df.fillna(0)
    
    df2 = pd.DataFrame(df,columns=["sub_count"])
    df2[ 'time' ] = df2.index
    
    
    return df2






### MAIN FUNCTIONS:
if __name__ == '__main__':
    engine = ds.bi_engine
    conn = engine.connect()
    s = bizdw_v6.lifecycle_events_subscribes.alias()
    #gen = group_by_date_and_count()
    #gen = group_by_minute_and_count()
    #
    #tmp_list = []
    #for i in gen:
    #    tmp_list.append(i)
    #
    #results = np.array(tmp_list)
    
    df = group_by_minute_and_count(s,conn)
    
    
    assert(False)
    
    
    tmp_list_1 = []
    tmp_list_2 = []
    cum_1 = 0
    cum_2 = 0
    for row_num, i in enumerate(df):
        if row_num < 1440:
        
            cum_1 = cum_1 + i
            tmp_list_1.append(cum_1)
            
        else:
            
            cum_2 = cum_2 + i
            tmp_list_2.append(cum_2)
            
    cumulative_1 = np.array(tmp_list_1) 
    cumulative_2 = np.array(tmp_list_2) 

    diff = []
    for row_num, i in enumerate(cumulative_1):
        try:
            diff.append(cumulative_1[row_num] - cumulative_2[row_num] + random.random())
        except:
            pass
    
    print(diff)
    #plt.plot(cumulative_1)
    #plt.plot(cumulative_2)
    plt.plot(diff)
    plt.show()
    
    conn.close()
    
    
    
    
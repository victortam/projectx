
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

from dteam import datastores
ds = datastores.bi()
from sqlalchemy_test import group_by_minute_and_count
import statsmodels.api as sm



engine = ds.bi_engine
conn = engine.connect()
s = bizdw_v6.lifecycle_events_subscribes.alias()
        
df = group_by_minute_and_count(s,conn)
        
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


#df = pd.DataFrame(diff)
#end = 1900+len(df)
#df.index = pd.Index(sm.tsa.datetools.dates_from_range('2014', '2014'))


arma_mod30 = sm.tsa.ARMA(df, (3,2)).fit()



pred = arma_mod30.predict(str(df.index.values[-1]), '2014-04-03', dynamic=True)

for i in pred:
    diff.append(i)

import cherrypy
import os

from sqlalchemy_test import group_by_minute_and_count

import json


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

from bidding import Bids
import statsmodels.api as sm





STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'rob_static')


b = Bids()

class Root(object):


    
    @cherrypy.expose
    def index(self):
        #self.b = Bids()
        #data = group_by_minute_and_count()
        #print(data)
        #return data
        return open(os.path.join(STATIC_DIR, u'index.html'))


    @cherrypy.expose
    def histogram(self):
        
        engine = ds.bi_engine
        conn = engine.connect()
        s = bizdw_v6.lifecycle_events_subscribes.alias()
        
        df = group_by_minute_and_count(s,conn)
        sub = df['sub_count']
        
        #print(sub)
        
        
        tmp_list_1 = []
        tmp_list_2 = []
        cum_1 = 0
        cum_2 = 0
        for row_num, i in enumerate(sub):
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

        
        
        l = []
        for index, i in enumerate(diff):
            b = []
            b.append(index)
            b.append(i)
            l.append(b)
        
        
        
        
        
            
        self.diff = l

        time = []
        for index, i in enumerate(df['time']):
            if index % 60 == 0:
                b = []
                b.append(index)
                p = str(i).split(" ")[1].split(":")
                b.append(p[0]+":"+p[1])
                time.append(b)
        

        conn.close()
        
        #print(l)
        
        hist_var = json.dumps(dict(title = self.diff, xaxis = time))
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return hist_var.encode('utf8')



    @cherrypy.expose
    def bid(self, a_name):
        cherrypy.session['a_name'] = a_name
        #self.b.add_bid(a_name)
        #b.add_bid(a_name)
        name, vote = b.parse_bid(a_name)
        #current_bids = str(self.b.d)
        current_bids = str(b.d)
        hist_var = json.dumps(dict(raw = current_bids, username = name, uservote = vote))
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return hist_var.encode('utf8') 





cherrypy.config.update({
    #'environment': 'production',
    #'request.show_tracebacks': True,
    #'tools.staticdir.debug': True,
    'log.screen': True,
    #'server.socket_host': '127.0.0.1',
    'server.socket_host': '10.0.32.200',
    #'server.socket_port': 23747,
    'tools.sessions.on': True,
    'tools.encode.on': True,
    'tools.encode.encoding': 'utf-8',
})

#**********************************************************#

config = {
            '/rob_static':
            {'tools.staticdir.on': True,
            'tools.staticdir.dir': STATIC_DIR,
            #'tools.staticdir.dir': '/home/joestox/webapps/freelinreg_static'
            }
}                                                                                                                                                                                

cherrypy.tree.mount(Root(), '/', config=config)
cherrypy.engine.start()

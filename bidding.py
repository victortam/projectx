class Bids():
    
    def __init__(self):
        self.d = {"js":[], "ew":[], "aj":[], "im":[], "jw":[], "zm":[], "vt":[]}
    
    def add_bid(self,name):
        self.d[name] += 1
    
    def parse_bid(self,bid_string):
    	name = bid_string.split(':')[0]
    	vote = bid_string.split(':')[1]

    	self.d[name].append(vote)
    	return name, vote

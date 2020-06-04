import re
from collections import OrderedDict
import CardCommon
from BaseCard import BaseCard
from CardCollection import CardCollection


class CardAttributes:
	def __init__(self, ):
		self.Is = []
		self.Costs = {}
		self.Has = {}

def generate_linear_equation(card):
	pass

def analyze_cost():
	coll = CardCollection.FullCollection("CardData.csv")
	
	coll_by_culture = CardCommon.SortByCulture(coll)
	coll_by_set = CardCommon.SortBySet(coll)
	
	for setnum in coll_by_set:
		for cardnum in coll_by_set[setnum]:
			card = coll_by_set[setnum][cardnum]
			
	
	
	
	
if __name__ == '__main__':
	analyze_cost()
	
	
	 attribute coefficient

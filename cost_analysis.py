import re
from collections import OrderedDict
import CardCommon
from BaseCard import BaseCard
from CardCollection import CardCollection


class CardAttributes:
	def __init__(self, card):
		self.ID = card.image
		self.Name = card.FullTitle()
		self.Is = []
		self.Costs = {}
		self.Has = {}
		
	def __str__(self):
		info = "\n==============="
		info += "\nCardAttributes Data:\n"
		info += f"Name: {self.Name}\n"
		info += f"ID: {self.ID}\n"
		info += f"Is: {self.Is}\n"
		info += f"Costs: {self.Costs}\n"
		info += f"Has: {self.Has}\n"
		info += "===============\n"

		return info

def parse_attributes(card):
	
	attribs = CardAttributes(card)
	
	if card.cardtype == "Companion":
		attribs.Is.append(card.cardtype)
		attribs.Is.append(card.race)
		attribs.Is.append(card.rarity)
		attribs.Is.append(card.setnum)
		
		attribs.Costs["twilight"] = card.twilight
		
		attribs.Has["strength"] = int(card.strength)
		attribs.Has["vitality"] = int(card.vitality)
		attribs.Has["resistance"] = int(card.resistance) if card.resistance else 7
		
		return attribs;
		
	return None

def analyze_cost():
	coll = CardCollection.FullCollection("CardData.csv")
	
	attributes = {}
	
	# coll_by_culture = CardCommon.SortByCulture(coll)
	# coll_by_set = CardCommon.SortBySet(coll)
	
	for card in coll.cards():
		attribs = parse_attributes(card)
		if not attribs:
			continue
			
		attributes[card.image] = attribs
		
		print(attribs)
			
	
	
	
	
if __name__ == '__main__':
	analyze_cost()


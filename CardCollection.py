import re
from collections import OrderedDict
import CardCommon
from BaseCard import BaseCard

class InvalidSetError(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)

class InvalidCardError(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)

class CardCollection():

	def __init__(self, setcoll):
		self.coll = setcoll

		#print(self.coll)
		#print(self.coll.keys())
		#print(type(self.coll))
		#print(type(self.coll[1]))

	def cards(self):
		for setnum in self.coll:
			for card in self.coll[setnum]:
				yield self.coll[setnum][card]

	def cardsinset(self, setnum):
		for card in self.coll[setnum]:
			yield self.coll[setnum][card]
			

	#Attempts to find a card by the given title and subtitle, optionally searching only one set.
	def FindCardByName(self, title, subtitle, suffix=None, setnum=None):
		if setnum != None:
			try:
				setnum = ValidateSetNum(setnum)
			except:
				raise

			for card in self.coll[setnum]:
				if card.title == title and card.subtitle == subtitle:
					if not suffix:
						return card
					elif card.suffix == suffix:
						return card

		#setnum was not provided, so we'll try to search the entire collection
		else:
			for aset in self.coll:
				for card in aset:
					if card.title == title and card.subtitle == subtitle:
						if not suffix:
							return card
						elif card.suffix == suffix:
							return card

		sufstr = ""
		if subtitle != "":
			sufstr = ", %s" %(subtitle)
		if suffix != "":
			sufstr += suffix
		if setnum is not None:
			sufstr += " in set %i" %(setnum)
		raise InvalidCardError("Cannot find card %s" %(sufstr))


	#Attempts to find a given card number within the given set.
	def FindCardByNumber(self, setnum, cardnum):
		try:
			CardCollection.ValidateCardNum(setnum, cardnum)
		except:
			raise

		return self.coll[setnum].get(cardnum)


	#this is the standard constructor to use.	Sets up a CardCollection with all 3500 cards
	@classmethod
	def FullCollection(cls, csv):
		cards = CardCollection.GetCollectionFromFile(csv)
		coll = cls(CardCommon.SortBySet(cards))
		
		# text = ""
		# for card in cards:
		# 	text += card.image + "\n"
			
		# writefile("test1.txt", text)
		
		# text = ""
		# for setnum in coll.coll:
		# 	print(f"{setnum}: {len(coll.coll[setnum])}")
			
		# 	for cardnum in coll.coll[setnum]:
		# 		card = coll.coll[setnum][cardnum]
		# 		#print(card)
		# 		text += card.image + "\n"

		# writefile("test2.txt", text)
		return coll


	#sets up a CardCollection with all tengwar removed (useful for LDC conversion)
	@classmethod
	def NonTengwar(cls, csv):
		cards = CardCollection.GetCollectionFromFile(csv)
		cards = CardCollection.FilterCollection(cards, ["(T)"])
		return cls(CardCollection.SortBySet(cards))


	#sets up a CardCollection with all suffixed cards removed (except for those in the static whitelist).
	# This is most useful for analysis, since most duplicate cards are removed in this process (but it
	# leaves cards reprinted across multiple normal sets, which is desired behavior).
	@classmethod
	def NoDupes(cls, csv):
		cards = CardCollection.GetCollectionFromFile(csv)
		cards = CardCollection.FilterCollection(cards, CardCollection.SUFFIXES, whitelist=CardCollection.WHITELIST)
		return cls(CardCollection.SortBySet(cards))

	@staticmethod
	#pulls a collection from the master CardData.csv at the location provided.	
	def GetCollectionFromFile(csv):
		cards = []

		if csv == "":
			csv = "CardData.csv"

		with open(csv, "r") as f:
			total = f.read()
			print(total.count('\n'))
			lines = total.splitlines()
			for line in lines:
				tokens = line.split("\t")
				#hack to ignore the initial row that has the names of all the columns
				if tokens[0] == "Name":
					continue

				card = BaseCard.fromCSVRow(tokens)

				cards.append(card)
		
		print(len(cards))
		return cards










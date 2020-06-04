import re
from collections import OrderedDict


SUFFIXES =	[
							"(P)",
							"(T)",
							"(M)",
							"(AI)",
							"(F)",
							"(O)",
							"(H)",
							"(AFD)",
							"(SPD)",
							"(D)",
							"(W)",
						]

WHITELIST = [ 
							("Ghan-buri-Ghan", "Chieftain of the Woses"),
							("Radagast's Staff", ""),
							("Anarion", "Lord of Anorien"),
							("Erkenbrand", "Master of Westfold"),
							("Tom Bombadil's Hat", ""),
							("Arwen", "Maiden of Rivendell")
						]	

TENGWAR_COUNT = {
									1: 15,
									2: 3,
									4: 14,
									5: 4,
									6: 1,
									7: 7,
									8: 6,
									10: 5,
									11: 6,
									12: 5,
									13: 7
								}

MAX_SET = 19

SET_NAMES = {
							0: "Promotional",
							1: "Fellowship of the Ring",
							2: "Mines of Moria",
							3: "Realms of the Elf-Lords",
							4: "The Two Towers",
							5: "Battle of Helm's Deep",
							6: "Ents of Fangorn",
							7: "Return of the King",
							8: "Siege of Gondor",
							9: "Reflections",
							10: "Mount Doom",
							11: "Shadows",
							12: "Black Rider",
							13: "Bloodlines",
							14: "Expanded Middle-Earth",
							15: "The Hunters",
							16: "The Wraith Collection",
							17: "Rise of Saruman",
							18: "Treachery & Deceit",
							19: "Age's End",
						}

SET_COUNT =	 {
								0: 163,
								1: 383,
								2: 129,
								3: 124,
								4: 381,
								5: 134,
								6: 132,
								7: 372,
								8: 128,
								9: 52,
								10: 127,
								11: 290,
								12: 226,
								13: 228,
								14: 15,
								15: 224,
								16: 6,
								17: 175,
								18: 167,
								19: 40
							}

SET_NUMBERS = {
									"Promotional": 0,
									"Promo": 0,
									"Fellowship of the Ring": 1,
									"FellowshipoftheRing": 1,
									"FellowshipOfTheRing": 1,
									"Mines of Moria": 2,
									"MinesofMoria": 2,
									"MinesOfMoria":2,
									"Realms of the Elf-Lords": 3,
									"Realms of the Elf-lords": 3,
									"RealmsoftheElfLords": 3,
									"RealmsoftheElflords": 3,
									"RealmsOfTheElfLords": 3,
									"The Two Towers": 4,
									"TheTwoTowers": 4,
									"Two Towers": 4,
									"TwoTowers": 4,
									"Battle of Helm's Deep": 5,
									"BattleofHelmsDeep": 5,
									"BattleOfHelmsDeep": 5,
									"Ents of Fangorn": 6,
									"EntsofFangorn": 6,
									"EntsOfFangorn": 6,
									"Return of the King": 7,
									"ReturnoftheKing": 7,
									"ReturnOfTheKing": 7,
									"Siege of Gondor": 8,
									"SiegeofGondor": 8,
									"SiegeOfGondor": 8,
									"Reflections": 9,
									"Mount Doom": 10,
									"MountDoom": 10,
									"Shadows": 11,
									"Black Rider": 12,
									"BlackRider": 12,
									"Bloodlines": 13,
									"Expanded Middle-Earth": 14,
									"Expanded Middle-earth": 14,
									"ExpandedMiddleEarth": 14,
									"ExpandedMiddleearth": 14,
									"The Hunters": 15,
									"TheHunters": 15,
									"Hunters": 15,
									"The Wraith Collection": 16,
									"TheWraithCollection": 16,
									"Wraith Collection": 16,
									"WraithCollection": 16,
									"Rise of Saruman": 17,
									"RiseofSaruman": 17,
									"RiseOfSaruman": 17,
									"Treachery & Deceit": 18,
									"Treachery and Deceit": 18,
									"Treachery&Deceit": 18,
									"TreacheryandDeceit": 18,
									"TreacheryAndDeceit": 18,
									"Age's End": 19,
									"Ages End": 19,
									"AgesEnd": 19,
							}






def GetSetName(setnum):
	return CardCollection.SET_NAMES.get(setnum, "")

def GetSetNumber(setname):
	return CardCollection.SET_NUMBERS.get(setname, -1)


# used to take an unorganized list of cards and organize them in an ordereddict
# by culture.	Each culture is its own key.
 
def SortByCulture(cards, split=False):
	foundcultures = {}

	for card in cards:
		if card.culture in foundcultures:
			foundcultures[card.culture][card.CollInfo()] = card
		else:
			newdic = OrderedDict()
			newdic[card.CollInfo()] = card
			foundcultures[card.culture] = newdic

	final = OrderedDict()

	#order of cards: the one ring cards, then all normal cultures in alphabetic order, then sites

	onering = foundcultures.pop("The One Ring", None)
	sites = foundcultures.pop("Site", None)

	if onering:
		final["The One Ring"] = onering

	for k in sorted(foundcultures):
		#sometimes for analysis purposes it's better to differentiate between FP gollum and shadow gollum
		if split and k == "Gollum":
			smeagol = OrderedDict()
			gollum = OrderedDict()
			for cardnum in foundcultures[k]:
				card = foundcultures[k][cardnum]
				if card.side == "Free Peoples":
					smeagol[card.CollInfo()] = card
				else: 
					gollum[card.CollInfo()] = card

			if smeagol:
				final["Gollum (Free Peoples)"] = smeagol
			if gollum:
				final["Gollum (Shadow)"] = gollum
		else:
			final[k] = foundcultures[k]

	if sites:
		final["Site"] = sites

	return final


#Takes an unordered list of cards and arranges them by set into an ordereddict 
def SortBySet(cards):
	foundsets = {}
	if not cards:
		return foundsets

	for card in cards:
		if card.setnum in foundsets:
			foundsets[card.setnum][card.cardnum] = card
		else:
			newdic = OrderedDict()
			newdic[card.cardnum] = card
			foundsets[card.setnum] = newdic

	final = OrderedDict()

	for k in sorted(foundsets):
		final[k] = foundsets[k]

	return final
	
#Takes an unordered list of cards and arranges them by set into an ordereddict, but without the set divisions
def SortBySetFlat(cards):
	foundsets = {" ":OrderedDict()}
	if not cards:
		return foundsets

	for card in cards:
		foundsets[" "][card.CollInfo()] = card

	final = OrderedDict()

	for k in sorted(foundsets):
		final[k] = foundsets[k]

	return final


#Takes a card list and returns a new list with all suffixes in cull removed, while sparing (title, subtitle)
# tuples in whitelist
def FilterCollection(cards, cull, whitelist=None):
	if cards == None:
		cards = CardCollection.GetCollectionFromFile("CardData.csv")

	toremove = []
	for card in cards:
		if card.suffix in cull:
			toremove.append(card)

	if whitelist:
		for tup in whitelist:
			title = tup[0]
			sub = tup[1]

			for card in toremove:
				if card.title == title and card.subtitle == sub:
					toremove.remove(card)

		for reject in toremove:
			cards.remove(reject)
	
	return cards


def ConvertSet(setnum):
	#first assume that setnum was instead sent as a string.	Two ways to interpret, either
	# an int cast as a string or the set's name

	#assume the set name first:
	num = CardCollection.SET_NUMBER.get(str(setnum), -1)
	#not the set name, assume a cast string:
	if num == -1:
		try:
			num = int(setnum)
			setnum = num
		except:
			#some string that's not a cast int nor a set name
			raise InvalidSetError("Invalid set name: %s" %(setnum))
	else:
		#setnum was a string that turned out to be a set name
		setnum = num

	return setnum

def ValidateSetNumber(setnum):
	#checks if the set number passed is a valid set number
	if setnum > MAX_SET or setnum < 0:
		raise InvalidSetError("Invalid set number: %i" %(setnum))

	return setnum


#checks the given card number within the given set, returns True if it's valid, otherwise
# throws either an InvalidSetError or InvalidCardError depending on which is wrong.
def ValidateCardNumber(setnum, cardnum):
	try:
		ValidateSetNumber(setnum)
	except:
		raise

	try:
		setnum = int(setnum)
	except:
		setnum = setnum[:-1]
		try:
			setnum = int(setnum)
		except:
			raise InvalidCardError("Invalid card number: %i in set number: %i" %(cardnum, setnum))

	#get the largest card number for a given set
	maxnum = CardCollection.SET_COUNT.get(setnum, 0)

	#checks if the card number is valid
	if cardnum < 1 or cardnum > maxnum:
		raise InvalidCardError("Invalid card number: %i in set number: %i" %(cardnum, setnum))

	return True
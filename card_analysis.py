import re
import CardCommon
from CardCollection import CardCollection





#prints card images in sections organized by whatever the key is, done in a format
# that is supported by dokuwiki, the wiki program used by lotrtcgwiki.com.
def dokuImageLinks(coll):
	
	data = ""

	for key in coll.keys():
		#print(key)
		data += f"\n\n==={key}===\n\n"

		for cardnum in coll[key]:
			card = coll[key][cardnum]
			#print(card)
			data += card.dokuImageLink() + ""

	return data


#prints card names as links in sections organized by whatever the key is, done in a format
# that is supported by dokuwiki, the wiki program used by lotrtcgwiki.com.
def dokuTextLinks(coll, div=0):
	data = ""

	for key in coll.keys():
		#print(key)
		data += f"\n\n==={key}===\n\n"

		for cardnum in coll[key]:
			card = coll[key][cardnum]
			if div > 0:
				data += addDivColumn(card.dokuTextLink(), div)
			else:
				data += card.dokuTextLink() + "\n"
			
	return data


#prints card info in an easily human-readable format to facilitate quick-and-dirty analyses. 
def printInfo(coll):
	data = ""
	for key in coll.keys():
		data += f"\n\n==={key}===\n\n"
		for cardnum in coll[key]:
			card = coll[key][cardnum]
			data += str(card)		
	return data
	
	
def getTableHeader(columns):
	data = "^"
	for key in columns:
		data += f"  {key}  ^"
		
	data += "\n"
	return data
	
def tableEntries(coll, columns, columnNames, repeatHeader=5000):
	data = ""
	
	for key in coll.keys():
		data += f"| {'|' * len(columns)}\n"
		data += f"^  {key}  {'^' * len(columns)}\n"
		data += f"| {'|' * len(columns)}\n"
		data += getTableHeader(columnNames)
		
		rowcount = 0
		for cardnum in coll[key]:
			card = coll[key][cardnum]
			data += card.dokuTextRowEntry(columns) + "\n"
			rowcount += 1
			if rowcount % repeatHeader == 0:
				data += getTableHeader(columnNames)
				
	data += "\n"
	return addDivColumn(data, 98)	
	
def getCardTitleList(coll):
	data = ""
	for key in coll.keys():
		for cardnum in coll[key]:
			card = coll[key][cardnum]
			data += f"[{card.image}] {card.FullTitle()}\n"
			
	return data

#jig function, writes a string to file
def writefile(filename, string):
	f = open(filename, 'w')
	f.write(string)
	f.close()

#prints card images in sections organized by whatever the key is, done in a format
# that is supported by dokuwiki, the wiki program used by lotrtcgwiki.com.
def writeImageLinks(filename, coll):
	data = dokuImageLinks(coll)

	writefile(filename, data)


#prints card names as links in sections organized by whatever the key is, done in a format
# that is supported by dokuwiki, the wiki program used by lotrtcgwiki.com.
def writeLinks(filename, coll, div=0):
	data = dokuTextLinks(coll, div=div)
			
	writefile(filename, data)

#prints card info in an easily human-readable format to facilitate quick-and-dirty
# analyses. 
def writeInfo(filename, coll):
	data = printInfo(coll)
	writefile(filename, data)
	
def writeTable(filename, coll, columns, columnNames):
	data = tableEntries(coll, columns, columnNames)
	
	writefile(filename, data)


def writeList(filename, coll):
	data = getCardTitleList(coll)
	
	writefile(filename, data)

#jig function, takes a string and wraps <div> tags around it with a given column percentage.
def addDivColumn (string, columnsize):
	return "<div column " + str(columnsize) + "%>\n" + string + "</div>"
	
def addDiv (string, columnsize):
	return "<div " + str(columnsize) + "%>\n" + string + "</div>\n"


class CardQuery():
	def __init__(self, filename="NONAME.txt", partname = "", columns = [], columnnames = [], sort="culture", query=""):
		self.result = []
		self.queryRegex = query
		self.partName = partname
		self.count = 0
		self.filename = filename
		self.tableColumns = columns
		self.tableColumnNames = columnnames
		self.sort = sort
	
stdCols = ["CollInfo", "TextLink",'FullTypeLine', 'text']
stdColNames = ["#", "Card", "Type", "Game Text"]

signetCols = ["CollInfo", "TextLink",'FullTypeLine', 'signet']
signetColNames = ["#", "Card", "Type", "Signet"]
	
queries = {}

queries["Direct-wound Cards"] = CardQuery("direct_wound", "lowertext", stdCols, stdColNames, "culture", r"(?<!(e than 1|o take a|ent that|vent all|for each| takes a|he first|not take| archery|revent a|m taking| take no|ch other|ards and|urden or|led by a|ens or \d|n spot \d|n spot a|nly take|u spot \d|e threat|ho has x|h time a|ch other| wraith,| up to \d)) wound(?!ed)(?!s may not be removed)")
queries["Prevent Wounds"] = CardQuery("prevent_wound", "lowertext", stdCols, stdColNames, "culture", r"(?<=(e than 1|o take a|ent that|vent all|for each| takes a|he first|not take| archery|revent a|m taking| take no|ch other|ards and|urden or|led by a|ens or \d|n spot \d|n spot a|nly take|u spot \d|e threat|ho has x|h time a|ch other| wraith,| up to \d)) wound")
queries["Characters With Aragorn Signets"] = CardQuery("aragorn_signets", "signet", signetCols, signetColNames, "flat", r"Aragorn")
queries["Characters With Frodo Signets"] = CardQuery("frodo_signets", "signet", signetCols, signetColNames, "flat", r"Frodo")
queries["Characters With Gandalf Signets"] = CardQuery("gandalf_signets", "signet", signetCols, signetColNames, "flat", r"Gandalf")
queries["Characters With Theoden Signets"] = CardQuery("theoden_signets", "signet", signetCols, signetColNames, "flat", r"Theoden")
queries["Signet-targeting abilities"] = CardQuery("signet_abilities", "lowertext", stdCols, stdColNames, "flat", r"signet")
queries["Ring-bound characters"] = CardQuery("ring_bound_characters", "text", stdCols, stdColNames, "culture", r"Ring-bound\.")
queries["Ring-bound abilities"] = CardQuery("ring_bound_abilities", "text", stdCols, stdColNames, "culture", r"[Rr]ing-bound[^\.]")

queries["Valiant characters"] = CardQuery("valiant_characters", "text", stdCols, stdColNames, "culture", r"Valiant\.")
queries["Valiant abilities"] = CardQuery("valiant_abilities", "text", stdCols, stdColNames, "culture", r"[Vv]aliant[^\.]")

queries["Wizards"] = CardQuery("wizard-spotting cards", "lowertext", stdCols, stdColNames, "culture", r"(?<!\[gandalf\] )wizard")

queries["While Triggers"] = CardQuery("while_abilities", "lowertext", stdCols, stdColNames, "culture", r"while")

#do analysis at this point
def analyze():
	coll = CardCollection.FullCollection("CardData.csv")
	#print(coll.coll)
	
	
	debug = True
	ccount = 0
	
	pausecount = 0
	
	sum = 0
	for setnum in coll.coll:
		print(f"{setnum}: {len(coll.coll[setnum])}")
		sum +=len(coll.coll[setnum])
	print(sum)
	
	for card in coll.cards():
		# if card.suffix in suffixes:
		#	 if card.suffix != "":
		#		 suffixes[card.suffix] += 1
		# else:
		#	 if card.suffix != "":
		#		 suffixes[card.suffix] = 1
		
		for query_name in queries:
			query = queries[query_name]
			match = re.search(query.queryRegex, getattr(card, query.partName))
			if match:
				query.count += 1
				query.result.append(card)
				print(f"'{query_name}' found: [{card.image}] {card.FullTitle()}")
		
		#the following regex finds cards that wound, while ignoring cards that affect one's ability to wound.	It seems a shame to delete such a long-ass regex, so it's been immortalized here, just in case.
		#match = re.search(r"(?<!(e than 1|o take a|ent that|vent all|for each| takes a|he first|not take| archery|revent a|m taking| take no|ch other|ards and|urden or|led by a|ens or \d|n spot \d|n spot a|nly take|u spot \d|e threat|ho has x|h time a|ch other| wraith,| up to \d)) wound(?!ed)(?!s may not be removed)", card.text.lower())
		#match = re.search(r"draw an", card.text.lower())
		#match2 = re.search(r"into hand", card.text.lower())

		ccount += 1
		if pausecount != 0 and ccount % pausecount == 0:
			input("press enter to continue")
		#if match:
		#if match and card.side == "Free Peoples" and (card.setnum =="01" or card.setnum =="02" or card.setnum =="03"):
		#if "helm" in card.text.lower():
			#print (card.printInfo())
			#query.append(card)
			#count += 1

		
		#if count % 10 == 0:
			#input("press enter to continue")

	#for index, item in enumerate(suffixes):
		#print("Set " + str(item) + " has " + str(suffixes[item]) + " cards.\n")
	#print(str(count) + " cards found.")

	

	#for x in sort:
		#print(x[1])

	print("\n\n\n")
		
	for query_name in queries:
		query = queries[query_name]
		print(f"'{query_name}' found {query.count} entries. Exporting to 'output/{query.filename}'...")
		
		setSort = CardCommon.SortBySet(query.result) # CardCommon.SortByCulture(query.result)
		cultureSort = CardCommon.SortByCulture(query.result, True)
		flatSort = CardCommon.SortBySetFlat(query.result)
		#sort = orderbyset(query)
		
		#print(sort)
		
		if(query.sort == "culture"):
			#writeImageLinks(f"output/{query.filename}__imagelinks.txt", cultureSort)
			#writeLinks(f"output/{query.filename}__cardlinks.txt", cultureSort, 23)
			
			writeTable(f"output/{query.filename}__table.txt", cultureSort, query.tableColumns, query.tableColumnNames)
			if debug: 
				writeList(f"output/{query.filename}__debug.txt", cultureSort)
				writeInfo(f"output/{query.filename}__info.txt", cultureSort)
			
		elif(query.sort == "set"):
			#writeImageLinks(f"output/{query.filename}__imagelinks.txt", setSort)
			#writeLinks(f"output/{query.filename}__cardlinks.txt", setSort, 23)
			
			writeTable(f"output/{query.filename}__table.txt", setSort, query.tableColumns, query.tableColumnNames)
			if debug: 
				writeList(f"output/{query.filename}__debug.txt", setSort)
				writeInfo(f"output/{query.filename}__info.txt", setSort)
			
		elif(query.sort == "flat"):
			#writeImageLinks(f"output/{query.filename}__imagelinks.txt", flatSort)
			#writeLinks(f"output/{query.filename}__cardlinks.txt", flatSort, 23)
			
			writeTable(f"output/{query.filename}__table.txt", flatSort, query.tableColumns, query.tableColumnNames)
			if debug: 
				writeList(f"output/{query.filename}__debug.txt", flatSort)
				writeInfo(f"output/{query.filename}__info.txt", flatSort)

if __name__ == '__main__':
	analyze()
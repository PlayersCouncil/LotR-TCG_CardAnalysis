import re
from collections import OrderedDict

import CardCommon

class InvalidCollectionError(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)

#an object that keeps track of all the attributes of a card.
# there is no effort to be efficient with the variables; for instance,
# the signet, site name, and resistance all take the same spot on a card,
# but no effort has been made to consolidate those attributes.  Thus, it
# is very possible that a card will have half of the below attributes 
# blank.  Also, most are strings because of tricky situations like
# +1 strength or -2 vitality or card number of 40T.  Some numbers are
# strings just to "bake in" formatting with leading zeroes and such,
# since math is never really performed on them, just printed.
class BaseCard():
  Collection = None


  def __init__(self, coll=None):
    self.title = ""
    self.subtitle = ""
    self.suffix = ""
    self.set = ""
    self.setnum = ""
    self.image = ""
    self.side = ""
    self.culture = ""
    self.cardtype = ""
    self.race = ""
    self.itemclass = ""
    self.phase = ""
    self.home = ""
    self.twilight = 0
    self.strength = ""
    self.vitality = ""
    self.resistance = ""
    self.signet = ""
    self.site = ""
    self.unique = False
    self.rarity = ""
    self.cardnum = ""
    self.cardnumeral = ""
    self.notes = ""
    self.lore = ""
    self.text = ""
    self.lowertext = ""

    if coll:
      BaseCard.Collection = coll

  #takes a csv row (previously sliced into an array) and puts each part
  # where it need to be.
  
  #  0: Name
  #  1: Set
  #  2: Set #
  #  3: Imagefile 
  #  4: Side  
  #  5: Culture 
  #  6: Type  
  #  7: Twilight  
  #  8: Strength
  #  9: Vitality
  # 10: Resistance  
  # 11: Signet/Site#
  # 12: Unique
  # 13: Rarity
  # 14: Card#
  # 15: Notes
  # 16: Lore
  # 17: Text
  
  @classmethod
  def fromCSVRow(cls, columns):
    card = cls()
    card.title, card.subtitle, card.suffix = cls.titleSlice(columns[0])

    if(len(columns) < 10):
      print(columns[0])
    card.set = columns[1]
    card.setnum = int(columns[2])

    card.image = columns[3]
    card.side = columns[4]
    card.culture = columns[5]

    card.cardtype, card.race, card.itemclass, card.home, card.phase = cls.typeSlice(columns[6])

    card.twilight = columns[7]
    card.strength = columns[8]
    card.vitality = columns[9]
    card.resistance = columns[10]

    if card.side == "Free Peoples" and card.cardtype == "Companion":
      card.signet = columns[11]
    else:
      card.site = columns[11]

    if columns[12] == 'U':
      card.unique = True

    card.rarity = columns[13]
    card.cardnum = columns[14]
    match = re.search(r"\d+", columns[14])
    if(match == None):
      card.cardnumeral = columns[14]
    else:
      card.cardnumeral = match[0]
    card.notes = columns[15]
    card.lore = columns[16]
    card.text = columns[17]
    card.lowertext = card.text.lower()

    return card

  @classmethod
  def FromCardNum(cls, setnum, cardnum, coll=None):
    if coll:
      BaseCard.Collection = coll

    if not BaseCard.Collection:
      raise InvalidCollectionError("No collection provided to search for card in.")

    card = None

    try:
      setnum = CardCollection.ConvertSet(setnum)
      card = CardCollection.FindCardByNumber(setnum, cardnum)
    except:
      raise

    return card


  @classmethod
  def FromCardName(cls, title, subtitle, suffix=None, setnum=None, coll=None):
    if coll:
      BaseCard.Collection = coll

    if not BaseCard.Collection:
      raise InvalidCollectionError("No collection provided to search for card in.")

    card = None

    try:
      if setnum:
        setnum = CardCollection.ConvertSet(setnum)

      Card = CardCollection.FindCardByName(title, subtitle, suffix, setnum)
    except:
      raise

    return card

  #takes the single line of information that contains the Title, Subtitle, and Suffix
  # of a card, and cuts it into its constituent parts.
  @staticmethod
  def titleSlice(fulltitle):
    title = ""
    subtitle = ""
    suffix = ""

    match = re.search(r"\(.*\)", fulltitle)
    
    if match:
      suffix = fulltitle[match.start(0):].strip() #from the starting position of the match to the end of the string
      fulltitle = fulltitle[:match.start(0)-1].strip()

    match = re.search(r", .*$", fulltitle)

    if match:
      subtitle = fulltitle[match.start(0)+2:].strip()
      fulltitle = fulltitle[:match.start(0)].strip() 

    title = fulltitle.strip()

    return title, subtitle, suffix


  #takes the type line that can contain Race, Item Class, Card Type, and/or Home Site
  # and cuts it into its contituent parts.
  @staticmethod
  def typeSlice(fulltype):
    cardtype = ""
    home = ""
    race = ""
    phase = ""
    itemclass = ""

    if '-' in fulltype:
      subs = fulltype.split('-')

      cardtype = subs[0].strip()

      if cardtype == "Ally":
        home = subs[1].strip()
        if len(subs) >2:
          race = subs[2].strip()
      elif cardtype == "Event":
        phase = subs[1].strip()
      elif cardtype == "Companion" or cardtype == "Minion":
        if len(subs) > 1:
          race = subs[1].strip()
      else:
        if len(subs) > 1:
          itemclass = subs[1].strip()
    else:
      cardtype = fulltype

    return cardtype, race, itemclass, home, phase

  #jig function for identifying a character
  def IsCharacter(self):
    return self.cardtype == "Companion" or self.cardtype == "Ally" or self.cardtype == "Minion"

  def IsItem(self):
    return self.cardtype == "Artifact" or self.cardtype == "Possession"

  #returns a string that puts the Title, Subtitle, and Suffix back together
  def FullTitle(self):
    fulltitle = ""

    if self.unique:
      fulltitle += "•"

    fulltitle += self.title

    if self.subtitle != "":
      fulltitle += ", " + self.subtitle

    if self.suffix != "":
      fulltitle += " " + self.suffix

    return fulltitle

  #returns a string of the collector's info (set number + rarity + card number)
  def CollInfo(self):
    return f"{self.setnum}{self.rarity}{self.cardnum}"
    
  def DisplayCollInfo(self):
    return f"{self.setnum} {self.rarity} {self.cardnumeral}"
    
  def SetName(self):
    return CardCommon.SET_NAMES[self.setnum]

  #returns a string of the type line in the middle of a card.
  def FullTypeLine(self):
    info = ""
    info += self.cardtype

    if self.cardtype == "Ally":
      info += " • " + self.home
      if self.race != "":
        info += " • " + self.race
    elif self.cardtype == "Event":
      if self.phase != "":
        info += " • " + self.phase
    elif self.cardtype == "Companion" or self.cardtype == "Minion":
      if self.race != "":
        info += " • " + self.race
    else:
      if self.itemclass != "":
        info += " • " + self.itemclass

    return info

  #returns a zero-filled string of the collector's info less the rarity, more useable as an ID.
  def ImageID(self):
    return str(self.setnum).zfill(2) + str(self.cardnum).zfill(3)

  def __repr__(self):
    return "<BaseCard(CollInfo=%r, FullTitle=%r)>" %(self.CollInfo(), self.FullTitle())

  def __str__(self):
    info = "\n==============="
    info += "\nBaseCard Data:\n"
    info += "Name: %s\n" %(self.FullTitle())
    info += "Collector's Info: %s\n" %(self.CollInfo())
    info += "Side: %s\n" %(self.side)
    info += "Culture: %s\n" %(self.culture)
    info += "Type Line: %s\n" %(self.FullTypeLine())
    info += "Twilight / Strength / Vitality / Resistance / Signet / Site :\n"
    info += "%s / %s / %s / %s / %s / %s\n" %(self.twilight, self.strength, self.vitality, self.resistance, self.signet, self.site)
    info += "Game Text: %s\n" %(self.text)
    info += "Lore: %s\n" %(self.lore)
    info += "Notes: %s\n" %(self.notes)
    info += "===============\n"

    return info

  
  #incomplete; this will eventually be used to get unicode titles for everything
  # for display purposes.
  def printFullUnicodeTitle(self):
    asciititle = self.FullTitle()
    unicodetitle = asciititle.replace('·', '•')
    #expand this with more replace lines, Eowyn to Éowyn, etc.





  #returns a string suitable for use in dokuwiki that is the code for displaying a
  # card image that doubles as a link to the card's wiki page.  Image is at about 
  # one-third maximum size.
  def dokuImageLinkSmall(self):
    text = ""
    text += "[[%s|{{cards:%s.jpg?200 |%s" %(self.image, self.image, self.title)

    if self.subtitle != "":
      text += ", " + self.subtitle
    if self.suffix != "":
      text += " " + self.suffix
    text += "}}]]"

    return text

  #returns a string suitable for use in dokuwiki that is the code for displaying a
  # card image that doubles as a link to the card's wiki page.  Image is at about 
  # two-thirds maximum size.
  def dokuImageLink(self):
    text = ""
    text += "[[%s|{{cards:%s.jpg?300 |%s" %(self.image, self.image, self.title)

    if self.subtitle != "":
      text += ", " + self.subtitle
    if self.suffix != "":
      text += " " + self.suffix
    text += "}}]]"

    return text

  #returns a string suitable for use in dokuwiki that is the code for displaying a
  # card's name as a link to the card's wiki page.  
  def dokuTextLink(self):
    text = ""
    text += "[[:%s|%s" %(self.image, self.title)
    if self.subtitle != "":
      text += ", %s" %(self.subtitle)
    if self.suffix != "":
      text += " %s" %(self.suffix)
    text += "]]"

    return text
    
  def dokuTextRowEntry(self, columns):
    text = "|"
    
    for col in columns:
      cell = ""
      if col == "FullTitle":
        cell += f"  {self.FullTitle()}  |"
      elif col == "TextLink":
        cell += f"  {self.dokuTextLink()}  |"
      elif col == "CollInfo":
        cell += f"  {self.CollInfo()}  |"
      elif col == "FullTypeLine":
        cell += f"  {self.FullTypeLine()}  |"
      elif col == "ImageID":
        cell += f"  {self.ImageID()}  |"
        
      elif hasattr(self, col):
        if col == "text":
          cell += f"{getattr(self, col)}  |"
        else:
          cell += f"  {getattr(self, col)}  |"
      else:
        cell += f"  ~MISSING ATTRIBUTE '{col}'~  |"

      text += cell
      
    return text
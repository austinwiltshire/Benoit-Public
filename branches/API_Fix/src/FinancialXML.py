import BeautifulSoup
import re
import sys

#import xml.etree.ElementTree as ETree
import lxml.objectify

#current new idea for a design - an xml manager as a singleton.  he will get queried for information.  he will then take
#those queries and have already loaded an xml query mapping that will give him the file+definitions of how the answer is supposed
#to be.  he loads the file, parses it and returns it
#example : >>> xmlmanager.get("google regular expressions")
# >>> should return what is currently in toReturn['regular expressions']


# ==============================================================================================================
# IMPORTANT!IMPORTANT!IMPORTANT!IMPORTANT!IMPORTANT!IMPORTANT!IMPORTANT!IMPORTANT!IMPORTANT!IMPORTANT!IMPORTANT!
# ==============================================================================================================
# TODO: Alright.  I need to come up with a TDD for objectifiable stuff.  Here's the preliminaries of what I'm thinking
# A kind of ... sub-DSL definition for every XML document has to assign every type that that XML document has as one of the following:
# "Object"
# "List"
# "Value"
# An object contains other things.  It's 'type' is the name of the actual xml thing, and it must have a 'name' attribute as well.
# A list is made up of other objects.  If the list's objects ALL have names, then it's actually turned into a dict with a name:value
# pairing.
# Value just trims itself down to the string between the <> </> + attributes...
# In fact, everything needs to be an object.  Hrm
# Either way, I can't do this now as I'd have to rewrite the entire google xml which I just don't have the energy to do right now.
# ================================================================================================================

def objectifiable(objectifiedXML):
		""" Decides whether or not this XML can be objectified according to my standards.  Does this by turning contracts on,
		then attempting to create a a valid XMLObject from it.  If I can, I return true.  If I throw, then I return false.
		
		Can this be put inside the XMLObject class?
		
		pre:
			isinstance(objectifiedXML, objectify.ObjectifiedElement) or isinstance(objectifiedXML, file)
		post[]:
			isinstance(__return__,bool)
		"""

class XMLObject(object):
	""" A specific type of XML to object mapping, loosely based on an unerlying LXML objectify.  Differences are that 
	attributes are treated as attributes of the object(rather than through a 'get' command).  These attributes map directly
	to unicode strings.  Members are mapped to lists that are first class member's of the parent object with the same name 
	as their type.  Name conflicts throw an exception. This cannot be used to write XML, just represent it. 
	
	>>> xmlstring = r"<webpage attr='name'><subvalue>example</subvalue></webpage>"
	>>> example = XMLObject(objectify.fromstring(xmlstring))
	>>> example.type
	u'webpage'
	>>> example.attr
	u'name'
	>>> example.subvalue
	[XMLObject]
	>>> example.subvalue[0].type
	u'subvalue'
	>>> str(example.subvalue[0])
	u'example'
	
	"""
	
	def __init__(self, objectifiedXML):
		""" Takes an underlying objectifiedXML object and wraps it 
		
		pre:
			isinstance(objectifiedXML, objectify.ObjectifiedElement) or isinstance(objectifiedXML, basestring)
		post[]:
			[hasattr(self,x) for x in objectifiedXML.keys()]
		"""
			   
		if isinstance(objectifiedXML,objectify.ObjectifiedElement):
			for attr,val in objectifiedXML.items():
				self._addAttribute(attr, val)
		
			for child in objectifiedXML.getchildren():
				self._addChild(child)
				
			self.type = objectifiedXML.tag
		
		self._setText(objectifiedXML)
	
	@classmethod
	def objectify(cls, filename, strict=False):
		""" Takes the filename of an xml file and returns a fully objectified representation.  Does not deal with
		filename errors so those throw to the caller. 
		
		>>> example = XMLObject.objectify("google.xml")
		>>> isinstance(example, XMLObject)
		
		
		pre:
			isString(filename)
		post[]:
			isinstance(__return__, objectify.XMLObject)
		"""
		
		return cls(lxml.objectify.parse(filename).getroot())
		#pass
	
	def _addAttribute(self, name, value):
		""" Used to map XML attributes to python Object attributes.  They are mapped from attribute name(as first class attributes)
		to attribute value, as a unicode string 
		
		pre:
			isString(name)
			isString(value)
			not hasattr(self, name)
		post:
			hasattr(self,name) and self.name == value
		"""
		
		setattr(self, name, value)
		#check for collisions.  if its already defined, throw.  promote this to a contract
		#add a helper function that decides whether what i'm looking at is legitimate xml for my objectify.  all
		#this function has to do is turn contracts on and try and turn it into an object.
	
	def _addChild(self, objectifiedXML):
		""" Adds this objectified XML as a child/member to the list to the parent object.  List name is added as a first
		class attribute with the same name as the type of these underlying children 
		
		pre:
			isinstance(objectifiedXML, objectify.ObjectifiedElement)
		post[]:
			hasattr(self, objectifiedXML.tag)
			isinstance(getattr(self, objectifiedXML.tag), list)
			objectifiedXML.tag == ((getattr(self,objectifiedXML.tag))[-1]).type
			
			
		"""
		
 #	   print type(objectifiedXML)
		
		child = XMLObject(objectifiedXML)
		if(hasattr(self, child.type)):
			self._appendChild(child)
		else:
			self._newChild(child)
		
		#get type of underlying objectifiedXML
		#that's the name to add it to.
		#self.thatName.append(XMLObject(objectifiedXML))
		#if thatName is not a list, throw.(already a keyword.)
		#if thatName is not defined, create it.
	
	def _newChild(self, newXMLObject):
		""" Called when I have a completely new type of subelement to add to the parent XMLObject. 
		
		pre:
			isinstance(newXMLObject, XMLObject)
			not hasattr(self, newXMLObject.type)
		post[]:
			hasattr(self, newXMLObject.type)
			isinstance(getattr(self, newXMLObject.type), list)
			newXMLObject.type == ((getattr(self,newXMLObject.type))[0]).type
		"""
		setattr(self, newXMLObject.type, newXMLObject)
		
	def _appendChild(self, newXMLObject):
		""" Called when I have a new child to add to a list of subelements that I already maintain. 
		
		pre:
			isinstance(newXMLObject, XMLObject)
			hasattr(self, newXMLObject.type)
		post[self]:
			#grow list by one
			len(getattr(self, newXMLObject.type) - len(getattr(__old__.self, newXMLObject.type)) == 1
			
			#make sure i added the right tyep to list
			newXMLObject.type == ((getattr(self,newXMLObject.type))[-1]).type
		
		"""
		
		(getattr(self, newXMLObject.type)).append(newXMLObject)
		
		  
	def __hash__(self):
		""" XMLObjects hash on their text value.  If they don't have one, they can't be hashed and this throws. 
		
		pre:
			hasattr(self,_hashString)
		post[]:
			__return__ == self._hashString if self._hashString else True
			isString(__return__) if self._hashString else True
		"""
		
		#check to make sure this throws if I hash 'none'  I need to throw manually.
		if not self._hashString:
			raise "Something"
		return self._hashString
	
	def __repr__(self):
		""" XMLObjects repr and str based on their text value.  If not that, they do so on their underlying type name 
		
		pre:
			hasattr(self,_repString) and self._repString is not None
		post[]:
			__return__ == self._repString
			isString(__return__)
		"""
		
		return self._repString
	
	def __str__(self):
		""" XMLObjects repr and str based on their text value.  If not that, they do so on their underlying type name 
		
		pre:
			hasattr(self,_repString) and self._repString is not None
		post[]:
			__return__ == self._repString
			isString(__return__)
		"""
		
		return self._repString
	
	def _setText(self, objectifiedXML):
		""" Used to set hash text and str text. 
		
		pre:
			not hasattr(self,_repString)
			not hasattr(self,_hashString)
			isinstance(objectifiedXML, objectify.ObjectifiedElement) or isinstance(objectifiedXML, basestring)
		post[]:
			self._repString == objectifiedXML.text if objectifiedXML.text else self._repString == objectifiedXML.tag
			self._hashString == objectifiedXML.text if objectifiedXML.text else self._hashString == None
		"""
		
		if isinstance(objectifiedXML, basestring):
			self._repString = self._hashString = objectifiedXML
			return
		
		if objectifiedXML.text:
			self._repString = self._hashString = objectifiedXML.text
		else:
			self._repString = objectifiedXML.tag
			self._hashString = None 
		#if there is text, then i set hashText and strText to be the same.
		#if not, hashText is set to None and strText is set to the type
	
#===============================================================================
# class XMLManager:
#	def __init__(self):
#		""" Constructor for XMLManager. Class is a singleton. """
#		pass
#	
#	def get(self, query):
#		""" Finds query, which is a string, in mapping file.  Mapping file declares a description and a filename.
#		Get then looks up the filename, and parses the information into the expected return value 
#		
#		Par example:
#		>>> regex = XMLManager.get("google regular expressions")
#		>>> "ForeignExchangeEffects" in regex
#		True
#		
#		>>> divisions = XMLManager.get("google divisions")
#		>>> print divisions["IncomeStatement"]["Annual"]
#		"incannualdiv"
#		
#		
#		>>> sec_documents = XMLManager.get("sec documents")
#		>>> "Revenue" in sec_documents["IncomeStatement"]
#		True
#		
#		pre:
#			isstring(query)
#		"""
#		pass
#		
#		#do a check first to make sure my query exists inside my mapping file, if not, throw an exception
#		
#		#look inside mapping file, probably need a "_getFilename" function and a "_getDefinition" function.  this will return
#		#the filename to load and parse and some sort of general parsing function that will load something in and then return
#		#the right object.
#		
#	def _getFilename(self, query):
#		""" Private member function.  Takes a query and returns the proper xml file that query responds to. """
#		pass
# 
#	def _getDefinition(self, query):
#		""" Private member function.  Takes a query and returns a function that parses over xml and returns some object. """
#		pass
#	
#===============================================================================






#do not currently enforce a TDD

#TODO: add a TDD
#TODO: add a unit test - do a search over the entire webpage for each Re, should only find it
#twice.  once in annual and once in quarterly.  if i find it 0 or more than 2 times, i've
#got a problem or they changed something.

def xml_to_dict():
	#google divisions  
	if sys.getwindowsversion() == (5, 1, 2600, 2, 'Service Pack 3'):
		parseroot = r"C:\Docume~1\JohnGr~1\workspace\Webstock\src" # I'm on the laptop
	else:
		parseroot = r"C:\Users\John\Workspace\Webstock\src" #im on the new computer
	
	
	webpage = lxml.objectify.parse(parseroot+r"\google.xml").getroot()
	
	
	toReturn = {}
	divisions = {}
	
	for div in webpage.divisions.div:
		name, annualMap, quarterlyMap = div.value, div.mapping[0], div.mapping[1] #unwrap the three kids which are name, annual, quarterly in that order
		#again im dereferencing an array hard coded, a sure sign i can do better than this.
		divisions[str(name)] = {annualMap.get("frequency"):str(annualMap), quarterlyMap.get("frequency"):str(quarterlyMap)}
	
	toReturn['divisions'] = divisions
	
	#google regexes
	regex = {}
	
	for rgx in webpage.regular_expressions.regex:
		regex[str(rgx.value)] = str(rgx.definition)
		
	toReturn['regular_expressions'] = regex
	
	#sec_stuff

	secDocumentDefinitions = lxml.objectify.parse(parseroot+r"\general.xml").getroot()
	
	sec_definition = {}
	
	for secDoc in secDocumentDefinitions.sec_doc:
		name = secDoc.get('name')
		values = [str(val) for val in secDoc.value]
		sec_definition[name] = values
	
	toReturn['sec_definition'] = sec_definition
		
	return toReturn 
		
	
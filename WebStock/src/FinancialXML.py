import BeautifulSoup
import re

#do not currently enforce a TDD

#TODO: add a TDD
#TODO: add a unit test - do a search over the entire webpage for each Re, should only find it
#twice.  once in annual and once in quarterly.  if i find it 0 or more than 2 times, i've
#got a problem or they changed something.

def xml_to_dict(filename):
    f = open(filename, "r")
    soup = BeautifulSoup.BeautifulSoup(f.read())
    
    toReturn = {}
    
    sec_definition = {}
    #this might be moved into a completely different XML file
    for sec_doc in soup.sec_document_definitions.findAll("sec_doc"):
        name = sec_doc['name']
        values = [val.string for val in sec_doc.findAll('value')]
        sec_definition[name] = values
        
    toReturn['sec_definition'] = sec_definition
    
    
    divisions = {}
    #assume divisions comes first. 
    #divisions block tells me where to find the balance sheet, income statement and cash flows
    for div in soup.divisions.findAll('div'):
        annualMap = div.find('mapping', frequency='Annual').string
        quarterlyMap = div.find('mapping', frequency='Quarterly').string
        
        divisions[div.value.string] = {'Annual':annualMap, 'Quarterly':quarterlyMap}
        
    toReturn['divisions'] = divisions
    
    #then regex definitions come
    #regex's map to individual items in the balance sheet, income, etc...
    regex = {}
    for rgx in soup.regular_expressions.findAll('regex'):
        regex[rgx.value.string] = rgx.definition.string
    
    toReturn['regular_expressions'] = regex
    
    f.close()
    return toReturn 
        
    
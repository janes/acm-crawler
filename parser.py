import urllib2
import re
import gc
import argparse
import sys 

from bs4 import BeautifulSoup
from datetime import datetime
from databaseHelper import DatabaseHelper

reload(sys)
sys.setdefaultencoding('utf8')

regex_tabs = '(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

def connect(url):
	headers = { 'User-Agent' : 'UbiCrawler' } #not sure
	req = urllib2.Request(url, None, headers)
	html = urllib2.urlopen(req).read()
	soup = BeautifulSoup(html)
	return soup


def print_publication_basics(title,authors,conference,journal,date):
	print "\n"
	print "Title: ", title + "\n"
	print "Authors: ", authors + "\n"
	if (conference):
		print "Conference: ", conference['content'] + "\n"
	if (journal):	
		print "Journal: ", journal['content'] + "\n"
	print "Date: ", date + + "\n"


def print_publication_references(refs):		
	for ref in refs:
		print ref.split("?")[1].split("&")[0]

def check_abstract(scripts):	
	return check(scripts, 'tab_abstract.cfm?')

def check_authors(scripts):	
	return check(scripts, 'tab_authors2.cfm?')

def check_references(scripts):	
	return check(scripts, 'tab_references.cfm?')

def check_citings(scripts):	
	return check(scripts, 'tab_citings.cfm?')

def check_indexterms(scripts):	
	return check(scripts, 'tab_indexterms.cfm?')

def check_conference(scripts):	
	return check(scripts, 'tab_source.cfm?')

def check(scripts,tab_name):
	items = []	
	for s in scripts:	
		if re.findall(tab_name + regex_tabs, s.get_text()):
			items = re.findall(tab_name + regex_tabs, 
				s.get_text())[0].split("'")[0]	

	return items



#arguments for the script
args_parser = argparse.ArgumentParser(description='Collect publications provided by ACM.')
args_parser.add_argument('integers', metavar='N', type=str, nargs='+',
                   help='the id of some publication')
args = args_parser.parse_args();

#arguments for the script

#connection
domain = 'http://dl.acm.org/'
publication_id = args.integers[0]
soup = connect(domain+'citation.cfm?id='+publication_id)

dbHelper = DatabaseHelper()
dbHelper.connectToLocalDatabase()



date_object = datetime.strptime(soup.find("meta", {"name":"citation_date"})['content'], '%m/%d/%Y')

authors_citation=''
if soup.find("meta", {"name":"citation_authors"}):
	authors_citation = soup.find("meta", {"name":"citation_authors"})['content']

publisher = soup.find("meta", {"name":"citation_publisher"})['content']
title = unicode(soup.title.string)

print "--------------/-----------------------/---------------------------------/"
print "publication "+publication_id

table = soup.find("table", {"class":"medium-text"})
bibliometrics =	table.find("td", {"class":"small-text"})
bibliometrics = ''.join(bibliometrics.text.split())
bibliometricsDict = dict(item.split(":")  for item in bibliometrics.split(u"\u00B7") if item)

#get basic info
#print_publication_basics(
#			soup.title.string,
#			soup.find("meta", {"name":"citation_authors"})['content'],
#			soup.find("meta", {"name":"citation_conference"}),
#			soup.find("meta", {"name":"citation_journal_title"}),
#			soup.find("meta", {"name":"citation_date"})['content']
#			)


dbHelper.insertPublication(	publication_id,
							title,
							publisher,
							bibliometricsDict,
							authors_citation	,
							date_object.strftime("%Y-%m-%d")
							)

#get extra info on each author
#print_publication_authors_each(soup.findAll(attrs={"title":"Author Profile Page"}))
authors = soup.findAll(attrs={"title":"Author Profile Page"})
for aut in authors:
		#print aut.get_text() + "  " + aut['href'].split("?")[1].split("&")[0]	
		author_id = aut['href'].split("?")[1].split("&")[0].split("id=")[1]								
		dbHelper.insertAuthor(author_id,aut.get_text())
		dbHelper.addAuthorToPublication(publication_id,author_id)





#get abstract
sourceScripts = soup.findAll('script')

abstractText = ''
abstract = check_abstract(sourceScripts)
if abstract: 
	print '\n...getting abstract...'
	soup = connect(domain + abstract)
	if soup.find('div',{'style':'display:inline'}) is not None:
		abstractText = soup.find('div',{'style':'display:inline'}).text

print '\n...getting export...'
soup = connect('http://dl.acm.org/exportformats.cfm?id='+ publication_id +'&expformat=bibtex')

pre_div = soup.find('pre',{'id':publication_id})

dbHelper.insertPublicationAbstract(	publication_id,
							abstractText ,
							pre_div.text
							)

#get references
reference = check_references(sourceScripts)
if reference: 
	print '\n...getting references...'
	soup = connect(domain + reference)
	links = soup.findAll('a',{'href':True})
	refs =[]
	for l in links:
		if re.findall('citation.cfm?' + regex_tabs, l['href']):
			refs.append(re.findall('citation.cfm?' + regex_tabs, l['href'])[0]);

	#print_publication_references(refs)	

	for ref in refs:
		idInQueue = ref.split("?")[1].split("&")[0].split("id=")[1]		
		if not dbHelper.findInQueue(str(idInQueue)) :
			print "adding to queue "+ idInQueue
			dbHelper.addToQueue(str(idInQueue))

		dbHelper.addReferenceToPublication(publication_id,str(idInQueue))
	if not refs:
		print " - No references related - "	
else:		
	print " - No references related - "	
		
#get citings
citings = check_citings(sourceScripts)
if citings: 
	print '\n...getting citings...'
	soup = connect(domain + citings)
	links = soup.findAll('a',{'href':True})
	cits =[]
	for l in links:
		if re.findall('citation.cfm?' + regex_tabs, l['href']):
			cits.append(re.findall('citation.cfm?' + regex_tabs, l['href'])[0]);

	#print_publication_references(refs)	

	for cit in cits:
		idInQueue = cit.split("?")[1].split("&")[0].split("id=")[1]		
		if not dbHelper.findInQueue(str(idInQueue)) :
			print "adding to queue "+ idInQueue
			dbHelper.addToQueue(str(idInQueue))
	if not cits:
		print " - No references related - "	
else:		
	print " - No references related - "	


conference = check_conference(sourceScripts)
if conference:	
	conference_id=''
	conference_title=''
	print "\n...getting conference..."
	soup = connect(domain + conference)	
	links = soup.findAll('a')
	for l in links:
		if l.has_attr('href'):
			if re.findall('event.cfm?' + regex_tabs, l['href']):			
				conference_title = l['title']
				conference_id = l['href'].split("?")[1].split("&")[0].split("id=")[1]
				conference_abbrv = l.findPrevious('strong').get_text()
				

	if conference_id and conference_title:		
		dbHelper.insertConference(conference_id,conference_title,conference_abbrv)
		dbHelper.addConferenceToPublication(publication_id,conference_id)
		print "added conference"
	else:
		print " - No events related - "	
else:
	print " - No events related - "	





dbHelper.setPublicationFullCollected(publication_id)
dbHelper.removeFromQueue(publication_id)
dbHelper.closeLocalConnection()	
print "\npublication added!"
print "\nSuccess! removed from queue..."
print "Releasing memory..."
gc.collect()
print "--------------/-----------------------/---------------------------------/"




		
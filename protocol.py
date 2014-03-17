# Protocol Class for Nature Protocol Exchange
# Copyright Charles Fracchia 2014
# fracchia@mit.edu

import urllib2, warnings, wordcloud, cgi, re, json
from os import path
from bs4 import BeautifulSoup

class Protocol(object):
  """docstring for Protocol"""
  def __init__(self, url):
    super(Protocol, self).__init__()
    self.url = url
    self.fullProtocol = self._loadProtocol(url)
    for key in self.fullProtocol.keys():
      setattr(self, key, self.fullProtocol[key])
    
  def _loadProtocol(self, url):
    """docstring for _loadProtocol"""
    pass
    protocol = {}
    soup = self._cleverSoupLoading(url)
    protocol['title'] = soup.find("h1", {"id" : "main"}).contents[0].replace('\n',"")
    protocol['doi'] = soup.find("dd", {"class" : "doi"}).text.replace("doi:","")
    protocol['published'] = soup.find("time", {"pubdate" : "pubdate"})['datetime']
    protocol['authors'] = []
    authors = soup.findAll("span", {"class" : "fn" , "class" : "name"})
    for author in authors:
      protocol['authors'].append(author.text.strip())
    labTag = soup.find(True, href=re.compile("protocolexchange/labgroups/\\d+"))
    protocol['lab'] = {
      "name" : labTag.text,
      "id" : labTag['href'].replace("/protocolexchange/labgroups/","")
    }
    protocol['introduction'] = soup.find("div", {"id" : "introduction"}).p.text
    protocol['reagents'] = soup.find("div", {"id" : "reagents"}).p.text
    protocol['equipment'] = soup.find("div", {"id" : "equipment"}).p.text
    protocol['procedure'] = soup.find("div", {"id" : "procedure"}).p.text
    protocol['timing'] = soup.find("div", {"id" : "time_taken"}).p.text
    protocol['critical'] = soup.find("div", {"id" : "critical_steps"}).p.text
    protocol['results'] = soup.find("div", {"id" : "anticipated_results"}).p.text
    protocol['references'] = soup.find("div", {"id" : "references"}).p.text
    
    rawSubjectTerms = soup.findAll("div", {"class" : "article-keywords"})[0].findAll("li")
    subjectTerms = []
    for keyword in rawSubjectTerms:
      subjectTerms.append(keyword.text.replace('\n',""))
    protocol['subjectTerms'] = subjectTerms
    
    rawKeywords = soup.findAll("div", {"class" : "article-keywords"})[1].findAll("li")
    keywords = []
    for keyword in rawKeywords:
      keywords.append(keyword.text.replace('\n',""))
    protocol['keywords'] = keywords
    
    return protocol
    
  def _cleverSoupLoading(self, url):
    """takes in a string that is either a live url or a cached html file path and returns the soup object"""
    pass
    if "http" in url:
      return BeautifulSoup(urllib2.urlopen(url).read())   #Load the URL into beautifulsoup
    else:
      return BeautifulSoup(open(url))                     #Load the file into beautifulsoup, allows offline testing without raising eyebrows
  
  def toJSON(self):
    json = "{"
    for key in self.fullProtocol.keys():
      
      if type(getattr(self, key)) == list:
        json = '%s "%s":[' % (json, key)
        for item in getattr(self, key):
          json = '%s "%s"' % (json, item.encode('ascii', 'xmlcharrefreplace'))
          json += ","
        json += "],"
      
      elif type(getattr(self, key)) == dict:
        json = '%s "%s":{' % (json, key)
        for dictKey in getattr(self, key).keys():
          json = '%s "%s":"%s",' % (json, dictKey, getattr(self, key)[dictKey].encode('ascii', 'xmlcharrefreplace'))
        json += "},"
      
      else:
        json = '%s "%s":"%s",' % (json, key, getattr(self, key).encode('ascii', 'xmlcharrefreplace'))
    json += "}"
    return json
    
#m = Protocol("http://www.nature.com/protocolexchange/protocols/153")
#print m.toJSON()
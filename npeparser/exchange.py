# Exchange (web portal) Class for Nature Protocol Exchange
# Copyright Charles Fracchia 2014
# fracchia@mit.edu

import urllib2, warnings, wordcloud, cgi, re, json
from os import path
from bs4 import BeautifulSoup
from protocol import Protocol

class ExchangeSearch(object):
  """docstring for Protocol"""
  def __init__(self, searchTerms="", perPage=500, pubType="community"):
    super(ExchangeSearch, self).__init__()
    self.url = self._buildURL(searchTerms, perPage, pubType)
    self.results = self._getProtocolURLs(self.url)
    
  def _cleverSoupLoading(self, url):
    """takes in a string that is either a live url or a cached html file path and returns the soup object"""
    pass
    if "http" in url:
      return BeautifulSoup(urllib2.urlopen(url).read())   #Load the URL into beautifulsoup
    else:
      return BeautifulSoup(open(url))                     #Load the file into beautifulsoup, allows offline testing without raising eyebrows
  
  def _buildURL(self, searchTerms, perPage, pubType ):
    """docstring for doSearch"""
    pass
    searchURL = ""
    base = "http://www.nature.com/protocolexchange/protocols?commit=Go"
    protocolSearchBase = "&protocol_search"
    typeSearchBase = "%5Bfacets%5D%5Bderived-protocol-type%5D="
    searchTermBase = "%5Bq%5D="
    perPageSearchBase = "&per_page="
    
    searchURL += base
    if type(searchTerms) == list:
      for i, term in enumerate(searchTerms):
        if i != (len(searchTerms)-1):
          searchTermBase += "%s+" % term
        else:
          searchTermBase += str(term)
    else:
      searchTermBase += str(searchTerms)
    
    if pubType == "community":  pubType = "Community+Contributed"
    elif pubType == "peer":  pubType = "Peer+Reviewed"
    elif pubType == "supplier":  pubType = "Supplier+Contributed"
    typeSearchBase += str(pubType)
      
    searchURL = base + perPageSearchBase + str(perPage) + protocolSearchBase + typeSearchBase + protocolSearchBase + searchTermBase
    
    return searchURL
  
  def _getProtocolURLs(self, searchURL):
    """docstring for _getProtocolURLs"""
    pass
    soup = self._cleverSoupLoading(searchURL)
    linksTitles = soup.findAll("h2", {"class" : "protocol-title"})
    links = []
    for linksTitle in linksTitles:
      links.append({"title" : linksTitle.a.text, "href": "http://www.nature.com" + linksTitle.a['href']})
    
    return links
  
  def dumpLinks(self, results):
    """docstring for dumpLinks"""
    pass
    f = open('searchResults.txt','w')
    for result in m.results:
      f.write("http://www.nature.com"+result['href']+'\n')
    f.close()
  
  def dumpProtocols(self, results):
    """docstring for dumpProtocols"""
    pass
    i = 0
    for result in results:
      if i < 10:
        protocol = Protocol(result['href'])
        protocolId = result['href'].replace("http://www.nature.com/protocolexchange/protocols/","")
        f = open("files/"+protocolId+'.txt','w')
        f.write(protocol.toJSON())
        f.close()
      else:
        break
      i += 1
      
    
#m = ExchangeSearch(["pcr"], 500, "community")
#m.dumpProtocols(m.results)
#p = Protocol("http://www.nature.com/protocolexchange/protocols/3077")
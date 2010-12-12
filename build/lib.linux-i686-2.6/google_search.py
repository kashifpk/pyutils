#!/usr/bin/env python
"""google_search.py
   This python module contains various Google functions to aid in searching and parsing results of the
famous Google search engine.

Revisions:
   [ 08-Mar-2007 ] 
      * Updated to parse google serach returned data using the BeautifulSoup xml/html parser.
   [ 20-Mar-2007 ] 
      * Added support for country prefixes allowing a specific google search webserver to use for search queries. 
      * Added support to fetch more than 100 records with one call.
      
TODO:
   1. Add proxy support.
   
"""
__author__ = "Kashif Iftikhar"
__version__ = "0.5"

import sys, re
import httplib
import urllib2
import urllib
import getopt
from BeautifulSoup import BeautifulSoup

class Google:
    "This the main class containing various methods for google search and proper parsing of results"

    def __init__(self, results_per_page=50, country_prefix='', search_domain='', \
    dict_headers={'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)'}):
        """Constructor that initilizes basic settings.
        PARAMETERS:
            results_per_pages     The number of results to fetch in one query.
            country_prefix        Use a specific country's google (like google.com.pk).
            search_domain         Only search a single domain (if search_domain is not empty).
            dict_headers          A dictionary containing HTTP headers to be sent with the request.
        """
        self.max_google_results = 100
        self.results_per_page = results_per_page
        self.google_domain = 'www.google.com' + country_prefix
        self.search_domain = search_domain
        self.headers = dict_headers

    def set_country_prefix(self, prefix):
        self.country_prefix = prefix
        self.google_domain = 'www.google.com' +  self.country_prefix
    def strip_tags(self, text):
        "Removes all tags from given text and returns plain text"
        finished = 0
        while not finished:
            finished = 1
            start = text.find("<")
            if start >= 0:
                stop = text[start:].find(">")
                if stop >= 0:
                    text = text[:start] + text[start+stop+1:]
                    finished = 0
        return text
    
    def parse_google_results(self, data):
        """Given a string, tries to treat the string as the contents of a google search result page and
        returns processed results.
        """
        soup = BeautifulSoup(data)
        #print repr(soup.contents)
        #print len(soup.contents)
        
        #print soup.contents[1]
        d = soup.contents[0]
        
        #print len(d.findAll('div', {'class': 'g'}))
        search_results = []
        
        for content in soup.contents:
            
            try:
                for div in content.findAll('div', {'class': 'g'}):
                    res_dict = {}
                    a_tag = div.findAll('a', {'class': 'l'})
                    
                    desc_tag = div.findAll('td', {'class': 'j'})
                    
                    if len(a_tag)>0:
                        a_tag = a_tag[0]
                        
                    
                    res_dict['url'] = self.strip_tags(a_tag['href'])
                    title = ''
                    for t in a_tag.contents:
                        title +=  str(t).strip()
                    
                    res_dict['title'] = self.strip_tags(title)
    
                    desc = str(desc_tag[0])
                    idx = desc.find('<span')
                    desc = desc[:idx]
                    res_dict['description'] = self.strip_tags(desc)
    
                    search_results.append(res_dict)
                    
            except:
                pass
            
        return(search_results)
    
    def search(self, search_query):
        """Searches using the given search query and returns a list of search result.
        each search result is reperesented by a list item. Each list item is a dictionary containing
        various parts of a search result like title, description, url etc."""
        search_query = urllib.quote_plus(search_query, '')
        search_line = 'http://' + self.google_domain + '/search?q=' + search_query
        if len(self.search_domain)>0:
            search_line += '+site%3A' + self.search_domain

        
        
        #UPDATE: Adding support for fetching more than max_google_results (100) 
        #First check if self.results_per_page > self.max_google_results
        #print search_line
        remaining_results = int(self.results_per_page)
        start = 0
        search_results = []
        last_run = False
        while True:
            current_search_line = search_line
            
            if remaining_results > self.max_google_results:
                current_search_line += '&num=' + str(self.max_google_results)
            else:
                current_search_line += '&num=' + str(remaining_results)
                last_run = True
            
            current_search_line += '&start=' + str(start)
            #print current_search_line
            
            request = urllib2.Request(current_search_line)
            
            start += self.max_google_results
            
            for key, val in self.headers.iteritems():
                request.add_header(key,val)
     
            opener = urllib2.build_opener()
            res = opener.open(request).read()
            
            #print res
            results = self.parse_google_results(res)
            search_results += results
            remaining_results = remaining_results - len(search_results)
            
            if remaining_results <= 0 or last_run:
                break
        
        return(search_results)


if __name__ == '__main__':
    if 1 == len(sys.argv):
        print """
        
        Usage:
        
              %s options
            
         Options are:
        -q query_string, --query=query_string (Required)
            The search query to search via google.
            
        -n num, --results=num (Optional)
            Number of results to return
            
        -d domain, --domain=domain (Optional)
            If given, only the specified domain is searched for results matching the query.
            
        -c prefix, --country=prefix (Optional)
            If given, the specified google mirror is used for example .pk specifies to use google.com.pk 
            for search queries.
        """ % sys.argv[0]
        sys.exit()
        
    
    short_opts = 'q:n:d:c:'
    long_opts = ['query=', 'results=', 'domain=', 'country=']
    
    try:
      given_opts, given_args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
      print "\nSorry, the option you have provided could not be recognized as a valid option\n"
      sys.exit(1)
    
    google = Google()
    q = ''
    for opt_item in given_opts:
        opt_name = opt_item[0]
        opt_val  = opt_item[1]
        
        if '-q' == opt_name or '--query' == opt_name:
            q = opt_val
            
        if '-n' == opt_name or '--results' == opt_name:
            google.results_per_page = opt_val
            
        if '-d' == opt_name or '--domain' == opt_name:
            google.search_domain = opt_val
            
        if '-c' == opt_name or '--country' == opt_name:
            google.set_country_prefix(opt_val)
            
    
    if len(q)>0:
        results = google.search(q)
    else:
        print "\n\nMust provide a search query"
        
    #print repr(results)
    sno = 1
    for result in results:
        try:
            print "\n%i.   %s\n    %s\n%s" % (sno, result['title'], result['url'], result['description'])
        
            sno += 1
        except UnicodeDecodeError:
            pass


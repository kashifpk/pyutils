#!/usr/bin/env python

"""html_parser.py
Parses given html document and returns data.   
"""
__author__ = "Kashif Iftikhar"
__version__ = "0.1"

import sys
from BeautifulSoup import BeautifulSoup

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "\nSyntax:\n\t%s filename\n\n" % sys.argv[0]
        sys.exit(0)
    
    fd = open(sys.argv[1])
    data = fd.read()
    fd.close()
    
    print "\nData Size: %i\n" % len(data)
    
    soup = BeautifulSoup(data)
    #print repr(soup.contents)
    print len(soup.contents)
    
    #print soup.contents[1]
    d = soup.contents[0]
    
    print len(d.findAll('div', {'class': 'g'}))
    
    for content in soup.contents:
        
        try:
            for div in content.findAll('div', {'class': 'g'}):
                print
                #print repr(div.findAll('a'))
                a_tag = div.findAll('a', {'class': 'l'})
                
                desc_tag = div.findAll('td', {'class': 'j'})
                
                if len(a_tag)>0:
                    a_tag = a_tag[0]
                    
                print a_tag['href']
                href = a_tag['href']
                title = ''
                for t in a_tag.contents:
                    title +=  str(t).strip()
                
                print title

                desc = str(desc_tag[0])
                
                
        except:
            pass
    


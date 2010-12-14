"""json2csv.py
Convert json object to CSV
"""
__author__ = "Kashif Iftikhar"
__version__ = "0.1"

import json


if '__main__' == __name__:
    import sys
    import pprint
    
    if len(sys.argv)<2:
        print "Enter json filename"
        sys.exit()
    
    f = open(sys.argv[1])
    
    data = json.load(f)
    
    f.close()
    
    #pprint.pprint(data)
    
    print '"name","phone","display_phone","location"'
    for r in data['businesses']:
        try:
            line = '"%s","%s","%s","%s"' % (r['name'], r['phone'], r['display_phone'],
                                            r['location']['address'][0] + ', ' +
                                            r['location']['city'] + ', ' +
                                            r['location']['postal_code'] + ', ' +
                                            r['location']['state_code'] + ', ' +
                                            r['location']['country_code'] 
                                            )
            print line
        except:
            pass
    
    
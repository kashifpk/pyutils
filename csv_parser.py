"""csv_parser.py
Improved CSV parsing module. Python's built-in module had a few short commings (or may be I didn't understand it correctly), any how; the result is a simplified library.

It is a start, should be improving it as time goes.

update- Added option to writing list of unicode (utf-8) strings to a file.

"""
__author__ = "Kashif Iftikhar"
__version__ = "0.2"

def parse_csv_line(line):
    "Parses given string as a CSV line and returns CSV values in a list"
    csv = []
    state = 0  # before a value
    val = ''
    
    line += ','
    
    for ch in line:
        if 0 == state:   # before a value
            if ',' == ch:  # value complete
                csv.append(val)
                val = ''
            elif '"' == ch:   # inside a quoted value
                state = 2
                val = ''
            else:
                val += ch
                state = 1
            
        elif 1 == state:   # inside a value
            if ',' == ch:
                csv.append(val)
                val = ''
                state = 0
            else:
                val += ch
                
        elif 2 == state: #inside a quoted value
            if '"' == ch:
                state = 0
            else:
                val += ch


    return csv
    


def parse_csv(csv_str):
    "Parses given multi-line csv string and returns a list containing the values"
    lines = csv_str.split('\n')
    ret = []
    for line in lines:
        line = line.strip()
        ret.append(parse_csv_line(line))
    
    return ret

def csv_line(L):
    "Given a list L returns its contents as a utf-8 comma separated string"
    
    if 0==len(L):
        return ""
    
    row_str = ""
    
    for i in L:
        row_str += '"%s",' % unicode(i).encode('utf-8')
    
    row_str = row_str[:-1] + "\n"
    
    return row_str
    
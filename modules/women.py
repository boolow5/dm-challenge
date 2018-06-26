import csv

class WomanFile(object):
    '''
    WomanFile handles writing data to WOMEN.TXT
    '''
    def __init__(self, content):
        self.content = content
    
    def save(self):
        f = open('WOMEN.TXT', 'w')
        f.write(self.content)
        print('done writing to WOMEN.TXT')
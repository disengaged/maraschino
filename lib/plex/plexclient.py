'''
Created on Jun 23, 2012

@author: Anne Jan Elsinga
'''

import urllib2

    
class PLEXLibrary(object):
    '''
    Connects to a Plex Media Server for various tasks
    '''
    def __init__(self, server="127.0.0.1", port="324000"):
        '''
        Keyword arguments:
        server
        port
        '''
        self.server=server
        self.port=port

    def str2int (self,string):
        ''' 
        converts a string to an int
        '''
        try:
            i = int(string)
        except (ValueError,TypeError):
            i = 0
        return i
    
    def plexgetxml (self, location):
        '''
        plexgetxml returns the root for an XML for Plex
        '''
        tree = ElementTree.parse(urlopen(self.server+location))
        root=tree.getroot()
        return root

class PLEXClient(object):
    '''
    connects to a Plex client for various tasks 
    '''
    def sendmessage (self, message):
        formedurl="http://"+self.server+":"+self.port+"/xbmcCmds/XbmcHttp?command=ExecBuiltIn(Notification("+urllib2.quote(message)+"))"
        print formedurl 
        urllib2.urlopen(formedurl)
        
        pass

    def __init__(self, server="127.0.0.1", port="3000"):
        '''
        Keyword arguments:
        name -- Name of the client
        icon_file -- location of an icon file, if any (png, jpg or gif)
        '''
        self.server=server
        self.port=port

'''
Created on Jun 23, 2012

@author: Anne Jan Elsinga
'''
__version__="0.1"

import urllib2
from elementtree import ElementTree
from collections import namedtuple
    
class PLEXLibrary(object):
    '''
    Connects to a Plex Media Server for various tasks
    '''
    TVitem = namedtuple("TVitem", 'showtitle synopsis title summary duration season episode viewcount')
    MovieItem = namedtuple ("MovieItem", 'title summary')
    ClientItem = namedtuple ("ClientItem", 'name host address port version uniqueid')
    
    def __init__(self, server="127.0.0.1", port="324000", MovieLibID="1", TVLibID="2", MusicLibID="3"):
        '''
        Constructor
        input: server, port 
        output: none
        '''
        self.server=server
        self.port=port
        self.TVLibrary=TVLibID
        self.MovieLibrary=MovieLibID
        self.MusicLibrary=MusicLibID

    def str2int (self,string):
        ''' 
        converts a string to an int
        input: string to convert
        output: integer
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
        formedurl="http://"+self.server+":"+self.port+location
        tree = ElementTree.parse(urllib2.urlopen(formedurl))
        root=tree.getroot()
        return root
    
    def getclients(self):
        root=self.plexgetxml("/clients")
        Clients=[]
        for node in root:
            Clients.append (self.ClientItem(node.get('name'), 
                                              node.get('host'),
                                              node.get('address'),
                                              node.get('port'),
                                              node.get('version'),
                                              node.get('machineIdentifier')
                                              ))
        return Clients

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

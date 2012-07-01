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
    TVitem = namedtuple("TVitem", 'title season episode showtitle playcount thumbnail')
    MovieItem = namedtuple ("MovieItem", 'title year rating playcount thumbnail')
    MusicItem = namedtuple ("MusicItem", 'title year rating artist thumbnail')
    ClientItem = namedtuple ("ClientItem", 'name host address port version uniqueid')
    
    def __init__(self, server="127.0.0.1:32400", MovieLibID="1", TVLibID="2", MusicLibID="3"):
        '''
        Constructor
        input: server including port 
        output: none
        '''
        self.server=server
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
        formedurl=self.server+location
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
    
    def getrecentlyaddedepisodes (self):
        '''
        getrecentlyaddedepisodes returns the recently added TV episodes from the library
        '''
        TVItems=[]
        root = self.plexgetxml("/library/sections/"+self.TVLibrary+"/recentlyAdded")
        for node in root:
                TVItems.append(self.TVitem(node.get('title'),
                                           node.get('parentIndex'), 
                                           node.get('index'),
                                           node.get('grandparentTitle'),
                                           node.get('viewCount'),
                                          node.get('thumb'))) 
        return TVItems
    
    def getrecentlyaddedmovies (self):
        '''
        getrecentlyaddedmovies returns the recently added movies from the library
        '''
        MovieItems=[]
        root = self.plexgetxml("/library/sections/"+self.MovieLibrary+"/recentlyAdded")
        for node in root:
                MovieItems.append(self.MovieItem(node.get('title'),
                                           node.get('year'), 
                                           node.get('rating'),
                                           node.get('viewCount'),
                                           node.get('thumb'))) 
        return MovieItems
    
    def getrecentlyaddedalbums (self):
        '''
        getrecentlyaddedalbums returns the recently added music from the library
        '''
        MusicItems=[]
        root = self.plexgetxml("/library/sections/"+self.MusicLibrary+"/recentlyAdded")
        for node in root:
                MusicItems.append(self.MusicItem(node.get('title'),
                                           node.get('year'), 
                                           node.get('rating'),
                                           node.get('artist'),
                                           node.get('thumb')))
        return MusicItems    
        

class PLEXClient(object):
    '''
    connects to a Plex client (aka the Plex Client) for various tasks 
    '''
    def sendmessage (self, message):
        formedurl="http://"+self.server+":"+self.port+"/xbmcCmds/XbmcHttp?command=ExecBuiltIn(Notification("+urllib2.quote(message)+"))" 
        urllib2.urlopen(formedurl)
        

    def __init__(self, server="127.0.0.1", port="3000"):
        '''
        Keyword arguments:
        name -- Name of the client
        icon_file -- location of an icon file, if any (png, jpg or gif)
        '''
        self.server=server
        self.port=port

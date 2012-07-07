'''
Created on Jun 23, 2012

@author: Anne Jan Elsinga
'''
__version__="0.1.1"

import urllib2
import time
import xml.etree.ElementTree as ElementTree
from collections import namedtuple
    
    
def str2int (string):
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
        urllib2.urlopen(self.commandurl+"ExecBuiltIn(Notification("+urllib2.quote(message)+"))")
        

    def __init__(self, server="127.0.0.1", port="3000"):
        '''
        Keyword arguments:
        name -- Name of the client
        icon_file -- location of an icon file, if any (png, jpg or gif)
        '''
        self.server=server
        self.port=port
        self.commandurl="http://"+self.server+":"+self.port+"/xbmcCmds/XbmcHttp?command="

    def currently_playing(self):
        url=urllib2.urlopen(self.commandurl+"GetCurrentlyPlaying")
        currently_playing_page=url.read()
        url.close()
        toprocess=currently_playing_page.replace("<html>","")
        toprocess=toprocess.replace("</html>","")
        toprocess = toprocess.split('<li>')
        
        curplay={}
        curplay['fanart']=''
        curplay['tvshowid']=0
        playerinfo={}
        playerinfo['shuffled']='Unknown'
        playerinfo['repeat']='Unknown'        
        for line in toprocess:
            if line.startswith("PlayStatus"):
                playStatus=line[11:].strip()
                curplay ['playstatus']=playStatus
            elif line.startswith('Track'):
                curplay['track']=line[6:].strip()
            elif line.startswith('Artist'):
                curplay['albumartist']=''
                curplay['artistid']=0
                curplay['artist']=line[7:].strip()
            elif line.startswith('Album'):
                curplay['albumid']=0
                curplay['album']=line[6:].strip()
            elif line.startswith('Lyrics'):
                curplay['lyrics']=line[7:].strip()
            elif line.startswith('URL'):
                curplay['url']=line[4:].strip()
            elif line.startswith('Samplerate'):
                curplay['samplerate']=line[11:].strip()
            elif line.startswith('SongNo'):
                curplay['songno']=line[7:].strip()
            elif line.startswith("Filename"):
                curplay['filename']=line[9:].strip()
            elif line.startswith("VideoNo"):
                curplay['videono']=line[8:].strip()
            elif line.startswith("Type"):
                curplay['type']=line[5:].strip().lower()
            elif line.startswith("Show Title"):
                curplay['showtitle']=line[11:].strip()
            elif line.startswith("Title"):
                curplay['title']=line[6:].strip()
            elif line.startswith("Plotoutline"):
                curplay['plotoutline']=line[12:].strip()
            elif line.startswith("Plot"):
                curplay['plot']=line[5:].strip()
            elif line.startswith("Year"):
                curplay['year']=line[5:].strip()
            elif line.startswith("Season"):
                curplay['season']=line[7:].strip()
            elif line.startswith("Episode"):
                curplay['episode']=line[8:].strip()
            elif line.startswith("Thumb"):
                curplay['thumbnail']=line[6:].strip()
            elif line.startswith("Time"):
                time=line[5:].strip()
                time=time.split(':')
                if len(time)==1:
                    curplay['time']={'hours':0,'minutes':0,'seconds':time}
                elif len(time)==2:
                    curplay['time']={'hours':0, 'minutes':time[0],'seconds':time[1]}
                elif len(time)==3:
                    curplay['time']={'hours':time[0], 'minutes': time[1],'seconds':time[2]}
            elif line.startswith("Duration"):
                duration=line[9:].strip()
                time=duration.split(':')
                if len(time)==1:
                    curplay['duration']={'hours':0,'minutes':0,'seconds':time}
                elif len(time)==2:
                    curplay['duration']={'hours':0, 'minutes':time[0],'seconds':time[1]}
                elif len(time)==3:
                    curplay['duration']={'hours':time[0], 'minutes': time[1],'seconds':time[2]}
            elif line.startswith("Percentage"):
                playerinfo['percentage']=line[11:].strip()
            elif line.startswith("File size"):
                curplay['filesize']=line[10:].strip()
            elif line.startswith("Changed"):
                curplay['changed']=line[8:].strip()
        return curplay,playerinfo

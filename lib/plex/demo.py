import os
from plexclient import PLEXClient, PLEXLibrary
'''
@author: Anne Jan Elsinga
This scripts serves as a demo for what the plex client library can do.
'''

PlexServer=""
PlexPort=""
TVSection=""
MovieSection=""
AlbumSection=""
NumOfItems=3
mediaplayer=object


#===============================================================================
# for servert in server.getclients():
#    print servert.address
#    print servert.uniqueid
#    print servert.version
#    print servert.name
#    print servert.host
#    
#    client=PLEXClient(servert.host,servert.port)
#    client.sendmessage(MessageTitle+","+MessageText)
#===============================================================================
#===============================================================================
# for episode in episodes:
#    print episode.title.encode('ascii','ignore') 
#===============================================================================
    
def clear_screen():
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
    
def print_menu():
    clear_screen()
    print "PLEXLibrary Demo"
    print "================="
    print
    print
    print_current_config()
    print
    print "1. Set connection info"
    
    if hasattr(mediaplayer,'server'):
        print "2. Show recently added movies"
        print "3. Show recently added episodes"
        print "4. Show recently added albums"
    print 
    print "q. quit"
    print 
 
def print_current_config():
    print "Current config:"
    print " - Plex server: ", PlexServer
    print " - Plex Port: ", PlexPort
    print " - Movies Library ID: ", MovieSection
    print " - Series Library ID: ", TVSection  
    print " - Albums Library ID: ", AlbumSection
    print " - show num of items: ", NumOfItems
    
    
def get_connection_info():
    global PlexServer
    global PlexPort
    global TVSection
    global MovieSection
    global AlbumSection
    global actions
    global NumOfItems
    
    print 
    print "Enter configuration info"
    print "========================"
    PlexServer=raw_input("Enter Plex Server (name or IP address):")
    PlexPort=raw_input("enter port: ")
    MovieSection=raw_input ("Enter the library ID for your movies: ")
    TVSection=raw_input ("Enter the library ID for your series: ")
    AlbumSection=raw_input ("Enter the library ID for your albums: ")
    NumOfItems=str2num(raw_input("Enter number of items to show: "))
    create_connection_object()
    
    
def str2num (string):
    try:
        i = int(string)
    except ValueError:
        i = 0
    return i
    
def create_connection_object():
    global mediaplayer
    
    plexconnectionstring="http://"+PlexServer+":"+PlexPort
    mediaplayer = PLEXLibrary(plexconnectionstring,MovieLibID=MovieSection, TVLibID=TVSection, MusicLibID=AlbumSection)

def no_such_action():
    print "Chosen option invalid. Please try again"

def wait_for_enter():
    raw_input("Press Enter to continue...")
    
def maxnum (item,itemstoshow):
    if len(item)<itemstoshow:
        x=len(item)
    else:
        x=NumOfItems
    return x

def showrecentlyaddedmovies():
    AllMovies=mediaplayer.getrecentlyaddedmovies()
    for x in range (0,maxnum(AllMovies,NumOfItems)):
        showmovie(AllMovies[x])
    wait_for_enter()

def showrecentlyaddedseries():
    AllSeries=mediaplayer.getrecentlyaddedepisodes()
    for x in range (0,maxnum(AllSeries,NumOfItems)):
        showseries(AllSeries[x])
    wait_for_enter() 

def showrecentlyaddedalbums():
    AllAlbums=mediaplayer.getrecentlyaddedalbums()
    for x in range (0,maxnum(AllAlbums,NumOfItems)):
        showalbums(AllAlbums[x])
    wait_for_enter() 
    
def showrecentlyairedseries():
    AllSeries=mediaplayer.recentlyAiredTV()
    for x in range (0,maxnum(AllSeries,NumOfItems)):
        showseries(AllSeries[x])
    wait_for_enter()        

def buildmenu():
    global actions
    while True:
        print_menu()
        selection = raw_input("Your selection: ")
        if "q" == selection:
            return
        toDo = actions.get(selection, no_such_action)
        toDo()
        
def asciiprint (item):
    print item.encode('ascii','ignore')
            
def showmovie(movie):
    asciiprint ("Movie title: " + movie.title)
    print ('-' * 80)

def showseries(series):
    asciiprint ("Series title: " + series.showtitle)
    asciiprint ("episode: " + str(series.season) + "x" + str(series.episode) + " " +series.title)
    print ('-' * 80)

def showalbums(album):
    asciiprint ("Album title: " + album.title)
    print ('-' * 80)
    

if __name__ == '__main__':
    actions = {"1": get_connection_info, "2": showrecentlyaddedmovies, "3": showrecentlyaddedseries,"4": showrecentlyaddedalbums}
    buildmenu()   

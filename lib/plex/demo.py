from plexclient import PLEXClient, PLEXLibrary
'''
@author: Anne Jan Elsinga
This scripts serves as a demo for what the plex client library can do.
'''

#===============================================================================
#  ask for Plex Media Server address and port
#===============================================================================
PlexServer=raw_input("Enter Plex Media Server:     ")
PlexPort=raw_input("Enter Plex Media Server port:")

MessageTitle="Test message"
MessageText="Sent to all clients"

server=PLEXLibrary("http://"+PlexServer+":"+PlexPort)
movies=server.getrecentlyaddedmovies()
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
    


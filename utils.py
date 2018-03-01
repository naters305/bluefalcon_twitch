# utils.py
# Utility Functions

import cfg
import urllib2, json
import time, thread
from time import sleep

# Function: Chat
# Sends a chat message to the server
#   Parameters:
#     sock -- the socket over which to send the message
#     msg  -- the message to send
def chat(sock, msg):
    sock.send("PRIVMSG #{} :{}\r\n".format(cfg.CHAN, msg))

# Function: Ban
# Bans a user from the channel
#   Parameters:
#       sock -- the socket in which to send a ban command
#       user -- the user that is to be banned
def ban(sock, user):
    chat(sock, ".ban {}".format(user))

# Function: Timeout
# timout a user from the channel for a set period of time
#   Parameters:
#       sock -- the socket in which to send a timeout command
#       user -- the user that is to be timedout
#       seocnds -- The length of the timeout in seconds (default 600)
def timeout(sock, user, seconds=600):
    chat(sock, ".timeout {}".format(user, seconds))

# Function: threadFillOpList
# Fills out the op list in a seperate thread
def threadFillOpList():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/naters302/chatters"
            req = urllib2.Request(url, headers={"accept": "*/*"})
            response = urllib2.urlopen(req).read()
            if response.find("502 Bad Gateway") == -1:
                cfg.oplist.clear()
                data = json.loads(response)
                for p in data["chatters"] ["moderators"]:
                    cfg.oplist[p] = "mod"
                for p in data["chatters"] ["global_mod"]:
                    cfg.oplist[p] = "global_mod"
                for p in data["chatters"] ["admins"]:
                    cfg.oplist[p] = "admin"
                for p in data["chatters"] ["staff"]:
                    cfg.oplist[p] = "staff"
        except:
            'do nothing'
        sleep(5)

def isOP(user):
    return user in cfg.oplist

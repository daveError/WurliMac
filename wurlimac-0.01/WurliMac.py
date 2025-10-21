import config
import time
import sqlite3
import random
import sys
import os
from iTunesControlClass import ITunesController

dbase = sqlite3.connect("%s.db" % config.DB_NAME)
cur = dbase.cursor()

itunes = ITunesController(config.COMMAND_SCRIPTS_DIR)
itunes.launch()

playbackModes = ["Background","Request"]
oldMode = None
ssActive = None
vizActive = None

def set_visuals(mode):
    global ssActive, vizActive

    if mode.lower() == "background":
        userPref = config.BACKGROUND_VISUALS
    else:
        userPref = config.REQUEST_VISUALS

    if userPref == 0:
        pass

    elif userPref == 1:
        if not ssActive:
            itunes.start_screensaver()
            ssActive = True
            vizActive = False

    elif userPref == 2:
        if not vizActive:
            itunes.start_visualizer()
            ssActive = False
            vizActive = True

def set_mode_volume(mode):
    if mode == "Background":
        userPref = config.BACKGROUND_VOLUME
    elif mode == "Request":
        userPref = config.REQUEST_VOLUME
    itunes.volume_change(userPref)

def mode_change(mode):
    global oldMode
    newMode = playbackModes[mode]
    if newMode == oldMode:
        pass
    else:
        set_mode_volume(newMode)
        set_visuals(newMode)
    
    oldMode = playbackModes[mode]    

def check_cooldown(trackID):
    print("Checking cooldown status...")
    defCooldownTime = config.BACKGROUND_COOLDOWN.split(":")
    cdSeconds = (int(defCooldownTime[0]) * 3600) + (int(defCooldownTime[1]) * 60)
   
    cdQuery = "SELECT last_played FROM music_library WHERE track_id = %s" % (trackID)
    cur.execute(cdQuery)
    lastPlayed = cur.fetchone()[0]
    timeItIs = int(time.time())
    if lastPlayed == None or ((timeItIs - lastPlayed) > cdSeconds):
        print("Track is available, queueing...")
        return True
        
    else:
        print('Track is in cooldown, trying again.')
        return False

def play_next_track(track_play_id):
    print("Playing track in iTunes.")
    itunes.play_track(track_play_id, config.PLAYLIST_NAME, config.LIBRARY_NAME)
    trackStatus = itunes.get_status()
    tStamp = int(time.time()) + int(trackStatus[4])
    print("Updating timestamp in last_played column...")
    cur.execute("UPDATE music_library SET last_played = ? WHERE track_id = ?", (tStamp,track_play_id))
    dbase.commit()
    sleepTime = (trackStatus[4] - trackStatus[3]) + 1
    print("Now Playing: %s by %s") % (trackStatus[0], trackStatus[1])
    return sleepTime

def select_track():
    
    cur.execute("SELECT track_id FROM request_queue")
    reqSongs = [row[0] for row in cur.fetchall()]
    if not reqSongs:
        print("No songs in Request Queue, moving to background playlist...")
        mode_change(0)
        selectLoop = True
        while selectLoop == True:
            cur.execute("SELECT track_id FROM pl_background")
            bgsongs = [row[0] for row in cur.fetchall()]
            nextTrackID = random.choice(bgsongs)
            trackAvail = check_cooldown(nextTrackID)
            if trackAvail == True:
               # print ("Selected track ID %s") % nextTrackID
                selectLoop = False
                return nextTrackID
            else:
                selectLoop = True
        
    else:
        print("Found request in the Request Queue...")
        mode_change(1)
        cur.execute("SELECT ROWID, track_id FROM request_queue ORDER BY ROWID ASC LIMIT 1")
        print("Queueing Request...")
        sql_out = cur.fetchone()
        cur.execute("DELETE FROM request_queue WHERE ROWID = ?", (sql_out[0],))
        dbase.commit()
        return sql_out[1]        

while True:
    sleepTime = play_next_track(select_track())
    time.sleep(sleepTime)
    
dbase.close()
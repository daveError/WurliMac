import config
import time
import sqlite3
import random
import sys

dbase = sqlite3.connect("%s.db" % config.DB_NAME)
cur = dbase.cursor()

def add_to_RQ(trakID):

# Only select the columns you need
    cur.execute("SELECT track_id, name, artist, album FROM music_library WHERE track_id = ?", (trakID,))
    row = cur.fetchone()

# Insert into request_queue with matching columns
    cur.execute("INSERT INTO request_queue (track_id, name, artist, album) VALUES (?, ?, ?, ?)", row)
    dbase.commit()

def check_cooldown():
    
    defCooldownTime = config.COOLDOWN_DEFAULT.split(":")
    cdSeconds = (int(defCooldownTime[0]) * 3600) + (int(defCooldownTime[1]) * 60)
    trkQuery = "SELECT track_id FROM wb_slots WHERE wb_row = '%s' AND wb_index = %s" % (sys.argv[1], sys.argv[2])
    cur.execute(trkQuery)
    trkID = cur.fetchone()[0]
    cdQuery = "SELECT last_played FROM music_library WHERE track_id = %s" % (trkID)
    cur.execute(cdQuery)
    lastPlayed = cur.fetchone()[0]
    timeItIs = int(time.time())
    if lastPlayed == None or ((timeItIs - lastPlayed) > cdSeconds):
        print('Track is available. Queueing in Request Queue...')
        add_to_RQ(trkID)
        
    else:
        print('Track is in cooldown, request rejected.')
        
check_cooldown()
dbase.close()
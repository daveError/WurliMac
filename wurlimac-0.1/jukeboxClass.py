import config
import time
import sqlite3
import random
import sys
import os
from AppleScriptControl import aScriptController


class iTunesJukebox:
    def __init__(self):
        self.dbase = sqlite3.connect("data/%s.db" % config.DB_NAME)
        self.dbCur = self.dbase.cursor()
        self.aScpt = aScriptController()
        self.visualMode = None
        self.playbackMode = None
        self.aScpt.it_launch()
        
    def set_current_mode(self, newMode):
        if newMode == self.playbackMode:
            pass
        else:
            if newMode == "Background":
                self.aScpt.it_volume_change(config.BACKGROUND_VOLUME)
                if config.BACKGROUND_VISUALS == 0:
                    pass
                elif config.BACKGROUND_VISUALS == 1:
                    if self.visualMode != "Screensaver":
                        self.aScpt.osx_start_screensaver()
                        self.visualMode = "Screensaver"
                elif config.BACKGROUND_VISUALS == 2:
                    if self.visualMode != "Visualizer":
                        self.aScpt.it_start_visualizer()
                        self.visualMode = "Visualizer"
            elif newMode == "Request":
                self.aScpt.it_volume_change(config.REQUEST_VOLUME)
                if config.REQUEST_VISUALS == 0:
                    pass
                elif config.REQUEST_VISUALS == 1:
                    if self.visualMode != "Screensaver":
                        self.aScpt.osx_start_screensaver()
                        self.visualMode = "Screensaver"
                elif config.REQUEST_VISUALS == 2:
                    if self.visualMode != "Visualizer":
                        self.aScpt.it_start_visualizer()
                        self.visualMode = "Visualizer"

            self.playbackMode = newMode
            
    def check_request_queue(self):
        self.dbCur.execute("SELECT track_id FROM request_queue ORDER BY ROWID ASC LIMIT 1")
        sql_out = self.dbCur.fetchone()
        if sql_out:
            trackID = sql_out[0]
            return trackID
        else:
            return False
                
    def pull_request(self,trackID):
        self.dbCur.execute("DELETE FROM request_queue WHERE track_id = ?", (trackID,))
        self.dbase.commit()
        
    def check_cooldown(self,trackID):
        self.dbCur.execute("SELECT last_played FROM music_library WHERE track_id = ?", (trackID,))
        sql_out = self.dbCur.fetchone()
        timestamp = int(sql_out[0])
        if self.playbackMode == "Background":
            cfgCooldown = config.BACKGROUND_COOLDOWN.split(":")
        elif self.playbackMode == "Request":
            cfgCooldown = config.REQUEST_COOLDOWN.split(":")
        cdSeconds = (int(cfgCooldown[0]) * 3600) + (int(cfgCooldown[1]) * 60)
        currentTime = int(time.time())
        if timestamp == None or ((currentTime - timestamp) > cdSeconds):
            return True
        else:
            return False
    
    def update_timestamp(self,trackID,trackDuration):
        tStamp = int(time.time()) + int(trackDuration)
        self.dbCur.execute("UPDATE music_library SET last_played = ? WHERE track_id = ?", (tStamp,trackID))
        self.dbase.commit()
    
    def select_random(self, rMode = config.RANDOM_MODE):
        cfgCooldown = config.BACKGROUND_COOLDOWN
        cooldownSeconds = (int(cfgCooldown[0]) * 3600) + (int(cfgCooldown[1]) * 60)
        rightNow = int(time.time())
        if rMode == 0: # "True" random
            sqlQuery = """
            SELECT track_id
            FROM pl_background
            JOIN music_library USING (track_id)
            WHERE last_played IS NULL OR last_played < %d
            ORDER BY RANDOM()
            LIMIT 1
            """ % (rightNow - cooldownSeconds)
        elif rMode == 1: # Weighted by timestamp
            sqlQuery = """
            SELECT track_id
            FROM pl_background
            JOIN music_library USING (track_id)
            WHERE last_played IS NULL OR last_played < %d
            ORDER BY (%d - IFNULL(last_played, 0)) * RANDOM() DESC
            LIMIT 1
            """ % ((rightNow - cooldownSeconds), rightNow)
        self.dbCur.execute(sqlQuery)
        sql_out = self.dbCur.fetchone()
        return int(sql_out[0])
    
    def play_song(self,trackID):
        self.aScpt.it_play_track(trackID)
        status = self.aScpt.it_get_status()
        self.update_timestamp(trackID,status[4])
        return status
    
    def stop_playback(self):
        self.aScpt.it_stop()
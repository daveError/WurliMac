#!/usr/bin/env python2.7
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import config
import urlparse
import json
import sqlite3
import os
import time
import random
import sys
import mimetypes

defCooldownTime = config.REQUEST_COOLDOWN.split(":")
cdSeconds = (int(defCooldownTime[0]) * 3600) + (int(defCooldownTime[1]) * 60)

def get_songs_forWB(params):
    letter = params.get('letter', [''])[0].upper()
    if not letter:
        return {"status": "error", "message": "Missing 'letter' parameter."}
    try:
        dbc = sqlite3.connect("data/%s.db" % config.DB_NAME)
        cur = dbc.cursor()
        cur.execute("SELECT name,artist,wb_index FROM wb_slots WHERE wb_row = ? ORDER BY CASE WHEN wb_index = 0 THEN 10 ELSE wb_index END ASC", (letter,))
        rows = cur.fetchall()
        dbc.close()
        
        selections = [{"index": r[2] , "name": r[0], "artist": r[1]} for r in rows]
        return {"status": "success", "letter": letter, "selections": selections}
    except sqlite3.Error as e:
        return {"status": "error", "message": str(e)}

def queue_song(params):
    letter = params.get('letter', [''])[0].upper()
    number = params.get('number', [''])[0]
    
    dbc = sqlite3.connect("data/%s.db" % config.DB_NAME)
    cur = dbc.cursor()
    trkQuery = "SELECT track_id FROM wb_slots WHERE wb_row = '%s' AND wb_index = %s" % (letter, number)
    cur.execute(trkQuery)
    trkID = cur.fetchone()[0]
    cdQuery = "SELECT last_played FROM music_library WHERE track_id = %s" % (trkID)
    cur.execute(cdQuery)
    lastPlayed = cur.fetchone()[0]
    timeItIs = int(time.time())
    if lastPlayed == None or ((timeItIs - lastPlayed) > cdSeconds):
        cur.execute("SELECT track_id, name, artist, album FROM music_library WHERE track_id = ?", (trkID,))
        row = cur.fetchone()
        cur.execute("INSERT INTO request_queue (track_id, name, artist, album) VALUES (?, ?, ?, ?)", row)
        dbc.commit()
        return {"status": "success", "message": "Added track to request queue."}
    else:
        return {"status": "error", "message": "Track is in cooldown, try again later."}

#def serve_html_wallbox(params)

def check_available_tracks(params):
    letter = params.get('letter', [''])[0].upper()
    availableTracks = []
    queuedTracks = []
    unavailableTracks = []
    npTrack = []
    lastP = []
    daTime = []
    if not letter:
        return {"status": "error", "message": "Missing 'letter' parameter."}    
    try:
        dbc = sqlite3.connect("data/%s.db" % config.DB_NAME)
        cur = dbc.cursor()
        cur.execute("SELECT track_id, wb_index FROM wb_slots WHERE wb_row = ? ORDER BY CASE WHEN wb_index = 0 THEN 10 ELSE wb_index END ASC", (letter,))
        rows = cur.fetchall()
        timeItIs = int(time.time())
        for trackId, trackIndex in rows:
            
            cur.execute("SELECT last_played FROM music_library WHERE track_id = ?", (trackId,))
            trackLastPlayed = cur.fetchone()[0]
            cur.execute("SELECT track_id FROM request_queue WHERE track_id = ?", (trackId,))
            trackInQueue = cur.fetchone()
            if trackLastPlayed == None:
                trackLastPlayed = 0
            if trackInQueue:
                queued = True
            else:
                queued = False
            
                 
            lastPlayed = int(trackLastPlayed)
            lastP.append(lastPlayed)
            daTime.append(timeItIs)
            if ((timeItIs - lastPlayed) > cdSeconds) and queued == False:
                availableTracks.append(trackIndex)
            elif ((timeItIs - lastPlayed) > cdSeconds) and queued == True:
                queuedTracks.append(trackIndex)
            else:
                if (lastPlayed > timeItIs):
                    npTrack.append(trackIndex)
                else:
                    unavailableTracks.append(trackIndex)
        dbc.close()
        return {"available": availableTracks,
        "queued": queuedTracks,
        "cooldown": unavailableTracks,
        "nowPlaying": npTrack,
#        "lpList": lastP,
#        "curTime": daTime
        }
    except sqlite3.Error as e:
        return {"status": "error", "message": str(e)}

def serve_html_wallbox(params):
    with open('web/wallbox_base_new.html', 'rb') as f:
        return (f.read())

def show_admin_panel(params):
    with open('web/admin_panel.html', 'rb') as f:
        return (f.read())

def admin_functions(params):
    pass

class httpHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, code=200):
        response = json.dumps(data)
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))

    def do_GET(self):
        parsed = urlparse.urlparse(self.path)
        params = urlparse.parse_qs(parsed.query)

        path_switch = {
            "/wbList": get_songs_forWB,
            "/queueSong": queue_song,
            "/checkAvail": check_available_tracks,
            "/adminFunc": admin_functions,
            "/main": serve_html_wallbox,
            "/admin": show_admin_panel
        }

        if parsed.path.startswith('/static/'):
            file_path = "web/"+parsed.path.lstrip('/')
            if os.path.exists(file_path):
                mime_type, _ = mimetypes.guess_type(file_path)
                self.send_response(200)
                self.send_header('Content-type', mime_type or 'application/octet-stream')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'File not found')
            return

        handler = path_switch.get(parsed.path)
        if handler:
            result = handler(params)

            if parsed.path == "/main":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(result.encode("utf-8"))
                
            elif parsed.path == "/admin":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(result.encode("utf-8"))
                
            else:
                self._send_json(result)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')


#    def do_POST(self):
#        length = int(self.headers.get('Content-Length', 0))
#        body = self.rfile.read(length)
#        params = urlparse.parse_qs(body)
#        result = handle_request(params)
#        self._send_json(result)

    def log_message(self, fmt, *args):
        # Silence default console logging (optional)
        pass

if __name__ == '__main__':
    PORT = config.HTTP_PORT
    server = HTTPServer(('0.0.0.0', PORT), httpHandler)
    print("Serving on port %d..." % PORT)
    server.serve_forever()
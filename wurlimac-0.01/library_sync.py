import config
import time
import calendar
import datetime
import os
import sqlite3
import plistlib
import re
from iTunesControlClass import ITunesController
iTunesLibrary = None

itunes = ITunesController(config.COMMAND_SCRIPTS_DIR)


dBase = config.DB_NAME + ".db"

sqlCon = sqlite3.connect(dBase)
cur = sqlCon.cursor()

def itunes_export():
   # print("Exporting library from iTunes...")
    itunes.launch()
    itunes.export_library()


def library_import():
    global iTunesLibrary
    iTunesLibrary = plistlib.readPlist(config.ITUNES_LIBRARY)

def sync_library():

    query = "DELETE FROM music_library"
    cur.execute(query)
    sqlCon.commit()
    tracks = iTunesLibrary['Tracks']

    for track_id_str, track_info in tracks.items():
        track_id = int(track_id_str)
        name = track_info.get('Name', '')
        artist = track_info.get('Artist', '')
        album = track_info.get('Album', '')
        last_played_utc = None
        last_played_utc = track_info.get('Play Date UTC' ,'')

        if last_played_utc:
            
            last_played_unix = int(calendar.timegm(last_played_utc.timetuple()))
       #     last_played_corrected = (last_played_unix - 10800)
            cur.execute("""
                INSERT OR REPLACE INTO music_library 
                (track_id, name, artist, album, last_played)
                VALUES (?, ?, ?, ?, ?)
            """, (track_id, name, artist, album, last_played_unix))
        
        else:

            cur.execute("""
                INSERT OR REPLACE INTO music_library 
                (track_id, name, artist, album)
                VALUES (?, ?, ?, ?)
            """, (track_id, name, artist, album))

    sqlCon.commit()
    print("Library import complete. {} tracks added.".format(len(tracks)))
    

def sync_background():

    cur.execute("DELETE FROM pl_background")
    playlists = iTunesLibrary['Playlists']

    for playlist in playlists:
        if playlist.get('Name') == 'Background':
            items = playlist.get('Playlist Items', [])
            print("Found playlist '{}', {} tracks".format(
                playlist['Name'], len(items)))

            rows = []
            for item in items:
                track_id = item['Track ID']
                track_info = iTunesLibrary['Tracks'].get(str(track_id), {})
                name = track_info.get('Name', '')
                artist = track_info.get('Artist', '')
                album = track_info.get('Album', '')
                rows.append((track_id, name, artist, album))

            # Bulk insert for efficiency
            cur.executemany("""
                INSERT INTO pl_background (track_id, name, artist, album)
                VALUES (?, ?, ?, ?)
            """, rows)

            sqlCon.commit()
            print("Playlist import complete. {} tracks added.".format(len(rows)))
            break

def sync_wallboxes():
    playlists = iTunesLibrary['Playlists']

    wallboxes = {}

    for playlist in playlists:
        name = playlist.get('Name', '')
        # Match wallbox + letter at start of name, ignore everything after
        m = re.match(r'wallbox([A-Z])', name, re.I)
        if not m:
            continue  # skip playlists that don't match

        letter = m.group(1).upper()

        items = playlist.get('Playlist Items', [])
        tracks = []

        for item in items:
            track_id = item['Track ID']
            track_info = iTunesLibrary['Tracks'].get(str(track_id), {})
            tracks.append({
                'track_id': track_id,
                'name': track_info.get('Name', ''),
                'artist': track_info.get('Artist', ''),
                'album': track_info.get('Album', '')
            })

        wallboxes[letter] = tracks[:10]

    # Write to wb_slots table
    cur.execute("DELETE FROM wb_slots")  # full reset

    for letter, tracks in wallboxes.items():
        for idx, track in enumerate(tracks):
            wb_index = idx + 1
            if wb_index == 10:
                wb_index = 0

            cur.execute("""
                INSERT INTO wb_slots (wb_row, wb_index, track_id, name, artist, album)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                letter,
                wb_index,
                track['track_id'],
                track['name'],
                track['artist'],
                track['album']
            ))

    sqlCon.commit()
    print("All wallboxes synced to wb_slots.")

print("Exporting iTunes library, please do not touch your mouse or keyboard.")
itunes_export()

time.sleep(4)
print("Hiding iTunes main window...")
itunes.hide_itunes()
time.sleep(3)
print("Importing new iTunes Library XML...")
library_import()
time.sleep(2)

sync_library()

sync_background()
sync_wallboxes()

sqlCon.close()

print("Hiding terminal window, enjoy WurliMac!")
time.sleep(2)
itunes.hide_terminal()
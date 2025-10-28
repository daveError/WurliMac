import config
import time

from jukeboxClass import iTunesJukebox

jukebox = iTunesJukebox()

while True:
    trackID = jukebox.check_request_queue()
    if trackID:
        jukebox.pull_request(trackID)
        jukebox.set_current_mode("Request")
        status = jukebox.play_song(trackID)
    else:
        if config.JUKEBOX_MODE == 0: # Requests only.
            time.sleep(1)
            continue
        elif config.JUKEBOX_MODE == 1: # Background and requests.
            trackID = jukebox.select_random()
            if trackID:
                jukebox.set_current_mode("Background")
                status = jukebox.play_song(trackID)
    trackDuration = int(status[4])
    trackPosition = int(status[3])
    sleepTime = (trackDuration - trackPosition) + 1
    time.sleep(sleepTime)
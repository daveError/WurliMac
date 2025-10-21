# Location of the iTunes Library XML for database syncing.
# DO NOT use iTunes Music Library.xml, always export a new copy.
ITUNES_LIBRARY = "savedLibrary.xml"

# Name of the directory with the AppleScripts that control iTunes.
COMMAND_SCRIPTS_DIR = "classCmdScripts"

# Name of the SQLite database. It will be this + ".db" when the script executes,
# no need to put the file extension here.
DB_NAME = "WurliMac"

# Port to run the HTTP daemon on.
HTTP_PORT = 7338

# Name of the playlist where playback happens.
PLAYLIST_NAME = "Jukebox"

# You can use the iTunes library, or choose a specifically curated playlist.
LIBRARY_NAME = "Library"

# Sets the iTunes volume for requests and background tracks.
# Will likely take some trial and error on your particular audio setup.
# Acceptable values between 0 and 100.
REQUEST_VOLUME = 95
BACKGROUND_VOLUME = 70

# What to display during playback.
# Options:
# 0 - Do nothing (show iTunes window/desktop)
# 1 - Run screensaver
# 2 - Run iTunes visualizer
REQUEST_VISUALS = 2      # what happens during a request
BACKGROUND_VISUALS = 1   # what happens during background playback

# Default cooldown time for requests and background tracks.
REQUEST_COOLDOWN = "02:00" #HH:MM
BACKGROUND_COOLDOWN = "08:00"

##----------- AS OF YET UNIMPLEMENTED FEATURES -----------##
##-----------     THESE SETTINGS DO NOTHING    -----------##

# Maximum number of requests per wallbox.
CONCURRENT_REQUESTS = 1

# If you want new requests to play immediately instead of waiting for 
# the current track to finish. 0 for off, 1 for on.
REQUEST_INTERRUPT = 0 

# Background playlist populates with two tracks
# at a time. You can use this and enable crossfading in iTunes.
# Should work, anyway.
TWO_AT_A_TIME = 1

# Runs background music when there's no request queued.
# Set to 0 if you want your jukebox to be "request only."
BACKGROUND_MODE = 1
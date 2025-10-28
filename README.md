WurliMac!
This project is inspired by the old-school Wurlitzer and Seeburg jukeboxes, as well as a practical "revitalization" project for any vintage PPC machine, provided it has the memory to run Tiger.

Inside you'll find a set of Python scripts and an SQLite database. You will need to install Python 2.7 on your Tiger installation, as it doesn't come with 2.7 by default, but it's very necessary to get a slightly newer version of Python for SQLite support. Other than that, the out-of-the-box versions of SQLite and iTunes should work well as those are what I used for development.
I recommend Macintosh Repository.

Your playlists are curated in iTunes. You'll want to create eleven playlists, one named Background, ten named wallboxA, wallboxB... through wallboxK, omitting I, with ten tracks in each. Your background playlist can have as many tracks as you wish. This data will get synced with the SQLite database when you run library_sync.py. Once you've done that, you should be able to run http_daemon.py and wurli_daemon.py.

http_daemon.py does exactly what it sounds like, it provides a simple set of endpoints that serve an HTML wallbox UI and its respective AJAX calls.
wurli_daemon.py is the main jukebox "daemon," which I'll admit isn't really a proper daemon, it's just a continuous loop that plays music. In the future I'll definitely add a "stop" button!

When a request comes through, the "daemon" plays it and switches the visuals into the selected mode for request tracks. You can see a few unimplemented features in config.py that I hope to write with the next version of this.

Everything else should be reasonably laid out in config.py. This is my first GitHub repository and this project was fueled by ADHD, so I apologize if my documentation isn't the most coherent. I do hope this project reaches an audience that will appreciate it, and possibly even help me improve on this.
Happy Grooving!

-Dave

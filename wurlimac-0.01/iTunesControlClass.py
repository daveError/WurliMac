import os

class ITunesController:
    def __init__(self, scripts_dir):
        self.scripts_dir = scripts_dir

    def play_track(self, track_index, playlist, library_name):
        #track_name_escaped = track_name.replace('"', '\\"')
        print("Playing Track ID %s.") % track_index
        cmd = 'osascript "%s/playTrack.scpt" "%s" "%s" "%s"' % (self.scripts_dir, int(track_index), playlist, library_name)
        os.popen(cmd).read()

    def stop(self):
        cmd = 'osascript "%s/stop.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()

    def pause(self):
        cmd = 'osascript "%s/pause.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()

    def playpause(self):
        cmd = 'osascript "%s/playpause.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()

    def volume_change(self, volLevel):
        print("Setting iTunes volume to %s...") % volLevel
        cmd = 'osascript "%s/adjustVolume.scpt" %s' % (self.scripts_dir, volLevel)
        os.popen(cmd).read()
        
    def get_status(self):
        cmd = 'osascript "%s/pollStatus.scpt"' % (self.scripts_dir)
        asOutput = os.popen(cmd).read().strip()
        parts = asOutput.split("||")
        if len(parts) >= 5:
            try:
                parts[3] = int(float(parts[3]))  # player position
                parts[4] = int(float(parts[4]))  # track duration
            except ValueError:
                parts[3] = 0
                parts[4] = 0
        return parts
        
    def launch(self):
        cmd = 'osascript "%s/launchiTunes.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()
    
    def start_visualizer(self):
        print("Starting iTunes visualizer...")
        cmd = 'osascript "%s/startViz.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()
    
    def start_screensaver(self):
        print("Starting Mac OS default screensaver...")
        cmd = 'osascript "%s/startSS.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()
    
    def export_library(self):
        print("Exporting iTunes library as XML, please do NOT touch your mouse or keyboard!")
        cmd = 'osascript "%s/exportLibrary.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()
        
    def hide_itunes(self):
        cmd = 'osascript "%s/hideiTunes.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()
        
    def hide_terminal(self):
        cmd = 'osascript "%s/hideTerminal.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()
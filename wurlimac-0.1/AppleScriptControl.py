import os
import config

class aScriptController:
    def __init__(self, scripts_dir = config.APPLESCRIPTS_DIR):
        self.scripts_dir = scripts_dir

    def it_play_track(self, track_index, playlist = config.PLAYLIST_NAME, library_name = config.LIBRARY_NAME):
        #track_name_escaped = track_name.replace('"', '\\"')
        print("Playing Track ID %s.") % track_index
        cmd = 'osascript "%s/playTrack.scpt" "%s" "%s" "%s"' % (self.scripts_dir, int(track_index), playlist, library_name)
        os.popen(cmd).read()

    def it_stop(self):
        cmd = 'osascript "%s/stop.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()

    def it_pause(self):
        cmd = 'osascript "%s/pause.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()

    def it_playpause(self):
        cmd = 'osascript "%s/playpause.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()

    def it_volume_change(self, volLevel):
        print("Setting iTunes volume to %s...") % volLevel
        cmd = 'osascript "%s/adjustVolume.scpt" %s' % (self.scripts_dir, volLevel)
        os.popen(cmd).read()
        
    def it_get_status(self):
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
        
    def it_launch(self):
        print("Launching iTunes!")
        cmd = 'osascript "%s/launchiTunes.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()
    
    def it_start_visualizer(self):
        print("Starting iTunes visualizer...")
        cmd = 'osascript "%s/startViz.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()
    
    def osx_start_screensaver(self):
        print("Starting Mac OS default screensaver...")
        cmd = 'osascript "%s/startSS.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()
    
    def it_export_library(self):
        workingDir = os.getcwd()
        print("Exporting iTunes library as XML, please do NOT touch your mouse or keyboard!")
        cmd = 'osascript "%s/exportLibrary.scpt" %s' % (self.scripts_dir, workingDir)
        os.popen(cmd).read()
        
    def osx_hide_itunes(self):
        print("Hiding iTunes window...")
        cmd = 'osascript "%s/hideiTunes.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()
        
    def osx_hide_terminal(self):
        print("Hiding the Terminal window...")
        cmd = 'osascript "%s/hideTerminal.scpt"' % (self.scripts_dir)
        os.popen(cmd).read()
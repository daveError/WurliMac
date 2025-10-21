tell application "System Events" 
    key code 53
    end tell
delay 1.5

tell application "iTunes"
    activate
    end tell

tell application "System Events"
    keystroke "t" using {command down}
    end tell
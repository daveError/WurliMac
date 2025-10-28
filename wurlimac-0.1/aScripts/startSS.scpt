tell application "System Events" 
    key code 53
    end tell
delay 1.5
do shell script "/System/Library/Frameworks/ScreenSaver.framework/Resources/ScreenSaverEngine.app/Contents/MacOS/ScreenSaverEngine >/dev/null 2>&1 &"
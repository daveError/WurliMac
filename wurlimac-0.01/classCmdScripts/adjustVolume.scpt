on run argv
	set volumeLevel to (item 1 of argv) as integer
	tell application "iTunes"
    	set sound volume to volumeLevel
	end tell
end run
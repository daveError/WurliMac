tell application "iTunes"
	if player state is playing then
		set trackName to name of current track
		set trackArtist to artist of current track
		set trackAlbum to album of current track
		set trackPosition to player position
		set trackDuration to duration of current track
		return trackName & "||" & trackArtist & "||" & trackAlbum & "||" & trackPosition & "||" & trackDuration
	else
		return "stopped"
	end if
end tell

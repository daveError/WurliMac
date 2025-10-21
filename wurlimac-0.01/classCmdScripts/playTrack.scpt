on run argv
    set trackIndex to (item 1 of argv)
    set tempPlaylistName to item 2 of argv
    set sourcePlaylistName to item 3 of argv
    
    tell application "iTunes"
         if not (exists playlist tempPlaylistName) then
            set tempPlaylist to make new user playlist with properties {name:tempPlaylistName}
        else
            set tempPlaylist to playlist tempPlaylistName
        end if

		-- Clear any existing tracks from Temp playlist
        repeat with t in (every track of tempPlaylist)
            delete t
        end repeat

        -- Get the track from the Library
        set sourcePlaylist to playlist sourcePlaylistName
        set trackToPlay to first track of sourcePlaylist whose database ID is trackIndex

        -- Duplicate track into Temp playlist
        duplicate trackToPlay to tempPlaylist
        set trackInTemp to first track of tempPlaylist

        -- Play the track in Temp playlist
        play trackInTemp
    end tell
end run

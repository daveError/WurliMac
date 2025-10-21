tell application "iTunes" to activate

tell application "System Events"
    tell process "iTunes"
        delay 1

        -- Step 1: open File menu
        perform action "AXPress" of menu bar item "File" of menu bar 1
        delay 0.5

        -- Step 2: choose Export Library… (item 11)
        perform action "AXPress" of menu item 11 of menu 1 of menu bar item "File" of menu bar 1
        delay 1.5
    end tell

    -- Step 3: open the "Go to Folder" sheet in the Save dialog
    key down command
    key down shift
    key code 5
    key up shift
    key up command
    delay 0.7

    -- Step 4: type the folder path, replace this with your path to the wurlimac directory
    keystroke "~/wurlimac"
    delay 0.3
    key code 36 -- Return to go there
    delay 0.8

    -- Step 5: type the export filename
    keystroke "savedLibrary"
    delay 0.3
    key code 36 -- Return to save

    delay 0.8
    key code 48 -- Tab
    delay 0.2
    key code 49 -- Space

end tell

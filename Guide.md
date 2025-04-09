# Generating Beat Markers for Video Editing with BeatMarker

This guide explains how to accurately determine your audio track's Beats Per Minute (BPM) and generate a list of timestamps (markers) using the `BeatMarker` tool. These markers can then be imported or used as guides in video editing software like DaVinci Resolve, Premiere Pro, Final Cut Pro, etc., to easily sync cuts or effects to the music's beat.

We'll use [Audacity](https://www.audacityteam.org/) for basic audio handling and [Arrow Vortex](https://arrowvortex.ddrnl.com/) for precise BPM and timing analysis.

## Prerequisites

1.  **Your Audio File:** The song or audio track you want to create markers for (preferably a high-quality WAV, FLAC, or high-bitrate MP3/M4A).
2.  **[Audacity](https://www.audacityteam.org/):** Free, open-source audio editor. Used for viewing waveforms and exporting to `.ogg` for Arrow Vortex.
    *   _(Optional but Recommended)_ Install the [FFmpeg library for Audacity](https://manual.audacityteam.org/man/installing_ffmpeg_for_windows.html) (or the equivalent for your OS) to open more audio formats like M4A.
3.  **[Arrow Vortex](https://arrowvortex.ddrnl.com/):** Free tool for rhythm game charting, excellent for finding BPM and precise beat timing.
    *   BSMG Re-packed [Zip Download](https://bsmg.dev/zY55r) (Recommended, easier setup)
    *   Arrow Vortex Website [Rar Download](https://arrowvortex.ddrnl.com/) (Requires software like 7-Zip to extract)
    *   See [Troubleshooting Arrow Vortex](#troubleshooting-arrow-vortex) if it doesn't run.
4.  **[BeatMarker](https://github.com/Jakey-Jakey/BeatMarker):** Your command-line tool for generating the timestamp list.
    *   Download the pre-built executable from the [Releases page](https://github.com/Jakey-Jakey/BeatMarker/releases) (easiest).
    *   Or run from the Python script (`beat_marker_generator.py`), ensuring you have Python 3.7+ and have installed dependencies: `pip install mutagen colorama`.

## Workflow Overview

1.  **Prepare Audio & Export for Analysis:** Use Audacity to prepare your audio file and export it in `.ogg` format for Arrow Vortex.
2.  **Find BPM & First Beat Time:** Use Arrow Vortex to determine the precise BPM and identify the exact timestamp of the first beat you want a marker on.
3.  **Get Audio Duration:** Obtain the total duration of your original audio file.
4.  **Generate Markers:** Use `BeatMarker` with the obtained Duration, BPM, and desired settings.
5.  **Use Markers in Editor:** Import or use the generated `beat_markers.txt` file in your video editing software and align the markers.

---

## Step 1: Prepare Audio & Export for Analysis (Audacity)

While `BeatMarker` can often read duration directly, Arrow Vortex works most reliably with `.ogg` files. We also use Audacity to confirm the total duration later.

1.  **Open Audio in Audacity:** Launch Audacity and open your original audio file (`File > Open`).
2.  **Check Quality (Optional but Recommended):** Ensure your audio looks clean in the waveform view. Avoid low-quality rips if possible, as clear transients make BPM detection easier.
3.  **Export as OGG:**
    *   Go to `File > Export > Export as OGG`.
    *   Save the file somewhere easily accessible (e.g., name it `song_for_av.ogg`).
    *   When prompted for OGG Quality, a setting of 5 or 6 is usually sufficient for analysis purposes. Click `Save`.
    *   You can ignore the metadata tags prompt and just click `OK`.

**Important:** Keep your *original* audio file (WAV, MP3, etc.) handy. You'll use the original file in your video editor, not necessarily this `.ogg` export. We only need the `.ogg` for Arrow Vortex analysis.

---

## Step 2: Find BPM & First Beat Time (Arrow Vortex)

Arrow Vortex helps us find the exact BPM and the timing of the first beat we care about.

1.  **Open Arrow Vortex:** Launch `ArrowVortex.exe`.
2.  **Load the OGG:** Drag and drop the `song_for_av.ogg` file you just created into the Arrow Vortex window.
3.  **View Waveform:** Go to the `View` menu and click `Time based (C-mod)` to see the waveform clearly against time. You can zoom using `Ctrl + Mouse Wheel`.
4.  **Find BPM:**
    *   Press `Shift + S` (or go to `Tempo > Adjust sync...`).
    *   Click the `Find BPM` button.
    *   Arrow Vortex will analyze the track. Often, it finds one BPM with high confidence. If it suggests multiple BPMs, the top one is usually correct, but you may need to verify.
    *   Click `Apply BPM` for the selected (usually top) BPM value.
5.  **Confirm BPM:**
    *   Press `F3` to toggle the metronome beat ticks on.
    *   Press `Spacebar` to play the audio. Listen carefully, especially during different sections (intro, verse, chorus, outro). Do the ticks align perfectly with the beat throughout the song?
    *   If the ticks drift, your song might have **variable BPM**. This makes marker generation much harder and may require manual adjustments or specialized tools beyond this guide. For simplicity, choose songs with a consistent BPM if possible. If ticks don't match even at the start, try other BPM suggestions from the `Find BPM` step if any were offered.
6.  **Identify First Beat Timestamp:**
    *   Play the song or scrub through the waveform in Arrow Vortex.
    *   Decide where you want your *first marker* to be placed. This might be the very first beat of the song, or the first beat of the main section after an intro.
    *   Carefully place the playback cursor (the thin vertical line) precisely on the start of that desired first beat. Zoom in (`Ctrl + Scroll`) for accuracy.
    *   Look at the time display in Arrow Vortex (usually near the top or bottom). Note down this exact time (e.g., `2.345` seconds). This is your **First Beat Timestamp**. *We won't directly input this into BeatMarker (as it doesn't currently take an offset), but we'll use it later for alignment.*
7.  **Note Down BPM:** Ensure you have the precise BPM value confirmed in step 5 (e.g., `128.000` or `95.500`).
8.  You can now close Arrow Vortex.

---

## Step 3: Get Audio Duration

`BeatMarker` needs the total duration of your song.

*   **Method 1: Automatic (Recommended)**
    *   Drag your **original** audio file (MP3, WAV, FLAC, M4A, etc.) directly onto the `BeatMarker.exe` file icon or onto the `beat_marker_generator.py` script in your terminal.
    *   If successful, `BeatMarker` will display the detected duration and skip asking for it manually. This requires the `mutagen` library to be installed if running the Python script, or included if using the executable.
*   **Method 2: Manual**
    *   If you didn't use drag-and-drop, or if it failed, `BeatMarker` will prompt you to enter the duration.
    *   You can find the exact duration in Audacity. Open your **original** audio file. The total length is usually displayed at the bottom or top of the window.
    *   Enter the duration in `MM:SS.sss` format (e.g., `03:45.500`) when prompted by `BeatMarker`.

---

## Step 4: Generate Markers (BeatMarker)

Now, run `BeatMarker` and provide the information gathered.

1.  **Run BeatMarker:**
    *   Double-click `BeatMarker.exe`.
    *   Or open a terminal/command prompt, navigate to the script's directory, and run `python beat_marker_generator.py`.
    *   _(If using drag-and-drop for duration, you would have already done this in Step 3)._
2.  **Follow Prompts:**
    *   **Duration:** Provide manually if not auto-detected (Step 3).
    *   **BPM:** Enter the precise BPM value you found using Arrow Vortex (Step 2, e.g., `128`).
    *   **Marker Interval:**
        *   `1`: Marker on every beat (e.g., 1, 2, 3, 4 in 4/4 time).
        *   `2`: Marker every 2 beats (e.g., 1, 3 in 4/4 time, often the half-measure).
        *   `4`: Marker every 4 beats (e.g., 1 in 4/4 time, often the start of a measure). Choose based on how frequent you need your guides.
    *   **Output Format:**
        *   `s`: Simple format (`MM:SS.sss`). Good for many general purposes.
        *   `tc`: Timecode format (`HH:MM:SS:FF`). Essential if your NLE uses timecode markers.
    *   **Framerate (if `tc` chosen):** Enter the exact framerate of your video editing project (e.g., `23.976`, `29.97`, `30`, `59.94`, `60`). **Getting this wrong will result in inaccurate timecode markers.**
3.  **Output:** `BeatMarker` will calculate and generate the markers, saving them to a file named `beat_markers.txt` in the same directory where you ran it.

---

## Step 5: Use Markers in Your Video Editor

The generated `beat_markers.txt` file contains your timestamps, calculated relative to the start (00:00.000) of the audio file based on the BPM. Now, align them in your editor:

1.  **Import Audio:** Import your **original** audio file (WAV, MP3, etc.) into your video editing software timeline.
2.  **Import/Place Markers:** This process varies greatly between editors:
    *   **Copy/Paste:** Some editors might allow you to copy the list from `beat_markers.txt` and paste them directly onto the timeline or media clip as markers.
    *   **Manual Placement:** Open `beat_markers.txt`. Go to the first timestamp in your editor, place a marker, go to the second, place a marker, and so on. This is tedious but always works.
    *   **Scripting:** Some editors (like DaVinci Resolve) might support scripting (Python) to read the text file and create markers automatically.
    *   **EDL Import:** You might be able to format the `beat_markers.txt` content into an Edit Decision List (EDL) format and import that. (Requires knowledge of EDL formats). Consult your editor's documentation for marker import options.
3.  **Align the Marker Sequence:**
    *   Find the **First Beat** in your audio waveform within your video editor – the same beat you identified the timestamp for in Arrow Vortex (Step 2).
    *   Select **all** the markers you just imported/placed.
    *   **Shift the entire group** of markers forwards or backwards on the timeline so that the **very first marker** in your sequence aligns perfectly with that **First Beat** you identified on the waveform.
    *   Once the first marker is aligned, all subsequent markers should automatically align correctly with the beats of the song, thanks to the accurate BPM calculation.

You now have precisely timed beat markers on your timeline, ready to guide your edits!

---

## Troubleshooting Arrow Vortex

*   **`MSVCP120.dll was not found` Error:** You need the Microsoft Visual C++ 2013 Redistributable (x86 version). Download and install `vcredist_x86.exe` from [Microsoft's support page](https://support.microsoft.com/en-us/help/4032938/update-for-visual-c-2013-redistributable-package). Make sure it's the **x86** version, even on a 64-bit system.
*   **Arrow Vortex Doesn't Open:** Ensure you extracted the `.zip` or `.rar` file correctly. Try running as administrator (though usually not needed). Ensure the C++ redistributable is installed.

---

This process gives you a robust way to sync visual elements to your audio track's rhythm using the convenient `BeatMarker` tool. Happy editing!

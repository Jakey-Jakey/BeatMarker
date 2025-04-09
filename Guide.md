# Generating Beat Markers for Video Editing with BeatMarker

This guide explains how to accurately determine your audio track's Beats Per Minute (BPM), adjust its starting offset, and generate a list of timestamps (markers) using the `BeatMarker` tool. These markers can then be imported or used as guides in video editing software like DaVinci Resolve, Premiere Pro, Final Cut Pro, etc., to easily sync cuts or effects to the music's beat.

We'll use [Audacity](https://www.audacityteam.org/) for audio preparation and [Arrow Vortex](https://arrowvortex.ddrnl.com/) for precise BPM and timing analysis.

## Prerequisites

1.  **Your Audio File:** The song or audio track you want to create markers for (preferably a high-quality WAV, FLAC, or high-bitrate MP3/M4A).
2.  **[Audacity](https://www.audacityteam.org/):** Free, open-source audio editor. Used for modifying the audio start time and exporting.
    *   _(Optional but Recommended)_ Install the [FFmpeg library for Audacity](https://manual.audacityteam.org/man/installing_ffmpeg_for_windows.html) (or the equivalent for your OS) to open more audio formats like M4A.
3.  **[Arrow Vortex](https://arrowvortex.ddrnl.com/):** Free tool for rhythm game charting, excellent for finding BPM and precise beat timing.
    *   BSMG Re-packed [Zip Download](https://bsmg.dev/zY55r) (Recommended, easier setup)
    *   Arrow Vortex Website [Rar Download](https://arrowvortex.ddrnl.com/) (Requires software like 7-Zip to extract)
    *   See [Troubleshooting Arrow Vortex](#troubleshooting-arrow-vortex) if it doesn't run.
4.  **[BeatMarker](https://github.com/Jakey-Jakey/BeatMarker):** Your command-line tool for generating the timestamp list.
    *   Download the pre-built executable from the [Releases page](https://github.com/Jakey-Jakey/BeatMarker/releases) (easiest).
    *   Or run from the Python script (`beat_marker_generator.py`), ensuring you have Python 3.7+ and have installed dependencies: `pip install mutagen colorama`.

---

## Step 1: Prepare Audio & Export for Analysis (Audacity)

Arrow Vortex works most reliably with `.ogg` files. We also use Audacity to potentially modify the audio's start time later.

1.  **Open Audio in Audacity:** Launch Audacity and open your original audio file (`File > Open`).
2.  **Check Quality (Optional but Recommended):** Ensure your audio looks clean in the waveform view. Avoid low-quality rips if possible.
3.  **Export as OGG:**
    *   Go to `File > Export > Export as OGG`.
    *   Save the file somewhere easily accessible (e.g., name it `song_for_av.ogg`).
    *   When prompted for OGG Quality, a setting of 5 or 6 is usually sufficient for analysis purposes. Click `Save`.
    *   You can ignore the metadata tags prompt and just click `OK`.

**Important:** Keep your *original* audio file project open in Audacity, or save it as an Audacity Project (`.aup3`), as you might modify it based on Arrow Vortex's findings.

---

## Step 2: Find BPM & Offset (Arrow Vortex) then Modify Audio (Audacity)

Arrow Vortex helps us find the exact BPM and the timing offset needed to align the first beat correctly. We then apply this offset in Audacity.

1.  **Open Arrow Vortex:** Launch `ArrowVortex.exe`.
2.  **Load the OGG:** Drag and drop the `song_for_av.ogg` file you just created into the Arrow Vortex window.
3.  **View Waveform:** Go to the `View` menu and click `Time based (C-mod)`. Zoom using `Ctrl + Mouse Wheel`.
4.  **Find BPM:**
    *   Press `Shift + S` (or go to `Tempo > Adjust sync...`).
    *   Click the `Find BPM` button.
    *   Arrow Vortex will analyze the track. Select the most likely BPM (usually the top one).
    *   Click `Apply BPM`.
5.  **Confirm BPM:**
    *   Press `F3` to toggle the metronome beat ticks on.
    *   Press `Spacebar` to play the audio. Listen carefully throughout the song. Do the ticks align perfectly with the beat?
    *   If the ticks drift, your song might have **variable BPM**, which complicates marker generation. Consider choosing a song with a consistent BPM if possible. If ticks don't match even at the start, try other BPM suggestions from the `Find BPM` step.
6.  **Determine Offset:**
    *   The goal is to make the *first beat you want a marker on* align perfectly with a beat line (ideally the very first one at time `0.000` *after* applying the offset).
    *   Still in the `Adjust sync...` window (`Shift+S`), look at the waveform preview.
    *   Use the `Move first beat <-` and `Move first beat ->` buttons ![Arrow Vortex move beat button](https://github.com/jakey-jakey/BeatMarker/assets/10910993/07c46b65-062a-4603-b505-252a3d08fa34){style="height: 1em; display: inline;"} to shift the audio relative to the beat grid. Your aim is to place the very start of the *first beat you care about* visually right on top of the main beat line (often the thickest line at the start of the grid display in the sync window).
    *   As you click the buttons, the `Music offset:` value in the window changes. This value represents the amount of silence (positive offset) or trimming (negative offset) needed at the *beginning* of your audio file.
    *   Adjust until the desired first beat aligns perfectly with the grid line.
    *   Note down the final `Music offset:` value (e.g., `0.123` or `-0.045`). This is the **Offset in seconds**.
    *   Note down the precise **BPM** value again, just to be sure.
    *   You can close Arrow Vortex.

7.  **Apply Offset in Audacity:**
    *   Go back to Audacity with your *original* audio file loaded (or reopen it).
    *   Switch to the Selection Tool ![Selection Tool](https://github.com/jakey-jakey/BeatMarker/assets/10910993/357a1214-6f2b-4126-8725-41043cfc5d31){style="height: 1em; display: inline;"}.

    *   **If the Offset is POSITIVE (e.g., `0.123`):** You need to add silence to the beginning.
        *   Place the cursor at the very start of the track (Press `Home` key).
        *   Go to `Generate > Silence...`.
        *   Enter the positive offset value (e.g., `0.123`) into the `Duration` field.
        *   Click `OK`. Silence is added to the start.

    *   **If the Offset is NEGATIVE (e.g., `-0.045`):** You need to remove sound from the beginning.
        *   Place the cursor at the very start of the track (Press `Home` key).
        *   Carefully drag the cursor to the right to select the exact amount of audio specified by the *absolute value* of the offset (e.g., select `0.045` seconds from the start). Use the selection duration indicator at the bottom of the Audacity window for precision. Zoom in heavily if needed.
        *   Press the `Delete` key to remove the selected audio.

8.  **Save Modified Audio:**
    *   Now that the offset is applied, export this modified audio. This is the version you'll use in your video editor *and* the version `BeatMarker` should ideally get the duration from.
    *   Go to `File > Export > Export as WAV` (recommended for quality in NLE) or `Export as MP3` (if preferred).
    *   Name it something clear, like `song_synced.wav`.

---

## Step 3: Get Modified Audio Duration

`BeatMarker` needs the total duration of your *offset-adjusted* song.

*   **Method 1: Automatic (Recommended)**
    *   Drag the **modified** audio file (`song_synced.wav` or similar) directly onto the `BeatMarker.exe` file icon or onto the `beat_marker_generator.py` script in your terminal.
    *   If successful, `BeatMarker` will display the detected duration.
*   **Method 2: Manual**
    *   If drag-and-drop isn't used or fails, `BeatMarker` will prompt you.
    *   The duration of the modified track is visible in Audacity.
    *   Enter the duration in `MM:SS.sss` format (e.g., `03:45.623`) when prompted by `BeatMarker`.

---

## Step 4: Generate Markers (BeatMarker)

Run `BeatMarker` with the information for the *modified* audio.

1.  **Run BeatMarker:**
    *   Double-click `BeatMarker.exe`.
    *   Or open a terminal/command prompt, navigate to the script's directory, and run `python beat_marker_generator.py`.
    *   _(If using drag-and-drop for duration, you would have already done this in Step 3)._
2.  **Follow Prompts:**
    *   **Duration:** Provide manually if not auto-detected (Step 3, using the duration of the *modified* file).
    *   **BPM:** Enter the precise BPM value you found using Arrow Vortex (Step 2, e.g., `128`).
    *   **Marker Interval:**
        *   `1`: Every beat.
        *   `2`: Every 2 beats.
        *   `4`: Every 4 beats.
    *   **Output Format:**
        *   `s`: Simple (`MM:SS.sss`).
        *   `tc`: Timecode (`HH:MM:SS:FF`).
    *   **Framerate (if `tc` chosen):** Enter the exact framerate of your video editing project (e.g., `23.976`, `29.97`, `60`). **Crucial for accurate timecode.**
3.  **Output:** `BeatMarker` calculates markers starting from `00:00.000` based on the BPM and modified duration. The markers are saved to `beat_markers.txt` in the same directory.

---

## Step 5: Use Markers in Your Video Editor

The generated `beat_markers.txt` contains timestamps relative to the start of your *modified* audio file.

1.  **Import Modified Audio:** Import the `song_synced.wav` (or your exported modified file) into your video editing software timeline. Place it at the very beginning of your sequence (00:00:00:00).
2.  **Import/Place Markers:** Use your editor's method to add markers based on the `beat_markers.txt` file:
    *   **Copy/Paste:** Some editors might allow pasting the list directly onto the timeline or audio clip.
    *   **Manual Placement:** Open `beat_markers.txt`. Go to each timestamp in your editor and place a marker.
    *   **Scripting/Import:** Check if your editor supports importing marker lists from text files or via scripting (e.g., Python in DaVinci Resolve, EDL import).
3.  **Verify Alignment:** Since you adjusted the audio file's start time in Audacity based on Arrow Vortex's offset, the *first marker generated by BeatMarker* should now align correctly with the *first beat you intended to mark* in your modified audio file, right near the beginning of the clip in your NLE. Play the sequence with a metronome or visually check the waveform peaks against the markers to confirm they are synchronized throughout the track.

You now have precisely timed beat markers aligned with your adjusted audio, ready to guide your edits!

---

## Troubleshooting Arrow Vortex

*   **`MSVCP120.dll was not found` Error:** Install the Microsoft Visual C++ 2013 Redistributable (**x86** version) from [Microsoft](https://support.microsoft.com/en-us/help/4032938/update-for-visual-c-2013-redistributable-package).
*   **Arrow Vortex Doesn't Open:** Ensure correct extraction, try running as admin, ensure C++ redistributable is installed.

---

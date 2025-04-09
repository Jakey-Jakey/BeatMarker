# Generating Beat Markers for Video Editing with BeatMarker

This guide explains how to accurately determine your audio track's Beats Per Minute (BPM), adjust its starting offset by adding silence, and generate a list of timestamps (markers) using the `BeatMarker` tool. These markers can then be imported or used as guides in video editing software like DaVinci Resolve, Premiere Pro, Final Cut Pro, etc., to easily sync cuts or effects to the music's beat.

We'll use [Audacity](https://www.audacityteam.org/) for audio preparation and [Arrow Vortex](https://arrowvortex.ddrnl.com/) for precise BPM and timing analysis.

## Prerequisites

1.  **Your Audio File:** The song or audio track you want to create markers for (preferably a high-quality WAV, FLAC, or high-bitrate MP3/M4A).
2.  **[Audacity](https://www.audacityteam.org/):** Free, open-source audio editor. Used for adding silence and exporting the final audio.
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

Arrow Vortex works most reliably with `.ogg` files. We also use Audacity to modify the audio's start time later.

1.  **Open Audio in Audacity:** Launch Audacity and open your original audio file (`File > Open`).
2.  **Check Quality (Optional but Recommended):** Ensure your audio looks clean in the waveform view. Avoid low-quality rips if possible.
3.  **Export as OGG:**
    *   Go to `File > Export > Export as OGG`.
    *   Save the file somewhere easily accessible (e.g., name it `song_for_av.ogg`).
    *   When prompted for OGG Quality, a setting of 5 or 6 is usually sufficient for analysis purposes. Click `Save`.
    *   You can ignore the metadata tags prompt and just click `OK`.

**Important:** Keep your *original* audio file project open in Audacity, or save it as an Audacity Project (`.aup3`), as you will modify it based on Arrow Vortex's findings.

---

## Step 2: Find BPM & Positive Offset (Arrow Vortex) then Modify Audio (Audacity)

Arrow Vortex helps us find the exact BPM and the timing offset needed to align the first beat correctly *after* time zero. We then apply this offset by adding silence in Audacity.

1.  **Open Arrow Vortex:** Launch `ArrowVortex.exe`.
2.  **Load the OGG:** Drag and drop the `song_for_av.ogg` file you just created into the Arrow Vortex window.
3.  **View Waveform:** Go to the `View` menu and click `Time based (C-mod)`. Zoom using `Ctrl + Mouse Wheel` to see the waveform clearly.

    ![Arrow Vortex Waveform View](path/to/your/av_waveform.png)
    *(Example waveform view)*

4.  **Find BPM:**
    *   Press `Shift + S` (or go to `Tempo > Adjust sync...`) to open the **ADJUST SYNC** window.
    *   Click the `Find BPM` button.
    *   Arrow Vortex will analyze the track and show results under `BPM detection results`.
        ![Arrow Vortex Adjust Sync window with multiple BPM results](path/to/your/av_sync_multiple_bpm.png)
        *(Example showing multiple BPM options)*
    *   Select the most likely BPM. Often it's the one with the highest confidence percentage (e.g., `#1 :: 125.00 BPM :: 100%`). If unsure, you might need to test multiple options in the next steps.
    *   Click `Apply BPM`.

5.  **Confirm BPM:**
    *   Press `F3` to toggle the metronome beat ticks on (you'll hear them during playback).
    *   Press `Spacebar` to play the audio. Listen carefully throughout the song. Do the ticks align perfectly with the beat?
    *   If the ticks drift, your song might have **variable BPM**, which complicates marker generation. Consistent BPM is ideal. If ticks don't match even at the start, go back to the `Adjust sync...` window (`Shift+S`), select a different BPM result (if available), click `Apply BPM`, and listen again.

6.  **Determine Offset:**
    *   The goal is to find how much silence needs to be added at the beginning so that the beats line up perfectly.
    *   Go back to the `Adjust sync...` window (`Shift+S`). It should have already decided the `Music offset:`
    *   Scroll around the waveform and identify where you want your bars and beats to align
    *   Use the `Move first beat` buttons to shift the audio relative to the beat grid.
    *   **Keep clicking the arrows until the start of your desired first beat aligns visually with a grid line, AND the `Music offset:` value shown is POSITIVE (greater than 0).** It doesn't have to be exactly `0.000`; you just need the *correct positive value* representing the necessary padding.
        ![Arrow Vortex Adjust Sync window showing a negative offset initially](path/to/your/av_sync_negative.png)
        *(Example: Initially negative offset. Use "Move first beat" buttons to make this positive)*
    *   Listen again with beat ticks (`F3`) on to confirm this alignment sounds correct for where you want the markers to start.
    *   Once satisfied, note down the final **positive** `Music offset:` value (e.g., `0.123`, `1.500`). This is the **Offset in seconds**.
    *   Double-check and note down the final **BPM** value as well.
    *   You can close Arrow Vortex.

7.  **Apply Positive Offset in Audacity:**
    *   Go back to Audacity with your *original* audio file loaded.
    *   Switch to the Selection Tool ![Selection Tool](https://github.com/jakey-jakey/BeatMarker/assets/10910993/357a1214-6f2b-4126-8725-41043cfc5d31){style="height: 1em; display: inline;"}.
    *   Place the cursor at the very start of the track (Press `Home` key).
    *   Go to `Generate > Silence...`.
    *   Enter the **positive offset value** you noted down from Arrow Vortex (e.g., `0.123`) into the `Duration` field.
    *   Click `OK`. The calculated amount of silence is added to the start of your track.

8.  **Save Modified Audio:**
    *   Now that the silence (offset) is added, export this modified audio. This is the version you'll use in your video editor *and* the version `BeatMarker` should get the duration from.
    *   Go to `File > Export > Export as WAV` (recommended for quality in NLE) or `Export as MP3` (if preferred).
    *   Name it something clear, like `song_synced_with_offset.wav`.

---

## Step 3: Get Modified Audio Duration

`BeatMarker` needs the total duration of your *offset-adjusted* song.

*   **Method 1: Automatic (Recommended)**
    *   Drag the **modified** audio file (`song_synced_with_offset.wav` or similar) directly onto the `BeatMarker.exe` file icon or onto the `beat_marker_generator.py` script in your terminal.
    *   If successful, `BeatMarker` will display the detected duration.
*   **Method 2: Manual**
    *   If drag-and-drop isn't used or fails, `BeatMarker` will prompt you.
    *   The duration of the modified track is visible in Audacity after adding silence.
    *   Enter the duration in `MM:SS.sss` format (e.g., `03:45.746`) when prompted by `BeatMarker`.

---

## Step 4: Generate Markers (BeatMarker)

Run `BeatMarker` with the information for the *modified* audio.

1.  **Run BeatMarker:**
    *   Double-click `BeatMarker.exe`.
    *   Or open a terminal/command prompt, navigate to the script's directory, and run `python beat_marker_generator.py`.
    *   _(If using drag-and-drop for duration, you would have already done this in Step 3)._
2.  **Follow Prompts:**
    *   **Duration:** Provide manually if not auto-detected (Step 3, using the duration of the *modified* file).
    *   **BPM:** Enter the precise BPM value you found using Arrow Vortex (Step 2, e.g., `125.000`).
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

The generated `beat_markers.txt` contains timestamps relative to the start of your *modified* audio file (which now includes the silence padding).

1.  **Import Modified Audio:** Import the `song_synced_with_offset.wav` (or your exported modified file) into your video editing software timeline. Place it at the very beginning of your sequence (00:00:00:00).
2.  **Import/Place Markers:** Use your editor's method to add markers based on the `beat_markers.txt` file:
    *   **Copy/Paste:** Some editors might allow pasting the list directly onto the timeline or audio clip.
    *   **Manual Placement:** Open `beat_markers.txt`. Go to each timestamp in your editor and place a marker.
    *   **Scripting/Import:** Check if your editor supports importing marker lists from text files or via scripting (e.g., Python in DaVinci Resolve, EDL import).
3.  **Verify Alignment:** Since you added silence to the start of the audio file based on the Arrow Vortex offset, the markers generated by `BeatMarker` (starting from 0) should now align correctly with the beats in your modified audio file in the NLE timeline. The first marker should correspond to the first beat you intended to mark after the silence. Play the sequence and visually check the waveform peaks against the markers to confirm synchronization.

You now have precisely timed beat markers aligned with your adjusted audio, ready to guide your edits!

---

## Troubleshooting Arrow Vortex

*   **`MSVCP120.dll was not found` Error:** Install the Microsoft Visual C++ 2013 Redistributable (**x86** version) from [Microsoft](https://support.microsoft.com/en-us/help/4032938/update-for-visual-c-2013-redistributable-package).
*   **Arrow Vortex Doesn't Open:** Ensure correct extraction, try running as admin, ensure C++ redistributable is installed.

---

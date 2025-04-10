# Generating Beat Markers for Video Editing with BeatMarker

This guide explains how to accurately determine an audio track's Beats Per Minute (BPM), adjust its starting offset by adding silence, and generate a list of timestamps (markers) using the `BeatMarker` tool. **This guide is primarily intended for video editors using software like DaVinci Resolve, Premiere Pro, Final Cut Pro, etc.,** who want to easily sync cuts or effects to the music's beat.

We'll use [Audacity](https://www.audacityteam.org/) for audio preparation and [Arrow Vortex](https://arrowvortex.ddrnl.com/) for precise BPM and timing analysis.

## Prerequisites

1.  **Your Audio File:** The song or audio track you want to create markers for (preferably a high-quality WAV, FLAC, or high-bitrate MP3/M4A).
2.  **[Audacity](https://www.audacityteam.org/):** Free, open-source audio editor. Used for adding silence and exporting the final audio.
3.  **[Arrow Vortex](https://arrowvortex.ddrnl.com/):** Free tool for rhythm game charting, excellent for finding BPM and precise beat timing.
    *   BSMG Re-packed [Zip Download](https://bsmg.dev/zY55r) (Recommended)
    *   Arrow Vortex Website [Rar Download](https://arrowvortex.ddrnl.com/) (Requires software like [7-Zip](https://www.7-zip.org/) to extract)
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

## Step 2: Find BPM & Positive Offset (Arrow Vortex)

Arrow Vortex helps us find the exact BPM and the timing offset needed so the first beat you care about happens *after* time zero.

1.  **Open Arrow Vortex:** Launch `ArrowVortex.exe`.
2.  **Load the OGG:** Drag and drop the `song_for_av.ogg` file you just created into the Arrow Vortex window.
3.  **View Waveform:** Go to the `View` menu and click `Time based (C-mod)`. Zoom using `Ctrl + Mouse Wheel` to see the waveform clearly.
    *(Image Placeholder: AV Waveform View)*
4.  **Find BPM:**
    *   Press `Shift + S` (or go to `Tempo > Adjust sync...`) to open the **ADJUST SYNC** window.
    *   Click the `Find BPM` button. Arrow Vortex will analyze and show results.
        *(Image Placeholder: AV Adjust Sync window with BPM results)*
    *   Select the most likely BPM (often highest confidence %). Click `Apply BPM`.
5.  **Confirm BPM:**
    *   Press `F3` to toggle metronome beat ticks on.
    *   Press `Spacebar` to play the audio. Listen throughout the song. Do the ticks align perfectly with the beat?
    *   If ticks drift, the song might have variable BPM (harder to work with). If they don't match the start, try another BPM result from the `Adjust sync...` window if available.
6.  **Determine Positive Offset:**
    *   The goal is to find how much silence to add later in Audacity.
    *   Go back to the `Adjust sync...` window (`Shift+S`).
    *   Visually identify the beat in the waveform where you want your markers to effectively start (e.g., the first strong downbeat after any intro fade).
    *   Use the `Move first beat` buttons (left/right arrows in the sync window) to shift the audio relative to the beat grid.
    *   **Crucially, keep adjusting until the start of your desired first beat aligns visually with a grid line AND the `Music offset:` value shown is POSITIVE (e.g., `0.123`, `1.500`).** A positive offset means the beat occurs *after* time zero, which is necessary for adding silence correctly. **If the offset is initially negative, you MUST use the `Move first beat` buttons until it becomes positive.**
        *(Image Placeholder: AV Adjust Sync window showing a positive offset after adjustment)*
    *   Listen again with beat ticks (`F3`) on to confirm this alignment sounds correct for where you want the markers to start relative to the music. While aligning to a downbeat is common, the most important thing is that the positive offset value results in the metronome sounding correct for your chosen starting point.
    *   Note down the final **positive** `Music offset:` value (this is the **Offset in seconds**) and the final **BPM** value.
    *   You can close Arrow Vortex.

---

## Step 3: Apply Positive Offset & Export Modified Audio (Audacity)

Now, use the offset value from Arrow Vortex to add silence to the beginning of your *original* audio file in Audacity.

1.  **Go Back to Audacity:** Ensure your *original* audio file is loaded (not the OGG).
2.  **Select Start:** Use the Selection Tool. Place the cursor at the very beginning of the track (Press `Home` key).
3.  **Generate Silence:**
    *   Go to `Generate > Silence...`.
    *   Enter the **positive offset value** (in seconds) you noted down from Arrow Vortex into the `Duration` field.
        *(Image Placeholder: Audacity Generate Silence dialog)*
    *   Click `OK`. Silence is added to the start.
        *(Image Placeholder: Audacity waveform showing added silence)*
4.  **Save Modified Audio:**
    *   Export this *modified* audio. This is the version you'll use in your video editor **and** the version `BeatMarker` needs the duration from.
    *   Go to `File > Export > Export as WAV` (recommended for NLE quality) or `Export as MP3` (if preferred).
    *   Name it something clear, like `song_synced_with_offset.wav`.

---

## Step 4: Get Modified Audio Duration

`BeatMarker` needs the total duration of your *offset-adjusted* song.

*   **Method 1: Automatic (Recommended)**
    *   Drag the **modified** audio file (`song_synced_with_offset.wav` or similar) directly onto the `BeatMarker.exe` file icon or onto the `beat_marker_generator.py` script in your terminal.
    *   If successful, `BeatMarker` will display the detected duration.
*   **Method 2: Manual**
    *   If drag-and-drop isn't used or fails, `BeatMarker` will prompt you.
    *   In Audacity, you can see the total duration of the modified track (often displayed at the bottom of the window, especially after selecting the entire track with `Ctrl+A`).
    *   Enter this duration in `MM:SS.sss` format (e.g., `03:45.746`) when prompted by `BeatMarker`.

---

## Step 5: Generate Markers (BeatMarker)

Run `BeatMarker` with the information for the *modified* audio.

1.  **Run BeatMarker:**
    *   Double-click `BeatMarker.exe`.
    *   Or open a terminal/command prompt, navigate to the script's directory, and run `python beat_marker_generator.py`.
    *   _(If using drag-and-drop for duration, you would have already done this in Step 4)._
2.  **Follow Prompts:**
    *   **Duration:** Provide manually if not auto-detected (Step 4, using the duration of the *modified* file).
    *   **BPM:** Enter the precise BPM value you found using Arrow Vortex (Step 2, e.g., `125.000`).
    *   **Marker Interval:** `1` (beat), `2` (half measure), `4` (full measure).
    *   **Output Format:** `s` (Simple `MM:SS.sss`) or `tc` (Timecode `HH:MM:SS:FF`).
    *   **Framerate (if `tc` chosen):** Enter the exact framerate of your video editing project (e.g., `23.976`, `29.97`, `60`). **This should match the framerate of the video footage or sequence you intend to use these markers with.**
3.  **Output:** `BeatMarker` calculates markers starting from `00:00.000` based on the BPM and modified duration. The markers are saved to `beat_markers.txt` in the same directory.

---

## Step 6: Use Markers in Your Video Editor

The generated `beat_markers.txt` contains timestamps relative to the start of your *modified* audio file (which now includes the silence padding).

1.  **Import Modified Audio:** Import the `song_synced_with_offset.wav` (or your exported modified file) into your video editing software timeline. Place it at the very beginning of your sequence (00:00:00:00).
2.  **Import/Place Markers:** Use your editor's method to add markers based on the `beat_markers.txt` file:
    *   **Copy/Paste:** Some editors might allow pasting the list directly onto the timeline or audio clip.
    *   **Manual Placement:** Open `beat_markers.txt`. Go to each timestamp in your editor and place a marker.
    *   **Scripting/Import:** Check if your editor supports importing marker lists from text files or via scripting (e.g., Python in DaVinci Resolve, EDL import). *Consult your NLE's documentation for specific steps.*
3.  **Verify Alignment:** Since you added silence based on the Arrow Vortex offset, the markers generated by `BeatMarker` (starting from 0) should now align correctly with the beats in your modified audio file on the timeline. The first marker should correspond to the beat you aligned in Arrow Vortex. Play the sequence and check alignment visually.

You now have precisely timed beat markers aligned with your adjusted audio, ready to guide your edits!

---

## Step 7: Troubleshooting Arrow Vortex

*   **`MSVCP120.dll was not found` Error:** Install the Microsoft Visual C++ 2013 Redistributable (**x86** version) from [Microsoft](https://support.microsoft.com/en-us/help/4032938/update-for-visual-c-2013-redistributable-package).
*   **Arrow Vortex Doesn't Open:** Ensure correct extraction, try running as admin, ensure C++ redistributable is installed.

---

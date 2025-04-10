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
    *   Save the file somewhere easily accessible (e.g., name it `audio_for_analysis.ogg`). This OGG file is *only* for Arrow Vortex.
    *   When prompted for OGG Quality, a setting of 5 or 6 is usually sufficient for analysis purposes. Click `Save`.
    *   You can ignore the metadata tags prompt and just click `OK`.

**Important:** Keep your *original* audio file project open in Audacity, or save it as an Audacity Project (`.aup3`), as you will modify it based on Arrow Vortex's findings.

---

## Step 2: Find BPM & Positive Offset (Arrow Vortex)

Arrow Vortex helps us find the exact BPM and the timing offset needed so the first beat you care about happens *after* time zero.

1.  **Open Arrow Vortex:** Launch `ArrowVortex.exe`.
2.  **Load the OGG:** Drag and drop the `.ogg` file you created (e.g., `audio_for_analysis.ogg`) into the Arrow Vortex window.
3.  **View Waveform:** Go to `View > Time based (C-mod)` and zoom (`Ctrl + Mouse Wheel`) to see the waveform clearly.
![Arrow Vortex Waveform View](https://github.com/Jakey-Jakey/BeatMarker/blob/main/guide/First%20Waveform.jpg?raw=true)
5.  **Find BPM:**
    *   Press `Shift + S` (or go to `Tempo > Adjust sync...`) to open the **ADJUST SYNC** window.
    *   Click `Find BPM`. Select the most likely BPM result (often highest confidence %) and click `Apply BPM`.
![Arrow Vortex Adjust Sync window with BPM results](https://github.com/Jakey-Jakey/BeatMarker/blob/42ef9d6d62ce4db9c4483c77705b3e8f9aa0f04e/guide/Adjust%20Sync%20window.jpg)
6.  **Confirm BPM:**
    *   Press `F3` (toggle beat ticks) and `Spacebar` (play). Listen throughout the song. Ensure ticks align with the beat. If not, try another BPM result or note potential variable BPM.
7.  **Ensure a Positive Offset:**
    *   The primary goal here is to ensure the `Music offset:` value shown in the `Adjust sync...` window (`Shift+S`) is **POSITIVE**. A positive offset (e.g., `0.123`, `1.500`) is required so you can correctly add silence at the beginning of your track in Audacity later.
    *   Use the `Move first beat` buttons to shift the audio relative to the grid. Keep clicking until the `Music offset:` value becomes positive. (Try and mostly use the 1-beat buttons, half-beat modifications can go wrong easily.)
        ![Arrow Vortex Adjust Sync window showing positive offset](https://github.com/Jakey-Jakey/BeatMarker/raw/main/guide/negativeaura.jpg)
    *   **Guideline:** Aim for enough positive offset so there's *at least* one empty measure's worth of time (typically 2-4 seconds, depending on the song's BPM) before the first sound you intend to place a marker on. This provides necessary padding.
    *   **(Optional) Align to a Specific Beat:** While adjusting for a positive offset, you *can* also try to visually align a specific beat (like the first strong downbeat you care about) with a grid line if it helps you visualize the timing. However, the most critical outcome is achieving a positive offset value.
        ![Arrow Vortex Waveform showing beat aligned to grid](https://github.com/Jakey-Jakey/BeatMarker/raw/main/guide/sucessful%20sync.jpg)
    *   **Final Check:** Before proceeding, double-check that the `Music offset:` displayed is positive. If it's negative or zero, continue using the `Move first beat` buttons.
    *   Listen again (`F3` ticks on) to confirm the timing sounds correct relative to the metronome with the current offset.
    *   Note down the final **positive** `Music offset:` value and the confirmed **BPM**.

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
    *   Name it something clear, like `your_song_final_synced.wav`.

---

## Step 4: Determine Duration of Modified Audio

`BeatMarker` needs the **total duration** of your audio file *after* you added the silence (e.g., `your_song_final_synced.wav`). This is because the added silence pushes the actual music forward, and BeatMarker calculates timestamps starting from 00:00.000 of this complete file.

*   **Method 1: Automatic (Recommended)**
    *   Drag the **modified audio file** (the WAV or MP3 you just exported) directly onto the `BeatMarker.exe` file icon or onto the `beat_marker_generator.py` script in your terminal.
    *   If successful, `BeatMarker` will automatically detect and display the correct duration.
*   **Method 2: Manual**
    *   If you don't use drag-and-drop, `BeatMarker` will prompt you for the duration.
    *   To find it, look in Audacity *after* adding silence. Select the entire track (`Ctrl+A` or `Cmd+A`) and the total duration is usually displayed at the bottom of the Audacity window (often labeled "Selection Length" or similar).
        *(Image Placeholder: Audacity bottom bar showing selection length)*
    *   Enter this full duration in `MM:SS.sss` format (e.g., `03:45.746`) when prompted by `BeatMarker`.

---

## Step 5: Generate Markers with BeatMarker

Now, run the `BeatMarker` tool using the information gathered in the previous steps.

1.  **Run BeatMarker:**
    *   Double-click `BeatMarker.exe`.
    *   Or open a terminal/command prompt, navigate to the script's directory, and run `python beat_marker_generator.py`.
    *   _(If using drag-and-drop for duration, BeatMarker will have already started and detected the duration in Step 4)._
2.  **Follow Prompts:** BeatMarker will ask for the following information:
    *   **Duration:** If not auto-detected via drag-and-drop, enter the **total duration of the modified audio file** (as determined in Step 4).
    *   **BPM:** Enter the **precise BPM value** you confirmed using Arrow Vortex (from Step 2, e.g., `125.000`).
    *   **Marker Interval:** Choose how often markers should be placed:
        *   `1`: Every beat.
        *   `2`: Every 2 beats (e.g., beats 1 and 3 in a 4/4 measure).
        *   `4`: Every 4 beats (e.g., the start of each 4/4 measure).
    *   **Output Format:** Choose the timestamp style:
        *   `s`: Simple format (`MM:SS.sss`). Primarily useful for direct copy-paste into Premiere Pro with the Markerbox extension.
        *   `tc`: Timecode format (`HH:MM:SS:FF`). **Required** when using the [editingtools.io Marker Converter](https://editingtools.io/marker/) for other NLEs. Also usable with Markerbox.
    *   **Framerate (Only if `tc` format chosen):** Enter the **exact framerate** of your video editing project sequence (e.g., `23.976`, `29.97`, `60`). This *must* match your target NLE settings for accurate timecode markers, especially when converting formats.
3.  **Output:** `BeatMarker` will calculate the markers based on your inputs and the modified audio's duration. The timestamps are saved to a file named `beat_markers.txt` in the same directory where you ran BeatMarker.

---

## Step 6: Import Markers into Your NLE

With `beat_markers.txt` generated, here’s how to get those markers into your Non-Linear Editor (NLE):

1.  **Import Modified Audio First:** Make sure you have imported the final audio file (e.g., `your_song_final_synced.wav`) into your NLE timeline and placed it at the very beginning (00:00:00:00).

2.  **Choose Your Path:**

    **A) For Adobe Premiere Pro Users:**
    *   The easiest method is using the free [Markerbox extension](https://markerbox.pro/).
    *   Install the Markerbox extension in Premiere Pro.
    *   Open the `beat_markers.txt` file generated by BeatMarker.
    *   Copy the entire list of timestamps.
    *   In Premiere Pro, open the Markerbox extension panel (`Window > Extensions > Markerbox`).
    *   Paste the copied timestamps into the Markerbox input area.
    *   Ensure the correct sequence/clip is targeted and click the button in Markerbox to add the markers to your Premiere timeline or clip. *(Either `Simple` or `Timecode` format from BeatMarker can work here).*

    **B) For Other NLEs (DaVinci Resolve, Final Cut Pro, etc.):**
    *   A versatile method is using the free online converter: [editingtools.io Marker Converter](https://editingtools.io/marker/).
    *   **Important:** You **must** use the **Timecode (`tc`)** format output from BeatMarker for this method. Generate `beat_markers.txt` using the `tc` option and specifying your NLE's exact framerate in Step 5. The `Simple` format will not work correctly with this converter.
    *   Open the `beat_markers.txt` file (containing timecode values).
    *   Copy the entire list of timecodes.
    *   Go to the [editingtools.io Marker Converter](https://editingtools.io/marker/) website.
    *   Paste your copied timecode list into the input field.
    *   Choose the appropriate **Output Format** for your specific NLE (e.g., CSV for DaVinci Resolve, FCPX XML for Final Cut Pro, etc.).
    *   Download the converted marker file.
    *   Import this downloaded file into your NLE. The exact import method varies, refer to your NLE's documentation.

3.  **Verify Alignment:** Whichever method you use, play back your sequence in the NLE. The imported markers should align visually and audibly with the beats of your modified audio track, starting from the beat you aligned in Arrow Vortex.

You now have precisely timed beat markers integrated into your editing project!

---

## Troubleshooting Arrow Vortex

*   **`MSVCP120.dll was not found` Error:** Install the Microsoft Visual C++ 2013 Redistributable (**x86** version) from [Microsoft](https://support.microsoft.com/en-us/help/4032938/update-for-visual-c-2013-redistributable-package).
*   **Arrow Vortex Doesn't Open:** Ensure correct extraction, try running as admin, ensure C++ redistributable is installed.

---

## Credits and Thanks

Massive thanks to the [Beat Saber Modding Group Wiki](https://bsmg.wiki) community and resources. This guide heavily utilizes ideas and information workflows inspired by their excellent [Basic Audio Setup guide](https://bsmg.wiki/mapping/basic-audio.html).

Special thanks to the original authors of that guide, their work was the foundation of this project:
*   **Kolezan** ([BeatSaver Profile](https://beatsaver.com/profile/4285318))
*   **Nik (n3tman)** ([BeatSaver Profile](https://beatsaver.com/profile/4286263))

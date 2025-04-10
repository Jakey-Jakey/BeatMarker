# Beat Marker - Command-Line Timestamp Generator

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A stylish command-line tool to generate timestamp markers based on a song's duration, BPM, and desired beat interval. Ideal for creating marker lists for video editing software (like DaVinci Resolve, Premiere Pro, Final Cut Pro) or other applications requiring timed cues.

For users who just want to use it with the workflow. Please check the [guide](https://github.com/Jakey-Jakey/BeatMarker/guide/guide.md)

![Screenshot Placeholder](https://github.com/Jakey-Jakey/BeatMarker/raw/main/Program%20Screenshot.jpg)

## Features

*   **Automatic Duration Detection:** Drag and drop a supported audio file (MP3, WAV, FLAC, M4A, etc.) onto the script/executable to automatically fetch its duration.
*   **Manual Duration Input:** Fallback to manual duration entry (MM:SS.sss format) if drag-and-drop is not used or fails.
*   **Flexible Beat Intervals:** Generate markers every beat (`1`), every half-measure (`2` beats), or every full measure (`4` beats) assuming 4/4 time.
*   **Multiple Output Formats:**
    *   **Simple:** `MM:SS.sss` (Minutes, Seconds, Milliseconds)
    *   **Timecode:** `HH:MM:SS:FF` (Hours, Minutes, Seconds, Frames) - requires specifying framerate.
*   **Framerate Input:** Prompts for video framerate (e.g., 23.976, 29.97, 30, 60) when Timecode format is selected.
*   **Stylish CLI:** Uses `colorama` for a visually appealing, colored command-line interface with section headers and an ASCII art title.
*   **Standalone Executable:** Can be easily packaged into a single `.exe` file for Windows using PyInstaller (instructions below).
*   **Cross-Platform:** Script works on Windows, macOS, and Linux. Color support relies on `colorama`. `.exe` building is typically OS-specific.

## Prerequisites

*   **Python 3:** Version 3.7 or higher recommended. [Download Python](https://www.python.org/downloads/)
*   **pip:** Python's package installer (usually included with Python).
*   **Libraries (Optional but Recommended):**
    *   `mutagen`: Required for automatic duration detection via drag-and-drop.
    *   `colorama`: Required for the colored text interface.

*If you only use the pre-built `.exe` (if provided), you do **not** need Python or these libraries installed.*

## Installation

There are two ways to use Beat Marker:

**Option 1: Download Pre-built Executable (if available)**

1.  Go to the [Releases page](https://github.com/Jakey-Jakey/BeatMarker/releases) of this repository.
2.  Download the latest `.exe` file for your operating system (e.g., `beat_marker_windows.exe`).
3.  Place the `.exe` file anywhere convenient. No installation needed!

**Option 2: Run from Python Script**

1.  **Clone or Download:**
    *   Clone the repository: `git clone https://github.com/Jakey-Jakey/BeatMarker.git`
    *   Or download the `beat_marker_generator.py` file directly from the repository page.
2.  **Navigate to Directory:** Open your terminal or command prompt and `cd` into the directory containing the script.
3.  **Install Dependencies (Recommended):**
    ```bash
    pip install mutagen colorama
    ```
    *(Note: The script includes fallbacks and will run without these, but with no reduced functionality).*

## Usage

1.  **Run the Tool:**
    *   **Executable:** Double-click the `.exe` file.
    *   **Python Script:** Open your terminal/command prompt in the script's directory and run: `python beat_marker_generator.py`
    *   **Drag-and-Drop (Recommended for Audio Files):** Drag your audio file (MP3, WAV, etc.) directly onto the `.exe` or `.py` script icon. This will automatically detect the duration.

2.  **Follow the Prompts:**
    *   **Duration:** If you didn't drag-and-drop, enter the song duration in `MM:SS` or `MM:SS.sss` format (e.g., `03:45.500`).
    *   **BPM:** Enter the song's Beats Per Minute (e.g., `120`).
    *   **Marker Interval:** Enter `1` (every beat), `2` (every 2 beats), or `4` (every 4 beats).
    *   **Output Format:** Enter `s` for Simple (`MM:SS.sss`) or `tc` for Timecode (`HH:MM:SS:FF`).
    *   **Framerate (if Timecode selected):** Enter the video framerate (e.g., `23.976`, `30`, `59.94`).

3.  **Check Output:** The script will calculate and display progress. Upon completion, it will create a file named `beat_markers.txt` in the **same directory where you ran the script/executable**.

## Output File (`beat_markers.txt`)

This file contains the generated timestamps, one per line, ready to be copied.

**Example (Simple Format):**

```
00:00.500
00:01.000
00:01.500
...
```

**Example (Timecode Format @ 30 FPS):**

```
00:00:00:15
00:00:01:00
00:00:01:15
...
```

## Building the Executable (from Source)

If you want to create your own standalone `.exe` file from the Python script:

1.  **Install Prerequisites:** Make sure you have Python 3 and `pip` installed.
2.  **Install Dependencies and PyInstaller:** Open your terminal/command prompt:
    ```bash
    pip install mutagen colorama pyinstaller
    ```
3.  **Navigate to Script Directory:** `cd` to the folder containing `beat_marker_generator.py`.
4.  **Run PyInstaller:**
    ```bash
    pyinstaller --onefile beat_marker_generator.py
    ```
    *   `--onefile`: Creates a single executable file.
    *   **Do NOT use `--noconsole` or `--windowed`:** The script requires the console for user interaction.
5.  **Find the Executable:** The `.exe` file will be located in the `dist` subfolder created by PyInstaller.
6.  **(Optional) Rename:** You can rename the `.exe` file (e.g., `BeatMarker.exe`).

*Note: It's generally best to build the executable on the target operating system (e.g., build on Windows for Windows users).*

## Troubleshooting

*   **`mutagen` or `colorama` not found warnings:** If running the `.py` script, install the missing libraries using `pip install mutagen colorama`. Drag-and-drop or colors won't work without them. The `.exe` should already include them.
*   **Antivirus Flags Executable:** Sometimes, executables created with PyInstaller (especially `--onefile`) can be flagged by antivirus software. This is often a false positive. You may need to add an exception for the file in your antivirus settings.
*   **Incorrect Timecode:** Double-check that you entered the correct framerate (FPS) for your project when prompted.

## Contributing

Contributions are welcome! If you have suggestions or find bugs:

1.  Check the [Issues](https://github.com/Jakey-Jakey/BeatMarker/issues) page to see if your issue/suggestion already exists.
2.  If not, open a new issue.
3.  To contribute code: Fork the repository, create a new branch for your feature/fix, make your changes, and submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (You should create a `LICENSE` file with the MIT license text).

## Author

*   **Jakey**

---

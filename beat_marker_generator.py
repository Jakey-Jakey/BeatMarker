import sys
import math
import os 
import time 
import shutil 

# --- Try importing mutagen ---
MUTAGEN_AVAILABLE = False
try:
    import mutagen
    MUTAGEN_AVAILABLE = True
except ImportError:
    pass 

# --- Try importing colorama ---
COLORAMA_AVAILABLE = False
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True) 
    COLORAMA_AVAILABLE = True
except ImportError:
    class DummyColor:
        def __getattr__(self, name): return "" 
    Fore = Back = Style = DummyColor()
    print("--- !!! WARNING: 'colorama' not installed. Visuals will be basic. !!! ---")
    print("--- Install using: pip install colorama ---")
    print("-" * 60)
    time.sleep(1) 


# ==============================================================================
# Visual Configuration & ASCII Art
# ==============================================================================
try:
    TERM_WIDTH = shutil.get_terminal_size().columns
except OSError:
    TERM_WIDTH = 79 

LINE_CHAR = "─" 
BORDER_COLOR = Fore.BLUE + Style.DIM 
TITLE_COLOR = Fore.CYAN + Style.BRIGHT
SECTION_COLOR = Fore.MAGENTA + Style.BRIGHT
INFO_COLOR = Fore.WHITE
HIGHLIGHT_COLOR = Fore.YELLOW + Style.BRIGHT
SUCCESS_COLOR = Fore.GREEN + Style.BRIGHT
WARNING_COLOR = Fore.YELLOW
ERROR_COLOR = Fore.RED + Style.BRIGHT
PROMPT_COLOR = Fore.CYAN
INPUT_AREA_COLOR = Fore.WHITE 

ascii_art = r"""
██████╗ ███████╗ █████╗ ████████╗     ███╗   ███╗ █████╗ ██████╗ ██╗  ██╗███████╗██████╗ 
██╔══██╗██╔════╝██╔══██╗╚══██╔══╝     ████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██╔══██╗
██████╔╝█████╗  ███████║   ██║        ██╔████╔██║███████║██████╔╝█████╔╝ █████╗  ██████╔╝
██╔══██╗██╔══╝  ██╔══██║   ██║        ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗ ██╔══╝  ██╔══██╗
██████╔╝███████╗██║  ██║   ██║        ██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗███████╗██║  ██║
╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝        ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                 By Jakey                                                                                                                                             
""".splitlines() 

# ==============================================================================
# Helper Functions for Formatted Output
# ==============================================================================
def print_line(color=BORDER_COLOR): print(color + LINE_CHAR * TERM_WIDTH + Style.RESET_ALL)
def print_centered(text, color=INFO_COLOR): print(color + text.center(TERM_WIDTH) + Style.RESET_ALL)
def print_title_art():
    print_line(TITLE_COLOR)
    for line in ascii_art: print(TITLE_COLOR + line.center(TERM_WIDTH) + Style.RESET_ALL)
    print_line(TITLE_COLOR)
    print() 
def print_section_header(text): print(f"\n{BORDER_COLOR}{LINE_CHAR * 3} {SECTION_COLOR}{text} {BORDER_COLOR}{LINE_CHAR * (TERM_WIDTH - len(text) - 5)}{Style.RESET_ALL}")
def print_info(label, value="", label_color=INFO_COLOR, value_color=HIGHLIGHT_COLOR):
    if value: print(f"{label_color}{label}: {value_color}{value}{Style.RESET_ALL}")
    else: print(f"{label_color}{label}{Style.RESET_ALL}")
def print_warning(message): print(f"{WARNING_COLOR}>> WARNING: {message}{Style.RESET_ALL}")
def print_error(message): print(f"{ERROR_COLOR}!! ERROR: {message}{Style.RESET_ALL}")
def print_success(message): print(f"{SUCCESS_COLOR}>> SUCCESS: {message}{Style.RESET_ALL}")

# ==============================================================================
# Core Logic Functions (Input Parsing, Formatting)
# ==============================================================================
def parse_duration(duration_str):
    try:
        parts = duration_str.split(':')
        if len(parts) != 2: raise ValueError("Invalid format (use MM:SS or MM:SS.sss)")
        minutes = int(parts[0])
        seconds = float(parts[1])
        if minutes < 0 or seconds < 0: raise ValueError("Time values cannot be negative.")
        return (minutes * 60) + seconds
    except ValueError as e:
        print_error(f"Invalid Duration - {e}")
        return None

def format_time_simple(total_seconds):
    """Formats time as MM:SS.sss"""
    if total_seconds < 0: total_seconds = 0 
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:06.3f}" 

def format_timecode(total_seconds, fps):
    """Formats time as HH:MM:SS:FF using the given framerate."""
    if total_seconds < 0: total_seconds = 0
    if fps <= 0: 
        print_error("Framerate must be positive for timecode calculation.")
        return "HH:MM:SS:FF_ERROR" # Return an error string

    # Calculate total frames first, rounding is important for precision
    total_frames = round(total_seconds * fps)
    
    # Calculate frames part (handle potential floating point FPS)
    rounded_fps = round(fps) # Use rounded FPS for frame count within a second
    if rounded_fps == 0: rounded_fps = 1 # Avoid division by zero
    frames = total_frames % rounded_fps

    # Calculate total integer seconds from total frames
    total_int_seconds = total_frames // rounded_fps
    
    seconds = total_int_seconds % 60
    total_minutes = total_int_seconds // 60
    minutes = total_minutes % 60
    hours = total_minutes // 60
    
    # Ensure frame number is padded correctly (e.g., 01, 02 ... 29 for 30fps)
    frame_digits = len(str(rounded_fps - 1)) # How many digits needed for frame count
    if frame_digits < 2: frame_digits = 2 # Minimum 2 digits for FF

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{frames:0{frame_digits}d}"


def get_positive_float_input(prompt_message):
    while True:
        try:
            print(f"{PROMPT_COLOR}{prompt_message} {Style.RESET_ALL}{INPUT_AREA_COLOR}", end="")
            value_str = input()
            print(Style.RESET_ALL, end="") 
            value = float(value_str)
            if value <= 0: print_warning("Value must be positive.")
            else: return value
        except ValueError:
            print_warning("Invalid input. Please enter a number.")

def get_beat_interval_multiplier(prompt_message):
    valid_multipliers = {"1": 1, "2": 2, "4": 4}
    while True:
        print(f"{PROMPT_COLOR}{prompt_message} {Style.RESET_ALL}{INPUT_AREA_COLOR}", end="")
        user_input = input().strip().lower() # Convert to lower for flexibility
        print(Style.RESET_ALL, end="") 
        if user_input in valid_multipliers: return valid_multipliers[user_input]
        else: print_warning("Invalid input. Please enter '1', '2', or '4'.")

def get_output_format_choice(prompt_message):
    """Gets the desired output format from the user."""
    valid_formats = {"s": "simple", "tc": "timecode"}
    while True:
        print(f"{PROMPT_COLOR}{prompt_message} {Style.RESET_ALL}{INPUT_AREA_COLOR}", end="")
        user_input = input().strip().lower()
        print(Style.RESET_ALL, end="") 
        if user_input in valid_formats:
            return valid_formats[user_input] # Return 'simple' or 'timecode'
        else:
            print_warning("Invalid input. Please enter 's' or 'tc'.")

# ==============================================================================
# Main Script Execution
# ==============================================================================

print_title_art()
time.sleep(0.3) 

if not MUTAGEN_AVAILABLE:
    print_warning("The 'mutagen' library is not installed.")
    print_warning("Audio file drag-and-drop DISABLED.")
    print_warning("Install using: pip install mutagen")
    print(f"{BORDER_COLOR}{LINE_CHAR * TERM_WIDTH}{Style.RESET_ALL}\n")
    time.sleep(1)

total_duration_seconds = None
source_filename = None 
markers = []
output_filename = "beat_markers.txt"
frame_rate = None # Initialize frame_rate

# --- Step 1: Get Duration ---
print_section_header("1. Song Duration")
if MUTAGEN_AVAILABLE and len(sys.argv) > 1:
    filepath = sys.argv[1]
    filename_base = os.path.basename(filepath)
    print_info("File Detected", filename_base)
    print(f"{INFO_COLOR}Attempting to read duration...{Style.RESET_ALL}")
    time.sleep(0.2) 
    try:
        audio = mutagen.File(filepath)
        if audio and audio.info and hasattr(audio.info, 'length') and audio.info.length > 0:
            total_duration_seconds = float(audio.info.length)
            source_filename = filename_base 
            print_success(f"Duration Found: {HIGHLIGHT_COLOR}{format_time_simple(total_duration_seconds)}")
        else: print_warning(f"Could not read valid duration from '{filename_base}'.")
    except mutagen.MutagenError as e:
        print_error(f"Reading audio metadata: {e}")
        print_warning("Ensure it's a supported audio file (MP3, WAV, FLAC, M4A, etc.).")
    except FileNotFoundError: print_error(f"File not found at path: {filepath}")
    except Exception as e: print_error(f"Unexpected error reading file: {e}")

if total_duration_seconds is None:
    if len(sys.argv) > 1: print_info("Proceeding with manual duration input...\n")
    while total_duration_seconds is None:
        duration_str = input(f"{PROMPT_COLOR}Enter song duration (MM:SS or MM:SS.sss): {INPUT_AREA_COLOR}") 
        print(Style.RESET_ALL, end="") 
        total_duration_seconds = parse_duration(duration_str) 

# --- Step 2: Get BPM ---
print_section_header("2. Song Tempo (BPM)")
bpm = get_positive_float_input("Enter song Beats Per Minute (e.g., 120):")

# --- Step 3: Get Beat Interval ---
print_section_header("3. Marker Interval")
print(f"{INFO_COLOR}  How often should markers be placed?")
print(f"  {HIGHLIGHT_COLOR}'1'{INFO_COLOR} = Every beat (1, 2, 3, 4)")
print(f"  {HIGHLIGHT_COLOR}'2'{INFO_COLOR} = Every 2 beats (1, 3)")
print(f"  {HIGHLIGHT_COLOR}'4'{INFO_COLOR} = Every 4 beats (Start of measure)")
beat_multiplier = get_beat_interval_multiplier("Enter interval choice (1, 2, or 4):")

# --- Step 4: Get Output Format --- M O V E D   H E R E ---
print_section_header("4. Output Format")
print(f"{INFO_COLOR}  Choose the output format for the markers:")
print(f"  {HIGHLIGHT_COLOR}'s'{INFO_COLOR}  = Simple ({HIGHLIGHT_COLOR}MM:SS.sss{INFO_COLOR})")
print(f"  {HIGHLIGHT_COLOR}'tc'{INFO_COLOR} = Timecode ({HIGHLIGHT_COLOR}HH:MM:SS:FF{INFO_COLOR})")
output_format = get_output_format_choice("Enter format choice ('s' or 'tc'):")

# --- Step 4b: Get Framerate (if Timecode selected) ---
if output_format == "timecode":
    print_info("Timecode format selected, requires framerate.")
    frame_rate = get_positive_float_input("Enter video framerate (FPS, e.g. 23.976, 24, 29.976, 30, 60):")

# --- Step 5: Calculations ---
print_section_header("5. Calculating...")
time.sleep(0.3) 

if bpm <= 0: 
    print_error("BPM must be positive. Exiting.")
    input(f"\n{PROMPT_COLOR}Press Enter to exit.{Style.RESET_ALL}")
    sys.exit(1) 
# Also check frame_rate if timecode was chosen
if output_format == "timecode" and (frame_rate is None or frame_rate <= 0):
     print_error("Valid positive framerate is required for timecode format. Exiting.")
     input(f"\n{PROMPT_COLOR}Press Enter to exit.{Style.RESET_ALL}")
     sys.exit(1)

seconds_per_full_beat = 60.0 / bpm
marker_interval_seconds = seconds_per_full_beat * beat_multiplier

print_info("Seconds per beat", f"{seconds_per_full_beat:.4f}")
print_info("Marker interval", f"{marker_interval_seconds:.4f} seconds")
print_info("Target duration", format_time_simple(total_duration_seconds)) # Show duration simply
if frame_rate: print_info("Using Framerate", f"{frame_rate} FPS")
print_info("Output Format", output_format.capitalize())


# --- Step 6: Generate Markers ---
print_section_header("6. Generating Markers")
time.sleep(0.2)
current_time = 0.0 
count = 0
generation_error = False
while True:
    current_time += marker_interval_seconds
    if current_time > total_duration_seconds + 1e-9: 
        break
    
    # --- CHOOSE FORMATTING FUNCTION ---
    if output_format == "timecode":
        formatted_marker = format_timecode(current_time, frame_rate)
        if "ERROR" in formatted_marker: # Check if formatting failed
            generation_error = True
            break # Stop generation if there's a critical error
    else: # Default to simple
        formatted_marker = format_time_simple(current_time)
        
    markers.append(formatted_marker)
    count += 1

if generation_error:
    print_error("Marker generation stopped due to formatting error (check framerate).")
elif markers:
    print_info(f"Generated {HIGHLIGHT_COLOR}{len(markers)}{INFO_COLOR} marker timestamps.")
else:
     print_warning("No markers generated. Song duration might be shorter than the calculated interval.")


# --- Step 7: Write to File ---
print_section_header(f"7. Writing Output File")
print_info("Output filename", output_filename)
time.sleep(0.3)

if not generation_error: # Only write if generation was successful
    try:
        with open(output_filename, "w") as f:
            if markers:
                for marker_time in markers:
                    f.write(marker_time + "\n")
                    
        if markers: 
            print_success(f"File '{output_filename}' created successfully!")
        else:
             print_info(f"File '{output_filename}' created (empty, no markers generated).")

    except IOError as e:
        print_error(f"Could not write to file '{output_filename}': {e}")
    except Exception as e:
         print_error(f"An unexpected error occurred during file writing: {e}")
else:
    print_warning(f"File '{output_filename}' was NOT written due to generation errors.")


# --- Done ---
print(f"\n{BORDER_COLOR}{LINE_CHAR * TERM_WIDTH}{Style.RESET_ALL}")
print_centered("✨ All Done! ✨", SUCCESS_COLOR if not generation_error else WARNING_COLOR)
print(f"{BORDER_COLOR}{LINE_CHAR * TERM_WIDTH}{Style.RESET_ALL}")

input(f"\n{PROMPT_COLOR}Press Enter to exit...{Style.RESET_ALL}")

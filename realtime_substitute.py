import sys

try:
    from pynput.keyboard import Key, Controller, Listener
except ImportError:
    print("Error: pynput is not installed. Please install it using 'pip install pynput'", file=sys.stderr)
    sys.exit(1)

# Default mapping
DEFAULT_MAPPING = {
    '0': 'o',
    '$': 's',
    '1': 'l',
    'vv': 'w',
    'zz': 'x'
}

# Global mapping dictionary
MAPPING = DEFAULT_MAPPING.copy()

# A buffer to store recent key presses
key_buffer = []
# The length of the longest key in the mapping
MAX_BUFFER_SIZE = 0

# Sorted mapping items for prioritized matching
sorted_mapping_items = []

keyboard = Controller()

def on_press(key):
    global key_buffer
    try:
        if hasattr(key, 'char') and key.char:
            key_buffer.append(key.char)
            if len(key_buffer) > MAX_BUFFER_SIZE:
                key_buffer.pop(0)

            # Check for mappings, longest ones first
            for old, new in sorted_mapping_items:
                if ''.join(key_buffer).endswith(old):
                    # Delete the matched string
                    for _ in range(len(old)):
                        keyboard.press(Key.backspace)
                        keyboard.release(Key.backspace)
                    # Type the new string
                    keyboard.type(new)
                    # Clear the buffer
                    key_buffer = []
                    break
        else:
            # Reset buffer on non-char keys (like space, enter, etc.)
            key_buffer = []

    except Exception as e:
        print(f"An error occurred: {e}")

def parse_mapping(mapping_str):
    mapping = {}
    for pair in mapping_str.split(','):
        if ':' not in pair:
            raise ValueError(f"Invalid mapping pair: {pair}")
        old, new = pair.split(':', 1)
        mapping[old] = new
    return mapping

def update_mapping_and_globals():
    global MAX_BUFFER_SIZE, sorted_mapping_items
    if MAPPING:
        MAX_BUFFER_SIZE = len(max(MAPPING.keys(), key=len))
    else:
        MAX_BUFFER_SIZE = 0
    sorted_mapping_items = sorted(MAPPING.items(), key=lambda item: len(item[0]), reverse=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            # If a mapping is provided, merge it with the default mapping
            cli_mapping = parse_mapping(sys.argv[1])
            MAPPING.update(cli_mapping)
        except ValueError as e:
            print(f"Error parsing command-line mapping: {e}", file=sys.stderr)
            sys.exit(1)

    update_mapping_and_globals()

    if not MAPPING:
        print("No mappings defined. Exiting.")
        sys.exit(0)

    print("Starting real-time substitution with the following mappings:")
    for old, new in MAPPING.items():
        print(f"  '{old}' -> '{new}'")
    print("Press Ctrl+C to stop.")

    try:
        with Listener(on_press=on_press) as listener:
            listener.join()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

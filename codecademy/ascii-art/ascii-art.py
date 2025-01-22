from ascii_map import ASCII_MAP

def print_string(text):
    """
    Renders text as ASCII art using ASCII_MAP, wrapping lines at 80 columns.
    """
    # We'll accumulate 7 "rows" of output at a time.
    output_lines = [""] * 7

    for char in text:
        # Convert to uppercase to match keys in ASCII_MAP (or fallback to '?').
        char_lines = ASCII_MAP.get(char.upper(), ASCII_MAP['?'])
        
        # Append each row of the char's ASCII art to the corresponding output row
        for row_index in range(7):
            candidate = output_lines[row_index] + char_lines[row_index] + " "
            if len(candidate) > 80:
                # Print the old line, start fresh with just this char.
                print(output_lines[row_index])
                output_lines[row_index] = char_lines[row_index]
            else:
                output_lines[row_index] = candidate

    # Print leftover line after the loop
    for row in range(7):
        print(output_lines[row])
    print()  # Blank line for separation

def main():
    user_input = input("Enter text to render (no extra spacing added): ")
    print_string(user_input)

if __name__ == "__main__":
    main()

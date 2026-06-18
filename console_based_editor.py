# --- Important Variables ---

content = ""
cursor_pos = 0
cursor_enabled = True 
lines = [""]
current_line_index = 0
line_cursor_enabled = False

add_text_commands = ["i", "I", "a", "A"]
move_cursor_commands = ["h","l","w","b","e","$","^", "j", "k"]
delete_commands = ["x", "X", "dw", "de", "db", "dc", "dd"]
other_commands = ["sw", "sb", "?", "v", "q", ".", ";", "o", "O", "J", "K"]
commands = move_cursor_commands + delete_commands + other_commands


# --- Core Functions ---

def main_function():
    """Run the editor loop: read commands, execute them, and display content."""
    global content, cursor_pos
    while True:
        command = input(">")
        cmd, text = deconstruct_command(command)

        if cmd is None: continue #ignores invalid command
        if cmd == "q": return #exits program

        execute_command(cmd, text)
        if cmd != "?": display_content()


def highlight_cursor():
    """Highlight the character at the current cursor position"""
    global content, cursor_pos
    left = content[:cursor_pos]
    char = content[cursor_pos]
    right = content[cursor_pos + 1:]
    highlighted = "\033[42m" + char + "\033[0m" #highlight current char with green background

    return left + highlighted + right


def display_content():
    """Display all lines with the row cursor on the active line"""
    global cursor_pos
    sync_to_lines()
    if cursor_pos >= len(content):
        cursor_pos = max(len(content) - 1, 0)
    for i, line in enumerate(lines):
        print(format_line_output(i, line))


def format_line_output(index, line):
    """Format a single line for output with its prefix and cursor body"""
    prefix = get_line_prefix(index)
    body = get_active_line_body() if index == current_line_index else line
    return prefix + body

    
def get_line_prefix(index):
    """Return the line cursor prefix symbol for the given line index"""
    if not line_cursor_enabled: return ""
    return "*" if index == current_line_index else " "


def get_active_line_body():
    """Return the active line text with the row cursor highlight if enabled"""
    if not content or not cursor_enabled:
        return content
    return highlight_cursor()


def deconstruct_command(command): 
    """Parse user input into a command key and optional text."""
    if not command: return None, None

    if command[0] in add_text_commands:
        if len(command) == 1:
            return None, None
        return command[0], command[1:]
    
    if command in commands: return command, None

    if command.isdigit() and int(command) > 0: return "line_no", int(command)
    
    return None, None


def execute_command(command, text):
    """Dispatch the command to their appropriate editor operation"""
    if command in add_text_commands:
        handle_insert_append(command, text)
    elif command in move_cursor_commands:
        handle_cursor_move(command)
    else:
        execute_non_motion(command, text)

def execute_non_motion(command, text):
    """Dispatch non-motion commands to their appropriate handlers"""
    if command in delete_commands:
        handle_delete(command)
    elif command == "line_no":
        jump_to_line(text)
    elif command in other_commands:
        handle_other_commands(command)



# --- Command Handling Functions --- 

def handle_cursor_move(command):
    """Send movement commands to the correct cursor function"""
    if command in ["h", "l"]:
        handle_horizontal_move(command)
    elif command in ["j", "k"]:
        handle_vertical_move(command)
    else:
        handle_word_line_move(command)


def handle_horizontal_move(command):
    """Move the cursor left or right"""
    if command == "h": move_left()
    elif command == "l": move_right()

def handle_vertical_move(command):
    """Move the cursor up or down between lines"""
    if command == "j": move_cursor_up()
    elif command == "k": move_cursor_down()

def handle_word_line_move(command):
    """Handle word-based and line-based cursor movement"""
    if command == "w": move_word_next()
    elif command == "b": move_word_prev_or_curr()
    elif command == "e": move_word_end()
    elif command == "$": move_line_end()
    elif command == "^": move_line_start()


def handle_insert_append(command, text):
    """Handle text insertion and append commands"""
    if command == "i": insert_before_cursor(text)
    elif command == "I": insert_beginning(text)
    elif command == "a": append_after_cursor(text)
    elif command == "A": append_end(text)


def handle_delete(command):
    """Handle delete commands for characters, words, or lines"""
    if command == "x": delete_under_cursor()
    elif command == "X": delete_before_cursor()
    elif command == "dd": delete_line()
    else: handle_word_delete(command)
    

def handle_word_delete(command):
    """Handle word deletion commands"""
    if command == "dw": delete_next()
    elif command == "de": delete_end()
    elif command == "db": delete_prev()
    elif command == "dc": delete_word_cursor()

def handle_other_commands(command):
    """Handle swap, help, toggle, and other extra commands"""
    if command == "sw": swap_next_word()
    elif command == "sb": swap_prev_word()
    elif command == "?": show_help()
    elif command == "v": pass
    elif command == ".": toggle_cursor()
    else: handle_multiline_commands(command)

def handle_multiline_commands(command):
    """Handle commands related to multiple lines"""
    if command == ";": toggle_line_cursor()
    elif command in ["o", "O"]: insert_empty_line(command)
    elif command in ["J", "K"]: move_line(command)



# --- Cursor Command Functions ---

def toggle_cursor():
    """Turn the row cursor display on or off using (.)"""
    global cursor_enabled
    cursor_enabled = not cursor_enabled


def move_left():
    """Move the cursor one position to the left using (h)"""
    global cursor_pos
    if cursor_pos > 0:
        cursor_pos -= 1


def move_right():
    """Move the cursor one position right using (l)"""
    global content, cursor_pos
    if cursor_pos < len(content) - 1:
        cursor_pos += 1


def move_line_start():
    """Move the cursor to the start of the line using (^)"""
    global cursor_pos
    cursor_pos = 0


def move_line_end():
    """Move the cursor to the end of the line using ($)"""
    global content, cursor_pos
    cursor_pos = max(len(content) - 1, 0)


def move_word_next():
    """Move the cursor to the start of the next word using (w)"""
    global content, cursor_pos
    #move to the end of the current word
    while cursor_pos < len(content) and content[cursor_pos] != " ":
        cursor_pos += 1

    #skip spaces to the start of the next word
    while cursor_pos < len(content) and content[cursor_pos] == " ":
        cursor_pos += 1


def move_word_prev_or_curr():
    "Move the cursor to the start of the current or previous word using (b)"
    global content, cursor_pos
    if cursor_pos == 0: return

    #skip spaces backward
    while cursor_pos > 0 and content[cursor_pos - 1] == " ":
        cursor_pos -= 1
    
    #move to start of word
    while cursor_pos > 0 and content[cursor_pos - 1] != " ":
        cursor_pos -= 1


def move_word_end():
    """Move the cursor to the end of the current or next word using (e)"""
    global content, cursor_pos
    if cursor_pos >= len(content):
        return
    
    #if at end of word, move forward first
    if cursor_pos < len(content) - 1 and content[cursor_pos + 1] == " ":
        cursor_pos += 1

    #skip spaces to next word
    while cursor_pos < len(content) and content[cursor_pos] == " ":
        cursor_pos += 1

    #move to end of that word
    while cursor_pos < len(content) - 1 and content[cursor_pos + 1] != " ":
        cursor_pos += 1


def move_cursor_up():
    "Move to the line above using (j)"
    global cursor_pos
    if current_line_index == 0: return
    sync_to_lines()
    target = current_line_index - 1
    cursor_pos = clamp_cursor_for_line(lines[target])
    load_line(target)


def move_cursor_down():
    """Move to the line below using (k)"""
    global cursor_pos
    if current_line_index == len(lines) - 1: return
    sync_to_lines()
    target = current_line_index + 1
    cursor_pos = clamp_cursor_for_line(lines[target])
    load_line(target)



# --- Text Insertion and Appending Functions ---

def insert_text_at(left_index, right_index, text):
    """Insert text into the editor content at the specified indices (right index and left index)."""
    global content, cursor_pos
    content = content[:left_index] + text + content[right_index:]
    cursor_pos = left_index + len(text) - 1 #cursor moves to end of inserted text


def insert_before_cursor(text):
    """Insert text before the cursor using (i)"""
    global cursor_pos
    pos = cursor_pos #marks beginning of inserted text
    insert_text_at(pos, pos, text)
    cursor_pos = pos 

def insert_beginning(text):
    """Insert text at the beginning of the line using (I)"""
    global cursor_pos
    insert_text_at(0, 0, text)
    cursor_pos = 0


def append_after_cursor(text):
    """Insert text after the cursor using (a)"""
    global cursor_pos
    insert_text_at(cursor_pos + 1, cursor_pos + 1, text)


def append_end(text):
    """Append text to the end of the line using (A)"""
    global content, cursor_pos
    insert_text_at(len(content), len(content), text)



# --- Text Deletion Functions ---

def delete_under_cursor():
    """Delete the character at the cursor using (x)"""
    global content, cursor_pos
    if not content: #nothing to delete
        return
    content = content[:cursor_pos] + content[cursor_pos + 1:]

    if cursor_pos >= len(content): #ensure cursor stays within bounds after deletion
        cursor_pos = len(content) - 1 if content else 0


def delete_before_cursor():
    """Delete the character before the cursor using (X)"""
    global content, cursor_pos
    if cursor_pos == 0: #nothing to delete
        return
    content = content[:cursor_pos - 1] + content[cursor_pos:]
    
    cursor_pos -= 1  


def delete_next():
    """Delete from the cursor to the start of the next word using (dw)"""
    global content, cursor_pos
    start = cursor_pos

    while cursor_pos < len(content) and content[cursor_pos] != " ":
        cursor_pos += 1 #move to end of current word
    while cursor_pos < len(content) and content[cursor_pos] == " ":
        cursor_pos += 1 #skip spaces to move to the start of next word
    
    content = content[:start] + content[cursor_pos:]
    #place cursor at next word start or at end 
    cursor_pos = start if start < len(content) else max(len(content) - 1, 0)


def delete_end():
    """Delete from the cursor to the end of the word using (de)"""
    global content, cursor_pos
    start = cursor_pos

    while cursor_pos < len(content) - 1 and content[cursor_pos + 1] == " ":
        cursor_pos += 1 #if on space, move to next word
    while cursor_pos < len(content) - 1 and content[cursor_pos + 1] != " ":
        cursor_pos += 1 #move to end of word

    content = content[:start] + content[cursor_pos + 1:]
    #keep cursor unless hit the end
    cursor_pos = start if start < len(content) else max(len(content) - 1, 0)


def delete_prev():
    """Delete from cursor back to the start of the previous word using (db)"""
    global content, cursor_pos
    original = cursor_pos
    
    while cursor_pos > 0 and content[cursor_pos - 1] == " ":
        cursor_pos -= 1 #skip spaces
    while cursor_pos > 0 and content[cursor_pos - 1] != " ":
        cursor_pos -= 1 #move to start of word
    
    content = content[:cursor_pos] + content[original + 1:]
    if cursor_pos >= len(content): 
        cursor_pos = max(len(content) - 1, 0)
    

def delete_word_cursor(): 
    """Delete the word or spaces at the cursor using (dc)"""
    global content, cursor_pos
    if content[cursor_pos] == " ":
        start, end = expand_over_spaces()
    else:
        start, end = expand_over_word()
    
    content = content[:start] + content[end:]

    if not content: cursor_pos = 0
    elif cursor_pos >= len(content): cursor_pos = len(content) - 1



# --- Swap Command Function ---

def swap_next_word():
    """Swap the current word with the next word using (sw)"""
    global cursor_pos, content
    if not is_on_word(): return

    curr_start, curr_end = expand_over_word()
    next_start, next_end = get_next_word_bounds(curr_end)
    
    if next_start is None: return

    #save the relative offset
    offset = cursor_pos - curr_start
    
    swap_words(curr_start, curr_end, next_start, next_end)
    spaces_len = next_start - curr_end
    cursor_pos = curr_start + (next_end - next_start) + spaces_len + offset


def swap_prev_word():
    """Swap the current word with the previous word using (sb)"""
    global cursor_pos, content
    if not is_on_word(): return

    curr_start, curr_end = expand_over_word()
    prev_start, prev_end = get_prev_word_bounds(curr_start)
    
    if prev_start is None: return

    #save the relative offset
    offset = cursor_pos - curr_start
    
    swap_words(prev_start, prev_end, curr_start, curr_end)
    cursor_pos = prev_start + offset



# --- Multi-Line Command Functions ---

def toggle_line_cursor():
    """Toggle the line marker on or off using (;)"""
    global line_cursor_enabled
    line_cursor_enabled = not line_cursor_enabled


def insert_empty_line(command):
    """Insert a blank line above (O) or below (o)"""
    global cursor_pos
    sync_to_lines()
    insert_index = current_line_index + (1 if command == "o" else 0)
    lines.insert(insert_index, "")
    cursor_pos = 0
    load_line(insert_index)


def delete_line():
    """Delete the current line using (dd)"""
    sync_to_lines()
    if len(lines) == 1:
        reset_to_empty_line()
        return
    lines.pop(current_line_index)
    switch_to_line(min(current_line_index, len(lines) - 1))


def reset_to_empty_line():
    """Reset the editor to one empty line"""
    global content, cursor_pos
    lines[0] = ""
    content = ""
    cursor_pos = 0


def move_line(command):
    """Move the current line up (J) or down (K)"""
    global current_line_index
    sync_to_lines()
    if command == "J" and current_line_index > 0:
        swap_lines(current_line_index - 1, current_line_index)
        current_line_index -= 1
    elif command == "K" and current_line_index < len(lines) - 1:
        swap_lines(current_line_index, current_line_index + 1)
        current_line_index += 1
    load_line(current_line_index)


def jump_to_line(line_no):
    """Jump to a specific line number"""
    global cursor_pos
    sync_to_lines()
    target = min(line_no - 1, len(lines) - 1)
    cursor_pos = 0
    load_line(target) 



# --- Help Command Function --- 

def show_help():
    """Display all available editor commands using (?)"""
    help_text = """
? - display this help info                       
. - toggle row cursor on and off
h - move cursor left
l - move cursor right
^ - move cursor to beginning of the line
$ - move cursor to end of the line
w - move cursor to beginning of next word
b - move cursor to beginning of current or previous word
e - move cursor to end of the word
i - insert <text> before cursor
a - append <text> after cursor
I - insert <text> from beginning
A - append <text> at the end
x - delete character at cursor
X - delete character before cursor
dw - delete to start of next word
de - delete to end of next word
db - delete to start of current or previous word
dc - delete whitespaces or entire word at cursor
sw - swap word at cursor with next word
sb - swap word at cursor with previous word
; - toggle line cursor on and off
j - move cursor up
k - move cursor down
o - insert empty line below
O - insert empty line above
dd - delete line
K - move line down
J - move line up
Line_No. - jump to specific line, first character
v - view editor content
q - quit program
"""
    print(help_text.strip())




# --- Helper Functions ---

def expand_over_spaces():
    """Find the full range of spaces around the cursor"""
    global content, cursor_pos
    start = cursor_pos
    end = cursor_pos

    while start > 0 and content[start - 1] == " ":
        start -= 1
    while end < len(content) and content[end] == " ":
        end += 1
    
    return start, end


def expand_over_word():
    """Find the full range of the word around the cursor"""
    global content, cursor_pos
    start = cursor_pos
    end = cursor_pos

    while start > 0 and content[start - 1] != " ":
        start -= 1
    while end < len(content) and content[end] != " ":
        end += 1
    
    return start, end


def is_on_word():
    """Check if the cursor is currently on a word"""
    global content, cursor_pos
    if not content or cursor_pos >= len(content):
        return False
    return content[cursor_pos] != " "


def get_next_word_bounds(current_word_end):
    """Return the start and end positions of the next word"""
    index = current_word_end
    while index < len(content) and content[index] == " ": 
        index += 1

    if index >= len(content): return None, None

    start = index
    end = index

    while end < len(content) and content[end] != " ": 
        end += 1
    return start, end


def get_prev_word_bounds(current_word_start):
    """Return the start and end positions of the previous word"""
    index = current_word_start
    while index > 0 and content[index-1] == " ": 
        index -= 1
    if index == 0: return None, None

    end = index
    start = index-1

    while start > 0 and content[start-1] != " ": 
        start -= 1
    return start, end


def swap_words(first_start, first_end, second_start, second_end):
    """Swap two words using their positions"""
    global content
    first_word = content[first_start:first_end]
    second_word = content[second_start:second_end]
    middle_space = content[first_end:second_start]

    content = content[:first_start] + second_word + middle_space + first_word + content[second_end:]


def sync_to_lines():
    """Save current content back into the active slot in the lines list"""
    lines[current_line_index] = content


def load_line(index):
    """Set the active line to the one at the given index"""
    global current_line_index, content
    current_line_index = index
    content = lines[index]


def clamp_cursor_for_line(line):
    """Return cursor_pos clamped to fit within the given line's length"""
    if not line: return 0
    return min(cursor_pos, len(line) - 1)


def switch_to_line(index):
    """Switch the active line, adjusting the cursor position as needed"""
    global cursor_pos
    cursor_pos = clamp_cursor_for_line(lines[index])
    load_line(index)


def swap_lines(index1, index2):
    """Swap two lines in the lines list by their indices"""
    lines[index1], lines[index2] = lines[index2], lines[index1]



# --- Text Editor Enabler --- 

if __name__ == "__main__":
    main_function()
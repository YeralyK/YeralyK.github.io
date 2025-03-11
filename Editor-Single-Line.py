import re

content = ""
cursor_id = 0
green_cursor = False   # Toggling cursor 
stacking_history = []  # Stores content and cursor_id  for undo
last_valid_cmd = None  # For repeat (excludes 'u', '?', 'r')

def get_info():
    print(
        "? - display this help info\n"
        ". - toggle row cursor on and off\n"
        "h - move cursor left\n"
        "l - move cursor right\n"
        "^ - move cursor to beginning of the line\n"
        "$ - move cursor to end of the line\n"
        "w - move cursor to beginning of next word\n"
        "b - move cursor to beginning of previous word\n"
        "i - insert <text> before cursor\n"
        "a - append <text> after cursor\n"
        "x - delete character at cursor\n"
        "dw - delete word and trailing spaces at cursor\n"
        "u - undo previous command\n"
        "s - show content\n"
        "q - quit program\n"
    )

def cursor_toggle():
    """Toggling the display of the cursor (green highlight) on and off."""
    global green_cursor
    green_cursor = not green_cursor

def move_left():
    """Moving the cursor one character to the left"""
    global cursor_id
    if cursor_id > 0:
        cursor_id -= 1

def move_right():
    """Moving the cursor one character to the right"""
    global cursor_id
    if cursor_id < len(content):
        cursor_id += 1

def to_the_start():
    """Moving the cursor to the beginning of the content"""
    global cursor_id
    cursor_id = 0

def to_the_end():
    """Moving the cursor to the end of the content"""
    global cursor_id
    if len(content) > 0:
        cursor_id = len(content) - 1
    else:
        cursor_id = 0

def next_word():
    """Moving the cursor to the beginning of the next word"""
    global cursor_id
    id = cursor_id

    while cursor_id < len(content) and content[cursor_id] != " ":
        cursor_id += 1

    while cursor_id < len(content) and content[cursor_id] == " ":
        cursor_id += 1

    if cursor_id == id:
        return  

def previous_word():
    """Moving the cursor to the beginning of the next word"""
    global cursor_id
    id = cursor_id

    if cursor_id == 0:
        return
    
    cursor_id -= 1

    while cursor_id > 0 and content[cursor_id] == " ":
        cursor_id -= 1
    while cursor_id > 0 and content[cursor_id - 1] != " ":
        cursor_id -= 1
    if cursor_id == id:
        return 

def insert(text):
    """Inserting the given text before the current cursor position"""
    global content, cursor_id
    content = content[:cursor_id] + text + content[cursor_id:]

def append(text):
    """Appending the given text after the current cursor position"""
    global content, cursor_id
    if len(content) == 0:
        content = text
        cursor_id = len(content) - 1
    else:
        content = content[:cursor_id + 1] + text + content[cursor_id + 1:]
        cursor_id += len(text)

def delete():
    """Deleting the character at the current cursor position"""
    global content
    if cursor_id < len(content):
        content = content[:cursor_id] + content[cursor_id + 1:]

def delete_word():
    """Deleting the word at the cursor along with any trailing spaces"""
    global content, cursor_id
    
    if cursor_id >= len(content):
        return

    # Finding the start of the current word
    start = cursor_id
    while start > 0 and content[start - 1] != " ":
        start -= 1

    # Finding the end of the word and trailing spaces
    end = cursor_id
    while end < len(content) and content[end] != " ":
        end += 1
    while end < len(content) and content[end] == " ":
        end += 1

    # Updating content and cursor
    content = content[:start] + content[end:]
    cursor_id = start

def show():
    """Showing the current content"""
    if green_cursor:
        if cursor_id < len(content):
            green_char = "\033[42m" + content[cursor_id] + "\033[0m"
            display = content[:cursor_id] + green_char + content[cursor_id + 1:]
        else:
            display = content + "\033[42m \033[0m"
        print(display)
    else:
        print(content)

def quit():
    """Exit the program"""
    raise SystemExit()

def command_executor(cmd):
    """Processing and executing command string."""
    global last_valid_cmd, stacking_history

    # Ignoting invalid commands
    if cmd.strip() != cmd:
        return
    
    # Saving state if the command changes the state (except for undo, help, or repeat commands)
    state_changing_cmds = {'h', 'l', '^', '$', 'w', 'b', 'x', 'dw', '.', 'i', 'a'}
    if cmd in state_changing_cmds or cmd.startswith(('i', 'a')):
        stacking_history.append((content, cursor_id))
        last_valid_cmd = cmd if cmd not in {'u', '?', 'r'} else None

    # Executing command
    if cmd == "?":
        get_info()
    elif cmd == ".":
        cursor_toggle()
    elif cmd == "h":
        move_left()
    elif cmd == "l":
        move_right()
    elif cmd == "^":
        to_the_start()
    elif cmd == "$":
        to_the_end()
    elif cmd == "w":
        next_word()
    elif cmd == "b":
        previous_word()
    elif cmd == "x":
        delete()
    elif cmd == "dw":
        delete_word()
    elif cmd == "q":
        quit()
    elif cmd == "u":
        undo()
    elif cmd == "r":
        repeat()
    else:
        # Checking for 'insert' command with no space between command and text
        matching = re.fullmatch(r"i(.+)", cmd)
        if matching:
            insert(matching.group(1))
        else:
            # Checking for 'append' command with no space between command and text
            matching = re.fullmatch(r"a(.+)", cmd)
            if matching:
                append(matching.group(1))
            else:
                pass

def undo():
    """Undoing the previous state-changing command"""
    global content, cursor_id, stacking_history
    if stacking_history:
        content, cursor_id = stacking_history.pop()

def repeat():
    """Repeating the last valid state-changing command"""
    if last_valid_cmd:
        command_executor(last_valid_cmd)

def main():
    """Main loop to run the text editor simulation"""
    while True:
        cmd = input(">")
        command_executor(cmd)
        if cmd not in {'?', 'q'}:
            show()

if __name__ == "__main__":
    main()
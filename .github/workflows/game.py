import sys, tty, termios, select, shutil

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
tty.setcbreak(fd)

width = shutil.get_terminal_size().columns 
pos = width // 2

try:
    while True:
        frame = ['!'] * width
        frame[pos] = '#'
        print(f"\r\033[K{''.join(frame)}", end='', flush=True)

        if select.select([sys.stdin], [], [], 0.05)[0]:
            key = sys.stdin.read(1)
            if key == 'a' and pos > 0:
                pos -= 1
            elif key == 'd' and pos < width - 1:
                pos += 1
            elif key == '\x1b':  # Клавиша Esc
                break

except KeyboardInterrupt:
    pass

finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    print()
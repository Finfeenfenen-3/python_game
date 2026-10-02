import sys
import tty
import termios
import select
import shutil

def main():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    try:
        tty.setcbreak(fd)
        
        pos = shutil.get_terminal_size().columns // 2
        lin = 0

        # Скрываем курсор и очищаем экран ОДИН РАЗ при запуске
        sys.stdout.write("\033[?25l\033[2J")
        sys.stdout.flush()

        while True:
            # Получаем размеры каждый кадр (на случай, если вы измените размер окна)
            width, lines = shutil.get_terminal_size()
            
            # Защита от выхода за границы при уменьшении окна
            if pos >= width: pos = width - 1
            if lin >= lines: lin = lines - 1
            if pos < 0: pos = 0
            if lin < 0: lin = 0

            # 1. Возвращаем курсор в левый верхний угол (НЕ очищаем экран, чтобы не мерцало)
            sys.stdout.write("\033[H")
            
            # 2. Генерируем кадр в памяти
            frame = [['!'] * width for _ in range(lines)]
            frame[lin][pos] = '#'
            screen_buffer = "\n".join("".join(row) for row in frame)
            
            sys.stdout.write(screen_buffer)
            sys.stdout.flush()


            if select.select([sys.stdin], [], [], 0.05)[0]:
                key = sys.stdin.read(1)
                
                if key == '\x1b':  
                    if select.select([sys.stdin], [], [], 0.001)[0]:
                        sys.stdin.read(2)
                        continue
                    else:
                        break 
                elif key == 'a' and pos > 0:
                    pos -= 1
                elif key == 'd' and pos < width - 1:
                    pos += 1
                elif key == 'w' and lin > 0:
                    lin -= 1
                elif key == 's' and lin < lines - 1:
                    lin += 1

    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        sys.stdout.write("\033[?25h\033[2J\033[H")
        sys.stdout.flush()
        print()

if __name__ == "__main__":
    main()

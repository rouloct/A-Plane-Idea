### RC Plane with Raspberry Pi Controller

This project explores the use of a Raspberry Pi as the flight controller for a custom-built RC plane. It's a final project for CS 2100 (Computer Organization).

**Running the Program**
1. Navigate to appropriate directory and open a terminal.
2. Type `sudo pigpiod` to run the pigpio daemon.
3. Type `screen` to create a new screen.
4. Hit `ENTER` to enter screen.
5. Type `python3 main.py` or `py main.py` to run the program.
6. Press `CTRL`+`A` then `CTRL`+`D` to disconnect the screen.
7. Disconnect the SSH connection: If in VSCode, close window. If in terminal, type `exit`.

**Quitting the Screen from Inside the Session**
1. Type `screen -ls` to see a list of screens. Take note of the screen's pid: for `4510.pts-0.raspberrypi` the pid is 4510.
2. Type `screen -r (pid)` where `(pid)` is the screen's pid to return to the screen.
3. Type `exit` to close the current screen.

**Quitting the Screen from Ouside the Session**
1. Type `screen -ls` to see a list of screens. Take note of the screen's pid: for `4510.pts-0.raspberrypi` the pid is 4510.
2. Type `screen -X -S (pid) quit` where `(pid)` is the screen's pid to force quit the screen.

**Presentation**  
[https://docs.google.com/presentation/d/1hiCboXv1AIqShtnhkoB7q91nwMJbQwPUNCncO6HIbKM](https://docs.google.com/presentation/d/1hiCboXv1AIqShtnhkoB7q91nwMJbQwPUNCncO6HIbKM)

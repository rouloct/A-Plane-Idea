### RC Plane with Raspberry Pi Controller

This project explores the use of a Raspberry Pi as the flight controller for a custom-built RC plane. It's a final project for CS 2100 (Computer Organization).

**Running the Program**
1. Navigate to appropriate directory.
2. Run `sudo pigpiod` in terminal.
3. Type `screen` into terminal.
4. Hit `ENTER` to enter screen.
5. Run main.py with `python3 main.py` or `py main.py`.
6. Detach screen with `CTRL+A` then `CTRL+D`.
7. Disconnect the SSH connection: If in VSCode, close window. If in terminal, type `exit`.

**Quitting the Screen**
1. Type `screen -ls` to see a list of screens. Take note of the screen's pid, the numbers at the start. ex) for `4510.pts-0.raspberrypi` the pid is 4510.
2. Type `screen -X -S (pid) quit` where `(pid)` is the screen's pid.

**Current Capabilities**

* Real-time input processing from the RC receiver.
* Direct servo control based on receiver commands.
* Switch-based control logic for the RC transmitter.

**Work in Progress**

* Airframe construction and assembly.

**Project Completion**

* Targeted completion date: April 25th.
* A demo video will showcase the final project in action.

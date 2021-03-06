# Mine collector simulator

Simulator of a mine collector robot, written in an evening from scratch for the university course of Software Engineering 2019.

It makes developing an algorithm for a mine collector robot less time consuming using a virtual environment with the same limitations as the real one, without using a real robot for the task.

## How to use

Edit the file `seek.py` to provide an algorithm that collects all the mine in the field.

The robot can use all variables and functions listed under `public variables` and `public functions`, and should not use the private variables.

Execute the simulator with the command

```
$ python ./main.py
```

Once the simulation is over, press Ctrl-C to terminate it.

The simulation is better viewed in a square-sized font, like [this one](http://strlen.com/square).

## Demo

Here's a demo of the program running, you can execute it by changing the `SOURCE_FILE` constant in `main.py` to `demo.py`.

![](demo.gif)
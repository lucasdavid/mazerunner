# Maze Runner

Final Project for Artificial Intelligence 2016-1 class at UNICAMP.

## Installing

```shell
python setup.py install --user
```

## Executing the Examples
First, start `Choregraph`:
```shell
/opt/Aldebaran\ Robotics/Choregraphe\ Suite\ 2.1/bin/naoqi-bin -p 5000
```

Then start the simulation on V-REP.

Finally, run the linker:
```shell
cd mazerunner/naovreplinker/
python2 single_nao_contro.py
```

Open a second terminal and run one of the examples:
```shell
python mazerunner/examples/simple_walker.py
```

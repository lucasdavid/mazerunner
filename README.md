# Maze Runner

Final Project for Artificial Intelligence 2016-1 class at UNICAMP.

### Requirements
- [v-rep] : A mostly free and awsome robot simulator.
- [Python NAOqi-SDK] : Contain all the function you need to manipulate your NAO (virtual or not) using python.
- [Choregraphe Suite] : This will allow you to manipulate your virtual robot easier and launch a virtual NAO on your computer.
- [Spyder] : This is not mandatory, but it's a good MATLAB-like development environment for python


## Installing

```shell
python setup.py install --user
```

## Executing the Examples
First, start `Choregraph`:
```shell
/opt/Aldebaran\ Robotics/Choregraphe\ Suite\ 2.1/bin/naoqi-bin -p 5000
```

Then start one the scenes in `scenes` folder the simulation on V-REP.
Finally, run one of the examples:
```shell
python mazerunner/examples/simple_walker.py
```


[v-rep]:http://www.coppeliarobotics.com/downloads.html
[Python NAOqi-SDK]:https://community.aldebaran.com/en/resources/software
[Choregraphe Suite]:https://community.aldebaran.com/en/resources/software

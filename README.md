# Maze Runner

Final Project for Artificial Intelligence 2016-1 class at UNICAMP.

Local navigation of the bibed robot NAO on a V-REP simulation using
reinforcement learning (Q-Learning).
The desired behavior is for the robot to use its sensors to avoid walls
and attempt to get as close as possible to a tag placed at the kitchen.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=n-5PvVGxibg"
   target="_blank"><img src="http://img.youtube.com/vi/n-5PvVGxibg/0.jpg"
alt="NAO navigation demonstration" width="480" height="315" border="0" /></a>

## Installing

This project has some dependencies that are not managed by pip.
They must, therefore, be installed manually:

* [V-REP simulator](http://www.coppeliarobotics.com/downloads.html)
* [Choregraphe](https://community.aldebaran.com/en/resources/software) Suite
* Aldebaran NAO [Python SDK](http://doc.aldebaran.com/2-1/dev/python/install_guide.html)

Finally, install MazeRunner:

```shell
python setup.py install --user
```

## Executing Navigation with QLearning

1. First, start `Choregraph`:
```shell
/opt/Aldebaran\ Robotics/Choregraphe\ Suite\ 2.1/bin/naoqi-bin -p 5000
```

2. Open the V-REP simulator:
```shell
/path/to/vrep/vrep.sh
```
Then open one of the scenes in `mazerunner/scenes` folder and run it.

3. Finally, run the navigation:
```shell
python mazerunner/examples/navigate.py
```

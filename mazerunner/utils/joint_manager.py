"""Joint Manager.

Joint manager used to link NAO robot to V-REP simulator.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging
import time
from threading import Thread

from . import vrep

logger = logging.getLogger('mazerunner')


class JointManager(Thread):
    """Joint Manager.

    Joint manager used to link NAO robot to V-REP simulator.

    This class gets joint's angles from Choregraphe and use them to move
    around in V-REP.

    :param link: V-REP connection link, which is shared by all agents
    through the environment.

    :param motion: ALMotion object-like associated to the RoboticAgent
    of interest.

    :param identity: int, default=0, an integer that identifies the robot
    in the V-REP simulator. If there's only one, then 0, an empty string or
    nothing at all should be passed.
    """

    JOINT_MAP = (
        # Head joints.
        ('HeadYaw', 0), ('HeadPitch', 1),
        # Left leg joints.
        ('LHipYawPitch3', 8), ('LHipRoll3', 9), ('LHipPitch3', 10),
        ('LKneePitch3', 11),
        ('LAnklePitch3', 12), ('LAnkleRoll3', 13),
        # Right leg joints.
        ('RHipYawPitch3', 14), ('RHipRoll3', 15), ('RHipPitch3', 16),
        ('RKneePitch3', 17), ('RAnklePitch3', 18), ('RAnkleRoll3', 19),
        # Left arm joints.
        ('LShoulderPitch3', 2), ('LShoulderRoll3', 3), ('LElbowYaw3', 4),
        ('LElbowRoll3', 5), ('LWristYaw3', 6),
        # Right arm joints.
        ('RShoulderPitch3', 20), ('RShoulderRoll3', 21), ('RElbowYaw3', 22),
        ('RElbowRoll3', 23), ('RWristYaw3', 24),
        # Left fingers' joints.
        ('NAO_LThumbBase', 7), ('Revolute_joint8', 7), ('NAO_LLFingerBase', 7),
        ('Revolute_joint12', 7), ('Revolute_joint14', 7),
        ('NAO_LRFinger_Base', 7), ('Revolute_joint11', 7),
        ('Revolute_joint13', 7),
        # Right fingers' joints.
        ('NAO_RThumbBase', 25), ('Revolute_joint0', 25),
        ('NAO_RLFingerBase', 25), ('Revolute_joint5', 25),
        ('Revolute_joint6', 25), ('NAO_RRFinger_Base', 25),
        ('Revolute_joint2', 25), ('Revolute_joint3', 25),
    )

    SYNC_PERIOD = .01
    MAX_SYNC_PERIOD = .1

    def __init__(self, link, motion, identity=''):
        super(JointManager, self).__init__()

        self.link = link
        self.motion = motion
        self.identity = identity or ''

        self.body_ = None
        self.active_ = False

        self.prepare()

    def prepare(self):
        logger.info('linking joints...')
        self.body_ = [vrep.simxGetObjectHandle(
            self.link, label + '#' + self.identity,
            vrep.simx_opmode_oneshot_wait)[1]
                      for label, _ in self.JOINT_MAP]
        logger.info('joints linked')

    @property
    def is_connected(self):
        return vrep.simxGetConnectionId(self.link) != -1

    def run(self):
        self.active_ = True

        while self.active_ and self.is_connected:
            angles = self.motion.getAngles('Body', False)

            for body_id, (label, angle_id) in enumerate(self.JOINT_MAP):
                angle = angles[angle_id]
                # Fingers' angles are inverted. Convert them again.
                if body_id > 23: angle = 1. - angle
                # Actually set angles.
                vrep.simxSetJointTargetPosition(self.link,
                                                self.body_[body_id], angle,
                                                vrep.simx_opmode_streaming)
            time.sleep(self.SYNC_PERIOD)

        if not self.is_connected:
            logger.warning('the connection to V-REP was lost')

        self.active_ = False

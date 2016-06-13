# -*- coding: utf-8 -*-
"""
@author: Pierre Jacquot
"""
import argparse
from threading import Thread

from naoqi import ALProxy

import handlers
import vrep
from manage_joints import get_first_handles, JointControl


def establish_connection(nao_ip='127.0.0.1', nao_port=5000):
    print 'Establishing connection...'

    try:
        vrep.simxFinish(-1)

        client_id = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

        assert client_id != -1, 'Could not connect to V-REP API.'

        motion_proxy = ALProxy("ALMotion", nao_ip, nao_port)
        posture_proxy = ALProxy("ALRobotPosture", nao_ip, nao_port)

        motion_proxy.stiffnessInterpolation('Body', 1.0, 1.0)
        posture_proxy.goToPosture('Stand', 1.0)

        get_first_handles(client_id, handlers.Body)
        commandAngles = motion_proxy.getAngles('Body', False)

        print('NAO --> V-REP link established.')
        JointControl(client_id, motion_proxy, 0, handlers.Body)
    except KeyboardInterrupt:
        pass
    finally:
        print 'Bye.'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=5000,
                        help="Robot port number")

    args = parser.parse_args()
    establish_connection(args.ip, args.port)

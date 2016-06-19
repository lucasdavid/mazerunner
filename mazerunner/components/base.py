"""Components Base.

Base interface for V-REP components abstractions.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
from ..utils import vrep


class Component(object):
    """A V-REP Component."""

    tag = 'NAO_component'

    def __init__(self, link, component_id=''):
        self.link = link

        errors, self.adapter = vrep.simxGetObjectHandle(
            link, self.tag + str(component_id),
            vrep.simx_opmode_oneshot_wait)

        assert not errors


class Sensor(Component):
    """A V-REP Sensor."""

    tag = 'NAO_sensor'

    def __init__(self, link, component_id=''):
        super(Sensor, self).__init__(link, component_id)

        self.last_read = None

    def read(self):
        raise NotImplementedError

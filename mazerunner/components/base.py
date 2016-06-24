"""Components Base.

Base interface for V-REP component abstraction.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
from ..utils import vrep


class Adapter(object):
    def __init__(self, link, component_tag):
        self.link = link
        self.component_tag = component_tag

        errors, self.handler = vrep.simxGetObjectHandle(
            link, str(component_tag), vrep.simx_opmode_blocking)

        assert not errors


class Component(object):
    """V-REP Component Base Class.

    Base class for correctly retrieving object handlers from V-REP API.

    :param link: v-rep link, required for every transaction with the simulator.
    :param component: str or instance of Adapter.
        If it's a string, it will be interpreted as a tag in the simulation
        and an Adapter will be created.
        If it's an adapter, it will be simply copied and stored.
    """

    def __init__(self, link, component):
        if isinstance(component, str):
            self.adapter = Adapter(link, component_tag=component)
        elif isinstance(component, Adapter):
            self.adapter = component
        else:
            raise ValueError('Illegal value for component parameter: {%s}'
                             % component)


class Sensor(Component):
    """V-REP Sensor Base Class."""

    def __init__(self, link, component):
        super(Sensor, self).__init__(link, component)

        self.last_read = None

    def read(self):
        raise NotImplementedError

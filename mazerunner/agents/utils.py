"""Agents Utils.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""


def stiffness_on(proxy):
    pNames = 'Body'
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

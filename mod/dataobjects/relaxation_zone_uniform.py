#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics Uniform Relaxation Zone data '''


from mod.dataobjects.relaxation_zone import RelaxationZone


class RelaxationZoneUniform(RelaxationZone):
    ''' Relaxation zone for uniform velocity wave generation '''

    def __init__(self, start=0, duration=0, domainbox_point=None, domainbox_size=None, domainbox_direction=None,
                 domainbox_rotateaxis_angle=0, domainbox_rotateaxis_point1=None, domainbox_rotateaxis_point2=None,
                 use_velocity=True, velocity=0, velocity_times=None, coefdt=1000, function_psi=0.9, function_beta=1):
        super().__init__()
        self.start = start
        self.duration = duration
        self.domainbox_point = domainbox_point if domainbox_point is not None else [0, 0, 0]
        self.domainbox_size = domainbox_size if domainbox_size is not None else [0, 0, 0]
        self.domainbox_direction = domainbox_direction if domainbox_direction is not None else [0, 0, 0]
        self.domainbox_rotateaxis_angle = domainbox_rotateaxis_angle
        self.domainbox_rotateaxis_point1 = domainbox_rotateaxis_point1 if domainbox_rotateaxis_point1 is not None else [
            0, 0, 0]
        self.domainbox_rotateaxis_point2 = domainbox_rotateaxis_point2 if domainbox_rotateaxis_point2 is not None else [
            0, 0, 0]
        self.use_velocity = use_velocity
        self.velocity = velocity
        self.velocity_times = velocity_times or []
        self.coefdt = coefdt
        self.function_psi = function_psi
        self.function_beta = function_beta

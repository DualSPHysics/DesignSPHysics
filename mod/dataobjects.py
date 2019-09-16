# -*- coding: utf-8 -*-
'''Data objects for DesignSPHysics

This module contains multiple data objects used in the execution
of DesignSPHysics.

'''

from os import path, environ
from sys import platform
from random import randint

import FreeCAD
import FreeCADGui

from PySide import QtCore, QtGui
from mod.utils import __, log, executable_contains_string
from mod.enums import *
from mod.constants import *

# Copyright (C) 2019
# EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo
# EPHYTECH Environmental Physics Technologies
#
# This file is part of DesignSPHysics.
#
# DesignSPHysics is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DesignSPHysics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DesignSPHysics.  If not, see <http://www.gnu.org/licenses/>.


class FloatProperty():
    ''' Float property of an DSPH object.

    Attributes:
        mk: Mk to witch this FloatProperty is binded.
        mass_density_type: Density type 0 is massbody; 1 is rhopbody.
        mass_density_value: Value for mass/density
        gravity_center: Coords in [x, y, z] format. None for auto.
        inertia: Coords in [x, y, z] format. None for auto.
        initial_linear_velocity: Coords in [x, y, z] format. None for auto.
        initial_angular_velocity: Coords in [x, y, z] format. None for auto.
        rotation_restriction: Coords in [x,y,z] format. None for auto.
    '''

    def __init__(self, mk=-1, mass_density_type=FloatingDensityType.MASSBODY, mass_density_value=100,
                 gravity_center=None, inertia=None, initial_linear_velocity=None,
                 initial_angular_velocity=None, translation_restriction=None,
                 rotation_restriction=None, material=None):
        self.mk = mk
        self.mass_density_type = mass_density_type
        self.mass_density_value = mass_density_value
        self.gravity_center = gravity_center
        self.inertia = inertia
        self.initial_linear_velocity = initial_linear_velocity
        self.initial_angular_velocity = initial_angular_velocity
        self.translation_restriction = translation_restriction
        self.rotation_restriction = rotation_restriction
        self.material = material


class FacesProperty():
    ''' Stores the faces selected to generate on GenCase for a given object '''

    def __init__(self, mk=-1, all_faces=False, front_face=False,
                 back_face=False, top_face=False, bottom_face=False,
                 left_face=False, right_face=False, face_print=''):
        self.mk = mk
        self.all_faces = all_faces
        self.front_face = front_face
        self.back_face = back_face
        self.top_face = top_face
        self.bottom_face = bottom_face
        self.left_face = left_face
        self.right_face = right_face
        self.face_print = face_print


class InitialsProperty():
    ''' Initial movement property of an DSPH object.

    Attributes:
        mk: Mk to witch this InitialsProperty is binded.
        force: Force in [x, y, z] format.
    '''

    def __init__(self, mk=-1, force=None):
        self.mk = mk
        self.force = force or []


class Material():
    ''' DualSPHysics compatible material.

    Attributes:
        bound_mk: List of mk groups this material is binded
    '''

    def __init__(self, mk=None):
        self.bound_mk = mk or []


class Movement():
    ''' DualSPHysics compatible movement.
        It includes a list of different motions to represent an entire simulation
        movement.

        Attributes:
            name: Name for this motion given by the user
            motion_list: List of motion objects in order
            loop: Boolean indicating if it is a loop
        '''

    def __init__(self, name="New Movement", motion_list=None, loop=False):
        self.name = name
        self.type = "Movement"
        self.motion_list = motion_list or []
        self.loop = loop

    def add_motion(self, motion):
        ''' Adds a motion to the movement '''
        if isinstance(motion, BaseMotion):
            motion.parent_movement = self
            self.motion_list.append(motion)
        else:
            raise TypeError(
                "You are trying to append a non-motion object to a movement list.")

    def set_loop(self, state):
        ''' Set loop state for the movement '''
        if isinstance(state, bool):
            self.loop = state
        else:
            raise TypeError("Tried to set a boolean with an {}".format(
                state.__class__.__name__))

    def remove_motion(self, position):
        ''' Removes a motion from the list '''
        self.motion_list.pop(position)

    def __str__(self):
        to_ret = "Movement <{}>".format(self.name) + "\n"
        to_ret += "Motion List:\n"
        for motion in self.motion_list:
            to_ret += str(motion) + "\n"
        return to_ret


class SpecialMovement():
    ''' DualSPHysics compatible special movement.
        It includes regular/irregular wave generators and file movements

        Attributes:
            name: Name for this motion given by the user
            generator: Generator assigned
        '''

    def __init__(self, name="New Movement", generator=None):
        self.name = name
        self.type = "Wave Movement"
        if not generator:
            generator = None
        self.generator = generator

    def set_wavegen(self, generator):
        ''' Sets the wave generator for the special movement '''
        if isinstance(generator, WaveGen):
            generator.parent_movement = self
            self.generator = generator
        else:
            raise TypeError("You are trying to set a non-generator object.")

    def __str__(self):
        to_ret = "SpecialMovement <{}> with an {}".format(
            self.name, self.generator.__class__.__name__) + "\n"
        return to_ret


class WaveGen():
    ''' Base Wave Generator. It holds properties common to Regular and Irregular waves.

    Attributes:
        parent_movement: The movement in which this property is contained
        mk_bound: Particle MK (for bounds) to which this property will be applied
        wave_order: Order wave generation (def 1, [1,2])
        start: Start time (def 0)
        duration: Movement duration, 0 means until simulation end
        depth: Fluid depth (def 0)
        wave_height: Wave height (def 0.5)
        wave_period: Wave period (def 1)
    '''

    def __init__(self, parent_movement=None, wave_order=1, start=0, duration=0, depth=0, wave_height=0.5,
                 wave_period=1):
        super(WaveGen, self).__init__()
        self.parent_movement = parent_movement
        self.type = "Base Wave Generator"
        self.wave_order = wave_order
        self.start = start
        self.duration = duration
        self.depth = depth
        self.wave_height = wave_height
        self.wave_period = wave_period


class RegularPistonWaveGen(WaveGen):
    ''' Piston Regular Wave Generator.

    Attributes:
        phase: Initial wave phase in function of PI
        ramp: Periods of ramp
        disksave_periods:
        disksave_periodsteps:
        disksave_xpos:
        disksave_zpos:
        piston_dir: Movement direction (def [1,0,0])
        awas: AWAS object
    '''

    def __init__(self, parent_movement=None, wave_order=2, start=0, duration=0,
                 depth=0, wave_height=0.5, wave_period=1, phase=0, ramp=0,
                 disksave_periods=24, disksave_periodsteps=20, disksave_xpos=2,
                 disksave_zpos=-0.15, piston_dir=None, awas=None):
        super(RegularPistonWaveGen, self).__init__(parent_movement, wave_order, start,
                                                   duration, depth, wave_height, wave_period)
        self.type = "Regular Piston Wave Generator"
        self.phase = phase
        self.ramp = ramp
        self.disksave_periods = disksave_periods
        self.disksave_periodsteps = disksave_periodsteps
        self.disksave_xpos = disksave_xpos
        self.disksave_zpos = disksave_zpos
        self.piston_dir = [1, 0, 0] if piston_dir is None else piston_dir
        self.awas = AWAS() if awas is None else awas


class AWAS():
    ''' AWAS configuration.

    Attributes:
        startawas: Time to start AWAS correction
        swl: "Still water level (free-surface water)
        elevation: Order wave to calculate elevation 1:1st order, 2:2nd order
        gaugex: Position in X from piston to measure free-surface water
        gaugey: Position in Y to measure free-surface water
        gaugezmin: Minimum position in Z to measure free-surface water, it must be in water
        gaugezmax: Maximum position in Z to measure free-surface water (def=domain limits)
        gaugedp: Resolution to measure free-surface water, it uses Dp*gaugedp
        coefmasslimit: Coefficient to calculate mass of free-surface
        savedata: Saves CSV with information
        limitace: Factor to limit maximum value of acceleration, with 0 disabled
        correction: Drift correction configuration
    '''

    def __init__(self, enabled=False, startawas=0, swl=0, elevation=AWASWaveOrder.SECOND_ORDER,
                 gaugex=0, gaugey=0, gaugezmin=0, gaugezmax=0, gaugedp=0, coefmasslimit=0,
                 savedata=AWASSaveMethod.BY_PART, limitace=0, correction=None):
        self.enabled = enabled
        self.startawas = startawas
        self.swl = swl
        self.elevation = elevation
        self.gaugex = gaugex
        self.gaugey = gaugey
        self.gaugezmin = gaugezmin
        self.gaugezmax = gaugezmax
        self.gaugedp = gaugedp
        self.coefmasslimit = coefmasslimit
        self.savedata = savedata
        self.limitace = limitace
        self.correction = correction if correction is not None else AWASCorrection()


class AWASCorrection():
    ''' AWAS drift correction property '''

    def __init__(self, enabled=False, coefstroke=1.8, coefperiod=1, powerfunc=3):
        self.enabled = enabled
        self.coefstroke = coefstroke
        self.coefperiod = coefperiod
        self.powerfunc = powerfunc


class IrregularPistonWaveGen(WaveGen):
    ''' Piston Regular Wave Generator.

    Attributes:
        spectrum: Spectrum type selected for the generation
        discretization: Type of discretization for the spectrum
        peak_coef: Peak enhancement coefficient
        waves: Number of waves to create irregular waves
        randomseed: Random seed to initialize RNG
        serieini: Initial time in irregular wave serie
        ramptime: Time of ramp
        piston_dir: Movement direction (def [1,0,0])
    '''

    def __init__(self, parent_movement=None, wave_order=1, start=0, duration=0, depth=0, wave_height=0.5,
                 wave_period=1, spectrum=IrregularSpectrum.JONSWAP,
                 discretization=IrregularDiscretization.STRETCHED,
                 peak_coef=0.1, waves=50, randomseed=randint(0, 9999), serieini=0, ramptime=0,
                 serieini_autofit=True, savemotion_time=30, savemotion_timedt=0.05, savemotion_xpos=2,
                 savemotion_zpos=-0.15, saveserie_timemin=0, saveserie_timemax=1300, saveserie_timedt=0.05,
                 saveserie_xpos=0, saveseriewaves_timemin=0, saveseriewaves_timemax=1000, saveseriewaves_xpos=2,
                 piston_dir=None, awas=None):
        super(IrregularPistonWaveGen, self).__init__(parent_movement, wave_order, start,
                                                     duration, depth, wave_height, wave_period)
        self.type = "Irregular Piston Wave Generator"
        self.spectrum = spectrum
        self.discretization = discretization
        self.peak_coef = peak_coef
        self.waves = waves
        self.randomseed = randomseed
        self.serieini = serieini
        self.serieini_autofit = serieini_autofit
        self.ramptime = ramptime
        self.savemotion_time = savemotion_time
        self.savemotion_timedt = savemotion_timedt
        self.savemotion_xpos = savemotion_xpos
        self.savemotion_zpos = savemotion_zpos
        self.saveserie_timemin = saveserie_timemin
        self.saveserie_timemax = saveserie_timemax
        self.saveserie_timedt = saveserie_timedt
        self.saveserie_xpos = saveserie_xpos
        self.saveseriewaves_timemin = saveseriewaves_timemin
        self.saveseriewaves_timemax = saveseriewaves_timemax
        self.saveseriewaves_xpos = saveseriewaves_xpos
        self.piston_dir = [1, 0, 0] if piston_dir is None else piston_dir
        self.awas = AWAS() if awas is None else awas


class RegularFlapWaveGen(WaveGen):
    ''' Flap Regular Wave Generator.

    Attributes:
        phase: Initial wave phase in function of PI
        ramp: Periods of ramp
        variable_draft: Position of the wavemaker hinge
        flapaxis0: Point 0 of axis rotation
        flapaxis1: Point 1 of axis rotation
    '''

    def __init__(self, parent_movement=None, wave_order=2, start=0, duration=0, depth=0, wave_height=0.5,
                 wave_period=1, phase=0, ramp=0, disksave_periods=24,
                 disksave_periodsteps=20, disksave_xpos=2, disksave_zpos=-0.15, variable_draft=0.0, flapaxis0=None,
                 flapaxis1=None):
        super(RegularFlapWaveGen, self).__init__(parent_movement, wave_order,
                                                 start, duration, depth, wave_height, wave_period)
        self.type = "Regular Flap Wave Generator"
        self.phase = phase
        self.ramp = ramp
        self.variable_draft = variable_draft
        self.flapaxis0 = [0, -1, 0] if flapaxis0 is None else flapaxis0
        self.flapaxis1 = [0, 1, 0] if flapaxis1 is None else flapaxis1
        self.disksave_periods = disksave_periods
        self.disksave_periodsteps = disksave_periodsteps
        self.disksave_xpos = disksave_xpos
        self.disksave_zpos = disksave_zpos


class IrregularFlapWaveGen(WaveGen):
    ''' Flap Irregular Wave Generator.

    Attributes:
        spectrum: Spectrum type selected for the generation
        discretization: Type of discretization for the spectrum
        peak_coef: Peak enhancement coefficient
        waves: Number of waves to create irregular waves
        randomseed: Random seed to initialize RNG
        serieini: Initial time in irregular wave serie
        ramptime: Time of ramp
        variable_draft: Position of the wavemaker hinge
        flapaxis0: Point 0 of axis rotation
        flapaxis1: Point 1 of axis rotation
    '''

    def __init__(self, parent_movement=None, wave_order=1, start=0, duration=0, depth=0, wave_height=0.5,
                 wave_period=1, spectrum=IrregularSpectrum.JONSWAP,
                 discretization=IrregularDiscretization.STRETCHED,
                 peak_coef=0.1, waves=50, randomseed=randint(0, 9999), serieini=0, ramptime=0,
                 serieini_autofit=True, savemotion_time=30, savemotion_timedt=0.05, savemotion_xpos=2,
                 savemotion_zpos=-0.15, saveserie_timemin=0, saveserie_timemax=1300, saveserie_timedt=0.05,
                 saveserie_xpos=0, saveseriewaves_timemin=0, saveseriewaves_timemax=1000, saveseriewaves_xpos=2,
                 variable_draft=0.0, flapaxis0=None, flapaxis1=None):
        super(IrregularFlapWaveGen, self).__init__(parent_movement, wave_order, start,
                                                   duration, depth, wave_height, wave_period)
        self.type = "Irregular Flap Wave Generator"
        self.spectrum = spectrum
        self.discretization = discretization
        self.peak_coef = peak_coef
        self.waves = waves
        self.randomseed = randomseed
        self.serieini = serieini
        self.serieini_autofit = serieini_autofit
        self.ramptime = ramptime
        self.savemotion_time = savemotion_time
        self.savemotion_timedt = savemotion_timedt
        self.savemotion_xpos = savemotion_xpos
        self.savemotion_zpos = savemotion_zpos
        self.saveserie_timemin = saveserie_timemin
        self.saveserie_timemax = saveserie_timemax
        self.saveserie_timedt = saveserie_timedt
        self.saveserie_xpos = saveserie_xpos
        self.saveseriewaves_timemin = saveseriewaves_timemin
        self.saveseriewaves_timemax = saveseriewaves_timemax
        self.saveseriewaves_xpos = saveseriewaves_xpos
        self.variable_draft = variable_draft
        self.flapaxis0 = [0, -1, 0] if flapaxis0 is None else flapaxis0
        self.flapaxis1 = [0, 1, 0] if flapaxis1 is None else flapaxis1


class FileGen(WaveGen):
    ''' File Generator. Loads movements from file

    Attributes:
        duration: Duration in seconds
        filename: File path to use
        fields: Number of columns of the file
        fieldtime: Column with time
        fieldx: Column with X-position
        fieldy: Column with Y-position
        fieldz: Column with Z-position
    '''

    def __init__(self, parent_movement=None, duration=0, filename="", fields=0, fieldtime=0, fieldx=0, fieldy=0,
                 fieldz=0):
        super(FileGen, self).__init__(parent_movement)
        self.duration = duration
        self.name = "File Wave Generator"
        self.filename = filename
        self.fields = fields
        self.fieldtime = fieldtime
        self.fieldx = fieldx
        self.fieldy = fieldy
        self.fieldz = fieldz


class RotationFileGen(WaveGen):
    ''' Rotation File Generator. Loads rotation movements from file

    Attributes:
        duration: Duration in seconds
        anglesunits: Units of the file (degrees, radians)
        filename: File path to use
        axisp1: Point 1 of the axis
        axisp2: Point 2 of the axis
    '''

    def __init__(self, parent_movement=None, duration=0, filename="", anglesunits="degrees", axisp1=None, axisp2=None):
        super(RotationFileGen, self).__init__(parent_movement)
        if axisp1 is None:
            axisp1 = [0, 0, 0]
        if axisp2 is None:
            axisp2 = [0, 0, 0]
        self.duration = duration
        self.name = "File Wave Generator"
        self.anglesunits = anglesunits
        self.filename = filename
        self.axisp1 = axisp1
        self.axisp2 = axisp2


class BaseMotion():
    ''' Base motion class to inherit by others.

        Attributes:
            duration: Movement duration in seconds
        '''

    def __init__(self, duration=1, parent_movement=None):
        self.duration = duration
        self.type = "Base Motion"
        self.parent_movement = parent_movement

    def __str__(self):
        return "BaseMotion [Duration: {}]".format(self.duration)


class RectMotion(BaseMotion):
    ''' DualSPHysics rectilinear motion.

        Attributes:
            velocity: Velocity vector that defines the movement
        '''

    def __init__(self, duration=1, velocity=None, parent_movement=None):
        if velocity is None:
            velocity = [0, 0, 0]
        BaseMotion.__init__(self, duration)
        self.parent_movement = parent_movement
        self.type = "Rectilinear Motion"
        self.velocity = velocity

    def __str__(self):
        return "RectMotion [Duration: {} ; Velocity: {}]".format(self.duration, self.velocity)


class AccRectMotion(BaseMotion):
    ''' DualSPHysics accelerated rectilinear motion.

        Attributes:
            velocity: Velocity vector that defines the movement
            acceleration: Acceleration vector that defines the aceleration
        '''

    def __init__(self, duration=1, velocity=None, acceleration=None, parent_movement=None):
        if velocity is None:
            velocity = [0, 0, 0]
        if acceleration is None:
            acceleration = [0, 0, 0]
        BaseMotion.__init__(self, duration)
        self.type = "Accelerated Rectilinear motion"
        self.parent_movement = parent_movement
        self.velocity = velocity
        self.acceleration = acceleration

    def __str__(self):
        return "AccRectMotion [Duration: {} ; Velocity: {} ; Acceleration: {}]" \
            .format(self.duration, self.velocity, self.acceleration)


class RotMotion(BaseMotion):
    ''' DualSPHysics rotational motion.

        Attributes:
            ang_vel: Angular velocity of the movement
            axis1: Starting point of the vector that defines the rotation axis
            axis2: Finishing point of the vector that defines the rotation axis
        '''

    def __init__(self, duration=1, ang_vel=None, axis1=None, axis2=None, parent_movement=None):
        if axis1 is None:
            axis1 = [0, 0, 0]
        if axis2 is None:
            axis2 = [0, 0, 0]
        if ang_vel is None:
            ang_vel = 0
        BaseMotion.__init__(self, duration)
        self.type = "Rotational Motion"
        self.parent_movement = parent_movement
        self.axis1 = axis1
        self.axis2 = axis2
        self.ang_vel = ang_vel

    def __str__(self):
        return "RotMotion [Duration: {} ; AngVelocity: {} ; Axis: [{}, {}]]" \
            .format(self.duration, self.ang_vel, self.axis1, self.axis2)


class AccRotMotion(BaseMotion):
    ''' DualSPHysics rotational motion.

        Attributes:
            ang_vel: Angular velocity of the movement
            ang_acc: Angular acceleration of the movement
            axis1: Starting point of the vector that defines the rotation axis
            axis2: Finishing point of the vector that defines the rotation axis
        '''

    def __init__(self, duration=1, ang_vel=None, ang_acc=None, axis1=None, axis2=None, parent_movement=None):
        if axis1 is None:
            axis1 = [0, 0, 0]
        if axis2 is None:
            axis2 = [0, 0, 0]
        if ang_vel is None:
            ang_vel = 0
        if ang_acc is None:
            ang_acc = 0
        BaseMotion.__init__(self, duration)
        self.type = "Accelerated Rotational Motion"
        self.parent_movement = parent_movement
        self.axis1 = axis1
        self.axis2 = axis2
        self.ang_vel = ang_vel
        self.ang_acc = ang_acc

    def __str__(self):
        return "AccRotMotion [Duration: {} ; AngVelocity: {} ; AngAccel: {} ; Axis: [{}, {}]]" \
            .format(self.duration, self.ang_vel, self.ang_acc, self.axis1, self.axis2)


class AccCirMotion(BaseMotion):
    ''' DualSPHysics circular motion.

        Attributes:
            ang_vel: Angular velocity of the movement
            ang_acc: Angular acceleration of the movement
            reference: Point of the object that rotates with the axis
            axis1: Starting point of the vector that defines the rotation axis
            axis2: Finishing point of the vector that defines the rotation axis
        '''

    def __init__(self, duration=1, ang_vel=None, ang_acc=None, reference=None, axis1=None, axis2=None,
                 parent_movement=None):
        if axis1 is None:
            axis1 = [0, 0, 0]
        if axis2 is None:
            axis2 = [0, 0, 0]
        if ang_vel is None:
            ang_vel = 0
        if ang_acc is None:
            ang_acc = 0
        if reference is None:
            reference = [0, 0, 0]
        BaseMotion.__init__(self, duration)
        self.type = "Circular Motion"
        self.parent_movement = parent_movement
        self.reference = reference
        self.axis1 = axis1
        self.axis2 = axis2
        self.ang_vel = ang_vel
        self.ang_acc = ang_acc

    def __str__(self):
        return "AccCirMotion [Duration: {} ; AngVelocity: {} ; AngAccel: {} ; Reference: {} ; Axis: [{}, {}]]".format(
            self.duration,
            self.ang_vel,
            self.ang_acc,
            self.reference,
            self.axis1,
            self.axis2)


class WaitMotion(BaseMotion):
    ''' DualSPHysics rectilinear motion.

        Attributes inherited from superclass.
        '''

    def __init__(self, duration=1, parent_movement=None):
        BaseMotion.__init__(self, duration)
        self.parent_movement = parent_movement
        self.type = "Wait Interval"

    def __str__(self):
        return "WaitMotion [Duration: {}]".format(self.duration)


class RotSinuMotion(BaseMotion):
    ''' DualSPHysics sinusoidal rotational motion.

        Attributes:
            axis1: Starting point of the vector that defines the rotation axis
            axis2: Finishing point of the vector that defines the rotation axis
            freq: Frequency
            ampl: Amplitude
            phase: Phase
        '''

    def __init__(self, duration=1, axis1=None, axis2=None, freq=None, ampl=None, phase=None, parent_movement=None):
        if axis1 is None:
            axis1 = [0, 0, 0]
        if axis2 is None:
            axis2 = [0, 0, 0]
        if freq is None:
            freq = 0
        if ampl is None:
            ampl = 0
        if phase is None:
            phase = 0
        BaseMotion.__init__(self, duration)
        self.type = "Sinusoidal Rotational Motion"
        self.parent_movement = parent_movement
        self.axis1 = axis1
        self.axis2 = axis2
        self.freq = freq
        self.ampl = ampl
        self.phase = phase

    def __str__(self):
        return "RotSinuMotion [Duration: {} ; Frequency: {} ; Amplitude: {} ; Phase: {} ; Axis: [{}, {}]]".format(
            self.duration,
            self.freq,
            self.ampl,
            self.phase,
            self.axis1,
            self.axis2)


class CirSinuMotion(BaseMotion):
    ''' DualSPHysics sinusoidal circular motion.

        Attributes:
            reference: Point of the object that rotates with the axis
            axis1: Starting point of the vector that defines the rotation axis
            axis2: Finishing point of the vector that defines the rotation axis
            freq: Frequency
            ampl: Amplitude
            phase: Phase
        '''

    def __init__(self, reference=None, duration=1, axis1=None, axis2=None, freq=None, ampl=None, phase=None,
                 parent_movement=None):
        if reference is None:
            reference = [0, 0, 0]
        if axis1 is None:
            axis1 = [0, 0, 0]
        if axis2 is None:
            axis2 = [0, 0, 0]
        if freq is None:
            freq = 0
        if ampl is None:
            ampl = 0
        if phase is None:
            phase = 0
        BaseMotion.__init__(self, duration)
        self.type = "Sinusoidal Circular Motion"
        self.parent_movement = parent_movement
        self.reference = reference
        self.axis1 = axis1
        self.axis2 = axis2
        self.freq = freq
        self.ampl = ampl
        self.phase = phase

    def __str__(self):
        return "CirSinuMotion [Duration: {} ; Frequency: {} ; Amplitude: {} ; " "Phase: {} ; Reference: {} ; Axis: [{}, {}]]".format(
            self.duration,
            self.freq,
            self.ampl,
            self.phase,
            self.reference,
            self.axis1,
            self.axis2)


class RectSinuMotion(BaseMotion):
    ''' DualSPHysics sinusoidal rectilinear motion.

        Attributes:
            freq: Frequency (vector)
            ampl: Amplitude (vector)
            phase: Phase (vector)
        '''

    def __init__(self, duration=1, freq=None, ampl=None, phase=None, parent_movement=None):
        if freq is None:
            freq = [0, 0, 0]
        if ampl is None:
            ampl = [0, 0, 0]
        if phase is None:
            phase = [0, 0, 0]
        BaseMotion.__init__(self, duration)
        self.type = "Sinusoidal Rectilinear Motion"
        self.parent_movement = parent_movement
        self.freq = freq
        self.ampl = ampl
        self.phase = phase

    def __str__(self):
        return "RectSinuMotion [Duration: {} ; Frequency: {} ; Amplitude: {} ; Phase: {}".format(
            self.duration,
            self.freq,
            self.ampl,
            self.phase)


class Damping():
    ''' DualSPHysics damping settings '''

    def __init__(self, enabled=True, overlimit=1, redumax=10):
        self.enabled = enabled
        self.overlimit = overlimit
        self.redumax = redumax

    def __str__(self):
        to_ret = ""
        to_ret += "Damping configuration structure ({})\n".format(
            "enabled" if self.enabled else "disabled")
        to_ret += "Overlimit: {}\n".format(self.overlimit)
        to_ret += "Redumax: {}".format(self.redumax)
        return to_ret


class MLPiston():
    ''' Multi-Layer Piston common attributes '''

    def __init__(self, incz=0):
        self.incz = incz


class MLPiston1D(MLPiston):
    ''' Multi-Layer Pistons using external velocity (for example, from SWASH) '''

    def __init__(self, filevelx=None, incz=0, timedataini=0, smooth=0):
        super().__init__(incz=incz)
        self.filevelx = filevelx
        self.timedataini = timedataini
        self.smooth = smooth


class MLPiston2DVeldata():
    ''' VelData attribute for MLPiston2D '''

    def __init__(self, filevelx="", posy=0, timedataini=0):
        self.filevelx = filevelx
        self.posy = posy
        self.timedataini = timedataini


class MLPiston2D(MLPiston):
    ''' Multi-Layer Pistons using external velocity (for example, from SWASH) '''

    def __init__(self, incz=0, smoothz=0, smoothy=0, veldata=None):
        super().__init__(incz=incz)
        self.smoothz = smoothz
        self.smoothy = smoothy
        self.veldata = veldata or []  # [MLPiston2DVeldata]


class RelaxationZone():
    ''' Base class for Relaxation Zone objects '''

    def __init__(self):
        pass


class RelaxationZoneRegular(RelaxationZone):
    ''' Relaxation zone for regular wave generation '''

    def __init__(self, start=0, duration=0, waveorder=1, waveheight=1, waveperiod=2, depth=1, swl=1, center=None,
                 width=0.5, phase=0, ramp=0,
                 savemotion_periods=24, savemotion_periodsteps=20, savemotion_xpos=0, savemotion_zpos=0,
                 coefdir=None, coefdt=1000, function_psi=0.9, function_beta=1, driftcorrection=0):
        super().__init__()
        self.start = start
        self.duration = duration
        self.waveorder = waveorder
        self.waveheight = waveheight
        self.waveperiod = waveperiod
        self.depth = depth
        self.swl = swl
        self.center = [0, 0, 0] if center is None else center
        self.width = width
        self.phase = phase
        self.ramp = ramp
        self.savemotion_periods = savemotion_periods
        self.savemotion_periodsteps = savemotion_periodsteps
        self.savemotion_xpos = savemotion_xpos
        self.savemotion_zpos = savemotion_zpos
        self.coefdir = [1, 0, 0] if coefdir is None else coefdir
        self.coefdt = coefdt
        self.function_psi = function_psi
        self.function_beta = function_beta
        self.driftcorrection = driftcorrection


class RelaxationZoneIrregular(RelaxationZone):
    ''' Relaxation zone for irregular wave generation '''

    def __init__(self, start=0, duration=0, peakcoef=3.3, spectrum=IrregularSpectrum.JONSWAP,
                 discretization=IrregularDiscretization.REGULAR, waveorder=1, waveheight=1,
                 waveperiod=2, waves=50, randomseed=randint(0, 9999), depth=1, swl=1, center=None,
                 width=0.5, ramptime=0, serieini=0,
                 savemotion_time=50, savemotion_timedt=0.1, savemotion_xpos=0, savemotion_zpos=0,
                 saveserie_timemin=0, saveserie_timemax=100, saveserie_timedt=0.1, saveserie_xpos=0,
                 saveseriewaves_timemin=0, saveseriewaves_timemax=1000, saveseriewaves_xpos=0,
                 coefdir=None, coefdt=1000, function_psi=0.9, function_beta=1, driftcorrection=0):
        super().__init__()
        self.start = start
        self.duration = duration
        self.peakcoef = peakcoef
        self.spectrum = spectrum
        self.discretization = discretization
        self.waveorder = waveorder
        self.waveheight = waveheight
        self.waveperiod = waveperiod
        self.waves = waves
        self.randomseed = randomseed
        self.depth = depth
        self.swl = swl
        self.center = [0, 0, 0] if center is None else center
        self.width = width
        self.ramptime = ramptime
        self.serieini = serieini
        self.savemotion_time = savemotion_time
        self.savemotion_timedt = savemotion_timedt
        self.savemotion_xpos = savemotion_xpos
        self.savemotion_zpos = savemotion_zpos
        self.saveserie_timemin = saveserie_timemin
        self.saveserie_timemax = saveserie_timemax
        self.saveserie_timedt = saveserie_timedt
        self.saveserie_xpos = saveserie_xpos
        self.saveseriewaves_timemin = saveseriewaves_timemin
        self.saveseriewaves_timemax = saveseriewaves_timemax
        self.saveseriewaves_xpos = saveseriewaves_xpos
        self.coefdir = [1, 0, 0] if coefdir is None else coefdir
        self.coefdt = coefdt
        self.function_psi = function_psi
        self.function_beta = function_beta
        self.driftcorrection = driftcorrection


class RelaxationZoneFile(RelaxationZone):
    ''' Relaxation zone with external file wave definition '''

    def __init__(self, start=0, duration=0, depth=1, swl=1, filesvel="", filesvelx_initial=0,
                 filesvelx_count=5, usevelz=False, movedata=None, dpz=2, smooth=0, center=None, width=0.5,
                 coefdir=None, coefdt=1000, function_psi=0.9, function_beta=1, driftcorrection=0,
                 driftinitialramp=0):
        super().__init__()
        self.driftinitialramp = driftinitialramp
        self.smooth = smooth
        self.dpz = dpz
        self.movedata = [0, 0, 0] if movedata is None else movedata
        self.usevelz = usevelz
        self.filesvelx_count = filesvelx_count
        self.filesvelx_initial = filesvelx_initial
        self.filesvel = filesvel
        self.start = start
        self.duration = duration
        self.depth = depth
        self.swl = swl
        self.center = [0, 0, 0] if center is None else center
        self.width = width
        self.coefdir = [1, 0, 0] if coefdir is None else coefdir
        self.coefdt = coefdt
        self.function_psi = function_psi
        self.function_beta = function_beta
        self.driftcorrection = driftcorrection


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


class AccelerationInput():
    ''' Acceleration Input control structure. Includes enabling/disabling and a list
    of AccelerationInputData objects'''

    def __init__(self, enabled=False, acclist=None):
        self.enabled = enabled
        self.acclist = acclist or []

    def set_list(self, acclist):
        ''' Sets the acceleration input list. '''
        self.acclist = acclist

    def set_enabled(self, state):
        ''' Enables/Disables acceleration input. '''
        self.enabled = state


class AccelerationInputData():
    ''' Acceleration Input Data '''

    def __init__(self, label="Acceleration Input", mkfluid=0, acccentre=None, globalgravity=True, datafile=""):
        self.label = label
        self.mkfluid = mkfluid
        self.acccentre = acccentre or [0, 0, 0]
        self.globalgravity = globalgravity
        self.datafile = datafile


class DomainFixedParameter():
    ''' Fixed Domain for a DSPH case.

    Attributes:
        xmin = Minimun X coordinate for the fixed domain
        xmax = Maximum X coordinate for the fixed domain
        ymin = Minimun Y coordinate for the fixed domain
        ymax = Maximum Y coordinate for the fixed domain
        zmin = Minimun Z coordinate for the fixed domain
        zmax = Maximum Z coordinate for the fixed domain
    '''

    def __init__(self, enabled, xmin, xmax, ymin, ymax, zmin, zmax):
        self.enabled = enabled
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def __str__(self):
        to_ret = '''
            Enabled: {}\n
            Xmin & Xmax: {} ; {}\n
            Ymin & Ymax: {} ; {}\n
            Zmin & Zmax: {} ; {}\n
            '''
        return to_ret.format(self.enabled, self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax)


class Constants():
    ''' Case constants '''

    def __init__(self):
        self.lattice_bound: int = 1
        self.lattice_fluid: int = 1
        self.gravity: list = [0, 0, -9.81]
        self.rhop0: float = 1000
        self.hswl: float = 0
        self.hswl_auto: bool = True
        self.gamma: float = 7
        self.speedsystem: float = 0
        self.speedsystem_auto: bool = True
        self.coefsound: float = 20
        self.speedsound: float = 0
        self.speedsound_auto: bool = True
        self.coefh: float = 1
        self.cflnumber: float = 0.2
        self.h: float = 0
        self.h_auto: bool = True
        self.b: float = 0
        self.b_auto: bool = True
        self.massbound: float = 0
        self.massbound_auto: bool = True
        self.massfluid: float = 0
        self.massfluid_auto: bool = True


class ExecutionParameters():
    ''' Execution parameters for the case '''

    def __init__(self):
        self.posdouble: int = 0
        self.stepalgorithm: int = 1
        self.verletsteps: int = 40
        self.kernel: int = 2
        self.viscotreatment: int = 1
        self.visco: float = 0.01
        self.viscoboundfactor: int = 1
        self.deltasph: int = 0
        self.deltasph_en: int = 0
        self.shifting: int = 0
        self.shiftcoef: int = -2
        self.shifttfs: int = 0
        self.rigidalgorithm: int = 1
        self.ftpause: float = 0.0
        self.coefdtmin: float = 0.05
        self.dtini: float = 0.0001
        self.dtini_auto: bool = True
        self.dtmin: float = 0.00001
        self.dtmin_auto: bool = True
        self.dtallparticles: int = 0
        self.dtfixed: str = 'DtFixed.dat'
        self.timemax: float = 1.5
        self.timeout: float = 0.01
        self.partsoutmax: int = 1
        self.rhopoutmin: int = 700
        self.rhopoutmax: int = 1300
        self.domainfixed: DomainFixedParameter = DomainFixedParameter(False, 0, 0, 0, 0, 0, 0)


class SimulationObject():
    ''' Represents an object on a DualSPHysics / GenCase case '''

    def __init__(self, name: str, obj_mk: int, obj_type: ObjectType, fillmode: ObjectFillMode):
        self.name: str = name
        self.obj_mk: int = obj_mk
        self.type: ObjectType = obj_type
        self.fillmode: ObjectFillMode = fillmode
        self.damping: Damping = None
        self.faces_configuration: FacesProperty = None

    def clean_faces(self):
        ''' Deletes face rendering information from this object '''
        self.faces_configuration: FacesProperty = None


class PeriodicityInfo():
    ''' Defines periodicty for an axis '''

    def __init__(self, enabled=False, x_increment=0.0, y_increment=0.0, z_increment=0.0):
        self.enabled: bool = enabled
        self.x_increment: float = x_increment
        self.y_increment: float = y_increment
        self.z_increment: float = z_increment


class Periodicity():
    ''' Periodicity information for the current case '''

    def __init__(self):
        self.x_periodicity: PeriodicityInfo = PeriodicityInfo()
        self.y_periodicity: PeriodicityInfo = PeriodicityInfo()
        self.z_periodicity: PeriodicityInfo = PeriodicityInfo()


class SDPositionProperty():
    ''' Position property for Simulation Domain '''

    def __init__(self, sdptype=SDPositionPropertyType.DEFAULT, value=0.0):
        self.type: SDPositionPropertyType = sdptype
        self.value: float = value


class SimulationDomain():
    ''' Case domain data information '''

    def __init__(self):
        self.enabled: bool = False
        self.posmin_x: SDPositionProperty = SDPositionProperty()
        self.posmin_y: SDPositionProperty = SDPositionProperty()
        self.posmin_z: SDPositionProperty = SDPositionProperty()
        self.posmax_x: SDPositionProperty = SDPositionProperty()
        self.posmax_y: SDPositionProperty = SDPositionProperty()
        self.posmax_z: SDPositionProperty = SDPositionProperty()


class ExecutablePaths():
    ''' Executables used by the application '''

    def __init__(self):
        self.gencase: str = ''
        self.dsphysics: str = ''
        self.partvtk4: str = ''
        self.floatinginfo: str = ''
        self.computeforces: str = ''
        self.measuretool: str = ''
        self.isosurface: str = ''
        self.boundaryvtk: str = ''
        self.flowtool: str = ''
        self.paraview: str = ''

    def check_and_filter(self):
        ''' Filters the executable removing those not matching the correct application.
            Returns whether or not all of them were correctly set. '''
        execs_correct: bool = True
        execs_to_check = {
            "gencase": self.gencase,
            "dualsphysics": self.dsphysics,
            "partvtk4": self.partvtk4,
            "floatinginfo": self.floatinginfo,
            "computeforces": self.computeforces,
            "measuretool": self.measuretool,
            "isosurface": self.isosurface,
            "boundaryvtk": self.boundaryvtk,
            "flowtool": self.flowtool
        }

        for word, executable in execs_to_check.items():
            if not executable_contains_string(executable, word):
                execs_correct = False
                executable = ""

        return execs_correct


class CaseInformation():
    ''' Stores miscellaneous information related with the case. '''

    def __init__(self):
        self.is_gencase_done: bool = False
        self.is_simulation_done: bool = False
        self.previous_particle_number: int = 0
        self.particle_number: int = 0
        self.particles_out: int = 0
        self.exported_parts: int = 0
        self.run_additional_parameters: str = ''
        self.needs_to_run_gencase: bool = True
        self.current_process: QtCore.QProcess = None
        self.current_export_process: QtCore.QProcess = None
        self.current_info_dialog: QtGui.QDialog = None
        self.current_output: str = ""
        self.measuretool_points: list = []
        self.measuretool_grid: list = []
        self.objectlist_table: QtGui.QTableWidget = None
        self.last_3d_width: float = -1.0


class MKBasedProperties():
    ''' Stores data related with an mk number on the case. '''

    def __init__(self, mk=None):
        self.mk: int = mk
        self.movements: list = []  # [Movement]
        self.float_property: FloatProperty = None
        self.initials: InitialsProperty = None
        self.mlayerpiston: MLPiston = None

    def has_movements(self) -> bool:
        ''' Returns whether this mk contains definition for movements or not '''
        return len(self.movements) > 0

    def remove_all_movements(self) -> None:
        ''' Removes all movements for the current mk properties '''
        self.movements: list = []


class Case():
    ''' Main data structure for the data inside a case properties, objects
    etcetera. Used as a way to store information and transform it for
    multiple needs '''
    __instance: 'Case' = None
    SUPPORTED_TYPES = ["Part::Box", "Part::Sphere", "Part::Cylinder"]

    def __init__(self, reset=False):
        ''' Virtually private constructor. '''
        if Case.__instance is not None and not reset:
            raise Exception(
                'Case class is a singleton and should not be initialized twice')
        Case.__instance = self
        self.version: str = VERSION
        self.name: str = ''
        self.path: str = ''
        self.dp: float = 0.01
        self.mode3d: bool = True
        self.constants: Constants = Constants()
        self.execution_parameters: ExecutionParameters = ExecutionParameters()
        self.objects: list = list()  # [SimulationObject]
        self.mkbasedproperties: dict = dict()  # {mk: MKBasedProperties}
        self.periodicity: Periodicity = Periodicity()
        self.domain: SimulationDomain = SimulationDomain()
        self.executable_paths: ExecutablePaths = ExecutablePaths()
        self.info: CaseInformation = CaseInformation()
        self.acceleration_input: AccelerationInput = AccelerationInput()
        self.relaxation_zone: RelaxationZone = None

    @staticmethod
    def instance() -> 'Case':
        ''' Static access method. '''
        if Case.__instance is None:
            Case()
        return Case.__instance

    def get_first_mk_not_used(self, object_type: ObjectType):
        ''' Checks simulation objects to find the first not used MK group number. '''
        mkset = set(map(lambda x: x.obj_mk, filter(lambda y: y.type == object_type, self.objects)))
        limit = {ObjectType.FLUID: 10, ObjectType.BOUND: 240}[object_type]
        for i in range(0, limit):
            if i not in mkset:
                return i
        return 0

    def get_all_simulation_object_names(self):
        ''' Returns a list with all the internal names used by the objects in the simulation. '''
        return list(map(lambda obj: obj.name, self.objects))

    def get_simulation_object(self, name) -> SimulationObject:
        ''' Returns a simulation object from its internal name.
        Raises an exception if the selected object is not added to the simulation. '''
        return next(filter(lambda obj: obj.name == name, self.objects), None)

    def number_of_objects_in_simulation(self):
        ''' Return the total number of objects in the simulation '''
        return len(list(filter(lambda obj: obj.type != ObjectType.SPECIAL, self.objects)))

    def get_mk_base_properties(self, mknumber: int) -> MKBasedProperties:
        ''' Returns the properties set for a given MK number '''
        if mknumber not in self.mkbasedproperties.keys():
            raise RuntimeError('MK has no properties applied! This should not happen.')
        return self.mkbasedproperties[mknumber]

    def has_mk_properties(self, mk) -> bool:
        ''' Returns whether a given mk has properties applier or not. '''
        return mk in self.mkbasedproperties.keys()

    def is_object_in_simulation(self, name) -> bool:
        ''' Returns whether an object is contained in the current case for simulating or not. '''
        return name in self.get_all_simulation_object_names()

    def reset(self):
        ''' Recreates the object from scratch. '''
        self.__init__(reset=True)

    def add_object(self, simobject: SimulationObject):
        ''' Adds an object to the current case '''
        if simobject.name in self.get_all_simulation_object_names():
            raise RuntimeError('Object with the name: {} is already added to the case'.format(simobject.name))
        self.objects.append(simobject)
        if not self.has_mk_properties(simobject.obj_mk):
            self.mkbasedproperties[simobject.obj_mk] = MKBasedProperties(mk=simobject.obj_mk)

    def remove_object(self, object_name: str) -> SimulationObject:
        ''' Tries to remove the given object name from the simulation.
        If no element is found an error is raised. '''
        if object_name not in self.get_all_simulation_object_names():
            raise RuntimeError('The object that you are trying to remove ({}) is not present in the simulation')
        self.objects = list(filter(lambda obj: obj.name != object_name, self.objects))

    def get_all_objects_with_damping(self):
        ''' Returns a list of SimulationObject that have damping '''
        return list(filter(lambda obj: obj.damping is not None, self.objects))

    def was_not_saved(self) -> bool:
        ''' Returns whether this case was or not saved before '''
        return self.path == '' and self.name == ''

    def reset_simulation_domain(self) -> None:
        ''' Restores the Simulation Domain to the default one. '''
        self.domain = SimulationDomain()

#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Properties.

This file contains a collection of Properties to add
in a DSPH related case.

"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
from dsphfc.propenums import *


# Copyright (C) 2016 - Andrés Vieira (anvieiravazquez@gmail.com)
# EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo
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


class FloatProperty(object):
    """ Float property of an DSPH object.

    Attributes:
        mk: Mk to witch this FloatProperty is binded.
        mass_density_type: Density type 0 is massbody; 1 is rhopbody.
        mass_density_value: Value for mass/density
        gravity_center: Coords in [x, y, z] format. Blank list() for auto.
        inertia: Coords in [x, y, z] format. Blank list() for auto.
        initial_linear_velocity: Coords in [x, y, z] format. Blank list() for auto.
        initial_angular_velocity: Coords in [x, y, z] format. Blank list() for auto.
    """

    def __init__(self, mk=-1, mass_density_type=0, mass_density_value=100,
                 gravity_center=list(), inertia=list(), initial_linear_velocity=list(),
                 initial_angular_velocity=list()):
        self.mk = mk
        self.mass_density_type = mass_density_type
        self.mass_density_value = mass_density_value
        self.gravity_center = gravity_center
        self.inertia = inertia
        self.initial_linear_velocity = initial_linear_velocity
        self.initial_angular_velocity = initial_angular_velocity


class InitialsProperty(object):
    """ Initial movement property of an DSPH object.

    Attributes:
        mk: Mk to witch this InitialsProperty is binded.
        force: Force in [x, y, z] format.
    """

    def __init__(self, mk=-1, force=list()):
        self.mk = mk
        self.force = force


class Material(object):
    """ DualSPHysics compatible material.

    Attributes:
        bound_mk: List of mk groups this material is binded
    """

    def __init__(self, mk=list()):
        self.bound_mk = mk


class Movement(object):
    """ DualSPHysics compatible movement.
        It includes a list of different motions to represent an entire simulation
        movement.

        Attributes:
            name: Name for this motion given by the user
            motion_list: List of motion objects in order
            loop: Boolean indicating if it is a loop
        """

    def __init__(self, name="New Movement", motion_list=None, loop=False):
        self.name = name
        self.type = "Movement"
        if not motion_list:
            motion_list = list()
        self.motion_list = motion_list
        self.loop = loop

    def add_motion(self, motion):
        """ Adds a motion to the movement """
        if isinstance(motion, BaseMotion):
            motion.parent_movement = self
            self.motion_list.append(motion)
        else:
            raise TypeError(
                "You are trying to append a non-motion object to a movement list.")

    def set_loop(self, state):
        """ Set loop state for the movement """
        if isinstance(state, bool):
            self.loop = state
        else:
            raise TypeError("Tried to set a boolean with an {}".format(
                state.__class__.__name__))

    def remove_motion(self, position):
        """ Removes a motion from the list """
        self.motion_list.pop(position)

    def __str__(self):
        to_ret = "Movement <{}>".format(self.name) + "\n"
        to_ret += "Motion List:\n"
        for motion in self.motion_list:
            to_ret += str(motion) + "\n"
        return to_ret


class SpecialMovement(object):
    """ DualSPHysics compatible special movement.
        It includes regular/irregular wave generators and file movements

        Attributes:
            name: Name for this motion given by the user
            generator: Generator assigned
        """

    def __init__(self, name="New Movement", generator=None):
        self.name = name
        self.type = "Wave Movement"
        if not generator:
            generator = None
        self.generator = generator

    def set_wavegen(self, generator):
        """ Sets the wave generator for the special movement """
        if isinstance(generator, WaveGen):
            generator.parent_movement = self
            self.generator = generator
        else:
            raise TypeError("You are trying to set a non-generator object.")

    def __str__(self):
        to_ret = "SpecialMovement <{}> with an {}".format(
            self.name, self.generator.__class__.__name__) + "\n"
        return to_ret


class WaveGen(object):
    """ Base Wave Generator. It holds properties common to Regular and Irregular waves.

    Attributes:
        parent_movement: The movement in which this property is contained
        mk_bound: Particle MK (for bounds) to which this property will be applied
        wave_order: Order wave generation (def 1, [1,2])
        start: Start time (def 0)
        duration: Movement duration, 0 means until simulation end
        depth: Fluid depth (def 0)
        fixed_depth: Fluid depth without paddle (def 0)
        wave_height: Wave height (def 0.5)
        wave_period: Wave period (def 1)
    """

    def __init__(self, parent_movement=None, wave_order=1, start=0, duration=0, depth=0, fixed_depth=0, wave_height=0.5, wave_period=1):
        super(WaveGen, self).__init__()
        self.parent_movement = parent_movement
        self.type = "Base Wave Generator"
        self.wave_order = wave_order
        self.start = start
        self.duration = duration
        self.depth = depth
        self.fixed_depth = fixed_depth
        self.wave_height = wave_height
        self.wave_period = wave_period


class RegularPistonWaveGen(WaveGen):
    """ Piston Regular Wave Generator.

    Attributes:
        phase: Initial wave phase in function of PI
        ramp: Periods of ramp
        disksave_periods:
        disksave_periodsteps:
        disksave_xpos:
        disksave_zpos:
        piston_dir: Movement direction (def [1,0,0])
        awas: AWAS object
    """

    def __init__(self, parent_movement=None, wave_order=2, start=0, duration=0, depth=0, fixed_depth=0, wave_height=0.5, wave_period=1, phase=0, ramp=0, disksave_periods=24,
                 disksave_periodsteps=20, disksave_xpos=2, disksave_zpos=-0.15, piston_dir=None, awas=None):

        super(RegularPistonWaveGen, self).__init__(parent_movement, wave_order, start,
                                                   duration, depth, fixed_depth, wave_height, wave_period)
        self.type = "Regular Piston Wave Generator"
        self.phase = phase
        self.ramp = ramp
        self.disksave_periods = disksave_periods
        self.disksave_periodsteps = disksave_periodsteps
        self.disksave_xpos = disksave_xpos
        self.disksave_zpos = disksave_zpos
        self.piston_dir = [1, 0, 0] if piston_dir is None else piston_dir
        self.awas = AWAS() if awas is None else awas


class AWAS(object):
    """ AWAS configuration.

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
    """

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


class AWASCorrection(object):
    """ AWAS drift correction property """

    def __init__(self, enabled=False, coefstroke=0, coefperiod=0, powerfunc=0):
        self.enabled = enabled
        self.coefstroke = coefstroke
        self.coefperiod = coefperiod
        self.powerfunc = powerfunc


class IrregularPistonWaveGen(WaveGen):
    """ Piston Regular Wave Generator.

    Attributes:
        spectrum: Spectrum type selected for the generation
        discretization: Type of discretization for the spectrum
        peak_coef: Peak enhancement coefficient
        waves: Number of waves to create irregular waves
        randomseed: Random seed to initialize RNG
        serieini: Initial time in irregular wave serie
        ramptime: Time of ramp
        piston_dir: Movement direction (def [1,0,0])
    """

    def __init__(self, parent_movement=None, wave_order=1, start=0, duration=0, depth=0, fixed_depth=0, wave_height=0.5, wave_period=1, spectrum=IrregularSpectrum.JONSWAP,
                 discretization=IrregularDiscretization.STRETCHED,
                 peak_coef=0.1, waves=50, randomseed=random.randint(0, 9999), serieini=0, ramptime=0,
                 serieini_autofit=True, savemotion_time=30, savemotion_timedt=0.05, savemotion_xpos=2,
                 savemotion_zpos=-0.15, saveserie_timemin=0, saveserie_timemax=1300, saveserie_timedt=0.05,
                 saveserie_xpos=0, saveseriewaves_timemin=0, saveseriewaves_timemax=1000, saveseriewaves_xpos=2, piston_dir=None):
        super(IrregularPistonWaveGen, self).__init__(parent_movement, wave_order, start,
                                                     duration, depth, fixed_depth, wave_height, wave_period)
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


class RegularFlapWaveGen(WaveGen):
    """ Flap Regular Wave Generator.

    Attributes:
        phase: Initial wave phase in function of PI
        ramp: Periods of ramp
        variable_draft: Position of the wavemaker hinge
        flapaxis0: Point 0 of axis rotation
        flapaxis1: Point 1 of axis rotation
    """

    def __init__(self, parent_movement=None, wave_order=2, start=0, duration=0, depth=0, fixed_depth=0, wave_height=0.5, wave_period=1, phase=0, ramp=0, disksave_periods=24,
                 disksave_periodsteps=20, disksave_xpos=2, disksave_zpos=-0.15, variable_draft=0.0, flapaxis0=None, flapaxis1=None):
        super(RegularFlapWaveGen, self).__init__(parent_movement, wave_order,
                                                 start, duration, depth, fixed_depth, wave_height, wave_period)
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
    """ Flap Irregular Wave Generator.

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
    """

    def __init__(self, parent_movement=None, wave_order=1, start=0, duration=0, depth=0, fixed_depth=0, wave_height=0.5, wave_period=1, spectrum=IrregularSpectrum.JONSWAP,
                 discretization=IrregularDiscretization.STRETCHED,
                 peak_coef=0.1, waves=50, randomseed=random.randint(0, 9999), serieini=0, ramptime=0,
                 serieini_autofit=True, savemotion_time=30, savemotion_timedt=0.05, savemotion_xpos=2,
                 savemotion_zpos=-0.15, saveserie_timemin=0, saveserie_timemax=1300, saveserie_timedt=0.05,
                 saveserie_xpos=0, saveseriewaves_timemin=0, saveseriewaves_timemax=1000, saveseriewaves_xpos=2, variable_draft=0.0, flapaxis0=None, flapaxis1=None):
        super(IrregularFlapWaveGen, self).__init__(parent_movement, wave_order, start,
                                                   duration, depth, fixed_depth, wave_height, wave_period)
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
    """ File Generator. Loads movements from file

    Attributes:
        duration: Duration in seconds
        filename: File path to use
        fields: Number of columns of the file
        fieldtime: Column with time
        fieldx: Column with X-position
        fieldy: Column with Y-position
        fieldz: Column with Z-position
    """

    def __init__(self, parent_movement=None, duration=0, filename="", fields=0, fieldtime=0, fieldx=0, fieldy=0, fieldz=0):
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
    """ Rotation File Generator. Loads rotation movements from file

    Attributes:
        duration: Duration in seconds
        anglesunits: Units of the file (degrees, radians)
        filename: File path to use
        axisp1: Point 1 of the axis
        axisp2: Point 2 of the axis
    """

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


class BaseMotion(object):
    """ Base motion class to inherit by others.

        Attributes:
            duration: Movement duration in seconds
        """

    def __init__(self, duration=1, parent_movement=None):
        self.duration = duration
        self.type = "Base Motion"
        self.parent_movement = parent_movement

    def __str__(self):
        return "BaseMotion [Duration: {}]".format(self.duration)


class RectMotion(BaseMotion):
    """ DualSPHysics rectilinear motion.

        Attributes:
            velocity: Velocity vector that defines the movement
        """

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
    """ DualSPHysics accelerated rectilinear motion.

        Attributes:
            velocity: Velocity vector that defines the movement
            acceleration: Acceleration vector that defines the aceleration
        """

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
    """ DualSPHysics rotational motion.

        Attributes:
            ang_vel: Angular velocity of the movement
            axis1: Starting point of the vector that defines the rotation axis
            axis2: Finishing point of the vector that defines the rotation axis
        """

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
    """ DualSPHysics rotational motion.

        Attributes:
            ang_vel: Angular velocity of the movement
            ang_acc: Angular acceleration of the movement
            axis1: Starting point of the vector that defines the rotation axis
            axis2: Finishing point of the vector that defines the rotation axis
        """

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
    """ DualSPHysics circular motion.

        Attributes:
            ang_vel: Angular velocity of the movement
            ang_acc: Angular acceleration of the movement
            reference: Point of the object that rotates with the axis
            axis1: Starting point of the vector that defines the rotation axis
            axis2: Finishing point of the vector that defines the rotation axis
        """

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
    """ DualSPHysics rectilinear motion.

        Attributes inherited from superclass.
        """

    def __init__(self, duration=1, parent_movement=None):
        BaseMotion.__init__(self, duration)
        self.parent_movement = parent_movement
        self.type = "Wait Interval"

    def __str__(self):
        return "WaitMotion [Duration: {}]".format(self.duration)


class RotSinuMotion(BaseMotion):
    """ DualSPHysics sinusoidal rotational motion.

        Attributes:
            axis1: Starting point of the vector that defines the rotation axis
            axis2: Finishing point of the vector that defines the rotation axis
            freq: Frequency
            ampl: Amplitude
            phase: Phase
        """

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
    """ DualSPHysics sinusoidal circular motion.

        Attributes:
            reference: Point of the object that rotates with the axis
            axis1: Starting point of the vector that defines the rotation axis
            axis2: Finishing point of the vector that defines the rotation axis
            freq: Frequency
            ampl: Amplitude
            phase: Phase
        """

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
    """ DualSPHysics sinusoidal rectilinear motion.

        Attributes:
            freq: Frequency (vector)
            ampl: Amplitude (vector)
            phase: Phase (vector)
        """

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


class CustomProperty(object):
    """ DualSPHysics compatible custom property.

            Attributes:
                name: Name of the property
                mkapplied: String with MK ranges and list
            """

    # TODO: Finish this.

    def __init__(self, name="New Property", mkapplied=""):
        self.name = name
        self.mkapplied = mkapplied


class Damping(object):
    """ DualSPHysics damping settings """

    def __init__(self, enabled=False, limitmin=None, limitmax=None, overlimit=1, redumax=10):
        self.enabled = enabled
        self.limitmin = [0, 0, 0] if limitmin is None else limitmin
        self.limitmax = [0, 0, 0] if limitmax is None else limitmax
        self.overlimit = overlimit
        self.redumax = redumax

    def __str__(self):
        to_ret = ""
        to_ret += "Damping configuration structure ({})\n".format(
            "enabled" if self.enabled else "disabled")
        to_ret += "Minimum limit: X:{} ; Y:{} ; Z:{}\n".format(*self.limitmin)
        to_ret += "Maximum limit: X:{} ; Y:{} ; Z:{}\n".format(*self.limitmax)
        to_ret += "Overlimit: {}\n".format(self.overlimit)
        to_ret += "Redumax: {}".format(self.redumax)
        return to_ret

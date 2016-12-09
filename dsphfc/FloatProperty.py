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
        pass

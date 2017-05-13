import numpy as np


# TODO
# 1. Explain using examples, the concept of field.
#    Then use this to describe electric fields and their relation to electric force.
# 2. Define the Volt and justify the use of V/m for E-fields
#    Show that electric force in Newtons is consistent with E-field in V/m
# 3. Explain equipotentials and their relation to work (energy)


class ChargeSystem:
    """Implementation of a fixed charged container"""
    def __init__(self, dimension):
        self.fixed_charges = []
        self.dimension = dimension

    def add_fixed_charge(self, charge: 'Charge'):
        self.fixed_charges.append(charge)

    def update(self):
        """Update the position and velocity of charges"""
        for charge in self:
            charge.update()
        # Avoid side effects
        for charge in self:
            charge.position = charge.new_position  # Interesting.

    def __iter__(self):
        return (charge for charge in self.fixed_charges)


class Charge:
    """Implementation of a fixed charge"""
    def __init__(self, charge: float, container: 'ChargeSystem', position=None, mass=1.):
        # Add it to the world
        self.container = container
        dimension = self.container.dimension

        if position is not None:
            assert dimension == len(position), "Dimensions of the container and the charge must agree"
            if type(position) is list:
                position = np.array(position)
            self.position = position
        else:
            self.position = np.zeros(dimension, dtype=float)
        container.add_fixed_charge(self)

        self.charge = charge
        self.mass = mass

        self.velocity = np.zeros(dimension, dtype=float)
        self.acceleration = np.zeros(dimension, dtype=float)
        self.new_position = None

    def calculate_attraction_force(self, charge2: 'Charge') -> np.array:
        """Calculate the attraction between two fixed_charges according to the Coulomb Law"""
        k = 9 * 10 ** 9  # 8.99 * 10 ** 9 to be more precise
        q1, q2 = self.charge, charge2.charge

        distance_vector = self.position - charge2.position

        distance_norm = np.linalg.norm(distance_vector)
        distance_unit = distance_vector / distance_norm

        magnitude = k * (q1 * q2) / (np.linalg.norm(distance_norm)) ** 2

        return magnitude * distance_unit

    def calculate_net_force(self) -> np.array:
        return sum([
            self.calculate_attraction_force(charge) for charge in self.container
            if charge is not self
        ])

    def calculate_acceleration(self) -> np.array:
        """Calculate the acceleration of this charge based on the formula F = m a"""
        F = self.calculate_net_force()
        m = self.mass
        a = F / m

        return a

    def update(self, force=False) -> None:
        """Update the acceleration and velocity of a charge
        Unless the option 'force' is set to True, the position will not be updated
        To update it, use ChargeSystem.update()"""
        self.acceleration = self.calculate_acceleration()
        self.velocity += self.acceleration

        if force:
            self.position += self.velocity
        else:
            self.new_position = self.position + self.velocity


def process_coordinates(void: 'ChargeSystem', steps: int) -> list:
    """
    Process coordinates for blender animations
    :param void: the void you want to process
    :param steps: int to show how many steps to calculate
    :return: list of list of coordinate lists
    ex: [
        [[x1, y1, z1], [x2, y2, z2], ...] # charge 1
        [[x1, y1, z1], [x2, y2, z2], ...] # charge 2
        ...
    ]
    """
    result = [[] for _ in void]

    for _ in range(steps):
        for ind, charge in enumerate(void):
            result[ind].append(list(charge.position))
        void.update()

    return result

if __name__ == '__main__':
    void_ = ChargeSystem(3)
    c1 = Charge(5 * 10 ** -5, void_, position=[10, 10, 10])
    c2 = Charge(-5 * 10 ** -5, void_, position=[0, 0, 0])
    print(process_coordinates(void_, 16))

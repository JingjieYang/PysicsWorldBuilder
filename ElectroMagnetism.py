import numpy as np


# TODO
# 1. Explain using examples, the concept of field.
#    Then use this to describe electric fields and their relation to electric force.
# 2. Define the Volt and justify the use of V/m for E-fields
#    Show that electric force in Newtons is consistent with E-field in V/m
# 3. Explain equipotentials and their relation to work (energy)


class FixedChargeContainer:
    """Implementation of a fixed charged container"""
    def __init__(self, dimension=2):
        self.fixed_charges = []
        self.dimension = dimension

    def add_fixed_charge(self, charge: 'FixedCharge'):
        self.fixed_charges.append(charge)

    def __iter__(self):
        return (charge for charge in self.fixed_charges)


class FixedCharge:
    """Implementation of a fixed charge"""
    def __init__(self, charge: float, container: 'FixedChargeContainer', pos_x=0., pos_y=0.):
        # Add it to the world
        self.container = container
        container.add_fixed_charge(self)

        self.charge = charge
        self.position = np.array([pos_x, pos_y])

    def calculate_attraction_force(self, charge2: 'FixedCharge'):
        # Calculate the attraction between two fixed_charges according to the Coulomb Law
        k = 9 * 10 ** 9
        c1, c2 = self.charge, charge2.charge

        distance_vector = charge2.position - self.position

        distance_norm = np.linalg.norm(distance_vector)
        distance_unit = distance_vector / distance_norm

        magnitude = k * (c1 * c2) / (np.linalg.norm(distance_norm)) ** 2
        return magnitude * distance_unit

    def calculate_net_force(self):
        return sum([
            self.calculate_attraction_force(charge) for charge in self.container
            if charge is not self
        ])


if __name__ == '__name__':
    # Hint: lol references
    void = FixedChargeContainer()
    # Add the champions in the game
    vel_koz = FixedCharge(5 * 10 ** -5, void, pos_x=0)
    cho_gath = FixedCharge(5 * 10 ** -5, void, pos_x=0.025)
    kha_zix = FixedCharge(-2.5 * 10 ** -5, void, pos_x=0.025 + 0.02)

    for charge_ in void:
        print(charge_.calculate_net_force())

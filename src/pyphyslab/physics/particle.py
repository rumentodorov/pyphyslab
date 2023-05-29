import numpy as np
import math

class Particle:
    def __init__(self, mass, velocity = [0.0, 0.0, 0.0], acceleration = [0.0, 0.0, 0.0], damping = 0.85):
        self._position = np.array([0.0,0.0,0.0])
        self._velocity = np.array(velocity)
        self._acceleration = np.array(acceleration)
        self.mass = mass
        self._damping = damping
        self._accumulated_force = np.array([0.0,0.0,0.0])

    @property
    def position(self):
        return self._position

    @property
    def velocity(self):
        return self._velocity
    
    @property
    def acceleration(self):
        return self._acceleration
    
    @position.setter
    def position(self, position):
        self._position = np.array(position)

    @velocity.setter
    def velocity(self, velocity):
        self._velocity =  np.array(velocity)
    
    @acceleration.setter
    def acceleration(self, acceleration):
        self._acceleration = acceleration

    def add_force(self, force):
        self._accumulated_force += np.array(force)

    def clear_accumulated_force(self):
        self._accumulated_force = np.array([0.0,0.0,0.0])

    def resolve(self, delta_time):
        
        if delta_time <= 0:
            return

        self._position += self._velocity * delta_time

        inverse_mass = 1 / self.mass
        result_acceleration = self._acceleration + self._accumulated_force * inverse_mass
        self._velocity += result_acceleration * delta_time

        self._velocity *= math.pow(self._damping, delta_time)

        self.clear_accumulated_force()
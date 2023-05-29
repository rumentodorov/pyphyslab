
import  numpy as np

Y_COORD = 1

class GroundCollisionDetector:

    def __init__(self, p1):
        self._detcted = False
        self._p1 = p1
    
    def detect(self):
        position = self._p1.position
        
        if position[Y_COORD] <= 0 and not self._detcted:
            self._detcted = True                        
            return GroundGontactResolver(self._p1)
        else:
            self._detcted = False
            return PassContacResolver(self._p1)


class ParticleCollisionDetector:

    def __init__(self):
        self._detcted = False

    def detect(self, p1, p2):
        
        midline =  p2.position - p1.position
        size = np.linalg.norm(midline)
        radius = 0.1

        if size <= 0 or size > radius:
            self._detcted = False
            return PassContacResolver(p1, p2)
        else: 
            if not self._detcted:
                contact_normal = midline * (1 / size)                
                self._detcted = True
        
                return ParticleContactResolver(p1, p2, contact_normal)
            return PassContacResolver(p1, p2)            


class GroundGontactResolver:

    def __init__(self, p1):
        self._p1 = p1
        self._restitution = 0.6
        self._min_resting_contact = -0.01
    
    def resolve(self, delta_time):  
        separating_velocity = self._p1.velocity            

        
        new_separating_velocity = -separating_velocity * self._restitution
        accumulated_caused_separation_velocity = self._p1.acceleration * delta_time

        new_separating_velocity += self._restitution * accumulated_caused_separation_velocity


        delta_velocity = new_separating_velocity - separating_velocity
        p1_inverse_mass = 1.0 / self._p1.mass

        if p1_inverse_mass < 0:
            return
        
        impulse = delta_velocity / p1_inverse_mass

        p1_velocity  = self._p1.velocity + (impulse * p1_inverse_mass)

        if self._p1.position[Y_COORD] <= self._min_resting_contact:
           self._p1.position[Y_COORD] = self._min_resting_contact
  
        self._p1.velocity = p1_velocity.tolist()

class PassContacResolver:
    def __init__(self, *p1):
        pass
    
    def resolve(self, delta_time):    
        pass


class ParticleContactResolver:
    def __init__(self, p1, p2, contact_normal):
        self._p1 = p1
        self._p2 = p2
        self._contact_normal = contact_normal
        self._restitution = 1.0        
  

    def resolve(self, delta_time):
        separating_velocity = self._separating_velocity()        

        new_separating_velocity = -separating_velocity * self._restitution
        accumulated_caused_velocity = self._p1.acceleration - self._p2.acceleration
        accumulated_caused_separation_velocity = accumulated_caused_velocity * self._contact_normal * delta_time

        new_separating_velocity += self._restitution * accumulated_caused_separation_velocity


        delta_velocity = new_separating_velocity - separating_velocity
        p1_inverse_mass = 1.0 / self._p1.mass
        p2_inverse_mass = 1.0 / self._p2.mass
        total_inverse_mass = p1_inverse_mass + p2_inverse_mass

        if total_inverse_mass < 0:
            return
        
        impulse = delta_velocity / total_inverse_mass
        impulse_per_mass = self._contact_normal * impulse

        p1_velocity  = self._p1.velocity + (impulse_per_mass * p1_inverse_mass)
        p2_velocity  = self._p2.velocity - (impulse_per_mass * p2_inverse_mass)

        self._p1.velocity = p1_velocity.tolist()
        self._p2.velocity = p2_velocity.tolist()

    def _separating_velocity(self):
        relative_velocity = self._p1.velocity - self._p2.velocity
        return relative_velocity * self._contact_normal 

    
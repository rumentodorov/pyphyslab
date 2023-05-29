from pyphyslab.physics.collision import ParticleCollisionDetector, GroundCollisionDetector

class World:
    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2
        self._particle_collision_detector = ParticleCollisionDetector()
        self._ground_collision_detectors = []
        self._ground_collision_detectors.append(GroundCollisionDetector(p1))

        if p2:
            self._ground_collision_detectors.append(GroundCollisionDetector(p2))
        
    @classmethod
    def single_particle(cls, p1):
        return cls(p1, None)

    def run_physics(self, delta_time):
        if self._p2 is not None:
            particle_cotact_resolver = self._particle_collision_detector.detect(self._p1, self._p2)
            particle_cotact_resolver.resolve(delta_time)

        for ground_collision_detector in self._ground_collision_detectors:
            ground_contact_resolver = ground_collision_detector.detect()
            ground_contact_resolver.resolve(delta_time)

        self._p1.resolve(delta_time)
        
        if self._p2 is not None:
            self._p2.resolve(delta_time)
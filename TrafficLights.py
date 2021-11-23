class TrafficLights(object):
    def __init__(self, env, name, res, t1, t2):
        self.env = env
        self.action = env.process(self.run(t1, t2))
        self.name = name
    
    def run(self, t1, t2):
        while True:
            with res.request() as req:
                yield req
                yield self.env.process(self.change(self.name, "Green", t1))
                yield self.env.process(self.change(self.name, "Yellow", t2))
            yield self.env.process(self.change(self.name, "Red", 35))
    
    def change(self, name, color, time):
        print('%s changes to %s at %d' % (name, color, self.env.now))
        yield self.env.timeout(time)

import simpy

env = simpy.Environment()
res = simpy.Resource(env, capacity=1)
sem1 = TrafficLights(env, 'TL 1', res, 30, 5)
sem2 = TrafficLights(env, 'TL 2', res, 40, 5)
env.run(until=201)
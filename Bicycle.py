import simpy

def bicycle(env):
    while True:
        print("Start riding at %d" % env.now)
        tiempo_rodada = 30
        yield env.timeout(tiempo_rodada)
        print("Rest at %d" % env.now)
        tiempo_descanso = 10
        yield env.timeout(tiempo_descanso)

env = simpy.Environment()
env.process(bicycle(env))
env.run(until = 100)
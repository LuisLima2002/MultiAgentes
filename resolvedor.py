from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.template import Template
from spade.message import Message
import time
import numpy

class Resolvedor(Agent):
    
    class getTipo(State):
        async def run(self):
            templateGetRaiz = Template()
            templateGetRaiz.set_metadata("performative", "inform")
            msg = Message(to = "lel2002@jix.im")
            msg.set_metadata("performative", "request")
            await self.send(msg)
            msg = await self.receive(timeout = 5)
            print(msg.body)
            self.set_next_state("getRaiz")
            if(msg.body == "1grau"):
                self.agent.fsm.add_state(name="getRaiz",state=self.agent.getRaiz1Grau())
            elif(msg.body == "2grau"):
                self.agent.fsm.add_state(name="getRaiz",state=self.agent.getRaiz2Grau())
            elif(msg.body == "3grau"):
                self.agent.fsm.add_state(name="getRaiz",state=self.agent.getRaiz3Grau())


    class getRaiz1Grau(State):
        x = [0, 100]
        y = []
        async def run(self):
            msg = Message(to = "lel2002@jix.im")
            msg.set_metadata("performative", "subscribe")
            
            msg.body = str(self.x[len(self.y)])
            await self.send(msg)
            res = None
            while not res:
                res = await self.receive(timeout = 5)
            self.y.append(float(res.body))

            if numpy.abs(self.y[-1]) < 10**(-5):
                print(self.x[len(self.y) - 1])
                await self.agent.stop()
            elif len(self.y) == len(self.x):
                root = (-self.y[0])/((self.y[1]-self.y[0])/(self.x[1]))
                self.x.append(root)
            self.set_next_state("getRaiz")

    class getRaiz2Grau(State):
        x = [0, 100, 200]
        y = []   
        async def run(self):
            msg = Message(to = "lel2002@jix.im")
            msg.set_metadata("performative", "subscribe")
            
            msg.body = str(self.x[len(self.y)])
            await self.send(msg)
            res = None
            while not res:
                res = await self.receive(timeout = 5)
            self.y.append(float(res.body))

            if numpy.abs(self.y[-1]) < 10**(-5):
                print(self.x[len(self.y) - 1])
                await self.agent.stop()
            elif len(self.y) == len(self.x):
                roots = numpy.roots(numpy.polyfit(self.x, self.y, len(self.x) - 1))
                self.x.append(roots[0])
            self.set_next_state("getRaiz")

    class getRaiz3Grau(State):
        x = [0, 100, 200, 300]
        y = []   
        async def run(self):
            msg = Message(to = "lel2002@jix.im")
            msg.set_metadata("performative", "subscribe")
            
            msg.body = str(self.x[len(self.y)])
            await self.send(msg)
            res = None
            while not res:
                res = await self.receive(timeout = 5)
            self.y.append(float(res.body))

            if numpy.abs(self.y[-1]) < 10**(-5):
                print(self.x[len(self.y) - 1])
                await self.agent.stop()
            elif len(self.y) == len(self.x):
                roots = numpy.roots(numpy.polyfit(self.x, self.y, len(self.x) - 1))
                self.x.append(roots[0])
            self.set_next_state("getRaiz")



    async def setup(self):
        print("setup")
        self.fsm = FSMBehaviour()
        self.fsm.add_state(name="getTipo",state=self.getTipo(), initial=True)
        self.fsm.add_transition(source="getTipo",dest="getRaiz")
        self.fsm.add_transition(source="getRaiz",dest="getRaiz")
        self.add_behaviour(self.fsm)
        
        
resolvedor = Resolvedor("resolvedor2002@jix.im", "Dudu2002")
resolvedor.start().result()
print("Wait until user interrupts with ctrl+C")

while resolvedor.is_alive():
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        resolvedor.stop()
        break
print("Agent finished")
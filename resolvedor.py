from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.template import Template
from spade.message import Message
import time
import numpy

class Resolvedor(Agent):
    
    class getTipo(OneShotBehaviour):
        async def run(self):
            templateGetRaiz = Template()
            templateGetRaiz.set_metadata("performative", "inform")
            msg = Message(to = "gerador@jabber.fr")
            msg.set_metadata("performative", "request")
            msg.sender = "resolvedor@jabber.fr"
            await self.send(msg)
            msg = await self.receive(timeout = 5)
            print(msg.body)
            if(msg.body == "1grau"):
                self.agent.add_behaviour(Resolvedor.getRaiz1Grau(), templateGetRaiz)
            elif(msg.body == "2grau"):
                self.agent.add_behaviour(Resolvedor.getRaiz2Grau(), templateGetRaiz)
            elif(msg.body == "3grau"):
                self.agent.add_behaviour(Resolvedor.getRaiz3Grau(), templateGetRaiz)


    class getRaiz1Grau(CyclicBehaviour):
        x = [0, 100]
        y = []
        async def run(self):
            msg = Message(to = "gerador@jabber.fr")
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

    class getRaiz2Grau(CyclicBehaviour):
        x = [0, 100, 200]
        y = []   
        async def run(self):
            msg = Message(to = "gerador@jabber.fr")
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

    class getRaiz3Grau(CyclicBehaviour):
        x = [0, 100, 200, 300]
        y = []   
        async def run(self):
            msg = Message(to = "gerador@jabber.fr")
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

    async def setup(self):
        print("setup")
        templateGetTipo= Template()
        templateGetTipo.set_metadata("performative", "inform")
        self.add_behaviour(self.getTipo(), templateGetTipo)
        
resolvedor = Resolvedor("resolvedor@jabber.fr", "123456789")
resolvedor.start()
print("Wait until user interrupts with ctrl+C")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...")
resolvedor.stop()

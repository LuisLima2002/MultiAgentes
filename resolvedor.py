from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.template import Template
from spade.message import Message
import time
import numpy

class Resolvedor(Agent):
    
    class getTipo(OneShotBehaviour):
        async def run(self):
            templateGetRaiz = Template()
            templateGetRaiz.set_metadata("performative","inform")
            templateGetRaiz.set_metadata("content","number")
            msg = Message(to="lel2002@jix.im")
            msg.set_metadata("performative", "request")
            msg.sender="resolvedor2002@jix.im"
            await self.send(msg)
            msg = await self.receive(timeout=5)
            print(msg.body)
            if(msg.body=="1grau"):
                self.agent.add_behaviour(Resolvedor.getRaiz1Grau(),templateGetRaiz)
            elif(msg.body=="2grau"):
                self.agent.add_behaviour(Resolvedor.getRaiz2Grau(),templateGetRaiz)
            elif(msg.body=="3grau"):
                self.agent.add_behaviour(Resolvedor.getRaiz3Grau(),templateGetRaiz)


    class getRaiz1Grau(OneShotBehaviour):
        async def run(self):
            x=[0,100]
            y=[]
            msg = Message(to="lel2002@jix.im")
            msg.set_metadata("performative", "subscribe")
            msg.set_metadata("type", "1grau")
            for i in range(2):
                msg.body=str(x[i])
                await self.send(msg)
                res = None
                while not res:
                    res = await self.receive(timeout=5)
                y.append(float(res.body))
            roots = numpy.roots(numpy.polyfit(x,y,1))
            print(roots)
            await self.agent.stop()

    class getRaiz2Grau(OneShotBehaviour):
        async def run(self):
            x=[0,100,200]
            y=[]
            msg = Message(to="lel2002@jix.im")
            msg.set_metadata("performative", "subscribe")
            msg.set_metadata("type", "2grau")
            for i in range(3):
                msg.body=str(x[i])
                await self.send(msg)
                res = None
                while not res:
                    res = await self.receive(timeout=5)
                y.append(float(res.body))
            roots = numpy.roots(numpy.polyfit(x,y,2))
            print(roots)
            await self.agent.stop()

    class getRaiz3Grau(OneShotBehaviour):
        async def run(self):
            x=[0,100,200,300]
            y=[]
            msg = Message(to="lel2002@jix.im")
            msg.set_metadata("performative", "subscribe")
            msg.set_metadata("type", "3grau")
            for i in range(4):
                msg.body=str(x[i])
                await self.send(msg)
                res = None
                while not res:
                    res = await self.receive(timeout=5)
                y.append(float(res.body))
            roots = numpy.roots(numpy.polyfit(x,y,3))
            print(roots)
            await self.agent.stop()

    async def setup(self):
        print("setup")
        templateGetTipo= Template()
        templateGetTipo.set_metadata("performative","inform")
        templateGetTipo.set_metadata("content","text")
        self.add_behaviour(self.getTipo(),templateGetTipo)
        
resolvedor = Resolvedor("resolvedor2002@jix.im", "Dudu2002")
resolvedor.start()
print("Wait until user interrupts with ctrl+C")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...")
resolvedor.stop()
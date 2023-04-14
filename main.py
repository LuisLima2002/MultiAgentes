from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random
import time
from numpy import polyfit
class Gerador(Agent):
    grau= random.randint(1,3)
    roots=[]
    y=[]
    for i in range(grau):
        roots.append(random.randint(-1000,1000))
        y.append(0)
    roots.append(0)
    y.append(random.randint(-100,100)+20)
    coef=polyfit(roots,y,grau)
    roots.pop()
    class funcao_1grau(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                x = float( Gerador.coef[0]*x + Gerador.coef[1] )
                print("Enviou para " + str(res.sender) + " = ",x)
                msg = Message(to=str(res.sender)) 
                msg.set_metadata("performative", "inform")  
                msg.set_metadata("content", "number")
                msg.body = str(x)
                await self.send(msg)

    class funcao_2grau(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                x = float( Gerador.coef[0]*x*x+ Gerador.coef[1]*x + Gerador.coef[2] )
                print("Enviou para " + str(res.sender) + " = ",x)
                msg = Message(to=str(res.sender)) 
                msg.set_metadata("performative", "inform")  
                msg.set_metadata("content", "number")
                msg.body = str((x))
                await self.send(msg)

    class funcao_3grau(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                x = float( Gerador.coef[0]*x*x*x+Gerador.coef[1]*x*x+ Gerador.coef[2]*x + Gerador.coef[3] )
                print("Enviou para " + str(res.sender) + " = ",x)
                msg = Message(to=str(res.sender)) 
                msg.set_metadata("performative", "inform")  
                msg.set_metadata("content", "number")
                msg.body = str((x))
                await self.send(msg)
   
    class tipo_funcao(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                msg = Message(to=str(res.sender))
                msg.set_metadata("performative", "inform")
                msg.set_metadata("content", "text")
                if Gerador.grau==1:
                    msg.body = "1grau" 
                if Gerador.grau==2:
                    msg.body = "2grau" 
                if Gerador.grau==3:
                    msg.body = "3grau" 
                
                await self.send(msg)
                print("Respondeu para " + str(msg.sender) + " com " + msg.body)
                

    async def setup(self):
        print("Roots da função: ", self.roots)
        
        t1 = Template()
        t1.set_metadata("performative","subscribe")
        t1.set_metadata("type","1grau")
        self.add_behaviour(self.funcao_1grau(),t1)

        t2 = Template()
        t2.set_metadata("performative","subscribe")
        t2.set_metadata("type","2grau")
        self.add_behaviour(self.funcao_2grau(),t2)

        t3 = Template()
        t3.set_metadata("performative","subscribe")
        t3.set_metadata("type","3grau")
        self.add_behaviour(self.funcao_3grau(),t3)

        ft = self.tipo_funcao()
        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(ft, template)


gerador = Gerador("lel2002@jix.im", "Dudu2002")
gerador.start()
print("Wait until user interrupts with ctrl+C")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...")
gerador.stop()
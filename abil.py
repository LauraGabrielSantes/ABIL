#Implementa la simulacion del Algoritmo de inundación limitada usando como base el algoritmo de PI Segall
import random
from event import Event
from model import Model


class ABIL(Model):
   contadorMensajes=0
   
   def init(self):
     print ("\nInicio funciones", self.id)
     print ("Mis vecinos son:", self.neighbors)
     self.visitado=False
     self.TTL = 0
     self.mis_recursos = self.llenaRecurso()
     print ("[",self.id,"]: Mis recursos son: ", self.mis_recursos,"\n")

   # Aqui se definen las acciones concretas que deben ejecutarse cuando se
   # recibe un evento
   def receive(self, event):
    origen=event.getSource()
    evento=event.getName()
    if isinstance (evento,tuple):
      nombre=evento[0]
      listaMensaje = evento [1]
      recursoBuscado = listaMensaje [0]
      emisorBusqueda = listaMensaje [1]
      TTL_recibido = listaMensaje [2]
    else:
      nombre = evento


    if nombre == "INICIA":
     self.visitado=True
     emisorBusqueda = self.id
     self.nodos_con_recurso = []
     self.TTL = TTL_recibido
     print ("\n[", self.id, "]: recibí INICIA y soy el nodo emisor de búsqueda con TTL ", self.TTL," en t=",self.clock," \n")
     self.TTL -= 1
     mensaje = ("M", [recursoBuscado,emisorBusqueda,self.TTL])
     for vecino in self.neighbors:
       newevent = Event(mensaje, self.clock + 1.0, vecino, self.id)
       ABIL.contadorMensajes += 1
       self.transmit(newevent)
    elif nombre == "M":
      print ("[", self.id, "]: recibí M de ", origen," con TTL = ", TTL_recibido," en t=",self.clock," ")
      if not self.visitado:
        self.visitado=True
        self.TTL = TTL_recibido
        print ("[", self.id, "]: actualizo TTL a ", self.TTL," \n")
        if self.localizaRecurso(self.mis_recursos, recursoBuscado):
          newevent = Event("ENCONTRADO", self.clock + 1.0, emisorBusqueda, self.id)
          ABIL.contadorMensajes += 1
          self.transmit(newevent)
        if self.TTL > 0:
         self.TTL -= 1
         mensaje = ("M",[recursoBuscado,emisorBusqueda,self.TTL])
         for vecino in self.neighbors:
          if vecino != origen:  
            newevent = Event(mensaje, self.clock + 1.0, vecino, self.id)
            ABIL.contadorMensajes += 1
            self.transmit(newevent)
      else:
        if self.TTL < TTL_recibido:
          self.TTL = TTL_recibido
          print ("[", self.id, "]: actualizo TTL a ", self.TTL," \n")
          if self.TTL > 0:
            self.TTL -= 1
            mensaje = ("M",[recursoBuscado,emisorBusqueda,self.TTL])
            for vecino in self.neighbors:
              if vecino != origen: #evaluar si se descarta el envío al nodo padre, o se permite que se le envíe 
                newevent = Event(mensaje, self.clock + 1.0, vecino, self.id)
                ABIL.contadorMensajes += 1
                self.transmit(newevent)
    elif nombre == "ENCONTRADO":
      self.nodos_con_recurso.append(origen)
      print ("[", self.id,"]: El nodo ", origen," tiene el recurso  t = ",self.clock,"\nactualizo lista de nodos con recurso: ",self.nodos_con_recurso,"\n")

   
   def llenaRecurso(self):
     listaRecursos =[]
     tam = random.randint(2,10) #llegaba solo a 6, pero no a 10 productos por nodo
     for _ in range (tam): #con esto garantizamos que se llenen los productos entre 2 y 10, ya que si nos salia un tam de 2 solo nos daria 1 producto realmente
       contenido = random.randint(1,100)
       if contenido not in listaRecursos: #esto nos evitara obtener contenido duplicado en los productos [4,4,4,5]
        listaRecursos.append(contenido)
     return listaRecursos

   
   def localizaRecurso(self, listaRecursos, recursoBuscado):
     for i in listaRecursos:
       if i == recursoBuscado:
         return True
     return False
     

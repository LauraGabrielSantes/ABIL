import random
import sys
import time
from event import Event
from simulation import Simulation
from abil import ABIL
import matplotlib.pyplot as plt
class main():
 if len(sys.argv) != 2:
  print ("Por favor proporcione el nombre de la grafica de comunicaciones")
  raise SystemExit(1)

 emisorBusqueda = int(input("Indique el id del nodo iniciador de la búsqueda: "))
 recursoBuscado = int(input("¿Qué recurso desea buscar? ")) 
 mensajes_TTL = []
 falsos_negativos = []
 
 for ttl in range(1,4): #se ejecuta el experimento con TTL = 1, 2 y 3
   random.seed(42)  # Establece la semilla para reproducibilidad
   print(f"Experimento con TTL = {ttl}")
   ABIL.contadorMensajes = 0
   inicio = time.time()
   experiment = Simulation(sys.argv[1], 60)  #pendiente validar tiempo de la simulación
   m = ABIL()
   for i in range(1,len(experiment.graph)+1):
    experiment.setModel(m, i)
    m = ABIL()

 # inserta un evento semilla en la agenda y arranca
   mensaje = ("INICIA", [recursoBuscado,emisorBusqueda,ttl])
   seed = Event(mensaje, 0.0, emisorBusqueda, 1)
   experiment.init(seed)
   experiment.run()
 #imprimimos la lista de los nodos que encontraron el recurso con el TTL de abil.
   encontradoABIL = experiment.table[emisorBusqueda].model.nodos_con_recurso
   total = len(encontradoABIL)
   print("\nNodos que encontraron el recurso con ABIL:", encontradoABIL)
   print("Total con ABIL:", total)
 #se genera una lista del total de nodos que si contienen el recurso buscado en el grafo completo, esto permite que se pueda comparar los encontrados
 #por abil y los que realmente tienen el recurso
   nodos_con_recurso = []
   for i in range(1, len(experiment.table)):
        if recursoBuscado in experiment.table[i].model.mis_recursos:
         nodos_con_recurso.append(i)
   totalGrafo = len(nodos_con_recurso)
   print("\nNodos que realmente tienen el recurso:", nodos_con_recurso)
   print("Total:", totalGrafo)
   falsosNegativos = totalGrafo - total #de nodos que realmente tienen el recurso menos el total de nodos que encontraron el recurso con ABIL
   if totalGrafo > 0:
    porcentaje = (falsosNegativos / totalGrafo) * 100
   else:
        porcentaje = 0
   print("Porcentaje de falsos negativos:", porcentaje, "%")
   fin = time.time()
   print("\nMensajes enviados:", ABIL.contadorMensajes)
   print(f"el total de falsos negativos es: {falsosNegativos}")
   mensajes_TTL.append(ABIL.contadorMensajes)
   falsos_negativos.append(porcentaje)

 print("\n==============================")
 print("Resumen de resultados")
 print("==============================")

 for i in range(3): #se realiza un bucle para imprimir los resultados de cada experimento con TTL = 1, 2 y 3
    print(
        f"TTL = {i+1} | "
        f"Mensajes = {mensajes_TTL[i]} | "
        f"FN = {falsos_negativos[i]:.2f}%"
    )
 ttl = [1, 2, 3]

# -----------------------------
# Gráfica 1
# -----------------------------
 plt.figure(figsize=(6,4))
 plt.plot(ttl, falsos_negativos, marker='o', linewidth=2)

 plt.title("Falsos negativos vs TTL")
 plt.xlabel("TTL")
 plt.ylabel("Falsos negativos (%)")
 plt.xticks(ttl)
 plt.grid(True)

 plt.savefig("FalsosNegativosVsTTL.png", dpi=300)
 plt.close()

# -----------------------------
# Gráfica 2
# -----------------------------
 plt.figure(figsize=(6,4))
 plt.plot(ttl, mensajes_TTL, marker='o', linewidth=2)

 plt.title("Mensajes enviados vs TTL")
 plt.xlabel("TTL")
 plt.ylabel("Mensajes enviados")
 plt.xticks(ttl)
 plt.grid(True)

 plt.savefig("MensajesVsTTL.png", dpi=300)
 plt.close()

 print("\nGráficas generadas correctamente.")

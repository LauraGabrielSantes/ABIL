import random
Nodos = 200
min=4
max=7

grafo = [set() for _ in range(Nodos)]

for i in range(Nodos):
    siguiente = (i+1) % Nodos
    anterior = (i-1) % Nodos
    grafo[i].add(siguiente)
    grafo[i].add(anterior)

while True:
    candidatos = [i for i in range(Nodos) if len(grafo[i]) < min]
    if not candidatos:
        break
    a = random.choice(candidatos)
    
    posibles = [b for b in range(Nodos) if b != a and len(grafo[b]) < max and b not in grafo[a]]
    if posibles:
        b = random.choice(posibles)
        grafo[a].add(b)
        grafo[b].add(a)

with open("grafo200.txt", "w") as f:
    for vecinos in grafo:
        linea = " ".join(str(v+1) for v in sorted(vecinos))
        f.write(linea + "\n")
print("Grafo generado y guardado en grafo200.txt")
from collections import defaultdict

# Definimos una clase llamada 'Graph' que representa un grafo con capacidades en las aristas.


class Graph:
    def __init__(self, graph):
        self.graph = graph  # Grafo residual (capacidades residuales)
        self.ROW = len(graph)  # Número de filas en el grafo
        self.COL = len(graph[0])  # Número de columnas en el grafo

    # Esta función realiza una búsqueda en amplitud (BFS) para encontrar un camino aumentante desde el origen al sumidero.
    def BFS(self, s, t, parent):
        # Inicializamos una lista para rastrear los nodos visitados
        visited = [False] * self.ROW
        queue = []  # Creamos una cola para BFS
        queue.append(s)  # Comenzamos desde el nodo origen 's'
        visited[s] = True  # Marcamos el nodo origen como visitado
        while queue:
            u = queue.pop(0)  # Tomamos el primer nodo de la cola
            for ind, val in enumerate(self.graph[u]):
                # Verificamos si el nodo vecino no ha sido visitado y si la capacidad residual es mayor que cero
                if visited[ind] == False and val > 0:
                    queue.append(ind)  # Agregamos el nodo vecino a la cola
                    # Marcamos el nodo vecino como visitado
                    visited[ind] = True
                    # Almacenamos el padre del nodo vecino en 'parent'
                    parent[ind] = u
        # Devolvemos True si llegamos al nodo sumidero, de lo contrario, False
        return True if visited[t] else False

    # Función principal que implementa el algoritmo Ford-Fulkerson para encontrar el flujo máximo.
    def FordFulkerson(self, source, sink):
        # Inicializamos una lista para rastrear los padres de los nodos en el camino aumentante
        parent = [-1] * self.ROW
        max_flow = 0  # Inicializamos el flujo máximo en cero

        # Paso 2: Mientras haya un camino aumentante desde el origen al sumidero
        while self.BFS(source, sink, parent):
            # Inicializamos el flujo en el camino aumentante como infinito
            path_flow = float("inf")
            s = sink

            # Paso 3: Encuentra el flujo máximo en el camino aumentante
            while s != source:
                # Buscamos la capacidad residual mínima en el camino aumentante
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Paso 4: Actualiza las capacidades residuales en el grafo
            v = sink
            while v != source:
                u = parent[v]
                # Restamos el flujo del camino aumentante de la capacidad residual de la arista
                self.graph[u][v] -= path_flow
                # Añadimos el flujo en sentido opuesto en el grafo residual
                self.graph[v][u] += path_flow
                v = parent[v]

            # Acumulamos el flujo del camino aumentante al flujo máximo total
            max_flow += path_flow

        # Devolvemos el flujo máximo calculado
        return max_flow


# Ejemplo de uso
graph = [[0, 16, 13, 0, 0, 0],
         [0, 0, 10, 12, 0, 0],
         [0, 4, 0, 0, 14, 0],
         [0, 0, 9, 0, 0, 20],
         [0, 0, 0, 7, 0, 4],
         [0, 0, 0, 0, 0, 0]]

g = Graph(graph)

source = 0
sink = 5

# Llamamos a FordFulkerson para calcular el flujo máximo
max_flow = g.FordFulkerson(source, sink)

print("Flujo Máximo:", max_flow)

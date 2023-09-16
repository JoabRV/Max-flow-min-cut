from collections import deque


class Graph:
    def __init__(self, graph):
        self.graph = graph  # Grafo residual (capacidades residuales)
        self.ROW = len(graph)  # Número de filas en el grafo
        self.COL = len(graph[0])  # Número de columnas en el grafo

    # Función de búsqueda en amplitud (BFS) para construir capas en el grafo residual.
    def BFS(self, s, t, level):
        level[s] = 0
        queue = deque()
        queue.append(s)
        while queue:
            u = queue.popleft()
            for v, capacity in enumerate(self.graph[u]):
                if level[v] < 0 and capacity > 0:
                    level[v] = level[u] + 1
                    queue.append(v)

    # Función recursiva para encontrar un bloqueo de flujo.
    def blocking_flow(self, u, t, flow, level, start):
        if u == t:
            return flow
        for v, capacity in enumerate(self.graph[u][start[u]:]):
            if level[v] == level[u] + 1 and capacity > 0:
                bottleneck = min(flow, capacity)
                bottleneck_flow = self.blocking_flow(
                    v, t, bottleneck, level, start)
                if bottleneck_flow > 0:
                    self.graph[u][start[u] + v] -= bottleneck_flow
                    self.graph[v][start[v] + u] += bottleneck_flow
                    return bottleneck_flow
        return 0

    # Función principal que implementa el algoritmo de Dinic para encontrar el flujo máximo.
    def Dinic(self, source, sink):
        max_flow = 0
        level = [-1] * self.ROW

        while True:
            # Paso 1: Construir capas en el grafo residual usando BFS
            self.BFS(source, sink, level)

            if level[sink] < 0:
                break  # Si no se puede alcanzar el sumidero, terminar

            start = [0] * self.ROW
            while True:
                # Paso 2: Encontrar bloqueos de flujo usando DFS
                flow = self.blocking_flow(
                    source, sink, float('inf'), level, start)
                if flow > 0:
                    max_flow += flow
                else:
                    break  # No se encontraron más bloqueos de flujo

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

# Llamamos a Dinic para calcular el flujo máximo
max_flow = g.Dinic(source, sink)

print("Flujo Máximo (Dinic):", max_flow)

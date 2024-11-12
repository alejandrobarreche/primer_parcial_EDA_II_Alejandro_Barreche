
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from memory_profiler import memory_usage
import timeit



class Graph:
    def __init__(self, localidades=None):
        # Create a NetworkX graph instance
        self.graph = nx.Graph()
        if localidades:
            # Populate the graph with nodes and edges from the dictionary
            for node, edges in localidades.items():
                for neighbor, distance in edges:
                    self.graph.add_edge(node, neighbor, weight=distance)

    def add_node(self, node):
        # Adds a node if it doesn't exist
        if node not in self.graph:
            self.graph.add_node(node)

    def add_edge(self, node1, node2, distance):
        # Adds an edge with a specified distance
        self.graph.add_edge(node1, node2, weight=distance)

    def shortest_path(self, origin, destination):
        # Finds the shortest path using Dijkstra's algorithm
        try:
            path = nx.shortest_path(self.graph, source=origin, target=destination, weight='weight')
            distance = nx.shortest_path_length(self.graph, source=origin, target=destination, weight='weight')
            return path, distance
        except nx.NetworkXNoPath:
            return None, float("inf")

    def is_connected(self):
        # Checks if the graph is connected
        return nx.is_connected(self.graph)

    def find_nodes_with_short_connections(self, max_distance=15):
        # Identifies nodes where all connections are below max_distance
        short_connection_nodes = []
        for node in self.graph.nodes:
            edges = self.graph.edges(node, data='weight')
            if all(weight < max_distance for _, _, weight in edges):
                short_connection_nodes.append(node)
        return short_connection_nodes

    def draw_graph(self):
        # Draws the graph with labels and edge weights
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.show()

    def ruta_mas_corta(self, origen, destino):
        """
        Encuentra la ruta más corta entre dos localidades usando el algoritmo de Dijkstra.
        Muestra la ruta a seguir y la distancia total.

        :param origen: Localidad de origen.
        :param destino: Localidad de destino.
        :return: Tupla con la ruta (lista de localidades) y la distancia total.
        """
        try:
            # Calcula la ruta más corta y la distancia total
            camino = nx.shortest_path(self.graph, source=origen, target=destino, weight='weight')
            distancia_total = nx.shortest_path_length(self.graph, source=origen, target=destino, weight='weight')

            # Muestra el resultado
            print("Ruta más corta desde", origen, "hasta", destino, ":", " -> ".join(camino))
            print("Distancia total:", distancia_total, "km")

            return camino, distancia_total
        except nx.NetworkXNoPath:
            print(f"No hay ruta entre {origen} y {destino}.")
            return None, float("inf")

    def localidades_con_conexiones_cortas(self, max_distance=15):
        """
        Encuentra las localidades donde todas las rutas conectadas tienen distancias
        menores a max_distance (por defecto 15 km) y devuelve una lista de dichas localidades.

        :param max_distance: Distancia máxima permitida para considerar una localidad.
        :return: Lista de localidades que cumplen el criterio.
        """
        localidades_cortas = []
        for localidad in self.graph.nodes:
            # Obtiene todas las conexiones de la localidad
            conexiones = self.graph.edges(localidad, data='weight')

            # Comprueba si todas las conexiones tienen una distancia menor a max_distance
            if all(distancia < max_distance for _, _, distancia in conexiones):
                localidades_cortas.append(localidad)

        # Muestra el resultado
        print("Localidades con todas las conexiones de menos de", max_distance, "km:", localidades_cortas)
        return localidades_cortas

    from collections import deque

    def es_conexo_dfs(self):
        """
        Verifica si el grafo es conexo utilizando DFS.

        :return: True si el grafo es conexo, False en caso contrario.
        """
        # Selecciona un nodo de inicio arbitrario
        start_node = next(iter(self.graph.nodes))
        visited = set()

        # Función de DFS recursiva
        def dfs(node):
            visited.add(node)
            for neighbor in self.graph.neighbors(node):
                if neighbor not in visited:
                    dfs(neighbor)

        # Ejecuta DFS desde el nodo inicial
        dfs(start_node)

        # Verifica si todos los nodos fueron visitados
        return len(visited) == len(self.graph.nodes)

    def es_conexo_bfs(self):
        """
        Verifica si el grafo es conexo utilizando BFS.

        :return: True si el grafo es conexo, False en caso contrario.
        """
        # Selecciona un nodo de inicio arbitrario
        start_node = next(iter(self.graph.nodes))
        visited = set()
        queue = deque([start_node])

        # Ejecuta BFS
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                for neighbor in self.graph.neighbors(node):
                    if neighbor not in visited:
                        queue.append(neighbor)

        # Verifica si todos los nodos fueron visitados
        return len(visited) == len(self.graph.nodes)

    def rutas_alternativas_sin_ciclos(self, origen, destino):
        """
        Encuentra todas las rutas alternativas entre dos localidades sin pasar por el mismo nodo dos veces,
        utilizando BFS para evitar ciclos.

        :param origen: Localidad de origen.
        :param destino: Localidad de destino.
        :return: Lista de rutas alternativas (cada ruta es una lista de localidades).
        """
        # Lista de rutas alternativas
        rutas = []
        # Cola para BFS, inicializada con el nodo de origen
        queue = deque([(origen, [origen])])

        while queue:
            # Extrae el nodo actual y la ruta hasta él
            nodo_actual, ruta = queue.popleft()

            # Si se llega al destino, agrega la ruta a la lista de rutas alternativas
            if nodo_actual == destino:
                rutas.append(ruta)
                continue

            # Expande a los vecinos que aún no se han visitado en la ruta actual
            for vecino in self.graph.neighbors(nodo_actual):
                if vecino not in ruta:  # Evita ciclos
                    queue.append((vecino, ruta + [vecino]))

        # Muestra las rutas encontradas
        print(f"Rutas alternativas sin ciclos entre {origen} y {destino}:")
        for r in rutas:
            print(" -> ".join(r))

        return rutas

    def ruta_mas_larga_sin_ciclos(self, origen, destino):
        """
        Calcula la ruta más larga posible entre dos localidades sin ciclos utilizando programación dinámica.

        :param origen: Localidad de origen.
        :param destino: Localidad de destino.
        :return: Tupla (ruta más larga, distancia total)
        """
        # Memoization dictionary to store longest paths to each node
        memo = {}

        def dfs(node, path):
            # If we reach the destination, return the path and its length
            if node == destino:
                return path, sum(self.graph[u][v]['weight'] for u, v in zip(path, path[1:]))

            # If we have already computed the longest path from this node, use the stored result
            if node in memo:
                return memo[node]

            max_path = []
            max_distance = 0

            # Explore neighbors
            for neighbor, edge_data in self.graph[node].items():
                if neighbor not in path:  # Avoid cycles
                    current_path, current_distance = dfs(neighbor, path + [neighbor])

                    # Update if a longer path is found
                    if current_distance > max_distance:
                        max_path = current_path
                        max_distance = current_distance

            # Store result in memoization dictionary
            memo[node] = (max_path, max_distance)
            return memo[node]

        # Start the DFS from the origin
        longest_path, longest_distance = dfs(origen, [origen])

        # Show and return the results
        print(f"Ruta más larga desde {origen} hasta {destino}: {' -> '.join(longest_path)}")
        print("Distancia total:", longest_distance, "km")

        return longest_path, longest_distance



    def benchmark_function(self, func_name, *args):
        """
        Benchmark the specified function by measuring execution time and memory usage,
        then plot the results.

        :param func_name: Name of the function to benchmark as a string.
        :param args: Arguments to pass to the function being benchmarked.
        """
        # Dictionary to map function names to actual methods
        methods = {
            "ruta_mas_corta": self.ruta_mas_corta,
            "localidades_con_conexiones_cortas": self.localidades_con_conexiones_cortas,
            "es_conexo_dfs": self.es_conexo_dfs,
            "es_conexo_bfs": self.es_conexo_bfs,
            "rutas_alternativas_sin_ciclos": self.rutas_alternativas_sin_ciclos,
            "ruta_mas_larga_sin_ciclos": self.ruta_mas_larga_sin_ciclos,
        }

        # Check if the function exists in the dictionary
        if func_name not in methods:
            print(f"Function '{func_name}' not found.")
            return

        # Get the function from the dictionary
        func = methods[func_name]

        # Measure execution time
        exec_time = timeit.timeit(lambda: func(*args), number=1)

        # Measure memory usage
        mem_usage = memory_usage((func, args), interval=0.1, max_iterations=1)

        # Plot the results
        fig, ax1 = plt.subplots(figsize=(8, 5))

        # Plot execution time as a bar
        ax1.bar(["Execution Time"], [exec_time], color="tab:blue", alpha=0.6)
        ax1.set_ylabel("Execution Time (s)", color="tab:blue")
        ax1.set_ylim(0, max(exec_time * 1.2, 0.1))  # Extend y-axis for better visualization
        ax1.tick_params(axis="y", labelcolor="tab:blue")

        # Plot memory usage as a line on a secondary y-axis
        ax2 = ax1.twinx()
        ax2.plot(range(len(mem_usage)), mem_usage, color="tab:red", marker="o", linestyle="--")
        ax2.set_ylabel("Memory Usage (MiB)", color="tab:red")
        ax2.tick_params(axis="y", labelcolor="tab:red")

        # Set plot title and show plot
        plt.title(f"Performance of {func_name} function")
        plt.show()

    def execute_all_tasks(self):
        """
        Execute the following tasks:
        1. Find the shortest path and distance between all pairs of localities.
        2. List localities with all connections under 15 km.
        3. Indicate if the graph is connected.
        4. Display all possible routes without cycles between two specified localities.
        """
        print("\n--- Task 1: Shortest Path Between All Localities ---")
        for origin in self.graph.nodes:
            for destination in self.graph.nodes:
                if origin != destination:
                    path, distance = self.shortest_path(origin, destination)
                    if path:
                        print(f"Shortest path from {origin} to {destination}: {path} (Distance: {distance} km)")
                    else:
                        print(f"No path from {origin} to {destination}.")

        print("\n--- Task 2: Localities with All Connections Under 15 km ---")
        short_connections = self.localidades_con_conexiones_cortas()
        print("Localities with connections under 15 km:", short_connections)

        print("\n--- Task 3: Connectivity Check ---")
        if self.is_connected():
            print("The graph is connected.")
        else:
            print("The graph is NOT connected.")

        print("\n--- Task 4: All Routes Without Cycles Between Two Localities ---")
        origin = input("Enter the origin locality for all routes without cycles: ")
        destination = input("Enter the destination locality for all routes without cycles: ")
        rutas = self.rutas_alternativas_sin_ciclos(origin, destination)
        print(f"All routes from {origin} to {destination} without cycles:")
        for route in rutas:
            print(" -> ".join(route))

localidades = {
    "Madrid": [("Alcorcón", 13), ("Villaviciosa de Odón", 22), ("Alcalá de Henares", 35)],
    "Villanueva de la Cañada": [("Villaviciosa de Odón", 11), ("Boadilla del Monte", 7)],
    "Alcorcón": [("Madrid", 13), ("Móstoles", 5)],
    "Móstoles": [("Alcorcón", 5), ("Fuenlabrada", 8)],
    "Fuenlabrada": [("Móstoles", 8), ("Getafe", 10)],
    "Getafe": [("Fuenlabrada", 10), ("Madrid", 16)],
    "Villaviciosa de Odón": [("Madrid", 22), ("Villanueva de la Cañada", 11)],
    "Boadilla del Monte": [("Villanueva de la Cañada", 7), ("Madrid", 15)],
    "Alcalá de Henares": [("Madrid", 35), ("Torrejón de Ardoz", 15)],
    "Torrejón de Ardoz": [("Alcalá de Henares", 15), ("Madrid", 20)]
}
if __name__ == "__main__":
    graph = Graph(localidades)

    # Benchmark specific functions
    graph.benchmark_function("ruta_mas_corta", "Madrid", "Getafe")
    graph.benchmark_function("localidades_con_conexiones_cortas")
    graph.benchmark_function("es_conexo_dfs")
    graph.benchmark_function("rutas_alternativas_sin_ciclos", "Madrid", "Getafe")
    graph.benchmark_function("ruta_mas_larga_sin_ciclos", "Madrid", "Getafe")

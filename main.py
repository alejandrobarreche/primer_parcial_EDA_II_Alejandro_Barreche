from rutas import Graph


# Assuming the Graph class and methods are defined as we discussed previously

# Initialize the graph with sample data
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

# Instantiate the Graph
graph = Graph(localidades)


def show_menu():
    print("\n--- Graph Operations Menu ---")
    print("1. Find the shortest path between two nodes")
    print("2. Check if the graph is connected")
    print("3. Find nodes with all connections under a certain distance")
    print("4. Calculate the shortest path using ")
    print("5. List localities with all connections under 15 km")
    print("6. Find all alternative routes without cycles")
    print("7. Find the longest path without cycles")
    print("8. Draw the graph")
    print("9. Execute all tasks")
    print("10. Draw graphs for timeit and memory_profiler")
    print("0. Exit")


def main():
    while True:
        show_menu()
        choice = input("Select an option (0-10): ")

        if choice == "1":
            origen = input("Enter the origin node: ")
            destino = input("Enter the destination node: ")
            path, distance = graph.shortest_path(origen, destino)
            print("Shortest path:", path, "Distance:", distance)

        elif choice == "2":
            connected = graph.is_connected()
            print("Graph is connected" if connected else "Graph is NOT connected")

        elif choice == "3":
            max_distance = int(input("Enter the maximum distance for connections: "))
            short_connection_nodes = graph.find_nodes_with_short_connections(max_distance)
            print("Nodes with short connections:", short_connection_nodes)

        elif choice == "4":
            origen = input("Enter the origin locality: ")
            destino = input("Enter the destination locality: ")
            camino, distancia_total = graph.ruta_mas_corta(origen, destino)


        elif choice == "5":
            localidades_cortas = graph.localidades_con_conexiones_cortas()


        elif choice == "6":
            origen = input("Enter the origin locality: ")
            destino = input("Enter the destination locality: ")
            rutas = graph.rutas_alternativas_sin_ciclos(origen, destino)
            print("Todas las rutas alternativas:", rutas)

        elif choice == "7":
            origen = input("Enter the origin locality: ")
            destino = input("Enter the destination locality: ")
            longest_path, longest_distance = graph.ruta_mas_larga_sin_ciclos(origen, destino)
            print("Ruta más larga:", longest_path)
            print("Distancia total:", longest_distance, "km")

        elif choice == "8":
            graph.draw_graph()

        elif choice == "9":
            graph.execute_all_tasks()

        elif choice == "10":
            graph.benchmark_function("ruta_mas_corta", "Madrid", "Getafe")
            graph.benchmark_function("localidades_con_conexiones_cortas")
            graph.benchmark_function("es_conexo_dfs")
            graph.benchmark_function("rutas_alternativas_sin_ciclos", "Madrid", "Getafe")
            graph.benchmark_function("ruta_mas_larga_sin_ciclos", "Madrid", "Getafe")

        elif choice == "0":
            print("Exiting the menu.")
            break

        else:
            print("Invalid option. Please select a number between 0 and 8.")


# Run the menu
if __name__ == "__main__":
    main()

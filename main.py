
import SSP as ssp  
def main():
    graph = ssp.SuccessiveShortestPathFlowNetwork()
    for _ in range(6):
        graph.add_node()  

    # Add edges of our graph
    graph.add_arc(0, 1, 0, 4, 1)
    graph.add_arc(0, 3, 0, 2, 5)
    graph.add_arc(1, 2, 0, 2, 1)
    graph.add_arc(1, 3, 0, 6, 1)
    graph.add_arc(2, 1, 0, 2, 1)
    graph.add_arc(2, 5, 0, 4, 0)
    graph.add_arc(3, 4, 0, 8, 1)
    graph.add_arc(4, 2, 0, 6, -3)
    graph.add_arc(4, 5, 0, 4, 1)

    result = graph.min_cost_max_flow(0, 5) 
    print(result)

if __name__ == "__main__":
    main()
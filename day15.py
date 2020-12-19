'''
This could be improved by using networkx during part 1 instead of walking back and forth repeatedly
- may be a task for a later date.
'''
class Node():
    def __init__(self, x,y, path, closed, result, goal=False):
        self.x = x
        self.y = y
        self.path = path
        self.closed = closed
        self.result = result
        self.distance = len(path)
        self.goal = goal
        self.oxygenated = False
        
    def __repr__(self):
        return "({},{})N".format(self.x,self.y)
        
def update_location(x,y,dr):
    '''Converts intcomputer-readable movement to x,y coordinates'''
    if dr==1:
        return x,y+1
    elif dr==2:
        return x,y-1
    elif dr==3:
        return x-1,y
    elif dr==4:
        return x+1,y
        
def wiggle(x,y,nodes,movement_options,reverse_movement,path,brain):
    '''Uses the intcode computer brain to visit nearby locations (adjacent to x,y), and check if they are open.
    Logs their information.'''
    # wiggle (based on x,y)
    for i in range(4):
        movement = movement_options[i]
        reverse = reverse_movement[i]

        new_x,new_y = update_location(x,y,movement)
        
        # skip node if it's been calculated before
        # might need to change to check for shorter path later
        if (new_x,new_y) in [(node.x,node.y) for node in nodes]:
            #print('skipping {},{}'.format(new_x,new_y))
            continue
        
        if new_x==0 and new_y==0:
            print('wow ok')
        current_path = path+[movement]
        # try move and find out what's there
        brain.add_input(movement)
        brain.process_code()
        result = brain.outputs[-1]
        

        # store result (if wall, empty, or goal)
        nodes.append(Node(new_x,new_y, path=current_path, closed=(result==0), 
                                                    result=result, goal=(result==2)))
        
        if result>0:
            # move back to starting location
            brain.add_input(reverse)
            brain.process_code()
            assert brain.outputs[-1]!=0
        
    return nodes
    
def part_1(brain):
    '''Fills out the list nodes by traveling to each node individually, then "wiggling" to visit each neighbor,
    while keeping track of position. Will continue until all locations have been tested.'''
    
    nodes = []
    movement_options = np.arange(1,5)
    reverse_movement = movement_options[[1,0,3,2]]

    # start at 0,0
    x,y = 0,0

    # store location
    nodes.append(Node(x,y,path=[], result=1, closed=False))
    
    max_distance = -1
    while max_distance!=max([node.distance for node in nodes]):
        max_distance = max([node.distance for node in nodes])
        
        # pick next x,y to wiggle around
        for node in nodes: 
            if node.distance==max_distance and ~node.closed:
                # move to node
                for dr in node.path:
                    brain.add_input(dr)
                    result = brain.process_code()
                    assert result!=0

                # wiggle
                nodes = wiggle(node.x,node.y,nodes,movement_options,reverse_movement,node.path,brain)

                # return to start
                for dr in node.path[::-1]:
                    brain.add_input(reverse_movement[dr-1])
                    assert brain.process_code()!=0
                    
    return nodes
    
def part_2(nodes, goal_node):
    '''Uses input list of nodes to create a graph in using networkx, then finds the furthest distance 
    from any node in the graph to the goal node'''
    import networkx as nx

    # convert nodes to dictionary
    node_guide = {(node.x,node.y):node.result for node in nodes}

    g = nx.Graph()

    # add all edges to graph
    for x,y in node_guide.keys():
        result = node_guide[(x,y)]
        
        if result==0: 
            continue

        if node_guide[(x-1,y)] == 1: 
            g.add_edge((x,y), (x-1,y))
        if node_guide[(x+1,y)] == 1: 
            g.add_edge((x,y), (x+1,y))
        if node_guide[(x,y-1)] == 1: 
            g.add_edge((x,y), (x,y-1))
        if node_guide[(x,y+1)] == 1: 
            g.add_edge((x,y), (x,y+1))

    # iterate through every location, finding the maximum number of steps from the oxygenated node
    # this is the number of minutes it will take for oxygen to fill the entire map
    num_minutes = 0
    for x, y in node_guide.keys():
        if node_guide[(x,y)]==0: 
            continue
        path_length =  len(nx.dijkstra_path(g,(goal_node.x,goal_node.y),(x,y)))
        if path_length > num_minutes:
            num_minutes = path_length
            
    return num_minutes-1
        
def main():
    with open('day15.txt', 'r') as f:
        data = np.array(f.read().strip().split(","), dtype=np.int64)
    f.close()
    
    # initialize computer
    from intComputer import IntcodeComputer

    brain = IntcodeComputer(dt=data)
    
    # part 1
    nodes = part_1(brain)
    goal_node = [node for node in nodes if node.goal][0]
    print(goal_node.distance)
    
    # part 2
    print(part_2(nodes, goal_node))

if __name__=='__main__':
    import numpy as np
    main()
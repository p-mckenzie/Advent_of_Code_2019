def part_1(connections):
    num_orbits = 0
    for key in connections.keys():
        while key in connections.keys():
            num_orbits += 1
            key = connections[key]
    return num_orbits
    
def part_2(connections):
    # calculate orbital steps from your current position to Center of Mass
    key = 'YOU'
    you_paths = []

    while key in connections.keys():
        key = connections[key]
        you_paths.append(key)
        
    # calculate orbital steps from Santa's current position to Center of Mass
    key = 'SAN'
    santa_paths = []

    while key in connections.keys():
        key = connections[key]
        santa_paths.append(key)
        
    # find the first intersection orbital mass
    intersection = [x for x in you_paths if x in santa_paths][0]
    
    # add the path you would take to get to intersection 
    ## to the path santa would take to get to intersection
    return len(you_paths[:you_paths.index(intersection)]+santa_paths[santa_paths.index(intersection)::-1])-1

def main():
    with open('day06.txt', 'r') as f:
        data = f.readlines()
    f.close()
    
    # create dictionary where key is orbiting the value
    connections = {}
    for item in data:
        orbits, orbiting = item.strip().split(')')
        connections[orbiting] = orbits
        
    print(part_1(connections))
    
    print(part_2(connections))

if __name__=='__main__':
	main()
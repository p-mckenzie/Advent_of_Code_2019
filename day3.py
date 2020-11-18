def translate_path(entry):
    # computes the axis, direction, and displacement for each path entry
    direction, distance = entry[0], int(entry[1:])
    if direction=='R':
        return 0,1,distance
    elif direction=='L':
        return 0,-1,distance
    elif direction=='U':
        return 1,1,distance
    elif direction=='D':
        return 1,-1,distance
    else:
        print("Error with entry:", entry)
        return
	
def location_formatter(x,y):
    # formats (x,y) pair as string for easier hashing
    return "{} {}".format(x,y)
	
def compute_locations(path):
    location = [0,0]
    locations = []
    
    for entry in path:
        axis,direction,displacement = translate_path(entry)

        for i in range(1, displacement+1):
            # calculate location after i steps in the current direction
            updated_location = location.copy()
            updated_location[axis] = updated_location[axis] + direction*i
            
            # store the updated location and step count to reach it
            locations.append(location_formatter(updated_location[0], updated_location[1]))

        # update location to the final (after walking all steps of the path)
        location = updated_location
        
    return locations
    
def part_1(locations_a, locations_b):
    # finds the overlapping location with the smallest manhattan distance to (0,0)
    overlap = set(locations_a).intersection(set(locations_b))

    for location in overlap:
        x,y = location.split()
        x,y = int(x), int(y)
        try:
            if abs(x)+abs(y)<min_distance:
                min_distance = abs(x)+abs(y)
                best_location = (x,y)
        except NameError:
            min_distance = abs(x)+abs(y)
            best_location = (x,y)
            
    return min_distance, sorted(overlap)

def main():
    # import data
    with open('day3.txt', 'r') as f:
        path_1, path_2 = f.read().split()
    f.close()

    path_1 = path_1.split(',')
    path_2 = path_2.split(',')
    
    # compute the locations on each path
    locations_1 = compute_locations(path_1)
    locations_2 = compute_locations(path_2)

    # part 1
    min_distance, overlap = part_1(locations_1, locations_2)
    print(min_distance)

    # part 2
    '''The index of a location in locations_x corresponds to the # of steps required to reach that location,
    starting with locations_x[0] as step #1 (hence why we add 1 to each)'''
    print(min([locations_1.index(item)+1+locations_2.index(item)+1 for item in overlap]))


if __name__=='__main__':
	main()
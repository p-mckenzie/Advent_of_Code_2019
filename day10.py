def metrics(a, b):
    # calculates distance and angle between asteroids a and b, where each is an (x,y) pair
    from numpy import sqrt
    from math import atan2
    
    slope = atan2(a[1]-b[1], a[0]-b[0])
    distance = sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    return slope, distance
    
def part_1(asteroids):
    count_visible = {}

    for i in range(len(asteroids)):
        source_asteroid = asteroids[i]

        slopes = {}
        for j in range(len(asteroids)):
            if j==i:
                continue
            target_asteroid = asteroids[j]
            slope = metrics(source_asteroid, target_asteroid)[0]

            if slope in slopes:
                slopes[slope] += 1
            else:
                slopes[slope] = 1

            #slopes.add(slope)
        count_visible[source_asteroid] = len(slopes)

    for idx, count in count_visible.items():
        if count==max(count_visible.values()):
            return idx, count
            
def create_mapping(asteroids, source_asteroid):
    from math import degrees
    mapping = {}

    # create mapping of angle -> all asteroids at that angle (including their distance from the source asteroid)
    for target_asteroid in asteroids:
        if target_asteroid==source_asteroid:
            continue

        # calculate metrics for this target
        angle, distance = metrics(source_asteroid, target_asteroid)
        angle = degrees(angle)

        # store metrics
        if angle in mapping:
            mapping[angle]['distances'].append(distance)
            mapping[angle]['asteroids'].append(target_asteroid)
        else:
            mapping[angle] = {'distances':[distance],
                             'asteroids':[target_asteroid]}

    # sort asteroids at each angle by distance (smallest to largest)
    for slope, dictionary in mapping.items():
        mapping[angle]['distances'] = sorted(dictionary['distances'])
        mapping[angle]['asteroids'] = [x for _,x in sorted(zip(dictionary['distances'],dictionary['asteroids']))]
        
    return mapping
    
def part_2(mapping):
    # hack to start from 90 degrees and go clockwise
    keys = sorted(mapping.keys())
    indexes = list(range(len(keys)))

    start_index = keys.index([key for key in keys if key>=90][0])

    delete_order = []

    for index in indexes[start_index:]+indexes[:start_index]:
        angle = keys[index]

        if angle not in mapping:
            continue

        # store the asteroid's location
        delete_order.append(mapping[angle]['asteroids'][0])

        # remove asteroid from mapping
        if len(mapping[angle]['asteroids'])>1:
            mapping[angle]['asteroids'] = mapping[angle]['asteroids'][1:]
            mapping[angle]['distances'] = mapping[angle]['distances'][1:]
        else:
            del mapping[angle]

    return delete_order[199][0]*100+delete_order[199][1]
    
def main():
    with open('day10.txt', 'r') as f:
        data = f.read().split()
    f.close()

    # transform data into list of (x,y) pairs of asteroids
    asteroids = []
    for y, row in enumerate(data):
        for x, element in enumerate(row):
            if element=='#':
                asteroids.append((x,y))

    source_asteroid, count = part_1(asteroids)
    print(count)

    mapping = create_mapping(asteroids, source_asteroid)

    print(part_2(mapping))
    
if __name__=='__main__':
    main()
def identify_locations(outputs):
    overlaps = [] # overlapping paths for part 1
    path = [] # all scaffold locations, for part 2

    for i in range(len(outputs)):
        for j in range(len(outputs[i])):
            characters = []
            
            #center
            characters.append(outputs[i][j]=='#')
            
            try:
                # north
                assert i-1>=0
                characters.append(outputs[i-1][j]=='#')
            except:
                characters.append(False)
            try:
                # south 
                assert i+1<=len(outputs)
                characters.append(outputs[i+1][j]=='#')
            except:
                characters.append(False)
            try:
                # east
                assert j+1<=len(outputs[i])
                characters.append(outputs[i][j+1]=='#')
            except:
                characters.append(False)
            try:
                # west 
                assert j-1>=0
                characters.append(outputs[i][j-1]=='#')
            except:
                characters.append(False)
                
            if outputs[i][j] not in['#','.']:
                start = (i,j)
                
            if sum(characters)==5:
                # it's 2 paths overlapping!
                overlaps.append((i,j))
            
            # store everything in path
            if characters[0]:
                path.append((i,j))
                
    return overlaps, path, start
    
def build_instructions(path, start):
    directions = [[0,1], [1,0], [0,-1], [-1,0]]

    # start drone facing down (inverted coordinates)
    start_direction = directions[3]

    # keep track of all the positions the drone has visited
    already_visited = []

    # initialize drone's position and direction
    current_y, current_x = start
    direction = start_direction

    # start the instruction list ([direction_0, length_0, direction_1, length_1, ...])
    instructions = [direction, 0]

    while len(set(path)-set(already_visited))>0:
        try:
            next_location = path.index((current_y+direction[0], current_x+direction[1]))
            # ^ if this passed, we can keep going straight
            
            # update distance (instructions[-1])
            instructions[-1] += 1
            
            # update locations
            current_y, current_x = path[next_location]
            already_visited.append((current_y,current_x))
            
        except:
            # need to turn drone
            if instructions[-1]==0:
                # drone hasn't moved in current direction - no need to store it
                instructions = instructions[:-2]
                
            try:
                # turn left 90 degrees
                direction = directions[directions.index(direction)-1]
                path.index((current_y+direction[0], current_x+direction[1]))
                instructions.append('L')
                instructions.append(direction)
                instructions.append(0)
                
                # instructions now looks like [...., [new_y_slope,new_x_slope], 0]
                continue
            except:
                try:
                    # turn right 90 degrees
                    direction = directions[directions.index(direction)-2]
                    path.index((current_y+direction[0], current_x+direction[1]))
                    instructions.append('R')
                    instructions.append(direction)
                    instructions.append(0)
                    
                    # instructions now looks like [...., [new_y_slope,new_x_slope], 0]
                    continue
                except:
                    break
                    
    return ','.join([str(x) for x in instructions if type(x)!=list])
    
def functionize(instructions):
    options = instructions.split(',')
    options = [",".join(options[i:i+2]) for i in range(0, len(options), 2)]
    
    # assemble set of all patterns in instructions, that could be made into function
    function_options = []
    for i in range(len(options)):
        for length in range(1,len(options)-i):
            slic = ','.join(options[i:i+length])
            if slic not in function_options:
                function_options.append(slic)
                
    # iterate through options, stop when we find one function combo that works
    from itertools import permutations

    for a,b,c in permutations(function_options, 3):
        cpy = instructions.replace(a, 'A').replace(b,'B').replace(c,'C')
        if 'R' not in cpy and 'L' not in cpy:
            break
            
    main = [ord(x) for x in cpy+'\n']
    a = [ord(x) for x in a+'\n']
    b = [ord(x) for x in b+'\n']
    c = [ord(x) for x in c+'\n']
    
    # check function lengths
    assert len(main)<=21 and len(a)<=21 and len(b)<=21 and len(c)<=21
    
    return main, a, b, c

def main():
    # read in data
    with open('day17.txt', 'r') as f:
        data = np.array(f.read().strip().split(','), dtype=np.int64)
    f.close()
    
    from intComputer import IntcodeComputer
    brain = IntcodeComputer(dt=data)
    
    # assemble map of scaffolds
    outputs = ''
    while True:
        output = brain.process_code()
        if output is not None:
            outputs += chr(output)
        else:
            break
            
    # split by newline character to form list of strings
    outputs = [output for output in outputs.split('\n') if len(output)>0]
    
    overlaps, path, start = identify_locations(outputs)
    
    # part 1
    print(sum([x*y for x,y in overlaps]))
    
    instructions = build_instructions(path, start)
    main, a, b, c = functionize(instructions)
    
    # wake up robot
    brain.dt[0] = 2
    # add calculated inputs to move the bot
    brain.inputs = main+a+b+c+[ord('n'), ord('\n')]
    
    # run robot until program terminates
    vals = [brain.process_code()]
    while vals[-1] is not None:
        vals.append(brain.process_code())
    # part 2
    print(vals[-2])
    
if __name__=='__main__':
    import numpy as np
    main()
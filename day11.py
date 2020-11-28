def update_direction(turn, direction):
    '''Manages clockwise/counter-clockwise turns of painting robot'''
    
    import numpy as np
    if turn==0:
        if direction[0]*direction[1]>0:
            return np.array([-direction[1], -direction[0]], dtype=np.int64)
        else:
            return np.array([-direction[1], direction[0]], dtype=np.int64)
    elif turn==1:
        if direction[0]*direction[1]<0:
            return np.array([-direction[1], -direction[0]], dtype=np.int64)
        else:
            return np.array([direction[1], -direction[0]], dtype=np.int64)
            
            
def paint_wall(dt, part_2=False):
    '''Runs the intcode computer on input instructions, outputs the painted pattern and locations 
    of all painted tiles.'''
    
    # initialize all-black board
    import numpy as np
    board = np.zeros((300,300), dtype=np.int64)
    if part_2:
        board[150,150] = 1

    # initialize computer
    from intComputer import IntcodeComputer
    
    brain = IntcodeComputer(dt=dt, inputs=[])
    location = np.array([150,150], dtype=np.int64)
    direction = np.array([0,1], dtype=np.int64)
    
    painted = set()

    while True:
        # add current color to inputs to computer
        try:
            brain.add_input(board[location[0], location[1]])
        except IndexError:
            break
        paint = brain.process_code()
        if paint is None:
            break
        turn = brain.process_code()
        if turn is None:
            break

        # update board paint
        board[location[0], location[1]] = paint

        # save where the robot has painted at least once (part 1)
        painted.add(str(location[0])+str(location[1]))

        # update location
        direction = update_direction(turn, direction)
        location = location+direction
    return board, painted
    
def main():
    import numpy as np

    with open('day11.txt', 'r') as f:
        data = np.array(f.read().split(','), dtype=np.int64)
    f.close()
    
    # part 1
    board, painted = paint_wall(data)
    print(len(painted))
    
    # part 2
    board, painted = paint_wall(data, part_2=True)

    import matplotlib.pyplot as plt

    x, y = (board>0).nonzero()

    plt.scatter(x,y, color='black')
    plt.ylim(140,155)
    plt.xlim(145,195)
    plt.show()
    
if __name__=='__main__':
    main()
import numpy as np

def step_ahead_system(time, num_moons, loc, vel):
    '''(Part 1) Steps the system ahead by "time" periods, using the provided locations 
    to update provided velocities. Returns final location & velocity per moon'''
    locations = loc.copy()
    velocities = vel.copy()
    period = np.zeros(3, dtype=np.int64)
    
    # holder for the locations/velocities at specific time
    final_output = []
    
    time_step = 0
    while (period==0).max() or len(final_output)==0:
        # calculate gravity updates to velocity
        for idx, moon_a in enumerate(locations):
            update = np.zeros(3, dtype=np.int64)
            for moon_b in np.delete(locations, idx, axis=0):
                update += moon_b-moon_a>0
                update += -1*(moon_a-moon_b>0)
            velocities[idx] += update

        # use new velocity to update position (1 time step)
        locations += velocities
        
        if time_step==time-1:
            # store the locations/velocities at specific time to return later
            final_output = [np.copy(locations), np.copy(velocities)]
            # loop should continue (if necessary) to calculate system periods
        
        # updates periods (the time interval for each axis to perform 1/2 oscillation)
        period[((velocities==0).sum(axis=0)==num_moons) & (period==0)] = time_step+1

        time_step += 1
        
    return final_output[0], final_output[1], period

def main():
    from re import findall

    # read data into numpy array
    with open('day12.txt', 'r') as f:
        data = f.read().strip()
    f.close()

    num_moons = len(data.split('\n'))
    num_steps = 1000

    locations = np.array(findall(r"[-\d]+", data),
            dtype=np.int64).reshape((num_moons,3))

    velocities = np.zeros((num_moons, 3), dtype=np.int64)
    
    # update locations and velocities after num_steps periods of time
    locations, velocities, period = step_ahead_system(num_steps, num_moons, locations, velocities)
    
    # part 1 solution (energy after num_steps periods of time)
    print(sum([np.abs(locations[idx]).sum()*np.abs(velocities[idx]).sum() for idx in range(num_moons)]))
    
    # part 2 (time required for system to repeat initial layout)
    print(2*np.lcm.reduce(period))
    
if __name__=='__main__':
    main()
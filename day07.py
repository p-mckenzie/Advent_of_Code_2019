def parse_parameters(entry):
    # extracts the action and parameters for a single instruction
    
    import numpy as np
    
    action = entry % 100
    params = np.zeros(3, dtype=np.int64)
    
    params[0] = (entry // 100) % 10
    params[1] = (entry // 1000) % 10
    params[2] = (entry // 10000) % 10
    
    return action, params
    
def process_code(dt, inputs, start=0, input_id=0):
    # performs all operations called for in the input code data (dt), using appropriate input
    
    data = dt.copy()
    
    # performs operations
    i = start
    while i<len(data):
        #print(i, data[i])
        action, params = parse_parameters(data[i])

        if action==99:
            # program terminates
            return None, i+1, data, input_id

        elif action==1:
            # addition
            if params[2]>0:
                # immediate
                print('Something went wrong!')
                break
            else:
                # position
                data[data[i+3]] = (data[data[i+1]] if params[0]==0 else data[i+1]) + (data[data[i+2]] if params[1]==0 else data[i+2])
            i += 4
            continue

        elif action==2:
            # multiplication
            if params[2]>0:
                # immediate
                print('Something went wrong!')
                break
            else:
                # position
                data[data[i+3]] = (data[data[i+1]] if params[0]==0 else data[i+1]) * (data[data[i+2]] if params[1]==0 else data[i+2])
            i += 4
            continue

        elif action==3:
            # stores input at parameter
            data[data[i+1]] = inputs[input_id]
            input_id += 1
            i += 2
            continue

        elif action==4:
            # outputs value at parameter
            if params[0]==1:
                return data[i+1], i+2, data, input_id
            else:
                return data[data[i+1]], i+2, data, input_id
        
        elif action==5:
            # jump-if-true

            # positional or instant
            if (params[0]==0 and data[data[i+1]]!=0) or (params[0]==1 and data[i+1]!=0):
                i = data[data[i+2]] if params[1]==0 else data[i+2]
            else:
                i += 3

        elif action==6:
            # jump-if-false

            if (params[0]==0 and data[data[i+1]]==0) or (params[0]==1 and data[i+1]==0):
                i = data[data[i+2]] if params[1]==0 else data[i+2]
            else:
                i += 3

        elif action==7:
            # less than

            if (data[data[i+1]] if params[0]==0 else data[i+1])<(data[data[i+2]] if params[1]==0 else data[i+2]):
                # update params[2] location to 1
                if params[2]==1:
                    # instant
                    data[i+3] = 1
                else:
                    # positional
                    data[data[i+3]] = 1
            else:
                # update params[2] location to 0
                if params[2]==1:
                    # instant
                    data[i+3] = 0
                else:
                    # positional
                    data[data[i+3]] = 0
            i += 4
            continue

        elif action==8:
            # equals
            if (data[data[i+1]] if params[0]==0 else data[i+1])==(data[data[i+2]] if params[1]==0 else data[i+2]):
                # update params[2] location to 1
                if params[2]==1:
                    # instant
                    data[i+3] = 1
                else:
                    # positional
                    data[data[i+3]] = 1
            else:
                # update params[2] location to 0
                if params[2]==1:
                    # instant
                    data[i+3] = 0
                else:
                    # positional
                    data[data[i+3]] = 0
            i += 4
            continue

        else:
            # invalid code
            print("Error at location {}, action requested #{}".format(i, action))
            break
            
def part_1(inp):
    # permutes through all configurations in [0,1,2,3,4]
    # selects the maximum output of all configurations
    from itertools import permutations
    
    outputs = []
    phase_settings = list(permutations(range(5)))

    for phase_setting in phase_settings:
        signal = 0

        for phase in phase_setting:
            signal = process_code(inp, [phase, signal])[0]

        outputs.append(signal)
        
    return max(outputs)
    
def part_2(inp):
    # permutes through all configurations in [5,6,7,8,9]
    # selects the maximum output of all configurations
    ## for each amplifier, stores code, current place, and inputs
    ## updates each in each loop (output of amp A gets appended to inputs to amp B)
    ## continues until first amp finishes (action 99, returns signal=None)
    
    from itertools import permutations
    
    final = []
    phase_settings = list(permutations(range(5,10)))

    for phases in phase_settings:
        # reset storage for "state" of each amp
        starts = [0]*5
        input_ids = [0]*5
        codes = [inp]*5
        inputs = [[phase] for phase in phases]

        signal = 0
        outputs = []

        while True:
            for i in range(len(phases)):
                # adds output from previous amp to inputs to current amp
                inputs[i].append(signal)

                # processes code with new inputs, using stored state
                signal, next_start, updated_code, next_input_id = process_code(codes[i], inputs[i], 
                                                                               start=starts[i],
                                                                              input_id=input_ids[i])

                # store state to replicate next time current amp must process inputs
                starts[i] = next_start
                codes[i] = updated_code
                input_ids[i] = next_input_id

                # check if entire program has finished
                if signal is None:
                    # save the max output that this configuration could've sent to thrusters
                    final.append(max(outputs))
                    break

            if signal is None:
                break

            # saves output from current run through all amps (could potentially go to thrusters)
            outputs.append(signal)
            
    # returns the maximum output that could've gone to an amp (from any configuration)
    return max(final)
    
def main():
    import numpy as np

    with open('day07.txt', 'r') as f:
        inp = np.array(f.read().split(','), dtype=np.int64)
    f.close()

    # call part 1
    print(part_1(inp))

    # call part 2
    print(part_2(inp))
    
if __name__=='__main__':
    main()
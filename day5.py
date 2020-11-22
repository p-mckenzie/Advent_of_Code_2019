def parse_parameters(entry):
    # extracts the action and parameters for a single instruction
    
    import numpy as np
    
    action = entry % 100
    params = np.zeros(3, dtype=np.int64)
    
    params[0] = (entry // 100) % 10
    params[1] = (entry // 1000) % 10
    params[2] = (entry // 10000) % 10
    
    return action, params
    
def process_code(dt, raw_input):
    # performs all operations called for in the input code data (dt), using appropriate input
    
    data = dt.copy()
    
    # performs operations
    i = 0
    while i<len(data):
        #print(i, data[i])
        action, params = parse_parameters(data[i])

        if action==99:
            # program terminates
            break

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
            data[data[i+1]] = raw_input
            i += 2
            continue

        elif action==4:
            # outputs value at parameter
            if params[0]==1:
                print('Returns {} at i={}'.format(data[i+1], i))
            else:
                print('Returns {} at i={}'.format(data[data[i+1]], i))
            i += 2
            continue

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
            
def main():
    import numpy as np

    with open('day5.txt', 'r') as f:
        inp = np.array(f.read().split(','), dtype=np.int64)
    f.close()

    # part 1
    process_code(inp, 1)

    # part 2
    process_code(inp, 5)
    
if __name__=='__main__':
    main()
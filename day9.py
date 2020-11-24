def parse_parameters(entry):
    # extracts the action and parameters for a single instruction
    
    import numpy as np
    
    action = entry % 100
    params = np.zeros(3, dtype=np.int64)
    
    params[0] = (entry // 100) % 10
    params[1] = (entry // 1000) % 10
    params[2] = (entry // 10000) % 10
    
    return action, params
    
def process_code(dt, inputs, start=0, input_id=0, relative_base=0):
    import numpy as np
    # performs all operations called for in the input code data (dt), using appropriate input
    if len(dt)<1000:
        data = np.concatenate((dt.copy(), np.zeros(1000, dtype=np.int64)))
    else:
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
            if params[2]==0:
                # position
                data[data[i+3]] = (data[data[i+1]] if params[0]==0 else data[i+1] if params[0]==1 else data[data[i+1]+relative_base]) + (data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+relative_base])
            elif params[2]==2:
                # relative
                data[data[i+3]+relative_base] = (data[data[i+1]] if params[0]==0 else data[i+1] if params[0]==1 else data[data[i+1]+relative_base]) + (data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+relative_base])
            else:
                print("Tried to add to instant mode! at {}".format(i))
            i += 4

        elif action==2:
            # multiplication
            if params[2]==0:
                # position
                data[data[i+3]] = (data[data[i+1]] if params[0]==0 else data[i+1] if params[0]==1 else data[data[i+1]+relative_base]) * (data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+relative_base])
            elif params[2]==2:
                # relative
                data[data[i+3]+relative_base] = (data[data[i+1]] if params[0]==0 else data[i+1] if params[0]==1 else data[data[i+1]+relative_base]) * (data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+relative_base])
            else:
                print("Tried to multiply to instant mode! at {}".format(i))
            i += 4

        elif action==3:
            # stores input at parameter
            if params[0]==1:
                # instant
                print("Should never write in immediate mode! at {}".format(i))
            elif params[0]==2:
                # relative
                data[data[i+1]+relative_base] = inputs[input_id]
            else:
                # positional
                data[data[i+1]] = inputs[input_id]
            input_id += 1
            i += 2

        elif action==4:
            # outputs value at parameter
            if params[0]==1:
                print("Ouputs {} at {}".format(data[i+1], i))
                #return data[i+1], i+2, data, input_id
            elif params[0]==2:
                print("Ouputs {} at {}".format(data[data[i+1]+relative_base], i))
                #return data[data[i+1]+relative_base], i+2, data, input_id
            else:
                print("Ouputs {} at {}".format(data[data[i+1]], i))
                #return data[data[i+1]], i+2, data, input_id
            i += 2
        
        elif action==5:
            # jump-if-true

            # positional or instant
            if (params[0]==0 and data[data[i+1]]!=0) or (params[0]==1 and data[i+1]!=0) or (params[0]==2 and data[data[i+1]+relative_base]!=0):
                i = data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+relative_base]
            else:
                i += 3

        elif action==6:
            # jump-if-false

            if (params[0]==0 and data[data[i+1]]==0) or (params[0]==1 and data[i+1]==0) or (params[0]==2 and data[data[i+1]+relative_base]==0):
                i = data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+relative_base]
            else:
                i += 3

        elif action==7:
            # less than
            if (data[data[i+1]] if params[0]==0 else data[i+1] if params[0]==1 else data[data[i+1]+relative_base])<(data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+relative_base]):
                # update params[2] location to 1
                if params[2]==1:
                    # instant
                    print("Tried to write in instant mode at {}".format(i))
                elif params[2]==2:
                    # relative
                    data[data[i+3]+relative_base] = 1
                else:
                    # positional
                    data[data[i+3]] = 1
            else:
                # update params[2] location to 0
                if params[2]==1:
                    # instant
                    print("Tried to write in instant mode at {}".format(i))
                elif params[2]==2:
                    # relative
                    data[data[i+3]+relative_base] = 0
                else:
                    # positional
                    data[data[i+3]] = 0
            i += 4

        elif action==8:
            # equals
            if (data[data[i+1]] if params[0]==0 else data[i+1] if params[0]==1 else data[data[i+1]+relative_base])==(data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+relative_base]):
                # update params[2] location to 1
                if params[2]==1:
                    # instant
                    print("Tried to write in instant mode at {}".format(i))
                elif params[2]==2:
                    # relative
                    data[data[i+3]+relative_base] = 1
                else:
                    # positional
                    data[data[i+3]] = 1
            else:
                # update params[2] location to 0
                if params[2]==1:
                    # instant
                    #data[i+3] = 0
                    print("Tried to write in instant mode at {}".format(i))
                elif params[2]==2:
                    # relative
                    data[data[i+3]+relative_base] = 0
                else:
                    # positional
                    data[data[i+3]] = 0
            i += 4
            
        elif action==9:
            # adjust relative base (supporting parameter modes)
            #if params[0]!=0 and params[0]!=1:
            #    print(i)
            relative_base += data[data[i+1]] if params[0]==0 else data[i+1] if params[0]==1 else data[data[i+1]+relative_base]
            i += 2

        else:
            # invalid code
            print("Error at location {}, action requested #{}".format(i, action))
            break
    
def main():
    import numpy as np

    with open('day9.txt', 'r') as f:
        data = np.array(f.read().strip().split(','), dtype=np.int64)
    f.close()
    
    # part 1
    process_code(data, [1])
    
    # part 2
    process_code(data, [2])
    
if __name__=='__main__':
    main()
class IntcodeComputer():
    def __init__(self, dt, inputs=[], start=0, input_id=0, relative_base=0, vocal=False):
        import numpy as np
        self.dt = np.concatenate((dt, np.zeros(3000, dtype=np.int64)))
        self.inputs = inputs
        self.start = start
        self.input_id = input_id
        self.relative_base = relative_base
        self.vocal = vocal
        
    def parse_parameters(self, entry):
        # extracts the action and parameters for a single instruction

        import numpy as np

        action = entry % 100
        params = np.zeros(3, dtype=np.int64)

        params[0] = (entry // 100) % 10
        params[1] = (entry // 1000) % 10
        params[2] = (entry // 10000) % 10

        return action, params
    
    def add_input(self, inp):
        self.inputs.append(inp)
        return
    
    def process_code(self):
        import numpy as np
        # performs all operations called for in the input code data (dt), using appropriate input
        data = self.dt.copy()

        # performs operations
        i = self.start
        input_id = self.input_id
        
        while i<len(data):
            #print(i, data[i])
            action, params = self.parse_parameters(data[i])

            if action==99:
                # program terminates
                if self.vocal:
                    print("Program terminated")
                self.start = i+1
                self.dt = data
                self.input_id = input_id
                
                return

            elif action==1:
                # addition
                if params[2]==0:
                    # position
                    data[data[i+3]] = (data[data[i+1]] if params[0]==0 else data[i+1] if params[0]==1 else data[data[i+1]+self.relative_base]) + (data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+self.relative_base])
                elif params[2]==2:
                    # relative
                    data[data[i+3]+self.relative_base] = (data[data[i+1]] if params[0]==0 else data[i+1] if params[0]==1 else data[data[i+1]+self.relative_base]) + (data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+self.relative_base])
                else:
                    if self.vocal:
                        print("Tried to add to instant mode! at {}".format(i))
                i += 4

            elif action==2:
                # multiplication
                if params[2]==0:
                    # position
                    data[data[i+3]] = (data[data[i+1]] if params[0]==0 else data[i+1] if params[0]==1 else data[data[i+1]+self.relative_base]) * (data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+self.relative_base])
                elif params[2]==2:
                    # relative
                    data[data[i+3]+self.relative_base] = (data[data[i+1]] if params[0]==0 else data[i+1] if params[0]==1 else data[data[i+1]+self.relative_base]) * (data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+self.relative_base])
                else:
                    if self.vocal:
                        print("Tried to multiply to instant mode! at {}".format(i))
                i += 4

            elif action==3:
                # stores input at parameter
                if params[0]==1:
                    # instant
                    if self.vocal:
                        print("Should never write in immediate mode! at {}".format(i))
                elif params[0]==2:
                    # relative
                    data[data[i+1]+self.relative_base] = self.inputs[input_id]
                else:
                    # positional
                    data[data[i+1]] = self.inputs[input_id]
                input_id += 1
                i += 2

            elif action==4:
                # outputs value at parameter
                if params[0]==1:
                    if self.vocal:
                        print("Ouputs {} at {}".format(data[i+1], i))
                    self.start = i+2
                    self.dt = data
                    self.input_id = input_id
                    return data[i+1]
                
                elif params[0]==2:
                    if self.vocal:
                        print("Ouputs {} at {}".format(data[data[i+1]+self.relative_base], i))
                    self.start = i+2
                    self.dt = data
                    self.input_id = input_id
                    return data[data[i+1]+self.relative_base]
                else:
                    if self.vocal:
                        print("Ouputs {} at {}".format(data[data[i+1]], i))
                    self.start = i+2
                    self.dt = data
                    self.input_id = input_id
                    return data[data[i+1]]
                i += 2

            elif action==5:
                # jump-if-true

                # positional or instant
                if (params[0]==0 and data[data[i+1]]!=0) or (params[0]==1 and data[i+1]!=0) or (params[0]==2 and data[data[i+1]+self.relative_base]!=0):
                    i = data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+self.relative_base]
                else:
                    i += 3

            elif action==6:
                # jump-if-false

                if (params[0]==0 and data[data[i+1]]==0) or (params[0]==1 and data[i+1]==0) or (params[0]==2 and data[data[i+1]+self.relative_base]==0):
                    i = data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+self.relative_base]
                else:
                    i += 3

            elif action==7:
                # less than
                if (data[data[i+1]] if params[0]==0 else data[i+1] if params[0]==1 else data[data[i+1]+self.relative_base])<(data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+self.relative_base]):
                    # update params[2] location to 1
                    if params[2]==1:
                        # instant
                        if self.vocal:
                            print("Tried to write in instant mode at {}".format(i))
                    elif params[2]==2:
                        # relative
                        data[data[i+3]+self.relative_base] = 1
                    else:
                        # positional
                        data[data[i+3]] = 1
                else:
                    # update params[2] location to 0
                    if params[2]==1:
                        # instant
                        if self.vocal:
                            print("Tried to write in instant mode at {}".format(i))
                    elif params[2]==2:
                        # relative
                        data[data[i+3]+self.relative_base] = 0
                    else:
                        # positional
                        data[data[i+3]] = 0
                i += 4

            elif action==8:
                # equals
                if (data[data[i+1]] if params[0]==0 else data[i+1] if params[0]==1 else data[data[i+1]+self.relative_base])==(data[data[i+2]] if params[1]==0 else data[i+2] if params[1]==1 else data[data[i+2]+self.relative_base]):
                    # update params[2] location to 1
                    if params[2]==1:
                        # instant
                        if self.vocal:
                            print("Tried to write in instant mode at {}".format(i))
                    elif params[2]==2:
                        # relative
                        data[data[i+3]+self.relative_base] = 1
                    else:
                        # positional
                        data[data[i+3]] = 1
                else:
                    # update params[2] location to 0
                    if params[2]==1:
                        # instant
                        #data[i+3] = 0
                        if self.vocal:
                            print("Tried to write in instant mode at {}".format(i))
                    elif params[2]==2:
                        # relative
                        data[data[i+3]+self.relative_base] = 0
                    else:
                        # positional
                        data[data[i+3]] = 0
                i += 4

            elif action==9:
                # adjust relative base (supporting parameter modes)
                self.relative_base += data[data[i+1]] if params[0]==0 else data[i+1] if params[0]==1 else data[data[i+1]+self.relative_base]
                i += 2

            else:
                # invalid code
                if self.vocal:
                    print("Error at location {}, action requested #{}".format(i, action))
                break
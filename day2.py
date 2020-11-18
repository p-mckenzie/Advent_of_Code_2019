def process_code(data):
	# performs operations
    i = 0
    while i<len(data):
        action = data[i]

        if action==99:
            # program terminates
            break
        elif action==1:
            # addition
            data[data[i+3]] = data[data[i+1]]+data[data[i+2]]
        elif action==2:
            # multiplication
            data[data[i+3]] = data[data[i+1]]*data[data[i+2]]        
        else:
            # invalid code
            print("Error at location {}, action requested #{}".format(i, action))
            break
        i += 4
        
    return data[0]
	
def part_1(input_data):
    # outputs answer to part 1
    data = input_data.copy()
    data[1] = 12
    data[2] = 2
    
    return process_code(data)
	
def part_2(input_data, goal):
    # grid search for appropriate parameters
	# outputs answer to part 2
    for noun in range(100):
        for verb in range(100):    
            data = input_data.copy()
            data[1] = noun
            data[2] = verb
            
            if process_code(data)==goal:
                return 100*noun + verb

def main():
	# import data, call the functions
    with open('day2.txt', 'r') as f:
        data = np.array(f.read().split(','), dtype=np.int64)
    f.close()

    print(part_1(data))

	# number is a custom parameter provided by the challenge website
    print(part_2(data), 19690720)


if __name__=='__main__':
	main()
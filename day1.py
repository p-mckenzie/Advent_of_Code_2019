def fuel_required(data):
    # calculate fuel requirement and set minumum
    fuel = data//3-2
    fuel[fuel<0] = 0
    
    return fuel
	
def part_1(data):
	# provides the answer to part 1
    return sum(fuel_required(data))
	
def part_2(data):
	# provides the answer to part 2
    fuel_requirement = 0
    mass = data.copy()

    while (mass!=0).max():
        mass = fuel_required(mass)
        fuel_requirement += mass

    return sum(fuel_requirement)

def main():
	# import data, call functions for part 1 and part 2 answers
    import numpy as np
    
    with open('day1.txt', 'r') as f:
        data = np.array(f.read().split(), dtype=np.int64)
    
    f.close()
    
    print(part_1(data))
    
    print(part_2(data))


if __name__=='__main__':
	main()
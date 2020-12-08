def valid_1(num):
    '''Checks for monotonically increasing sequence, with at least one duplicated 
    pair of sequential numbers'''
    
    num = str(num)
    duplicated = False
    for i in range(1, len(num)):
        # find at least one duplicated sequence
        if num[i-1]==num[i]:
            duplicated = True
            
        # check sequence is monotonically increasing
        if num[i-1]>num[i]:
            return False
        
    # return whether sequence met requirements
    return duplicated
	
def valid_2(num):
    '''Checks for monotonically increasing sequence, with at least one duplicated (and no longer than 2) 
    pair of sequential numbers'''
    num = str(num)
    duplicated = False
    
    counts = [0]*10
    for i in range(0, len(num)):
        # record what # the current character is
        counts[int(num[i])] += 1
        
        # find at least one duplicated sequence
        if i>0:
            if num[i-1]==num[i]:
                duplicated = True
            # check sequence is monotonically increasing
            if num[i-1]>num[i]:
                return False
        
    # return whether sequence met requirements
    return (duplicated and (2 in counts))
	
def main():
    # import data
    with open('day04.txt', 'r') as f:
        bottom, top = f.read().split('-')
        bottom, top = int(bottom), int(top)
    f.close() 
    
    # part 1
    print(sum([valid_1(number) for number in range(bottom, top)]))
    
    # part 2
    print(sum([valid_2(number) for number in range(bottom, top)]))


if __name__=='__main__':
	main()
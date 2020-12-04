def phase(sig, pat):
    '''performs row dot product of expanded pattern against input signal'''
    sums = np.array([sum(sig*np.tile(np.repeat(pat, i+1),(len(sig)//(4*(i+1))+1))[1:sig.shape[0]+1]) 
                         for i in range(sig.shape[0])])
    return np.abs(sums) % 10
    
def part_1(txt):
    input_signal = np.array(list(txt), dtype=np.int64)
    pattern = np.array([0,1,0,-1], dtype=np.int64)
    
    signal = input_signal.copy()
    for i in range(100):
        signal = phase(signal, pattern)

    return ''.join(signal.astype(str)[:8])
    
def part_2(txt):
    # could be made more efficient, perhaps by using all arrays instead of converting 
    # to string and back - maybe later
    full_input = txt*10000

    # only store offset onward (memory and compute hack)
    signal = full_input[int(full_input[0:7]):]

    for phase in range(100):
        # update progress
        #if phase%10==0:
        #    print(phase)

        # compute sum of all digits, and first digit
        total = np.array(list(signal), dtype=np.int64).sum()
        string = str(total%10)

        for i in range(1, len(signal)):
            # subtract each digit incrementally, take modulo for result
            total -= int(signal[i-1])
            string += str(total%10)

        # store result before moving on
        signal = string

    return signal[0:8]
    
def main():
    with open('day16.txt', 'r') as f:    
        # expand input 10000x as requested
        txt = f.read().strip()
    f.close()

    print(part_1(txt))
    print(part_2(txt))
    
if __name__=='__main__':
    import numpy as np
    main()
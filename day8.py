def part_1(data, slices):
    # find cutoffs for evenly-sized slices of pixels (layers)
    num_zeros = []

    # iterate through layers, store how many zeros are in each layer
    for i in range(1, len(slices)):
        num_zeros.append(sum(data[slices[i-1]:slices[i]]==0))

    # find layer with least # of zeros
    important_layer = num_zeros.index(min(num_zeros))

    return (data[slices[important_layer]:slices[important_layer+1]]==1).sum() * (data[slices[important_layer]:slices[important_layer+1]]==2).sum()

def part_2(data, slices, input_size):
    # displays the image created by combining layers
    
    import numpy as np
    display = np.repeat(2, input_size[0]*input_size[1])
    
    # iterate from top layer to bottom layer
    for i in range(len(slices)-1, 0, -1):
        layer = data[slices[i-1]:slices[i]]

        display = np.where((display!=layer)&(layer!=2), layer, display)
        
    from PIL import Image

    w, h = input_size
    data = np.zeros((w, h, 3), dtype=np.uint8)
    data[:,:,0] = display.reshape(input_size)*255
    img = Image.fromarray(data, 'RGB')
    img.show()
    
def main():
    import numpy as np

    with open('day8.txt', 'r') as f:
        data = np.array(list(f.read().strip()), dtype=np.int64)
    f.close()

    input_size = (6,25)
    slices = list(range(0,len(data)+1, input_size[0]*input_size[1]))

    print(part_1(data, slices))

    part_2(data, slices, input_size)
    
if __name__=='__main__':
    main()
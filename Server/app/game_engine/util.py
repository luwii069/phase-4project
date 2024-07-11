
conv_1=["A","B","C","D","E","F","G","H"]
conv_2={
    'A':0,
    'B':1,
    'C':2,
    'D':3,
    'E':4,
    'F':5,
    'G':6,
    'H':7
}

def toHumanCordinates(arr):
    new_arr=[]
    for el in arr:
        x_cor=int(el['x'])
        conv_cor=conv_1[x_cor]
        new_arr.append(f"{conv_cor}{el['y']+1}")
        
    return new_arr

def toPcCordinates(str):
    arr=[]
    for char in str:
        arr.append(char)
    x=conv_2[arr[0]]
    y=int(arr[1])-1
    print(f"x={x} y={y}")
    return {'x':x, 'y':y}
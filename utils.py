
def get_weight(binary_values: list):
    """Calcula segmento peso para valor binário"""
    sum=0

    for i in range(len(binary_values)):
        x = binary_values[i]*(2**-(i+1))
        sum+=x

    return sum

if __name__=="__main__":

    lst = [1,1,1,1,0,0]
    get_weight(lst)
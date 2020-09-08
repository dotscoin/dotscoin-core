
def bestblock(merkle_roots=[]):
    key_value=dict()
    max=[]
    for i,merkle_root in enumerate(merkle_roots):
        
        if not merkle_root in key_value.keys():
            key_value[merkle_root]=1
        else:
            key_value[merkle_root] += 1
                        
    for key in key_value.keys():
        max.append(key_value[key])
        max.sort(reverse=True)
    for key in key_value.keys():
         if key_value[key] == max[0]:
           print(key)
           return key
bestblock(['hello','hello','there','there','hi','hi','hi'])
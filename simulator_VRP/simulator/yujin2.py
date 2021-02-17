import matplotlib.pyplot as plt
def find_coord(node_num):

    if node_num == 0:
        return 0.2269, 0.0710
    elif node_num == 1:
        return 0.7061, 0.3116
    elif node_num == 2:
        return 0.4412, 0.9985  
    elif node_num == 3:
        return 0.2660, 0.0143  
    elif node_num == 4:
        return 0.2090, 0.7717  
    elif node_num == 5:
        return 0.4854, 0.0801  
    elif node_num == 6:
        return 0.0146, 0.5719  

def find_distance(node1,node2):
    x1, y1 = find_coord(node1)
    x2, y2 = find_coord(node2)
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5
def find_total(route):
    dist1 = find_distance(0,route[0])
    dist2 = find_distance(route[0],route[1])
    dist3 = find_distance(route[1],route[2])
    dist4 = find_distance(route[2],route[3])
    dist5 = find_distance(route[3],route[4])
    dist6 = find_distance(route[4],route[5])
    dist7 = find_distance(route[5],0)
    total = dist1 + dist2 +dist3 +dist4 +dist5 +dist6 +dist7
    return total
route = [1,2,3,4,5,6]

result = []
for i in range(6):
    for j in range(6):
        if i == j:
            continue
        tmp_route = [route[0], route[1] ,route[2], route[3], route[4], route[5]]
        tmp_route[i], tmp_route[j] = tmp_route[j], tmp_route[i] 
        if find_total(route) > find_total(tmp_route):
            result.append(find_total(tmp_route))
            route = tmp_route

plt.plot(result)
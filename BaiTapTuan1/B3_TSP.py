import heapq


def calc_min_out(thanh_pho):
    n=len(thanh_pho)
    return [min(thanh_pho[i][j] for j in range(n) if j!=i) for i in range(n)]

def calc_lower_bound(cost_Current,path_Current,visited,min_out):
    lowerbound=cost_Current+min_out[path_Current[-1]]
    for v in range(len(min_out)):
        if not visited[v]:
            lowerbound+=min_out[v]
    return lowerbound

def tsp_main(thanh_pho):
    n=len(thanh_pho)
    if n==1:
        return 0,[0,0]
    result=float('inf')
    best_path=[]
    min_out=calc_min_out(thanh_pho)

    visited_goc=[False]*n
    visited_goc[0]=True
    pq=[]
    heapq.heappush(pq,(calc_lower_bound(0,[0],visited_goc,min_out),0,[0],visited_goc))

    while len(pq)>0:
        lowerbound_Current, cost_Current, path_Current, visited_Current=heapq.heappop(pq)
        if lowerbound_Current>=result:
            continue
        if len(path_Current)==n:
            sum_cost=cost_Current+thanh_pho[path_Current[-1]][0]
            if sum_cost<result:
                result=sum_cost
                best_path=path_Current+[0]
            continue
        for v in range(n):
            if visited_Current[v]:
                continue
            cost_New=cost_Current+thanh_pho[path_Current[-1]][v]
            path_New=path_Current+[v]
            visited_New=visited_Current[:]
            visited_New[v]=True
            lowerbound_new=calc_lower_bound(cost_New,path_New,visited_New,min_out)
            if lowerbound_new<result:
                heapq.heappush(pq,(lowerbound_new,cost_New,path_New,visited_New))
    return result,best_path

n = int(input("Nhap vao so luong thanh pho: "))
thanh_pho=[]
for i in range(n):
    hang=[int(x) for x in input().split()]
    thanh_pho.append(hang)
result,path=tsp_main(thanh_pho)
print("Duong di ngan nhat la",path)
print("Tong do dai duong di la",result)

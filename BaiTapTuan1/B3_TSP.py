import math
import heapq


def calc_lower_bound_ban_dau(thanh_pho):
    sum_all_path=0
    for hang in thanh_pho:
        hang_sorted=sorted(hang)
        for i in range(1,3):
            sum_all_path+=hang_sorted[i]
    return math.ceil(sum_all_path/2)

def tsp_main(thanh_pho):
    n=len(thanh_pho)
    result=float('inf')
    best_path=[]
    lowerbound_goc=calc_lower_bound_ban_dau(thanh_pho)

    pq=[]
    heapq.heappush(pq,(lowerbound_goc,0,[0]))

    while len(pq)>0:
        lowerbound_Current, cost_Current, path_Current=heapq.heappop(pq)
        if lowerbound_Current>=result:
            continue
        if len(path_Current)==n:
            sum_cost=cost_Current+thanh_pho[path_Current[-1]][0]
            if sum_cost<result:
                result=sum_cost
                best_path=path_Current+[0]
            continue
        for v in range(n):
            if v in path_Current:
                continue
            cost_New=cost_Current+thanh_pho[path_Current[-1]][v]
            path_New=path_Current+[v]
            hang_v=thanh_pho[v]
            hang_u=thanh_pho[path_Current[-1]]
            hang_u_sorted=sorted(hang_u)
            hang_v_sorted=sorted(hang_v)
            lowerbound_new=math.ceil(lowerbound_Current+thanh_pho[path_Current[-1]][v]-(hang_v_sorted[2]+hang_u_sorted[2])/2)
            heapq.heappush(pq,(lowerbound_new,cost_New,path_New))
        pass
    return result,best_path

n = int(input("Nhap vao so luong thanh pho: "))
thanh_pho=[]
for i in range(n):
    hang=[int(x) for x in input().split()]
    thanh_pho.append(hang)
result,path=tsp_main(thanh_pho)
print("Duong di ngan nhat la",path)
print("Tong do dai duong di la",result) 
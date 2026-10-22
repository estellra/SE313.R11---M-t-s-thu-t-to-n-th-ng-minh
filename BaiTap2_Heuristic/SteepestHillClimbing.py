h={}
ke={}
duong_di=[]
tim_thay=False

def in_ket_qua():
    if tim_thay:
        print(f"\n--- Duong di tim duoc ({len(duong_di)-1} buoc) ---")
    else:
        print(f"\n--- Khong tim duoc duong di, bi ket tai {duong_di[-1]} ---")
    for u in duong_di:
        print(f"Dinh {u}: h={h[u]}")
    print()

def leo_doi_doc_dung(start, goal):
    global tim_thay
    u=start
    duong_di.append(u)
    while u!=goal:
        tot_nhat=None
        for v in ke[u]:
            if tot_nhat is None or h[v]<h[tot_nhat]:
                tot_nhat=v
        if tot_nhat is None or h[tot_nhat]>=h[u]:
            return
        u=tot_nhat
        duong_di.append(u)
    tim_thay=True

print("Nhap heuristic cua tung dinh (dinh h), dong trong de ket thuc:")
while True:
    dong=input().split()
    if not dong:
        break
    h[dong[0]]=float(dong[1])
    ke[dong[0]]=[]

print("Nhap cac canh (u v chi_phi), dong trong de ket thuc:")
while True:
    dong=input().split()
    if not dong:
        break
    u, v=dong[0], dong[1]
    while u not in h or v not in h:
        print("Dinh chua co heuristic, nhap lai.")
        u, v=input().split()[:2]
    ke[u].append(v)

start=input("Nhap dinh bat dau: ").strip()
goal=input("Nhap dinh dich: ").strip()

leo_doi_doc_dung(start, goal)
in_ket_qua()
print(f"Duong di: {' -> '.join(duong_di)}")

so_nghiem=0

def in_ket_qua():
    global so_nghiem
    so_nghiem+=1
    print(f"--- Loi giai {so_nghiem} ---")
    for i in range(1, n+1):
        dong=["." for _ in range(n)]
        dong[h[i]-1]="Q"
        print(" ".join(dong))
    print()

def Try(i):
    for j in range(1, n+1):
        if not a[j] and not b[i+j] and not c[i-j+n]:
            h[i]=j
            a[j]=b[i+j]=c[i-j+n]=True
            if i==n:
                in_ket_qua()
            else:
                Try(i+1)
            a[j]=b[i+j]=c[i-j+n]=False

n=int(input("Nhap n (So quan hau & kich thuoc ban co): "))

h=[0]*(n+1)
a=[False]*(n+1)
b=[False]*(2*n+1)
c=[False]*(2*n+1)

Try(1)
print(f"Tong so loi giai tim duoc: {so_nghiem}")
n=0
danh_sach=[]
ket_qua=[]

def in_ket_qua():
    print(f"\n--- Danh sach cong viec duoc chon ({len(ket_qua)} cong viec) ---")
    for stt, start, end in ket_qua:
        print(f"Cong viec {stt}: [{start} -> {end}]")
    print()

def tham_lam():
    danh_sach.sort(key=lambda x: x[2])
    
    last_end=-float('inf')
    for cv in danh_sach:
        stt, start, end=cv
        if start>=last_end:
            ket_qua.append(cv)
            last_end=end

n = int(input("Nhap so luong cong viec n: "))

print("Nhap gio bat dau va ket thuc cua tung cong viec (start end):")
for i in range(1, n+1):
    start, end=map(int, input(f"Cong viec {i}: ").split())
    danh_sach.append((i, start, end))

tham_lam()
in_ket_qua()
print(f"Tong so cong viec thuc hien duoc toi da: {len(ket_qua)}")
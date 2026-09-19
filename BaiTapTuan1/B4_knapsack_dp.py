
def dp_main(weight,value,w):
  n=len(weight)
  dp = [[0]*(w+1) for _ in range (n+1)]

  for i in range (1,n+1):
      for j in range (w+1):
         if weight[i-1]>j:
            dp[i][j]=dp[i-1][j]
            continue
         dp[i][j]=max(dp[i-1][j],value[i-1]+dp[i-1][j-weight[i-1]])

  item=[]
  weight_bag=w
  for i in range (n,0,-1):
      if dp[i][weight_bag]==dp[i-1][weight_bag]:
         continue
      item.append(i-1)
      weight_bag-=weight[i-1]

  item.reverse() 
  return dp[n][w],item 




w=int(input("Nhap vao suc chua cua balo: "))
n=int(input("Nhap vao so luong vat pham: "))
weight=[]
value=[]
print("Hay nhap lan luot trong luong cho cac vat pham")
weight=[int(x) for x in input().split()]
print("Hay nhap lan luot gia tri cua cac vat pham")
value=[int(x) for x in input().split()]


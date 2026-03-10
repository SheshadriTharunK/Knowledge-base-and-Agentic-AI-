# n = 4
# l = []
# for i in range(n):
#     start, end, profit = map(int,input().split())
#     l.append((start,end,profit)) 
l = [[1,2,50],[3,5,20],[6,19,10],[2,100,200]]
if len(l)==1: 
    print(l[0][2])
m = [k[0] for k in l]
for s in l:
        if s[1] in m: 
            for i in l:
                if s[1] == i[0]: 
                    if s[2] > i[2]:
                        s.remove(i)
print(l)                
s1, e1, p1 = l[0][0], l[0][1], l[0][2]
for i, j, k in l:
    if i < s1 and j > e1: 
        s1, e1, p1 = i, j, k 
print(s1,e1,p1)
if s1 != l[0][0] and  e1 != l[0][1]:
    print(p1)             
sum = 0 
for i in l:
    sum = sum + i[2]
print(sum) 

    
# Test Case 1:
# Input:
# 4
# 1 2 50
# 3 5 20
# 6 19 10
# 2 100 200
# Expected output: 200
# Explanation : Combination: (2, 100, 200)
# Test Case 2
# Input:
# 3
# 1 2 20
# 3 4 30
# 5 6 25
# Expected output: 75
# Explanation : Combination: (1, 2, 20) + (3, 4, 30) + (5, 6, 25)
# Test Case 3
# Input:
# 3
# 1 2 10
# 2 3 20
# 3 4 30
# Expected output: 40
# Explanation : Combination: (1, 2, 10) + (3, 4, 30)
# Test Case 4
# Input:
# 5
# 1 3 50
# 3 5 20
# 4 6 70
# 6 7 60
# 8 9 30
# Expected output: 150
# Explanation : Combination: (1, 3, 50) + (4, 6, 70) + (8, 9, 30)
# Test Case 5:
# Input:
# 1
# 5 10 99
# Expected output: 99
# Explanation : Combination: (5, 10, 99)
# Test Case 6:
# Input:
# 6
# 1 4 70
# 2 3 60
# 4 6 70
# 5 8 120
# 7 9 60
# 10 11 30
# Expected output: 220
# Explanation : Combination: (1, 4, 70) + (5, 8, 120) + (10, 11, 30) or (2, 3, 60) + (4, 6, 70) + (7, 9, 60) + (10, 11, 30)
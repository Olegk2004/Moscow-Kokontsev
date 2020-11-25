a = '1' * 101
k = 1
while '111' in a:
    print(a)
    a.replace('111', '22', 1)
    #a.replace('222', '11', 1)
    k+=1
print(a)
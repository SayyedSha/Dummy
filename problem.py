from random import randint
import re
def rec (a,n):
    return (a+n)    
def rec1 (a,n):
    return (a-n)
    
def rec2(a,n):
    return a*n
def rec3(a,n):
    return a/n
user = input("Enter values: ")
main = list(user)
list1= map(int, re.split('\+|\-|\*|\/', user))
list2 = list(list1)
sym =[]
total = 0
list_size = len(list2)
finall = [total]
for i in list2:
    print(list2)
    break
for i in range(len(main)):
    if (main[i].isdigit()):
        continue
    else:
        sym.append(main[i])
for i in list2: 
    for j in sym:
        for k in finall:
            if j =="+":
                total = rec(k,i)
                finall=[total]
                
            elif j=="-":
                total =  rec1(k,i)
                finall=[total]
            
            elif j=="*":
                total =  rec2(k,i)
                finall=[total]
                
            elif j=="/":
                total =  rec3(k,i)
                finall=[total]
                    
print(finall)                        

from telnetlib import SUPDUP
from pysat.formula import CNF
from pysat.solvers import Solver
import csv



test_case=input("test_case no.:")
k=input("value of k is=")
k=int(k)

def pair(raw):
    if(raw<k*k):
        return 1
    
    if(raw>k*k-1):
        return 2



def lit(k,pair,raw,col,no):
    if(pair==1):
        return ((k**4)*(no-1))+((k*k)*raw)+col+1
    if(pair==2):
        return (k**6)+(k**4)*(no-1)+((k*k)*(raw-k*k))+col+1

input="sudoku"+test_case
sudoku_1=list(csv.reader(open(input+".csv")))

cnf=CNF()

# input from csv file is in str form
for r in range(2*k*k):
    for c in range(k*k):
        sudoku_1[r][c]=int(sudoku_1[r][c])

        
# total (16*4)*2=128 
# 1-16 are bollean for value 1, 17-32 are for value 2,...same in 2nd of sudoku pair 65-80 are for 1,...

for r in range(2*k*k):
    for c in range(k*k):
        if(sudoku_1[r][c]!=0):
            cnf.append([lit(k,pair(r),r,c,sudoku_1[r][c])])

            for i in range(1,k*k+1):
                if(i!=sudoku_1[r][c]):
                    cnf.append([-lit(k,pair(r),r,c,i)])
            
                 
# not same no. in any column 
for r in range(k*k):
    for n in range(1,k*k+1):
        for cc in range(k*k-1):
            for ccc in range(cc+1,k*k):
                cnf.append([-lit(k,pair(r),r,cc,n),-lit(k,pair(r),r,ccc,n)])

for r in range(k*k,2*k*k):
    for n in range(1,k*k+1):
        for cc in range(k*k-1):
            for ccc in range(cc+1,k*k):
                cnf.append([-lit(k,pair(r),r,cc,n),-lit(k,pair(r),r,ccc,n)])


# not same number in any raw
for c in range(k*k):
    for n in range(1,k*k+1):
        for rr in range(k*k-1):
            for rrr in range(rr+1,k*k):
                cnf.append([-lit(k,pair(rr),rr,c,n),-lit(k,pair(rrr),rrr,c,n)])
        
        for rr in range(k*k,2*k*k-1):
            for rrr in range(rr+1,2*k*k):
                cnf.append([-lit(k,pair(rr),rr,c,n),-lit(k,pair(rrr),rrr,c,n)])

# this can be made more efficient  
# not in that square box
for r in range(2*k):
    for c in range(k):
        from_r=r*k
        from_c=c*k
        haha=[i for i in range(k*k)]
        for n in range(1,k*k+1):
            for oth_r in range(from_r,from_r+k):
                for oth_c in range(from_c,from_c+k):
                    haha[(oth_r-from_r)*k+(oth_c-from_c)]=lit(k,pair(oth_r),oth_r,oth_c,n)
                    
            for i in range(k*k-1):
                for j in range(i+1,k*k):
                    cnf.append([-haha[i],-haha[j]])
            
    
# any box contains at least one value
for r in range(2*k*k):
    for c in range(k*k):
        cnf.append([lit(k,pair(r),r,c,i)for i in range(1,k*k+1)])
        

        
# sudoku pair condition,respective coordinate value not same
for r in range(k*k):
    for c in range(k*k):
        for n in range(1,k*k+1):
            cnf.append([-lit(k,pair(r),r,c,n),-lit(k,pair(r+k*k),r+k*k,c,n)])
   


s=Solver(bootstrap_with=cnf.clauses,use_timer=True)
s.solve()


if(s.get_model()==None):
    print("NONE")

else:
    model_ans=list(s.get_model())
    answer=[[0 for i in range(k*k)] for j in range(2*k*k)]
    
    for r in range(2*k*k):
        for c in range(k*k):
            for n in range(1,k*k+1):
                if(model_ans[lit(k,pair(r),r,c,n)-1]>0):
                    answer[r][c]=n
                   
    
    with open("output_Q1.csv","w",newline="") as my_csv:
        output_array = csv.writer(my_csv,delimiter=',')
        output_array.writerows(answer)  



s.delete()





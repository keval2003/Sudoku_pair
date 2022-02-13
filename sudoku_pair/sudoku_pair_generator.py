from pysat.formula import CNF
from pysat.solvers import Solver
import random
import csv

k=input("value of k is:")
k=int(k)

def lit(k,raw,col,no):
    return ((k**4)*(no-1))+((k*k)*raw)+col+1

cnf=CNF()

# not same no. in any column 
for r in range(k*k):
    for n in range(1,k*k+1):
        for cc in range(k*k-1):
            for ccc in range(cc+1,k*k):
                cnf.append([-lit(k,r,cc,n),-lit(k,r,ccc,n)])
    
# not same number in any row
for c in range(k*k):
    for n in range(1,k*k+1):
        for rr in range(k*k-1):
            for rrr in range(rr+1,k*k):
                cnf.append([-lit(k,rr,c,n),-lit(k,rrr,c,n)])
            

# this can be made more efficient  
# not in that square box
for r in range(k):
    for c in range(k):
        from_r=r*k
        from_c=c*k
        haha=[i for i in range(k*k)]
        for n in range(1,k*k+1):
            for oth_r in range(from_r,from_r+k):
                for oth_c in range(from_c,from_c+k):
                    haha[(oth_r-from_r)*k+(oth_c-from_c)]=lit(k,oth_r,oth_c,n)
                        
            for i in range(k*k-1):
                for j in range(i+1,k*k):
                    cnf.append([-haha[i],-haha[j]])
                
        
# any box contains at least one value
for r in range(k*k):
    for c in range(k*k):
        cnf.append([lit(k,r,c,i)for i in range(1,k*k+1)])
    
s=Solver(bootstrap_with=cnf.clauses)
s.solve()

solution=[[0 for i in range(k*k)]for j in range(k*k)]

if(s.solve()==True):
    answer_model=s.get_model()
    
            
answer_trues=[i for i in answer_model if i>0]
s.add_clause([-v for v in answer_trues])
remain = list(answer_trues[:])
random.shuffle(remain)
necessary=[]
necessary_assumptions=list(necessary)
s.set_phases(v*(random.randint(0,1)*2-1) for v in range(1,k**6+1))

# finding necessities for minimun 
while len(remain):
    temp = remain.pop()
    ass=remain+list(necessary_assumptions)

    if s.solve(assumptions=ass):
        necessary_assumptions.append(temp) #necessary to get unique solution of sudoku  
    else:
        #not necesarry case /droppable
        core = s.get_core()
        remain = [l for l in remain if l in core]

sudoku_1=[[0 for i in range(k*k)]for j in range(k*k)]

necessary_assumptions= set(necessary_assumptions)

for r in range(k*k):
    for c in range(k*k):
        flag=0
        for n in range(1,k*k+1):
            if answer_model[lit(k,r,c,n)-1]>0:
                if lit(k,r,c,n) in necessary_assumptions:
                    sudoku_1[r][c]=n
                    flag=1
                
        if flag==0:
            sudoku_1[r][c]=0  
                
        
s.delete()
sudoku_2=[[0 for i in range(k*k)]for j in range(k*k)]

for r in range(k*k):
    for c in range(k*k):
        if(sudoku_1[r][c]==0):
            sudoku_2[r][c]=0
        elif(sudoku_1[r][c]==k*k):
            sudoku_2[r][c]=1
        else:
            sudoku_2[r][c]=sudoku_1[r][c]+1

with open("output_Q2.csv","w",newline="") as my_csv:
        output_array = csv.writer(my_csv)
        output_array.writerows(sudoku_1)
        output_array.writerows(sudoku_2)  



















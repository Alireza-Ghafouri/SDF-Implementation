def read_file():
    file= open ("topology_matrix.txt","rt")
    matrix= [[int(num) for num in line.split(",")] for line in file.readlines()]
    file= open ("marking_vector.txt" , "rt")
    marking= [int(line) for line in file.readlines()]
    file= open( "actor_process_times.txt" , "rt")
    actor_process_times=[int (num) for num in file.readline().split(",")]
    return matrix , marking , actor_process_times

class actor:
    def __init__(self, proc_time, inp, out, busy=False ):
        self.proc_time= int(proc_time)
        self.busy=bool(busy)
        self.input=[]
        self.input=inp
        self.output=[]
        self.output=out

number_of_input_tokens= input("number of input tokens:")
#time_limit=input("time limitation:")
matrix , marking , actor_process_times = read_file()
actor_list=[]
for i in range (len (actor_process_times)):
    inp=[]
    out=[]
    for x in range ( len(matrix) ) :
        if matrix[x][i] > 0:
            out.append([ x , matrix[x][i] ])
        elif matrix[x][i] <0 :
            if i==0:
                inp=[-1,number_of_input_tokens,number_of_input_tokens]
            else:
                inp.append([ x , marking[x] , -1* matrix[x][i] ])

    actor_list.append( actor( actor_process_times[i] , inp , out ) )

#temp=0
#for item in actor_list:
    #print("actor" ,temp," output:", item.output)
    #print("actor" ,temp," input:", item.input)
    #temp=temp+1



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
        self.timer=0

def ready_to_fire(node):
    if len(node.input) ==0:
        return True
    temp=0
    for item in node.input:
            if marking[item[0]] >= item[1]:
                temp+=1
    if temp==len(node.input):
        return True
    return False

time_limit=int (input("time limitation:") )
matrix , marking , actor_process_times = read_file()
actor_list=[]
# forming actor list
for i in range (len (actor_process_times)):
    inp=[]
    out=[]
    for x in range ( len(matrix) ) :
        if matrix[x][i] > 0:
            out.append([ x , matrix[x][i] ])
        elif matrix[x][i] <0 :
            inp.append([ x , -1* matrix[x][i] ])

    actor_list.append( actor( actor_process_times[i] , inp , out ) )

total_time=0
num_of_out_tokens=0
while (total_time <= time_limit):
    for node in actor_list:
        if node.busy :
            node.timer+=1
            if node.timer==node.proc_time:
                for item in node.output:
                    marking[item[0]] += item[1]
                node.timer=0
                node.busy=False
        if ready_to_fire(node)==True and node.busy==False :
            for item in node.input:
                marking[item[0]] -= item[1]
            node.busy=True
            #if len(node.output) ==0 :
            #    num_of_out_tokens+=1
            #    print_token (num_of_out_tokens,total_time)

    total_time+=1



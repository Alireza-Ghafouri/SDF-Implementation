def read_file():
    file= open ("topology_matrix.txt","rt")
    matrix= [[int(num) for num in line.split(",")] for line in file.readlines()]
    file= open ("marking_vector.txt" , "rt")
    marking= [int(line) for line in file.readlines()]
    file= open( "actor_process_times.txt" , "rt")
    actor_process_times=[int (num) for num in file.readline().split(",")]
    return matrix , marking , actor_process_times

class actor:
    def __init__(self, proc_time, inp, out ):
        self.proc_time= int(proc_time)
        self.busy=False
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

def print_token(token_number , token_time):
    print("out token " , token_number , " received at:" , token_time)
    global latency
    global max_time_distance
    global last_token_time
    if max_time_distance < token_time - last_token_time:
        max_time_distance= token_time - last_token_time
    last_token_time=token_time
    
    if token_number == wanted_token_for_latency:
        latency = token_time - producer_node_first_activation
    

time_limit=int (input("time limitation:") )
matrix , marking , actor_process_times = read_file()
actor_list=[]

# forming actor list
for i in range (len (actor_process_times)):     #actors
    inp=[]
    out=[]
    for x in range ( len(matrix) ) :            #edges
        if matrix[x][i] > 0:
            out.append([ x , matrix[x][i] ])
        elif matrix[x][i] <0 :
            inp.append([ x , -1* matrix[x][i] ])

    actor_list.append( actor( actor_process_times[i] , inp , out ) )


latency=0
last_token_time=0
max_time_distance=0
first_node_fire=False
#wanted_token_for_latency=0
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

            if actor_list.index(node) == 0 and first_node_fire==False:      # producer node (calculating latency)
                producer_node_first_activation = total_time
                first_node_fire=True
                producer_node_input_edges= [ind[0] for ind in node.input]
                all_toknes=0
                temp_tokens=0
                for temp in marking:
                    all_toknes += temp
                for i in producer_node_input_edges:
                    temp_tokens += marking[i]
                wanted_token_for_latency= all_toknes - temp_tokens + num_of_out_tokens + 1
                
            for item in node.input:
                marking[item[0]] -= item[1]
            node.busy=True
            if len(node.output) ==0 :
                num_of_out_tokens+=1
                print_token (num_of_out_tokens,total_time)
                node.busy=False

    total_time+=1

throughput= "1/" + str(max_time_distance)
print("----------------------------------")
if (latency == 0):  
    print ("the time limitation you entered was not enough to calculate the exact latency of the system")
    print ("the time limitation you entered was not enough to calculate the certain throughput of the system")
else:  
    print ("latency:",latency)
    if max_time_distance==0:
        print ("the time limitation you entered was not enough to calculate the exact throughput of the system")
    else:
        print("throughput:" ,throughput )




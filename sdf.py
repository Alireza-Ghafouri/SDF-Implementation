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

def print_log(actor_token_number ,status, token_time):
    
    if status == "activated":
        result= str(token_time) + ": actor number " + str(actor_token_number) + " " + status
        if actor_token_number ==0 :
            result= str(token_time) + ": SRC " + status
        elif actor_token_number == len(actor_process_times) -1:
            result= str(token_time) + ": SNK " + status

    elif status == "fired":
        result= str(token_time) + ": actor number " + str(actor_token_number) + " " + status
        if actor_token_number ==0 :
            result= str(token_time) + ": SRC " + status
        elif actor_token_number == len(actor_process_times) -1:
            result= str(token_time) + ": SNK " + status
    elif status == "exited":
        result= str(token_time) + ": out token " + str(actor_token_number) + " " + status + " from SNK" 
    
        global latency
        global throughput_temp
        global throughput

        # global max_time_distance
        # global last_token_time
        # if max_time_distance < token_time - last_token_time:
        #     max_time_distance= token_time - last_token_time
        # last_token_time=token_time
    
        if actor_token_number == wanted_token_for_latency:
            latency = token_time - producer_node_first_activation
            throughput_temp=token_time
        elif actor_token_number == wanted_token_for_latency +1 :
            throughput = "1/" + str ( token_time - throughput_temp)

            
    print(result)
    print(" ")

time_limit=int (input("time limitation:") )
matrix , marking , actor_process_times = read_file()
actor_list=[]
print("--------------------------------------------")
print("         HISTORY OF EVENTS")
print("--------------------------------------------")

# FORMING ACTOR LISTS
for i in range (len (actor_process_times)):     #actors
    inp=[]
    out=[]
    for x in range ( len(matrix) ) :            #edges
        if matrix[x][i] > 0:
            out.append([ x , matrix[x][i] ])
        elif matrix[x][i] <0 :
            inp.append([ x , -1* matrix[x][i] ])

    actor_list.append( actor( actor_process_times[i] , inp , out ) )

# MAIN

latency=0
throughput_temp=0
# last_token_time=0
# max_time_distance=0
wanted_token_for_latency=0
total_time=0
num_of_out_tokens=0
num_of_in_tokens=0
num_of_initial_tokens=0
for x in marking:
    num_of_initial_tokens += x
while (total_time <= time_limit):
    for node in actor_list:
        if node.busy :
            node.timer+=1
            if node.timer==node.proc_time:
                for item in node.output:
                    marking[item[0]] += item[1]
                node.timer=0
                node.busy=False
                print_log( actor_list.index(node) , "fired" , total_time )
        if ready_to_fire(node)==True and node.busy==False :
        
            if actor_list.index(node) == 0:
                num_of_in_tokens +=1
                if num_of_in_tokens == 1:      # Producer Node First Fire 
                    producer_node_first_activation = total_time
                    producer_node_input_edges= [ind[0] for ind in node.input]
                    all_toknes=0
                    temp_tokens=0
                    for temp in marking:
                        all_toknes += temp
                    for i in producer_node_input_edges:
                        temp_tokens += marking[i]
                    wanted_token_for_latency= all_toknes - temp_tokens + num_of_out_tokens + 1
                
            print_log ( actor_list.index(node) , "activated" , total_time )
                    
                
                
            for item in node.input:
                marking[item[0]] -= item[1]
            node.busy=True
            if len(node.output) ==0 :
                num_of_out_tokens+=1
                print_log (num_of_out_tokens, "exited", total_time)
                node.busy=False

    total_time+=1

# nm_throughput= "1/" + str(max_time_distance)


# PRINTING RESULTS

if num_of_out_tokens ==0:
    print("No output token!")
print("--------------------------------------------")
print("         SYSTEM FUNCTION")
print("--------------------------------------------")
if (latency == 0):
    if wanted_token_for_latency ==0:
        print("Time limitation too law!")
        print("The producer actor even did not fire! ")
    else:
        print ("Unable to calculate latency!")
        print("     Not enough time limitation!")
    print ("Unable to calculate throughput!")
    print("     Not enough time limitation!")
else:  
    print ("Latency:",latency)
    print("Throughput:" , throughput)

    # if max_time_distance==0:
    #     print ("the time limitation you entered was not enough to calculate the certain throughput of the system")
    # else:
    #     print("Non Memmory Throughput:" ,nm_throughput )
    

print("--------------------------------------------")
print("         FINAL SYSTEM INFO")
print("--------------------------------------------")
print("End system marking:")
print(" ")

edge=1
for x in marking:
    print(" Edge" , edge , ":" , x)
    edge +=1
num_of_busy_actors=0
for act in actor_list:
    if act.busy:
        num_of_busy_actors +=1

print(" ")
print("Number of tokens entered the system:" , num_of_in_tokens)
print("Number of tokens left the system:" , num_of_out_tokens)
print("Number of initial tokens:" , num_of_initial_tokens)
print("Number of busy actors :", num_of_busy_actors)
print("--------------------------------------------")








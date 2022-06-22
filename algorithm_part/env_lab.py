import numpy as np
from JSSP_Env import SJSSP
from uniform_instance_gen import uni_instance_gen
from Params import configs
import time

#read from data1.txt
f=open("data1.txt")
data=eval(f.read().split("\n")[0])
f.close()
job=data[0]
machine=data[1]
job_list=[]
machine_list=[]
for j in job:
    for k in range(j["number"]):
        job_list.append(eval(j["name"]))
for m in machine:
    machine_list.append(eval(m["bom"]))

# construct PT,MT
PT=[]
MT=[]

for i in job_list:
    job_single = []
    machine_single = []
    for k in range(len(machine_list[i])):
        job_single.append(machine_list[i][k][1])
        machine_single.append(machine_list[i][k][0])
    PT.append(job_single)
    MT.append(machine_single)


print(PT)
print(MT)
n_j = len(PT)
n_m = len(PT[0])
low = 1
high = 99
SEED = 42
np.random.seed(SEED)
env = SJSSP(n_j=n_j, n_m=n_m)

# Test network
from mb_agg import *
import torch
# import sys
# sys.path.append("../models/")
from agent_utils import select_action
from agent_utils import greedy_select_action
from actor_critic import ActorCritic



torch.manual_seed(configs.torch_seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(configs.torch_seed)
device = torch.device(configs.device)

# define network
actor_critic = ActorCritic(n_j=n_j,
                           n_m=n_m,
                           num_layers=configs.num_layers,
                           learn_eps=False,
                           neighbor_pooling_type=configs.neighbor_pooling_type,
                           input_dim=configs.input_dim,
                           hidden_dim=configs.hidden_dim,
                           num_mlp_layers_feature_extract=configs.num_mlp_layers_feature_extract,
                           num_mlp_layers_actor=configs.num_mlp_layers_actor,
                           hidden_dim_actor=configs.hidden_dim_actor,
                           num_mlp_layers_critic=configs.num_mlp_layers_critic,
                           hidden_dim_critic=configs.hidden_dim_critic,
                           device=device)

path = './SavedNetwork/{}.pth'.format(str(6) + '_' + str(6) + '_' + str(1) + '_' + str(99))
# ppo.policy.load_state_dict(torch.load(path))
actor_critic.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
# calculate g_pool for each step
g_pool_step = g_pool_cal(graph_pool_type=configs.graph_pool_type,
                         batch_size=torch.Size([1, n_j * n_m, n_j * n_m]),
                         n_nodes=n_j * n_m,
                         device=device)






data = (np.array(PT),np.array(MT))
print("MT =",np.array(MT).shape)
print("PT =",np.array(PT).shape)
adj, fea, omega, mask = env.reset(data)
rewards = [- env.initQuality]
t=0
while True:
    fea_tensor = torch.from_numpy(np.copy(fea)).to(device)
    adj_tensor = torch.from_numpy(np.copy(adj)).to(device)
    candidate_tensor = torch.from_numpy(np.copy(omega)).to(device)
    mask_tensor = torch.from_numpy(np.copy(mask)).to(device)
    t+=1
    with torch.no_grad():

        pi, _ = actor_critic(x=fea_tensor,
                             graph_pool=g_pool_step,
                             padded_nei=None,
                             adj=adj_tensor,
                             candidate=candidate_tensor.unsqueeze(0),
                             mask=mask_tensor.unsqueeze(0))
        # action, _ = select_action(pi, omega, None)
        _, indices = pi.squeeze().cpu().max(0)
        action = omega[indices.numpy().item()]
        adj, fea, reward, done, omega, mask = env.step(action.item())

        rewards.append(reward)
        if env.done():
            break
makespan = sum(rewards) - env.posRewards
print('makespan',makespan)
#print('env.posRewards',env.posRewards)
print('env.LBs',env.LBs)
print('env.opIDsOnMchs',env.opIDsOnMchs)
print(env.mchsStartTimes)

'''# Test random instances
for _ in range(3):
    times, machines = uni_instance_gen(n_j=configs.n_j, n_m=configs.n_m, low=configs.low, high=configs.high)
    print(times)'''
#print((env.opIDsOnMchs+1)//15)
#print((env.opIDsOnMchs+1)%15)
print(torch.cat((torch.tensor((env.opIDsOnMchs+1)//15).unsqueeze(2),torch.tensor((env.opIDsOnMchs+1)%15).unsqueeze(2)),dim=-1))
file_path = 'plan.txt'
with open(file_path, mode='w', encoding='utf-8') as file_obj:
    file_obj.write(str(env.LBs))
    file_obj.write(str(env.opIDsOnMchs))
    file_obj.write(str(makespan)+"-")
    file_obj.write(str(n_j)+"-"+str(n_m)+"-")
    file_obj.write(str(env.mchsStartTimes))


from pabutools.election import Instance, Project, ApprovalBallot, ApprovalProfile
"""
p1 = Project("p1", 1)   # The constructor takes the name and cost of the project
p2 = Project("p2", 1)
p3 = Project("p3", 3)



instance = Instance()   # There are many optional parameters
instance.add(p1)   # Use set methods to populate
instance.update([p2, p3])

instance.budget_limit = 3   # The instance stores the budget limit for the projects



b1 = ApprovalBallot([p1, p2])   # Initialize an approval ballot with two projects
b1.add(p2)   # Add projects to the approval ballot using set methods
b2 = ApprovalBallot({p1, p2, p3})
b3 = ApprovalBallot({p3})
profile=ApprovalProfile([b1,b2,b3])
"""
import random
import pandas as pd
import matplotlib.pyplot as plt
import metrics as mt
from pabutools.election import parse_pabulib
from pabutools.election import Cost_Sat
from pabutools.election import Instance, Project, ApprovalBallot, ApprovalProfile
from pabutools.rules import sequential_phragmen, method_of_equal_shares
from pabutools.analysis import avg_satisfaction, gini_coefficient_of_satisfaction, percent_non_empty_handed
import os
from metrics import fs_ratio, fs_abs
import rules.greedy_budgeting as gb
from time import time


entries = os.listdir('pabulib')
df=pd.read_excel('results/test_mes.ods')
X=[i for i in range(len(entries))]
S=[]
df2=pd.read_excel('results/test_greedy.ods')
S2=[]
df3=pd.read_excel('results/test_mesc.ods')
S3=[]
i=0

for st in entries:
	i+=1
	print(st)
	instance, profile = parse_pabulib('pabulib/'+st)
	if True:
		a=time()
		list_projects=[p for p in instance]
		random.shuffle(list_projects)
		output2 = gb.greedy_budgeting(instance, profile, Cost_Sat,list_projects)
		t2=time()-a
		s2=float(avg_satisfaction(instance, profile, output2, Cost_Sat))
		gini2=float(gini_coefficient_of_satisfaction(instance, profile, output2, Cost_Sat))
		CC2=float(percent_non_empty_handed(instance, profile, output2))
		ratio2=float(fs_ratio(instance,profile,output2,sat_class=Cost_Sat))
		diff2=float(fs_abs(instance,profile,output2,sat_class=Cost_Sat))
		S2.append(ratio2)
		print("Gini index of DMES_share",gini2)

		a=time()
		output = method_of_equal_shares(instance, profile, sat_class=Cost_Sat)
		t1=time()-a
		s=float(avg_satisfaction(instance, profile, output, Cost_Sat))
		gini1=float(gini_coefficient_of_satisfaction(instance, profile, output, Cost_Sat))
		CC1=float(percent_non_empty_handed(instance,profile,output))
		ratio1=float(fs_ratio(instance,profile,output,sat_class=Cost_Sat))
		diff1=float(fs_abs(instance,profile,output,sat_class=Cost_Sat))
		S.append(ratio1)
		print("Gini index of DMES_cost",gini1)

		a=time()
		output3 = method_of_equal_shares(instance, profile, sat_class=Cost_Sat,voter_budget_increment=1)
		t3=time()-a
		s3=float(avg_satisfaction(instance, profile, output, Cost_Sat))
		gini3=float(gini_coefficient_of_satisfaction(instance, profile, output, Cost_Sat))
		CC3=float(percent_non_empty_handed(instance,profile,output))
		ratio3=float(fs_ratio(instance,profile,output,sat_class=Cost_Sat))
		diff3=float(fs_abs(instance,profile,output,sat_class=Cost_Sat))
		S3.append(ratio3)
		print("Gini index of mes",gini3)


		data=[len([b for b in profile]),len([p for p in instance]),instance.budget_limit,s,gini1,CC1,ratio1,diff1]
		data2=[len([b for b in profile]),len([p for p in instance]),instance.budget_limit,s2,gini2,CC2,ratio2,diff2]
		data3=[len([b for b in profile]),len([p for p in instance]),instance.budget_limit,s3,gini3,CC3,ratio3,diff3]

		df[st]=data
		df2[st]=data2
		df3[st]=data3
		df.to_excel("results/test_mes.ods", sheet_name="test_input", index=False)
		df2.to_excel("results/test_greedy.ods", sheet_name="test_input", index=False)
		df3.to_excel("results/test_mesc.ods", sheet_name="test_input", index=False)
		print("Advancing",100*i/len(entries),"%")

plt.figure(figsize=(5, 2.7), layout='constrained')
plt.plot(X,S,label='DMES_share',color='red')
plt.plot(X,S2,label='DMES_cost',color='green')
plt.plot(X,S3,label='mes',color='blue')
plt.xlabel('instance')
plt.ylabel('Ratio distance to equal share')
plt.title('measure')
plt.legend(loc='upper left')
plt.show()


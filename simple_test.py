from pabutools.election import Instance, Project, ApprovalBallot, ApprovalProfile

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

import random
import pandas as pd
import matplotlib.pyplot as plt
import metrics as mt
from pabutools.election import parse_pabulib
from pabutools.election import Cost_Sat, Effort_Sat
from pabutools.election import Instance, Project, ApprovalBallot, ApprovalProfile
from pabutools.rules import sequential_phragmen, method_of_equal_shares
from pabutools.analysis import avg_satisfaction, gini_coefficient_of_satisfaction, percent_non_empty_handed
import os
from metrics import fs_ratio, fs_abs
import rules.greedy_budgeting as gb
from time import time
form rules.bos import bounded_overspending #Todo: edit this code to adapt it to pabutools environment
from pabutools.election import SatisfactionProfile, SatisfactionMeasure


output = method_of_equal_shares(instance, profile, sat_class=Effort_Sat)
print(output)x
output2 = method_of_equal_shares(instance, profile, sat_class=Cost_Sat)
print(output2)




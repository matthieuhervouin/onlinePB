from pabutools.election import Instance, Project, ApprovalBallot, ApprovalProfile
from pabutools.election import parse_pabulib
from pabutools.election import Cost_Sat, Effort_Sat
from pabutools.election.profile import AbstractProfile
from pabutools.election.satisfaction import SatisfactionMeasure
from rules.greedy_budgeting import MESVoter


def fair_share(
	instance: Instance,
	profile: AbstractProfile,
	voter: MESVoter
	):

	s=0
	for project in voter.ballot:
		s+=project.cost/profile.approval_score(project)
	return min(voter.budget,s)

def share(
	instance: Instance,
	profile: AbstractProfile,
	output: list[Project],
	voter: MESVoter
	):
	s=0
	for project in output:
		if project in voter.ballot:
			s+=project.cost/profile.approval_score(project)
	return s



def fs_ratio(
    instance: Instance,
    profile: ApprovalProfile,
    output: list[Project],
    sat_class: type[SatisfactionMeasure]
    ):

    nb_voters= len([b for b in profile])
    initial_budget_per_voter= instance.budget_limit / nb_voters
    mprofile=profile.as_multiprofile()
    voters = []
    sat_profile = profile.as_sat_profile(sat_class)
    s=0
    for voter in mprofile:
        v_share=0
        for project in output:
            if project in voter:
                v_share+=project.cost/profile.approval_score(project)
        fs=0
        for project in voter:
            fs+=project.cost/profile.approval_score(project)
        fs=min(fs,initial_budget_per_voter)
        if fs>0:
            m=float(v_share / fs)
            s+=min(1,m)*mprofile.multiplicity(voter)
    return float(s / nb_voters)

def fs_abs(
    instance: Instance,
    profile: ApprovalProfile,
    output: list[Project],
    sat_class: type[SatisfactionMeasure]
    ):
    nb_voters= len([b for b in profile])
    initial_budget_per_voter= instance.budget_limit / nb_voters
    mprofile=profile.as_multiprofile()
    s=0
    for voter in mprofile:
        v_share=0
        for project in output:
            if project in voter:
                v_share+=project.cost/profile.approval_score(project)
        fs=0
        for project in voter:
            fs+=project.cost/profile.approval_score(project)
        a=abs(v_share - fs)
        s+=a*mprofile.multiplicity(voter)
    return float(s / nb_voters)

   











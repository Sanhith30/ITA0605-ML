"""Q5: transparent case-based reasoning retrieval and reviewed retention."""
from common import *
CASES=[
 {'case':'C1','noise':'Yes','overheating':'No','pressure':'Low','solution':'Replace seal'},
 {'case':'C2','noise':'No','overheating':'Yes','pressure':'Normal','solution':'Clean cooling fins'},
 {'case':'C3','noise':'Yes','overheating':'Yes','pressure':'High','solution':'Reduce load and inspect bearing'},
 {'case':'C4','noise':'No','overheating':'No','pressure':'Low','solution':'Refill lubricant'},
 {'case':'C5','noise':'Yes','overheating':'No','pressure':'Normal','solution':'Tighten mounting'},
 {'case':'C6','noise':'No','overheating':'Yes','pressure':'High','solution':'Replace coolant pump'},
]
QUERY={'noise':'Yes','overheating':'Yes','pressure':'Low'}
LEVEL={'Low':0,'Normal':1,'High':2}

def similarity(query,case,weights=(.3,.4,.3)):
    s1=float(query['noise']==case['noise'])
    s2=float(query['overheating']==case['overheating'])
    s3=1.0-abs(LEVEL[query['pressure']]-LEVEL[case['pressure']])/2.0
    return (weights[0]*s1+weights[1]*s2+weights[2]*s3)/sum(weights)

def retrieve(casebase,query,weights=(.3,.4,.3)):
    return sorted([{'case':c['case'],'similarity':similarity(query,c,weights),
                    'solution':c['solution']} for c in casebase],
                  key=lambda r:(-r['similarity'],r['case']))

def retain(casebase,query,verified_solution,new_id):
    if not verified_solution.strip():raise ValueError('Technician-confirmed solution is required')
    if any(c['case']==new_id for c in casebase):raise ValueError('Duplicate case ID')
    return casebase+[{'case':new_id,**query,'solution':verified_solution}]

def run():
    ranking=retrieve(CASES,QUERY);double=retrieve(CASES,QUERY,(.3,.8,.3))
    save_table('q5_similarity_rankings.csv',[{'case':c['case'], 'normal_score':similarity(QUERY,c),
            'double_overheat_score':similarity(QUERY,c,(.3,.8,.3)), 'solution':c['solution']} for c in CASES])
    # Illustrative review: a new case is only actually retained in the program after a technician provides the verified solution.
    proposed_revision='Inspect bearing and verify low-pressure condition before adjusting load'
    extended=retain(CASES,QUERY,proposed_revision,'C7')
    pd.DataFrame(extended).to_csv(DATA/'q5_retained_case_base.csv',index=False)
    result={'query':QUERY,'normal_ranking':ranking,'doubled_weight_ranking':double,
            'proposed_adaptation':proposed_revision,'retained_as_C7_example':extended[-1],
            'retention_requires_verification':True}
    write_json('q5_results.json',result)
    return result
if __name__=='__main__':print(run()['normal_ranking'])

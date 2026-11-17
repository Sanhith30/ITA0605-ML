"""Run all experiments and recreate every CSV and figure from scratch."""
import json
import q1_knn, q2_scaling, q3_lwr, q4_rbf, q5_cbr, q6_cost_noise, q7_redesign

def main():
    for name,mod in [('Q1',q1_knn),('Q2',q2_scaling),('Q3',q3_lwr),('Q4',q4_rbf),
                     ('Q5',q5_cbr),('Q6',q6_cost_noise),('Q7',q7_redesign)]:
        print('Running',name,flush=True)
        result=mod.run()
        print(name,'completed:',str(result)[:550],flush=True)

if __name__=='__main__':main()

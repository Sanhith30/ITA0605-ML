"""Q7 redesign: measurable speed/memory objective, prototype, same-input validation and diagrams."""
import time, gc
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from common import DIAGRAMS, GRAPHS, OUT, save_json, read_prod
from Q6_reproducible_pipeline import optimize


def naive_rate(df):
    x=df.copy()
    x['Defect_Rate']=x.apply(lambda row: row['Defects']/row['Output_Units'],axis=1)
    return x

def revised_rate(df):
    x=df.copy()
    x['Defect_Rate']=x['Defects']/x['Output_Units']
    return optimize(x)

def clock(fn,df):
    gc.collect(); start=time.perf_counter()
    answer=fn(df); time_ms=(time.perf_counter()-start)*1000
    return answer,time_ms

def diagram():
    labels=['Load and validate\nrequired columns',
            'Remove identical duplicates\ncheck unique production keys',
            'Normalise and impute\nrecorded missing values',
            'Vectorise defect rate\nuse categories and narrow integers',
            'Validate merge cardinality\nproduce audit-ready summary']
    fig,ax=plt.subplots(figsize=(11,2.6))
    ax.set(xlim=(0,11),ylim=(0,2.6));ax.axis('off')
    for i,lab in enumerate(labels):
        x=.12+i*2.21
        ax.add_patch(FancyBboxPatch((x,.74), (2.02),1.12,boxstyle='round,pad=0.06,rounding_size=0.08',
                    edgecolor='#254662',facecolor='#eef3f7',linewidth=1.6))
        ax.text(x+1.01,1.3,lab,ha='center',va='center',fontsize=8)
        if i<4: ax.add_patch(FancyArrowPatch((x+2.03,1.29),(x+2.18,1.29),arrowstyle='-|>',
                           mutation_scale=14,linewidth=1.3,color='#254662'))
    ax.text(5.5,2.29,'Q7 – Redesign of the weekly production-data pipeline',
            ha='center',va='center',fontsize=13,fontweight='bold')
    fig.savefig(DIAGRAMS/'Q7_redesign_workflow.png',dpi=220,bbox_inches='tight');plt.close(fig)

def figure(mean_baseline,mean_revised,original_memory,revised_memory):
    fig,axs=plt.subplots(1,2,figsize=(9,3.8))
    axs[0].bar(['Row-wise apply','Vectorised'],[mean_baseline,mean_revised],color=['#ae5e55','#276482'])
    axs[0].set_yscale('log');axs[0].set(ylabel='Time (ms, logarithmic)',title='Computation: same 100,000 rows')
    axs[1].bar(['Original types','Compact types'],[original_memory/1e6,revised_memory/1e6],color=['#ae5e55','#276482'])
    axs[1].set(ylabel='DataFrame memory (MB)',title='Memory: same 100,000 rows')
    for ax in axs: ax.grid(axis='y',alpha=.2)
    fig.tight_layout();fig.savefig(GRAPHS/'Q7_redesign_comparison.png',dpi=200,bbox_inches='tight');plt.close(fig)

def main():
    clean=read_prod()
    test=pd.concat([clean.drop(columns='Defect_Rate')]*100,ignore_index=True)
    assert len(test)==100000
    times_baseline=[];times_revised=[]
    old_output=None;new_output=None
    for i in range(3):
        old,base_ms=clock(naive_rate,test)
        new,revised_ms=clock(revised_rate,test)
        assert np.array_equal(old['Defect_Rate'].to_numpy(),new['Defect_Rate'].to_numpy())
        assert old['Output_Units'].sum()==new['Output_Units'].sum()
        assert old['Defects'].sum()==new['Defects'].sum()
        times_baseline.append(base_ms);times_revised.append(revised_ms)
        old_output=old; new_output=new
    old_b=int(old_output.memory_usage(deep=True).sum())
    new_b=int(new_output.memory_usage(deep=True).sum())
    median_baseline=float(np.median(times_baseline))
    median_revised=float(np.median(times_revised))
    speedup=median_baseline/median_revised
    reduction=100*(1-new_b/old_b)
    diagram();figure(median_baseline,median_revised,old_b,new_b)
    goals={'speedup_at_least_10x':10,'memory_reduction_at_least_30_percent':30,
           'statistical_output_equal':True,'accept_tradeoff':'bounded integer ranges and category setup cost'}
    achieved=speedup>=10 and reduction>=30
    res=dict(input_rows=len(test),repetitions=3,
       predetermined_goals=goals, baseline_apply_time_ms=times_baseline,
       redesigned_vectorised_time_ms=times_revised,baseline_median_ms=median_baseline,
       redesigned_median_ms=median_revised,speedup_factor=speedup,
       original_dataframe_bytes=old_b,redesigned_dataframe_bytes=new_b,
       memory_reduction_pct=reduction,results_identical=True,
       output_sum_identical=True,defects_sum_identical=True,
       objectives_met=bool(achieved),figures=['Q7_redesign_comparison.png','Q7_redesign_workflow.png'])
    save_json(7,res)
    pd.DataFrame({'Run':[1,2,3],'Baseline_Apply_ms':times_baseline,
                  'Redesign_Vectorised_ms':times_revised}).to_csv(OUT/'Q7_timings.csv',index=False)
    print('Q7 BASELINE apply (ms)',times_baseline)
    print('REDESIGN vectorised (ms)',times_revised)
    print('MEDIAN SPEEDUP',speedup,'x')
    print('DATAFRAME MEMORY',old_b,'->',new_b,'reduction',reduction,'%')
    print('VALIDATION: computed values, output sums, defect sums identical')
    print('OBJECTIVES ACHIEVED?',achieved)

if __name__=='__main__': main()

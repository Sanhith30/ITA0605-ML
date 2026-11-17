"""Q4: Inner/left/outer joins, concat, grouping, pivoting, filtering and stable ranking."""
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from common import DATA, OUT, read_prod, save_json

def machine_info(seed=20260504):
    rng=np.random.default_rng(seed)
    ids=[f'M{i:02d}' for i in range(1,13)]+['M14']  # M13 deliberately absent; M14 has no records
    num=np.array([int(x[1:]) for x in ids])
    line=np.where(num<=4,'A',np.where(num<=8,'B','C'))
    info=pd.DataFrame({'Machine_ID':ids,'Line':line,
       'Installed_Year':rng.integers(2004,2025,len(ids)),
       'Supervisor':rng.choice(['Devi','Kumar','Ravi','Meena'],len(ids))})
    return info

def aggregated(df,group):
    return df.groupby(group,as_index=False).agg(
       Total_Output=('Output_Units','sum'), Mean_Defect_Rate=('Defect_Rate','mean'),
       Maximum_Defects=('Defects','max'), Record_Count=('Machine_ID','size'))

def main():
    data=read_prod()
    assert len(data)==1000
    info=machine_info()
    info.to_csv(DATA/'Machine_Info.csv',index=False)
    joins={}
    for how in ['inner','left','outer']:
        m=data.merge(info,on='Machine_ID',how=how,indicator=True,validate='many_to_one',suffixes=('','_Info'))
        m.to_csv(OUT/f'Q4_{how}_merge.csv',index=False)
        joins[how]={'rows':len(m),'indicator':{k:int(v) for k,v in m['_merge'].value_counts().items()},
            'unique_machines':int(m['Machine_ID'].nunique())}
    inner=data.merge(info,on='Machine_ID',how='inner',validate='many_to_one',suffixes=('','_Info'))
    left=data.merge(info,on='Machine_ID',how='left',validate='many_to_one',indicator=True,suffixes=('','_Info'))
    outer=data.merge(info,on='Machine_ID',how='outer',validate='many_to_one',indicator=True,suffixes=('','_Info'))
    assert len(left)==1000 and len(outer)==len(left)+1
    march=pd.read_csv(DATA/'Production_2026_03.csv',parse_dates=['Date'])
    april=pd.read_csv(DATA/'Production_2026_04.csv',parse_dates=['Date'])
    recombined=pd.concat([march,april],ignore_index=True,sort=False)
    keys=['Machine_ID','Date','Shift']
    assert_frame_equal(recombined.sort_values(keys).reset_index(drop=True),
                       data.sort_values(keys).reset_index(drop=True),check_exact=False,rtol=1e-12)
    assert recombined.duplicated(keys).sum()==0
    line_group=aggregated(data,'Line')
    machine_group=aggregated(data,'Machine_ID')
    line_group.to_csv(OUT/'Q4_group_by_line.csv',index=False)
    machine_group.to_csv(OUT/'Q4_group_by_machine.csv',index=False)
    pivot=pd.pivot_table(data,index='Line',columns='Shift',values='Defect_Rate',aggfunc='mean')
    pivot.to_csv(OUT/'Q4_line_shift_pivot.csv')
    groupby_shift=data.groupby(['Line','Shift'])['Defect_Rate'].mean().unstack()
    assert np.allclose(pivot.to_numpy(),groupby_shift.to_numpy())
    overall=float(data['Defect_Rate'].mean())
    high=data.groupby('Machine_ID').filter(lambda g:g['Defect_Rate'].mean()>overall)
    high_ids=sorted(high['Machine_ID'].unique().tolist())
    sorted_machines=machine_group.sort_values(['Mean_Defect_Rate','Total_Output'],ascending=[False,False],kind='mergesort')
    sorted_machines.to_csv(OUT/'Q4_sorted_machine_ranking.csv',index=False)
    # Stable tied-row order illustration: rows with identical two sorting keys keep original order.
    demo=pd.DataFrame({'Machine_ID':['B','A','C'],'Mean_Defect_Rate':[.02,.02,.01],
                       'Total_Output':[500,500,400]})
    demo_order=demo.sort_values(['Mean_Defect_Rate','Total_Output'],ascending=[False,False],kind='mergesort')['Machine_ID'].tolist()
    full_line=data.groupby('Line')['Defect_Rate'].mean()
    inner_line=inner.groupby('Line')['Defect_Rate'].mean()
    comparison=pd.DataFrame({'Line':full_line.index,
                   'Keep_All_Production':full_line.values,'Drop_Unmatched':inner_line.reindex(full_line.index).values})
    comparison['Difference_pp']=(comparison['Keep_All_Production']-comparison['Drop_Unmatched'])*100
    comparison.to_csv(OUT/'Q4_unmatched_effect.csv',index=False)
    res=dict(seed=20260504,production_rows=len(data),machine_info_rows=len(info),
       machine_info_without_records=['M14'],production_machine_without_info=['M13'],
       joins=joins,march_rows=len(march),april_rows=len(april),concat_rows=len(recombined),
       concat_index_type=type(recombined.index).__name__, concat_columns=list(recombined.columns),
       concat_roundtrip_ok=True, concat_duplicate_keys=int(recombined.duplicated(keys).sum()),
       line_groups=line_group.to_dict('records'),machine_groups=machine_group.to_dict('records'),
       pivot=pivot.reset_index().to_dict('records'),pivot_matches_groupby=True,
       overall_mean_defect_rate=overall,above_overall_mean_machines=high_ids,
       top5=sorted_machines.head(5).to_dict('records'),bottom5=sorted_machines.tail(5).to_dict('records'),
       stable_demo=demo_order,unmatched_effect=comparison.to_dict('records'))
    save_json(4,res)
    print('Q4 MACHINE_INFO\n',info.to_string(index=False))
    print('MERGE COMPARISON',joins)
    print('CONCAT MARCH/APRIL',len(march),len(april),'->',len(recombined),'no missing or extra keys')
    print('GROUP BY LINE\n',line_group.to_string(index=False))
    print('GROUP BY MACHINE\n',machine_group.to_string(index=False))
    print('PIVOT LINE x SHIFT\n',pivot.to_string())
    print('OVERALL RATE',overall,'HIGH MACHINES',high_ids)
    print('TOP 5\n',sorted_machines.head().to_string(index=False))
    print('BOTTOM 5\n',sorted_machines.tail().to_string(index=False))
    print('STABLE SORT TIED KEYS RETAIN',demo_order)
    print('EFFECT OF INNER JOIN: KEEP VS DROP UNMATCHED\n',comparison.to_string(index=False))

if __name__=='__main__': main()

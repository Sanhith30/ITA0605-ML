"""Q6: Functional weekly pipeline, schema/merge/key checks, timing, memory and rerun tests."""
import gc, time, tracemalloc
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pandas.testing import assert_frame_equal
from common import DATA, GRAPHS, OUT, clean_production, save_json, read_prod

REQUIRED={'Machine_ID','Date','Line','Shift','Output_Units','Defects'}

def load(df):
    """Accept a DataFrame (potentially obtained from CSV); return validated, parsed DataFrame."""
    absent=REQUIRED-set(df.columns)
    if absent: raise ValueError(f'Input is missing required columns: {sorted(absent)}')
    loaded=df.copy()
    loaded['Date']=pd.to_datetime(loaded['Date'],errors='raise')
    return loaded

def clean(df):
    """Return cleaned DataFrame; exact duplicate input rows are expected and removed."""
    cleaned,_=clean_production(df,strict_key=True)
    keys=['Machine_ID','Date','Shift']
    if cleaned.duplicated(keys).any(): raise ValueError('Duplicate keys after cleaning')
    return cleaned

def combine(df, machine_info):
    """A DataFrame-to-DataFrame left merge; no rows may be lost or multiplied."""
    if machine_info['Machine_ID'].duplicated().any():
        raise ValueError('Machine_Info has duplicate Machine_ID keys; merge would multiply rows')
    joined=df.merge(machine_info,on='Machine_ID',how='left',validate='many_to_one',
                    suffixes=('','_Info'),indicator='Metadata_Merge')
    if len(joined)!=len(df):
        raise ValueError(f'Unexpected merge row count {len(df)} -> {len(joined)}')
    return joined

def summarise(df):
    """Return one row per production line as a DataFrame."""
    return df.groupby('Line',as_index=False).agg(
        Total_Output=('Output_Units','sum'),
        Mean_Defect_Rate=('Defect_Rate','mean'),
        Record_Count=('Machine_ID','size'))

def plot(df, output_file):
    """Render a graph from a DataFrame and return a (non-mutated) DataFrame."""
    fig,ax=plt.subplots(figsize=(7.5,3.8))
    ax.bar(df['Line'],df['Mean_Defect_Rate']*100,color='#285d7b')
    ax.set(title='Validated weekly pipeline: mean defect rate by line',
           xlabel='Production line',ylabel='Mean defect rate (%)')
    ax.set_ylim(bottom=0);ax.grid(axis='y',alpha=.2)
    fig.tight_layout();fig.savefig(output_file,dpi=200,bbox_inches='tight');plt.close(fig)
    return df.copy()

def pipeline(raw, info, fig_name=None):
    loaded=load(raw)
    cleaned=clean(loaded)
    merged=combine(cleaned,info)
    summary=summarise(merged)
    if fig_name: summary=plot(summary,GRAPHS/fig_name)
    return summary

def time_and_peak(fn):
    gc.collect()
    tracemalloc.start()
    start=time.perf_counter()
    arr=fn()
    ms=(time.perf_counter()-start)*1000
    _,peak=tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return np.asarray(arr,dtype=float), ms, peak

def benchmark(df):
    assert len(df)>=100000
    def loop():
        return np.array([d/o for o,d in zip(df['Output_Units'].to_numpy(),df['Defects'].to_numpy())])
    def apply():
        return df.apply(lambda row: row['Defects']/row['Output_Units'],axis=1).to_numpy()
    def vector():
        return (df['Defects']/df['Output_Units']).to_numpy()
    results={}; values={}
    for name,fn in [('Python_loop',loop),('DataFrame_apply',apply),('Vectorised',vector)]:
        val,ms,peak=time_and_peak(fn)
        values[name]=val
        results[name]={'time_ms':ms,'peak_allocated_bytes':int(peak),'output_nbytes':int(val.nbytes)}
    assert np.array_equal(values['Python_loop'],values['DataFrame_apply'])
    assert np.array_equal(values['Python_loop'],values['Vectorised'])
    return results

def optimize(df):
    """Exact-value preservation: categories + bounded integer dtypes, float64 rate unchanged."""
    x=df.copy()
    for c in ['Machine_ID','Line','Shift']: x[c]=x[c].astype('category')
    if x['Output_Units'].between(-32768,32767).all(): x['Output_Units']=x['Output_Units'].astype('int16')
    if x['Defects'].between(-128,127).all(): x['Defects']=x['Defects'].astype('int8')
    return x

def main():
    raw=pd.read_csv(DATA/'Production_Raw_1012.csv',parse_dates=['Date'])
    info=pd.read_csv(DATA/'Machine_Info.csv')
    result_a=pipeline(raw,info,'Q6_first_pipeline.png')
    result_b=pipeline(raw,info,'Q6_repeat_pipeline.png')
    assert_frame_equal(result_a,result_b,check_exact=True)
    altered=raw.copy()
    first=int(altered['Output_Units'].first_valid_index())
    identify=altered.loc[first,['Machine_ID','Date','Shift']]
    matching=(altered['Machine_ID'].eq(identify['Machine_ID']) & altered['Date'].eq(identify['Date']) &
              altered['Shift'].eq(identify['Shift']))
    altered.loc[matching,'Output_Units']=altered.loc[matching,'Output_Units']+50
    altered.to_csv(DATA/'Production_Changed_1012.csv',index=False)
    changed_summary=pipeline(altered,info,'Q6_changed_pipeline.png')
    delta=changed_summary.set_index('Line')[['Total_Output','Mean_Defect_Rate']]-\
          result_a.set_index('Line')[['Total_Output','Mean_Defect_Rate']]
    affected=delta.loc[(delta.abs()>1e-12).any(axis=1)]
    assert len(affected)>=1
    check_failures={}
    try: pipeline(raw.drop(columns='Defects'),info)
    except ValueError as ex: check_failures['missing_column']=str(ex)
    try:
        conflict=raw.iloc[[first]].copy()
        conflict['Output_Units']=float(conflict['Output_Units'].iloc[0])+13
        pipeline(pd.concat([raw,conflict],ignore_index=True),info)
    except ValueError as ex: check_failures['conflicting_production_key']=str(ex)
    try:
        info_duplicate=pd.concat([info,info.iloc[[0]]],ignore_index=True)
        pipeline(raw,info_duplicate)
    except ValueError as ex: check_failures['duplicate_merge_key']=str(ex)
    assert len(check_failures)==3
    large=pd.concat([read_prod()]*100,ignore_index=True)
    assert len(large)==100000
    bench=benchmark(large)
    old_bytes=int(large.memory_usage(deep=True).sum())
    optimized=optimize(large)
    new_bytes=int(optimized.memory_usage(deep=True).sum())
    assert old_bytes>new_bytes
    assert np.array_equal(large['Defect_Rate'].to_numpy(),optimized['Defect_Rate'].to_numpy())
    res=dict(input_rows=len(raw),clean_rows=1000,unchanged_rerun_identical=True,
       changed_input=identify.to_dict(),changed_input_units_increment=50,
       original_summary=result_a.to_dict('records'),modified_summary=changed_summary.to_dict('records'),
       changed_line_statistics=affected.reset_index().to_dict('records'),
       checks_caught_examples=check_failures,
       benchmark_rows=len(large),benchmark_equivalent_values=True,benchmark=bench,
       original_memory_bytes=old_bytes,optimised_memory_bytes=new_bytes,
       saved_memory_pct=100*(1-new_bytes/old_bytes),
       original_dtypes={k:str(v) for k,v in large.dtypes.items()},
       optimised_dtypes={k:str(v) for k,v in optimized.dtypes.items()})
    save_json(6,res)
    result_a.to_csv(OUT/'Q6_original_summary.csv',index=False)
    changed_summary.to_csv(OUT/'Q6_changed_summary.csv',index=False)
    print('Q6 SAME INPUT, TWO RUNS EXACTLY IDENTICAL:',True)
    print('ORIGINAL\n',result_a.to_string(index=False))
    print('CHANGED INPUT LINE EFFECT\n',affected.to_string())
    print('DELIBERATE CHECK FAILURES:',check_failures)
    print('BENCHMARK 100,000 ROWS:\n',pd.DataFrame(bench).T.to_string())
    print('MEMORY BEFORE AFTER',old_bytes,new_bytes,'SAVING %',res['saved_memory_pct'])
    print('DTYPES ORIGINAL',res['original_dtypes'])
    print('DTYPES OPTIMISED',res['optimised_dtypes'])

if __name__=='__main__': main()

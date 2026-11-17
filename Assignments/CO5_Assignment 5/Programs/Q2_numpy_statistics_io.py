"""Q2: Numerical indexing, outliers, vectorised statistics and verified disk formats."""
import time
import numpy as np
import pandas as pd
from common import DATA, OUT, save_json
np.set_printoptions(precision=3, suppress=True, linewidth=110)

def main():
    rng = np.random.default_rng(20260502)
    readings = np.clip(rng.normal(75,4.3,(50,30)),61,89).astype('float64')
    inserted = {(2,3):146.,(7,14):9.,(12,27):151.,(25,15):160.,(38,5):6.,(44,19):143.,(48,28):12.}
    for (i,j), val in inserted.items(): readings[i,j] = val
    np.savetxt(DATA/'Q2_raw_with_outliers.csv', readings, delimiter=',', fmt='%.17g')
    last_7_first_10 = readings[:10,-7:]
    machines_3_7_12 = readings[np.array([2,6,11]),:]   # 1-based machine labels
    above90 = readings[readings > 90]
    mean,std = readings.mean(), readings.std()
    z = (readings-mean)/std
    outlier_mask = np.abs(z)>3
    found = list(zip(*np.where(outlier_mask)))
    assert set(found)==set(inserted), f'Unexpected outliers: {found}'
    med_per_machine = np.median(readings,axis=1,keepdims=True)
    cleaned = np.where(outlier_mask,med_per_machine,readings)
    assert cleaned.shape==readings.shape
    np.save(DATA/'Q2_cleaned.npy',cleaned)
    np.savez(DATA/'Q2_cleaned.npz', cleaned=cleaned)
    np.savetxt(DATA/'Q2_cleaned.csv',cleaned,delimiter=',',fmt='%.17g')
    load_npy = np.load(DATA/'Q2_cleaned.npy')
    with np.load(DATA/'Q2_cleaned.npz') as data: load_npz = data['cleaned']
    load_txt = np.loadtxt(DATA/'Q2_cleaned.csv',delimiter=',',dtype=np.float64)
    io = {k:{'values_equal':bool(np.array_equal(cleaned,v)), 'dtype_equal':bool(cleaned.dtype==v.dtype)}
          for k,v in [('npy',load_npy),('npz',load_npz),('csv_savetxt',load_txt)]}
    assert all(v['values_equal'] and v['dtype_equal'] for v in io.values())
    machine_summary = pd.DataFrame({'Machine':np.arange(1,51), 'Mean':readings.mean(axis=1),
       'Median':np.median(readings,axis=1), 'Std':readings.std(axis=1),
       'Min':readings.min(axis=1),'Max':readings.max(axis=1),'P90':np.percentile(readings,90,axis=1)})
    day_summary = pd.DataFrame({'Day':np.arange(1,31),'Mean':readings.mean(axis=0),
       'Median':np.median(readings,axis=0), 'Std':readings.std(axis=0),
       'Min':readings.min(axis=0),'Max':readings.max(axis=0),'P90':np.percentile(readings,90,axis=0)})
    machine_summary.to_csv(OUT/'Q2_machine_statistics.csv',index=False)
    day_summary.to_csv(OUT/'Q2_day_statistics.csv',index=False)
    timing_data = rng.normal(70,6,(1000,200))  # 200,000 elements
    def loop_calc(): return np.array([np.mean(row) for row in timing_data])
    def vec_calc(): return timing_data.mean(axis=1)
    time_stats = {}
    for name,fn in [('loop',loop_calc),('vectorised',vec_calc)]:
        samples=[]
        for _ in range(7):
            t=time.perf_counter(); got=fn(); samples.append((time.perf_counter()-t)*1000)
        time_stats[name+'_median_ms']=float(np.median(samples))
    assert np.allclose(loop_calc(),vec_calc())
    overall = dict(mean=float(mean),median=float(np.median(readings)),std=float(std),
                   minimum=float(readings.min()),maximum=float(readings.max()),
                   p90=float(np.percentile(readings,90)))
    clean_stats = dict(mean=float(cleaned.mean()),median=float(np.median(cleaned)),
                       std=float(cleaned.std()), maximum=float(cleaned.max()))
    res = dict(seed=20260502, shape=list(readings.shape), last_7_first_10=last_7_first_10,
       machines_3_7_12=machines_3_7_12, count_above_90=int(len(above90)), above_90=above90,
       overall_before=overall, overall_after=clean_stats, per_machine_shape=list(machine_summary.shape),
       per_day_shape=list(day_summary.shape), per_machine_first_5=machine_summary.head().to_dict('records'),
       per_day_first_5=day_summary.head().to_dict('records'),
       inserted=[{'machine_0_based':r,'day_0_based':c,'value':v} for (r,c),v in inserted.items()],
       detected=[{'machine_0_based':int(r),'day_0_based':int(c),'value':float(readings[r,c]),
          'z_score':float(z[r,c])} for r,c in found], replacement_count=int(outlier_mask.sum()),
       clean_shape=list(cleaned.shape), io_verification=io, benchmark=time_stats,
       speedup=time_stats['loop_median_ms']/time_stats['vectorised_median_ms'])
    save_json(2,res)
    print('Q2 SHAPE',readings.shape,'last7 first10 shape',last_7_first_10.shape)
    print('LAST 7 DAYS FOR FIRST 10\n',last_7_first_10)
    print('MACHINES 3,7,12 (1-BASED)\n',machines_3_7_12)
    print('ABOVE THRESHOLD 90:',len(above90),'values',above90)
    print('OVERALL BEFORE',overall,' AFTER',clean_stats)
    print('PER-MACHINE STATISTICS FIRST FIVE\n',machine_summary.head().to_string(index=False))
    print('PER-DAY STATISTICS FIRST FIVE\n',day_summary.head().to_string(index=False))
    print('OUTLIERS (zero-based coordinates, z-score)\n',pd.DataFrame(res['detected']).to_string(index=False))
    print('MASK REPLACEMENTS:',outlier_mask.sum(),'same shape?',cleaned.shape==readings.shape)
    print('SAVE/LOAD VERIFICATION:',io)
    print('200000-element mean benchmark:',time_stats,'speedup',res['speedup'])

if __name__=='__main__': main()

"""Q3: Read/inspect/clean the provided seven-row example; generate and round-trip 1,000 cleaned records."""
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from common import DATA, OUT, save_json, clean_production

SAMPLE=[
 ['M01','2026-03-01','A','480','12'], ['M02','2026-03-01','A','455','9'],
 ['M03','2026-03-01','B','N/A','15'], ['M01','2026-03-02','A','492',''],
 ['M02','2026-03-02','A','455','9'], ['M02','2026-03-02','A','455','9'],
 ['M03','2026-03-02','b','510','14']]

def make_production(seed=20260503):
    rng=np.random.default_rng(seed)
    machines=np.array([f'M{i:02d}' for i in range(1,14)])
    dates=pd.date_range('2026-03-01','2026-04-30',freq='D')
    space=pd.MultiIndex.from_product([machines,dates,['Day','Night']],names=['Machine_ID','Date','Shift']).to_frame(index=False)
    selected=space.iloc[rng.choice(len(space),1000,replace=False)].reset_index(drop=True)
    num=selected['Machine_ID'].str[1:].astype(int).to_numpy()
    selected['Line']=np.where(num<=4,'A',np.where(num<=8,'B','C'))
    # Nonuniform output, weekday/shift effects, machine effects and M13 lower reliability.
    units=480+(num%5-2)*11 + np.where(selected['Shift'].eq('Night'),-28,12)
    units=units+rng.normal(0,32,len(selected))
    selected['Output_Units']=np.clip(np.rint(units),290,660).astype(float)
    baseline_rate=0.016 + np.where(num>=9,.007,0) + np.where(selected['Shift'].eq('Night'),.005,0)
    baseline_rate=baseline_rate+np.where(num==13,.075,0)
    selected['Defects']=rng.poisson(selected['Output_Units'].to_numpy()*baseline_rate).astype(float)
    # Deliberately introduce missing values and varied text formatting before appending duplicates.
    out_missing=rng.choice(1000,30,replace=False)
    def_missing=rng.choice(np.setdiff1d(np.arange(1000),out_missing),24,replace=False)
    lower_line=rng.choice(1000,35,replace=False)
    selected.loc[out_missing,'Output_Units']=np.nan
    selected.loc[def_missing,'Defects']=np.nan
    selected.loc[lower_line,'Line']=selected.loc[lower_line,'Line'].str.lower()
    duplicated=selected.iloc[rng.choice(1000,12,replace=False)].copy()
    raw=pd.concat([selected,duplicated],ignore_index=True)
    return raw

def main():
    sample=pd.DataFrame(SAMPLE,columns=['Machine_ID','Date','Line','Output_Units','Defects'])
    sample.to_csv(DATA/'Q3_given_sample.csv',index=False)
    s=pd.read_csv(DATA/'Q3_given_sample.csv',na_values=['N/A',''],parse_dates=['Date'])
    describe=s.describe(include='all').to_string()
    with open(OUT/'Q3_dataframe_inspection.txt','w',encoding='utf-8') as f:
        f.write('HEAD\n'+s.head().to_string(index=False)+'\n\nINFO\n')
        s.info(buf=f)
        f.write('\nDTYPES\n'+s.dtypes.to_string()+'\nSHAPE '+str(s.shape))
        f.write('\nNULL COUNTS\n'+s.isna().sum().to_string()+'\n\nDESCRIBE\n'+describe+'\n')
    sample_dedup=s.drop_duplicates().copy()
    sample_dedup['Line']=sample_dedup['Line'].str.strip().str.upper()
    sample_dedup['Output_Units']=pd.to_numeric(sample_dedup['Output_Units'],errors='coerce')
    sample_dedup['Defects']=pd.to_numeric(sample_dedup['Defects'],errors='coerce')
    drop_strategy=sample_dedup.dropna(subset=['Output_Units','Defects']).copy()
    filled=sample_dedup.copy()
    for col in ['Output_Units','Defects']:
        groupmed=filled.groupby('Line')[col].transform('median')
        filled[col]=filled[col].fillna(groupmed).fillna(filled[col].median())
    filled['Defect_Rate']=filled['Defects']/filled['Output_Units']
    bool_sel=filled.loc[(filled['Line']=='A') & (filled['Output_Units']>470),['Machine_ID','Date','Output_Units']]
    label_sel=filled.loc[filled['Machine_ID']=='M02',['Date','Defects']]
    pos_sel=filled.iloc[:2,:3]
    multi=filled.set_index(['Machine_ID','Date']).sort_index()
    filled.to_csv(OUT/'Q3_small_cleaned.csv',index=False)
    raw=make_production()
    raw.to_csv(DATA/'Production_Raw_1012.csv',index=False,float_format='%.17g')
    read=pd.read_csv(DATA/'Production_Raw_1012.csv',parse_dates=['Date'],float_precision='round_trip',na_values=['N/A',''])
    assert_frame_equal(raw.reset_index(drop=True),read.reset_index(drop=True),check_exact=True)
    raw.to_json(DATA/'Production_Raw_1012.json',orient='table',date_format='iso',date_unit='ns')
    json_read=pd.read_json(DATA/'Production_Raw_1012.json',orient='table')
    assert_frame_equal(raw.reset_index(drop=True),json_read.reset_index(drop=True),check_exact=True)
    clean, cleaning_log=clean_production(read)
    assert len(clean)==1000 and clean.duplicated(['Machine_ID','Date','Shift']).sum()==0
    clean.to_csv(DATA/'Production_Cleaned_1000.csv',index=False,date_format='%Y-%m-%d')
    for month, mon_df in clean.groupby(clean['Date'].dt.month):
        mon_df.to_csv(DATA/f'Production_2026_{month:02d}.csv',index=False,date_format='%Y-%m-%d')
    raw_nulls=read.isna().sum().to_dict()
    bias_by_line=pd.DataFrame({'Rows':clean.groupby('Line').size(),
          'Mean_Rate':clean.groupby('Line')['Defect_Rate'].mean()}).reset_index()
    res=dict(seed=20260503,sample_initial_rows=len(s),sample_exact_duplicates=int(s.duplicated().sum()),
       sample_missing_before=s.isna().sum().to_dict(),sample_dtypes={k:str(v) for k,v in s.dtypes.items()},
       sample_shape=list(s.shape), sample_drop_rows=len(drop_strategy),sample_fill_rows=len(filled),
       sample_cleaned=filled.to_dict('records'),
       sample_column_selection=filled[['Machine_ID','Output_Units']].to_dict('records'),
       sample_loc=label_sel.to_dict('records'),sample_iloc=pos_sel.astype(str).to_dict('records'),
       sample_boolean=bool_sel.to_dict('records'),sample_multiindex_names=list(multi.index.names),
       production_raw_rows=len(read), production_target_clean_rows=len(clean), raw_nulls=raw_nulls,
       production_clean_log=cleaning_log, roundtrip_csv_equal=True, roundtrip_json_equal=True,
       production_clean_rows_by_line=bias_by_line.to_dict('records'),
       production_column_types={k:str(v) for k,v in clean.dtypes.items()})
    save_json(3,res)
    print('Q3 GIVEN SAMPLE BEFORE\n',s.to_string(index=False))
    print('Sample shape',s.shape,'dtypes',s.dtypes.to_dict(),'nulls',s.isna().sum().to_dict())
    print('Drop strategy rows:',len(drop_strategy),'fill strategy rows:',len(filled))
    print('SAMPLE CLEANED/IMPUTED\n',filled.to_string(index=False))
    print('SELECTION BY .loc\n',label_sel.to_string(index=False))
    print('SELECTION BY .iloc\n',pos_sel.to_string(index=False))
    print('BOOLEAN SELECTION\n',bool_sel.to_string(index=False))
    print('MULTIINDEX\n',multi.to_string())
    print('Q3 1000-RECORD DATA: raw',len(read),'clean',len(clean),'log:',cleaning_log)
    print('Raw missing by column:',raw_nulls)
    print('CSV/JSON round trips: EXACT DTYPE, VALUES, DATES MATCH')
    print('Clean column types:',res['production_column_types'])

if __name__=='__main__': main()

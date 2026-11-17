"""Q7: train-only mutual-information feature filtering before distance-based retrieval."""
from common import *
from sklearn.feature_selection import mutual_info_classif
from sklearn.metrics import accuracy_score
from time import perf_counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

REDESIGN_OBJECTIVE = 'Increase mean validation accuracy by at least 0.05 vs 22D baseline; reduce used features from 22 to 2.'

def compare(seed,k,vote):
    X,y,ix=q2_split(seed)
    X22=add_irrelevant(X,seed,20)
    scaler=StandardScaler().fit(X22[ix['train']]);Z=scaler.transform(X22)
    mutual=mutual_info_classif(Z[ix['train']],y[ix['train']],random_state=seed,n_neighbors=3)
    # Top TWO features selected using TRAIN partition and TRAIN labels only.
    choice=np.argsort(-mutual,kind='stable')[:2]
    outcome=[]
    for name,col in [('Original 22 features',np.arange(22)),('Redesigned top-2 features',choice)]:
        m=knn(k,vote)
        st=perf_counter();m.fit(Z[ix['train']][:,col],y[ix['train']]);fitms=(perf_counter()-st)*1000
        va=Z[ix['validation']][:,col]
        query1000=np.tile(va,(5,1))[:1000]
        pred_times=[]
        for _ in range(3):
            t=perf_counter();m.predict(query1000);pred_times.append((perf_counter()-t)*1000)
        outcome.append({'seed':seed,'model':name,'validation_accuracy':accuracy_score(y[ix['validation']],m.predict(va)),
                        'train_time_ms':fitms,'prediction_ms_per_1000':np.median(pred_times),
                        'features_used':len(col),'selected_indices_zero_based':','.join(map(str,col)),
                        'mi_first_feature':mutual[0],'mi_second_feature':mutual[1]})
    return outcome

def run():
    config=json.loads((RESULT/'q2_results.json').read_text());k=config['k'];vote=config['vote']
    rows=[]
    for seed in SEEDS:rows.extend(compare(seed,k,vote))
    save_table('q7_redesign_comparison.csv',rows)
    df=pd.DataFrame(rows)
    base=df[df.model=='Original 22 features'].validation_accuracy.mean()
    redesigned=df[df.model=='Redesigned top-2 features'].validation_accuracy.mean()
    gain=redesigned-base
    summary={'objective_preset':REDESIGN_OBJECTIVE,'baseline_mean_validation_accuracy':base,
             'redesigned_mean_validation_accuracy':redesigned,'gain':gain,
             'met_accuracy_objective':bool(gain>=.05),'baseline_features':22,'redesign_features':2,
             'seed_count':len(SEEDS),'selection_rule':'training-only mutual information, top two'}
    write_json('q7_results.json',summary)
    fig,axes=plt.subplots(1,2,figsize=(10.5,4))
    t=df.pivot(index='seed',columns='model',values='validation_accuracy')
    t.plot.bar(ax=axes[0],rot=0,legend=False)
    axes[0].set(xlabel='Seed',ylabel='Validation accuracy',title='Same split; before vs after feature filtering')
    timing=df.groupby('model').prediction_ms_per_1000.mean()
    timing.plot.bar(ax=axes[1],rot=0)
    axes[1].set(xlabel='',ylabel='Milliseconds / 1000 queries',title='Mean prediction latency')
    for a in axes:a.grid(axis='y',alpha=.2)
    axes[0].legend(fontsize=7,loc='lower center')
    fig.tight_layout();fig.savefig(GRAPH/'q7_redesign.png',dpi=190);plt.close(fig)
    return summary

if __name__=='__main__':print(run())

"""Q2: preprocessing, distance weighting, dimensionality and held-out test."""
from common import *
from sklearn.metrics import accuracy_score
from scipy.spatial.distance import cdist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def run():
    X,y,ix=q2_split(SEEDS[0]);part=np.array(['']*len(y),dtype=object)
    for name,indices in ix.items():part[indices]=name
    pd.DataFrame({'record_id':np.arange(1,1001),'large_scale_feature':X[:,0],
                 'small_scale_feature':X[:,1],'label':y,'partition':part}).to_csv(DATA/'q2_1000.csv',index=False)
    sweep=[]
    for scaled in (False,True):
        xuse=fixed_scale(X,ix)[0] if scaled else X
        for k in KS:
            mod=knn(k).fit(xuse[ix['train']],y[ix['train']])
            accuracy=accuracy_score(y[ix['validation']],mod.predict(xuse[ix['validation']]))
            sweep.append({'scaled':scaled,'k':k,'validation_accuracy':float(accuracy)})
    save_table('q2_k_selection.csv',sweep)
    best_scaled=sorted((r for r in sweep if r['scaled']),key=lambda r:(-r['validation_accuracy'],r['k']))[0]
    best_raw=sorted((r for r in sweep if not r['scaled']),key=lambda r:(-r['validation_accuracy'],r['k']))[0]
    k=best_scaled['k']
    seeds=[]
    for seed in SEEDS:
        Xi,yi,ii=q2_split(seed);Z,_=fixed_scale(Xi,ii)
        for vote in ('uniform','distance'):
            model=knn(k,vote).fit(Z[ii['train']],yi[ii['train']])
            acc=accuracy_score(yi[ii['validation']],model.predict(Z[ii['validation']]))
            seeds.append({'seed':seed,'vote':vote,'k':k,'validation_accuracy':float(acc)})
    save_table('q2_weight_seeds.csv',seeds)
    agg=[]
    for vote in ('uniform','distance'):
        vals=np.array([r['validation_accuracy'] for r in seeds if r['vote']==vote])
        agg.append({'vote':vote,'mean_accuracy':vals.mean(),'sd_accuracy':vals.std(ddof=1),
                    'min_accuracy':vals.min(),'max_accuracy':vals.max()})
    best_vote=sorted(agg,key=lambda d:(-d['mean_accuracy'],d['vote']!='uniform'))[0]['vote']
    # Irrelevant-feature study done only on validation partitions.
    dimensional=[]
    for extra in (0,2,5,10,20,50):
        Z = add_irrelevant(X,SEEDS[0],extra)
        Z,s=fixed_scale(Z,ix)
        model=knn(k,best_vote).fit(Z[ix['train']],y[ix['train']])
        acc=accuracy_score(y[ix['validation']],model.predict(Z[ix['validation']]))
        d=cdist(Z[ix['validation']],Z[ix['train']])
        ratio=np.mean(d.min(axis=1)/d.max(axis=1))
        dimensional.append({'irrelevant_features':extra,'total_features':2+extra,'validation_accuracy':float(acc),
                            'mean_nearest_farthest_ratio':float(ratio)})
    save_table('q2_dimensionality.csv',dimensional)
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    ddf=pd.DataFrame(dimensional)
    axes[0].plot(ddf.irrelevant_features,ddf.validation_accuracy,'o-',linewidth=2)
    axes[0].set(xlabel='Number of irrelevant features',ylabel='Validation accuracy',title='Performance vs. irrelevant features')
    axes[1].plot(ddf.irrelevant_features,ddf.mean_nearest_farthest_ratio,'s-',linewidth=2)
    axes[1].set(xlabel='Number of irrelevant features',ylabel='Mean nearest / farthest distance',title='Distance concentration')
    for ax in axes:ax.grid(alpha=.25)
    fig.tight_layout();fig.savefig(GRAPH/'q2_dimensionality.png',dpi=190);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.5))
    for scaled in (False,True):
        rows=sorted((r for r in sweep if r['scaled']==scaled),key=lambda r:r['k'])
        ax.plot([r['k'] for r in rows],[r['validation_accuracy'] for r in rows],marker='o',label=('Scaled' if scaled else 'Unscaled'))
    ax.set(xlabel='k neighbours',ylabel='Validation accuracy',title='Training-only scaling and k choice');ax.legend();ax.grid(alpha=.2)
    fig.tight_layout();fig.savefig(GRAPH/'q2_scaling.png',dpi=190);plt.close(fig)
    Z,_=fixed_scale(X,ix)
    final_model=knn(k,best_vote).fit(Z[ix['train']],y[ix['train']])
    test_acc=accuracy_score(y[ix['test']],final_model.predict(Z[ix['test']]))
    out={'k':int(k),'vote':best_vote,'best_scaled':best_scaled,'best_unscaled':best_raw,
         'seed_summary':agg,'test_accuracy':float(test_acc),'train_n':600,'validation_n':200,'test_n':200,
         'seed':SEEDS[0], 'noise_rate':.06}
    write_json('q2_results.json',out)
    return out

if __name__=='__main__':print(run())

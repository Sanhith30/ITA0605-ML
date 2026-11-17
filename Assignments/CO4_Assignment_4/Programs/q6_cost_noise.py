"""Q6: nested training sizes, three seeds, 0/10/20% noise, tree-vs-brute timing."""
from common import *
from time import perf_counter
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SIZES=(200,500,1000,2000,5000)

def get_expanded_train(seed):
    X,y,ix=q2_split(seed)
    # Use the EXACT original Q2 training partition, extending it by fresh observations
    # from the exact same generator; keep the Q2 validation/test partitions untouched.
    moreX,moreY=draw_q2(4400,seed+50000)
    return np.vstack([X[ix['train']],moreX]), np.concatenate([y[ix['train']],moreY]), X[ix['validation']],y[ix['validation']]

def eager():
    return make_pipeline(StandardScaler(),PolynomialFeatures(degree=3,include_bias=False),
                         LogisticRegression(max_iter=500,random_state=0))

def lazy(k,vote,algorithm='brute'):
    return make_pipeline(StandardScaler(),knn(k,vote,algorithm=algorithm))

def elapsed_predict1000(model,Xva):
    queries=np.tile(Xva,(int(np.ceil(1000/len(Xva))),1))[:1000]
    times=[]
    for _ in range(3):
        start=perf_counter();model.predict(queries);times.append((perf_counter()-start)*1000)
    return float(np.median(times))

def run():
    config=json.loads((RESULT/'q2_results.json').read_text());k=config['k'];vote=config['vote']
    rows=[]
    for seed in SEEDS:
        Xtr,ytr,Xva,yva=get_expanded_train(seed)
        for n in SIZES:
            for label in ('k-NN','Polynomial logistic regression'):
                model=lazy(k,vote) if label=='k-NN' else eager()
                start=perf_counter();model.fit(Xtr[:n],ytr[:n]);fit_ms=(perf_counter()-start)*1000
                score=accuracy_score(yva,model.predict(Xva));predict_ms=elapsed_predict1000(model,Xva)
                if label=='k-NN':
                    count=n
                    memory_bytes=int(n*Xtr.shape[1]*8+n*8)
                else:
                    inner=model[-1]
                    count=int(inner.coef_.size+inner.intercept_.size)
                    memory_bytes=int(count*8)
                rows.append({'seed':seed,'train_n':n,'model':label,'train_time_ms':fit_ms,
                             'prediction_ms_per_1000':predict_ms,'stored_params_or_instances':count,
                             'estimated_storage_bytes':memory_bytes,'validation_accuracy':score})
    save_table('q6_size_sweep.csv',rows)
    noisy=[]
    for seed in SEEDS:
        Xtr,ytr,Xva,yva=get_expanded_train(seed)
        n=1000
        for portion in (0,.1,.2):
            yy=ytr[:n].copy()
            rng=np.random.default_rng(seed+777+int(1000*portion))
            if portion:
                changed=rng.choice(n,size=int(n*portion),replace=False)
                yy[changed] = 1-yy[changed]
            for label in ('k-NN','Polynomial logistic regression'):
                m=lazy(k,vote) if label=='k-NN' else eager()
                m.fit(Xtr[:n],yy)
                noisy.append({'seed':seed,'flip_rate':portion,'model':label,
                              'validation_accuracy':accuracy_score(yva,m.predict(Xva))})
    save_table('q6_label_noise.csv',noisy)
    Xtr,ytr,Xva,yva=get_expanded_train(SEEDS[0])
    indexed=[]
    for irrelevant in (0,50):
        # Important: apply the identical new feature map to training and queries,
        # without label-based fitting on the held-out validation set.
        base=np.vstack([Xtr,Xva]);ex=add_irrelevant(base,SEEDS[0]+6000,irrelevant)
        full_tr,full_va=ex[:len(Xtr)],ex[len(Xtr):]
        for method in ('brute','kd_tree','ball_tree'):
            m=lazy(k,vote,algorithm=method)
            st=perf_counter();m.fit(full_tr, ytr);fitms=(perf_counter()-st)*1000
            elapsed=elapsed_predict1000(m,full_va)
            indexed.append({'irrelevant_features':irrelevant,'total_dimensions':2+irrelevant,
                            'index':method,'fit_ms':fitms,'prediction_ms_per_1000':elapsed,
                            'validation_accuracy':accuracy_score(yva,m.predict(full_va))})
    save_table('q6_index_times.csv',indexed)
    r=pd.DataFrame(rows);fig,axs=plt.subplots(1,2,figsize=(11,4.2))
    for model in r.model.unique():
        sub=r[r.model==model].groupby('train_n').agg({'prediction_ms_per_1000':'mean','validation_accuracy':'mean'})
        axs[0].plot(sub.index,sub.prediction_ms_per_1000,marker='o',label=model)
        axs[1].plot(sub.index,sub.validation_accuracy,marker='o',label=model)
    axs[0].set(xlabel='Training observations',ylabel='Time to predict 1000 (ms)',title='Latency vs training size')
    axs[1].set(xlabel='Training observations',ylabel='Validation accuracy',title='Accuracy vs training size')
    for a in axs:a.grid(alpha=.2);a.legend(fontsize=8)
    fig.tight_layout();fig.savefig(GRAPH/'q6_size_tradeoff.png',dpi=190);plt.close(fig)
    ndf=pd.DataFrame(noisy)
    fig,ax=plt.subplots(figsize=(7.4,4.2))
    for model in ndf.model.unique():
        sub=ndf[ndf.model==model].groupby('flip_rate').validation_accuracy.agg(['mean','std'])
        ax.errorbar(sub.index*100,sub['mean'],yerr=sub['std'],marker='o',capsize=4,label=model)
    ax.set(xlabel='Training labels flipped (%)',ylabel='Validation accuracy',title='Label-noise sensitivity (mean ± SD, 3 seeds)')
    ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(GRAPH/'q6_noise.png',dpi=190);plt.close(fig)
    summary={'k':k,'vote':vote,'train_sizes':SIZES,'seeds':SEEDS,
            'measurement':'median of three 1000-query timing runs per fit',
            'note':'Q2 validation retained exactly; additional observations generated only for expanded training sets'}
    write_json('q6_results.json',summary)
    return {'size_rows':len(rows),'noise_rows':len(noisy),'index_rows':indexed}

if __name__=='__main__':print(run())

"""Q3: manually checked local least-squares and numeric LWR from scratch."""
from common import *
from time import perf_counter
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

X_HAND=np.array([1.,2.,3.,4.,5.]);Y_HAND=np.array([1.2,1.9,3.2,3.9,5.5])

def local_predict(x,y,queries,tau):
    """Per-query weighted least squares; rescale weights to avoid underflow."""
    xx=np.column_stack((np.ones(len(x)),x))
    ans=[]
    for q in np.asarray(queries).ravel():
        dist2=(x-q)**2
        w=np.exp(-(dist2-dist2.min())/(2*tau*tau))
        # numpy least-squares is numerically more stable than explicit inversion.
        theta=np.linalg.lstsq(xx*np.sqrt(w)[:,None],y*np.sqrt(w),rcond=1e-12)[0]
        ans.append(float(np.array([1,q])@theta))
    return np.asarray(ans)

def timed100(f, queries, runs=3):
    times=[]
    for _ in range(runs):
        st=perf_counter();f(queries);times.append((perf_counter()-st)*1000)
    return float(np.median(times))

def run():
    xq=3.5;tau=1
    W=np.exp(-((X_HAND-xq)**2)/(2*tau**2))
    mat=np.column_stack((np.ones(5),X_HAND))
    xtwx=mat.T @ (W[:,None]*mat); xtwy=mat.T@(W*Y_HAND)
    theta=np.linalg.solve(xtwx,xtwy)
    local=float(np.array([1,xq])@theta)
    ordinary_theta=np.linalg.lstsq(mat,Y_HAND,rcond=None)[0]
    global_pred=float(np.array([1,xq])@ordinary_theta)
    assert np.isclose(local,local_predict(X_HAND,Y_HAND,[xq],1)[0],atol=1e-9)
    manual={'xq':xq,'tau':1,'weights':W,'XtwX':xtwx,'Xtwy':xtwy,'theta':theta,
            'local_prediction':local,'global_theta':ordinary_theta,'global_prediction':global_pred}
    write_json('q3_manual.json',manual)
    seed=73;rng=np.random.default_rng(seed)
    x=np.sort(rng.uniform(0,10,100));y=np.sin(x)+rng.normal(0,.18,100)
    tr,va=train_test_split(np.arange(len(x)),test_size=.25,random_state=seed)
    part=np.array(['validation']*len(x),dtype=object);part[tr]='train'
    pd.DataFrame({'x':x,'y':y,'partition':part}).to_csv(DATA/'q3_nonlinear_100.csv',index=False)
    xtr,ytr=x[tr],y[tr];xva,yva=x[va],y[va]; grid=np.linspace(x.min(),x.max(),200)
    allrows=[];pred100=np.linspace(x.min(),x.max(),100)
    taus=(.07,.3,.8,2.0,20.0)
    fig,ax=plt.subplots(figsize=(10,5.2))
    ax.scatter(xtr,ytr,s=14,alpha=.55,label='Training points')
    ax.scatter(xva,yva,s=22,marker='x',label='Validation points')
    for bw in taus:
        predtrain=local_predict(xtr,ytr,xtr,bw);predval=local_predict(xtr,ytr,xva,bw)
        ms=timed100(lambda queries:local_predict(xtr,ytr,queries,bw),pred100)
        allrows.append({'model':'LWR','bandwidth':bw,'train_mse':mean_squared_error(ytr,predtrain),
                        'validation_mse':mean_squared_error(yva,predval),'prediction_ms_for_100_queries':ms})
        ax.plot(grid,local_predict(xtr,ytr,grid,bw),linewidth=1.7,label=f'LWR τ={bw:g}')
    for deg in (1,5):
        c=np.polynomial.polynomial.polyfit(xtr,ytr,deg=deg)
        fn=lambda qs,coeff=c:np.polynomial.polynomial.polyval(qs,coeff)
        row={'model':('Global linear' if deg==1 else 'Polynomial degree 5'),'bandwidth':np.nan,
             'train_mse':mean_squared_error(ytr,fn(xtr)), 'validation_mse':mean_squared_error(yva,fn(xva)),
             'prediction_ms_for_100_queries':timed100(fn,pred100)}
        allrows.append(row)
        ax.plot(grid,fn(grid),linestyle='--',label=row['model'],alpha=.9)
    ax.set(xlabel='Control setting x',ylabel='Process output y',title='Locally weighted fits: bandwidth and edge effects');ax.grid(alpha=.15)
    ax.legend(fontsize=7.5,ncol=2);fig.tight_layout();fig.savefig(GRAPH/'q3_lwr_curves.png',dpi=190);plt.close(fig)
    save_table('q3_errors_and_times.csv',allrows)
    results={'manual':manual,'rows':allrows,'seed':seed,'n_train':75,'n_validation':25}
    write_json('q3_results.json',results)
    return {'manual_prediction':local,'global_prediction':global_pred,'rows':allrows}

if __name__=='__main__':print(run())

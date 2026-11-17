"""Q4: Gaussian RBF centres with student-implemented linear output fitting."""
from common import *
from sklearn.datasets import make_moons
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from scipy.spatial.distance import cdist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def design_matrix(X, centers, sigma):
    return np.column_stack((np.ones(len(X)),np.exp(-(cdist(X,centers,'sqeuclidean'))/(2*sigma**2))))

def rbf_train(X,y,centres_n,factor,seed=71):
    km=KMeans(n_clusters=centres_n,random_state=seed,n_init=5,max_iter=150).fit(X)
    centers=km.cluster_centers_
    center_d=cdist(centers,centers)
    np.fill_diagonal(center_d,np.inf)
    base=float(np.median(center_d.min(axis=1)))
    sigma=max(.001, factor*base)
    a=design_matrix(X,centers,sigma)
    coef=np.linalg.lstsq(a,y,rcond=1e-12)[0]
    return {'centres':centers,'sigma':sigma,'coefficients':coef,
            'parameter_count':int(2*centres_n+1+(centres_n+1))}  # centre coords, shared σ, linear weights incl bias

def rbf_predict(X,model):
    return (design_matrix(X,model['centres'],model['sigma'])@model['coefficients']>=.5).astype(int)

def run():
    sigma2=.5
    xor=np.array([[0,0],[0,1],[1,0],[1,1]],float);target=np.array([0,1,1,0],float)
    centers=np.array([[0,0],[1,1]],float)
    phi=np.exp(-cdist(xor,centers,'sqeuclidean')/(2*sigma2))
    A=np.column_stack((np.ones(4),phi))
    coef=np.linalg.lstsq(A,target,rcond=1e-12)[0]
    predictions=A@coef
    save_table('q4_xor_features.csv',[{'x1':int(p[0]),'x2':int(p[1]),'phi1':ph[0],'phi2':ph[1],
                                      'target':int(yy),'regression_output':float(pr),'classification':int(pr>=.5)}
                                     for p,ph,yy,pr in zip(xor,phi,target,predictions)])
    write_json('q4_xor_matrices.json',{'design_matrix':A,'AtA':A.T@A,'Aty':A.T@target,'weights_bias':coef,
                                     'outputs':predictions,'linear_feature_rule':'class 1 if phi1 + phi2 < 0.9'})
    assert np.array_equal((predictions>=.5).astype(int),target)
    X,y=make_moons(n_samples=1000,noise=.24,random_state=71)
    tr,other=train_test_split(np.arange(1000),train_size=.6,stratify=y,random_state=271)
    va,te=train_test_split(other,test_size=.5,stratify=y[other],random_state=272)
    split=np.array(['']*len(X),dtype=object);split[tr]='train';split[va]='validation';split[te]='test'
    pd.DataFrame({'x1':X[:,0],'x2':X[:,1],'class':y,'partition':split}).to_csv(DATA/'q4_crescents_1000.csv',index=False)
    scaler=StandardScaler().fit(X[tr]);Z=scaler.transform(X)
    sweep=[]; saved={}
    for n in (2,5,10,20,50):
        for factor in (.35,.75,1.5):
            model=rbf_train(Z[tr],y[tr],n,factor)
            acc_tr=accuracy_score(y[tr],rbf_predict(Z[tr],model))
            acc_va=accuracy_score(y[va],rbf_predict(Z[va],model))
            record={'centres':n,'width_factor':factor,'sigma':model['sigma'],
                    'train_accuracy':acc_tr,'validation_accuracy':acc_va,
                    'parameters':model['parameter_count']}
            sweep.append(record);saved[(n,factor)]=model
    save_table('q4_rbf_sweep.csv',sweep)
    best=sorted(sweep,key=lambda r:(-r['validation_accuracy'],r['parameters'],abs(r['width_factor']-.75)))[0]
    best_model=saved[(best['centres'],best['width_factor'])]
    q2info=json.loads((RESULT/'q2_results.json').read_text())
    k=q2info['k'];vote=q2info['vote']
    benchmark=knn(k,vote).fit(Z[tr],y[tr]);knn_val=accuracy_score(y[va],benchmark.predict(Z[va]))
    # IMPORTANT: Both results tested only after validation-based selections.
    result={'best':best,'rbf_test_accuracy':accuracy_score(y[te],rbf_predict(Z[te],best_model)),
            'knn_recipe_from_q2':{'k':k,'vote':vote},'knn_validation_accuracy_on_moons':knn_val,
            'knn_test_accuracy_on_moons':accuracy_score(y[te],benchmark.predict(Z[te])),
            'n_train':600,'n_validation':200,'n_test':200,'seed':71}
    write_json('q4_results.json',result)
    raw_x,raw_y=np.meshgrid(np.linspace(X[:,0].min()-.3,X[:,0].max()+.3,190),
                            np.linspace(X[:,1].min()-.3,X[:,1].max()+.3,160))
    mesh=np.column_stack((raw_x.ravel(),raw_y.ravel()));mZ=scaler.transform(mesh)
    fig,axes=plt.subplots(1,3,figsize=(13.8,4.2),sharex=True,sharey=True)
    for ax,(name,model) in zip(axes,[('Underfitted: 2 centres, wide',saved[(2,1.5)]),
                                     (f'Selected: {best["centres"]} centres',best_model),
                                     ('High-capacity: 50 centres, narrow',saved[(50,.35)])]):
        region=rbf_predict(mZ,model).reshape(raw_x.shape)
        ax.contourf(raw_x,raw_y,region,levels=[-.5,.5,1.5],colors=['#dceafd','#fce2d8'],alpha=.8)
        ax.contour(raw_x,raw_y,region,levels=[.5],colors=['#333333'],linewidths=.9)
        ax.scatter(X[tr,0],X[tr,1],c=y[tr],cmap='coolwarm',s=5,alpha=.4)
        ax.set(title=name,xlabel='Feature 1');ax.grid(alpha=.08)
    axes[0].set_ylabel('Feature 2');fig.suptitle('Q4 — RBF decision boundaries at different capacities',y=1.01)
    fig.tight_layout();fig.savefig(GRAPH/'q4_rbf_boundaries.png',dpi=170,bbox_inches='tight');plt.close(fig)
    return result

if __name__=='__main__':print(run())

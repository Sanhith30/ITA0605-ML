"""Q1: completely independent manual k-NN including a reproducible Voronoi sketch."""
from common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from scipy.spatial import Voronoi, voronoi_plot_2d

IDS = np.array(['P1','P2','P3','P4','P5','P6','P7','P8'])
X = np.array([[1,2],[2,1],[2,3],[3,2.5],[4,4],[4.5,3],[3.5,1],[5,5]],float)
Y = np.array(['Normal','Normal','Normal','Worn','Worn','Worn','Normal','Worn'])
QUERY = np.array([3.,3.])

def classify(query, k=3, metric='euclidean'):
    query=np.asarray(query,float)
    d = np.linalg.norm(X-query,axis=1) if metric=='euclidean' else np.sum(np.abs(X-query),axis=1)
    order = sorted(range(len(X)), key=lambda i: (round(float(d[i]),12), str(IDS[i])))
    chosen=order[:k]
    counts={c:int(np.sum(Y[chosen]==c)) for c in sorted(set(Y))}
    contenders=[c for c in counts if counts[c]==max(counts.values())]
    # Class vote ties break using closest neighbour; exactly equal distances use lexicographic ID.
    prediction=next(Y[i] for i in order if Y[i] in contenders)
    return prediction, order, chosen, counts, d

def run():
    results={}
    for metric in ('euclidean','manhattan'):
        pred,order,chosen,votes,d=classify(QUERY,3,metric)
        rows=[{'id':IDS[i], 'vibration':X[i,0], 'temperature':X[i,1],
               'class':Y[i], 'distance':float(d[i]),'rank':order.index(i)+1} for i in range(len(X))]
        save_table('q1_distances_'+metric+'.csv',rows)
        for k in ((1,3,5) if metric=='euclidean' else (3,)):
            p,r,c,v,_=classify(QUERY,k,metric)
            results[metric+'_k'+str(k)]={'class':p,'ranking':[str(IDS[i]) for i in r],
                                        'selected':[str(IDS[i]) for i in c], 'votes':v}
            nn=KNeighborsClassifier(n_neighbors=k,metric=metric)
            nn.fit(X,Y)
            assert str(nn.predict(QUERY.reshape(1,-1))[0])==p
    # Look for a clearly non-training query that changes between odd k values.
    second=None
    for a in np.arange(1.2, 4.8, .1):
        for b in np.arange(1.2, 4.8, .1):
            p1=classify((a,b),1)[0];p5=classify((a,b),5)[0]
            if p1!=p5 and min(np.linalg.norm(X-np.array([a,b]),axis=1)) > .28:
                second=np.array([round(a,2),round(b,2)]); break
        if second is not None: break
    if second is None: raise RuntimeError('Need a k-sensitive example')
    results['second_query']={'point':second.tolist(), 'k_predictions':{str(k):classify(second,k)[0] for k in (1,3,5)},
                             'ranked_neighbours':[str(IDS[i]) for i in classify(second,5)[1]]}
    xs,ys=np.meshgrid(np.linspace(.4,5.6,300), np.linspace(.4,5.6,300))
    points=np.column_stack([xs.ravel(),ys.ravel()])
    dist=np.sum((points[:,None,:]-X[None,:,:])**2,axis=2)
    nearest=np.argmin(dist,axis=1)
    cls=(Y[nearest]=='Worn').astype(int).reshape(xs.shape)
    plt.figure(figsize=(7.2,6.1))
    plt.contourf(xs,ys,cls,levels=[-.5,.5,1.5],colors=['#dbeafe','#ffe2db'],alpha=.8)
    plt.contour(xs,ys,cls,levels=[.5],colors=['#9b1c1c'],linewidths=2)
    voronoi_plot_2d(Voronoi(X), ax=plt.gca(), show_vertices=False, show_points=False, line_colors='#617185', line_width=.75, line_alpha=.65)
    for i,pt in enumerate(X):
        plt.scatter(*pt,marker=('s' if Y[i]=='Worn' else 'o'),color=('#a91d29' if Y[i]=='Worn' else '#185ca6'),s=70,zorder=5)
        plt.annotate(IDS[i],pt,xytext=(5,6),textcoords='offset points',fontsize=10)
    plt.scatter(*QUERY,marker='*',c='#0e8a63',s=170,zorder=9,label='Query (3,3)')
    plt.scatter(*second,marker='X',c='#5b39a4',s=120,zorder=9,label='k-sensitive query')
    plt.xlim(.4,5.6);plt.ylim(.4,5.6)
    plt.xlabel('Vibration level');plt.ylabel('Temperature index')
    plt.title('Q1 — 1-NN Voronoi decision regions (red: class boundary)')
    plt.legend(loc='lower right',fontsize=8);plt.grid(alpha=.12)
    plt.tight_layout();plt.savefig(GRAPH/'q1_voronoi.png',dpi=190);plt.close()
    write_json('q1_results.json',results)
    return results

if __name__=='__main__':print(run())

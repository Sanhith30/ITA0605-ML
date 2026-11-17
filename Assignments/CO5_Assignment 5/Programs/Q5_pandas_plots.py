"""Q5: Publication-ready output, defect, shift and misleading-axis figures."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from common import GRAPHS, OUT, read_prod, save_json

# Use readable technical figures; no external image files required.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':11,
                     'axes.labelsize':9,'figure.dpi':120,'savefig.dpi':200})

def line_chart(df, filename):
    daily=df.groupby(['Date','Line'])['Output_Units'].sum().unstack(fill_value=0)
    fig,ax=plt.subplots(figsize=(10,4.5))
    for line in daily.columns: ax.plot(daily.index,daily[line],label=f'Line {line}',linewidth=1.6)
    ax.set(title='Daily total production by line',xlabel='Date (2026)',ylabel='Output (units/day)')
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    ax.grid(alpha=.25); ax.legend(title='Production line'); fig.autofmt_xdate(rotation=30)
    fig.savefig(GRAPHS/filename,bbox_inches='tight'); plt.close(fig)
    return daily

def bar_chart(df,filename):
    mean=(df.groupby('Machine_ID')['Defect_Rate'].mean()*100).sort_values(ascending=False)
    fig,ax=plt.subplots(figsize=(9,4))
    ax.bar(mean.index,mean.values,color='#285b83')
    ax.set(title='Average defect rate by machine (descending)',xlabel='Machine ID',ylabel='Mean defect rate (%)')
    ax.set_ylim(bottom=0); ax.grid(axis='y',alpha=.22); fig.tight_layout()
    fig.savefig(GRAPHS/filename,bbox_inches='tight');plt.close(fig)
    return mean

def hist_chart(df,filename):
    fig,ax=plt.subplots(figsize=(8,4))
    ax.hist(df['Defect_Rate']*100,bins=25,edgecolor='white',color='#3a718c')
    ax.set(title='Distribution of production-record defect rates (25 bins)',xlabel='Defect rate (%)',ylabel='Number of records')
    ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(GRAPHS/filename,bbox_inches='tight');plt.close(fig)

def box_chart(df,filename):
    shifts=sorted(df['Shift'].unique())
    fig,ax=plt.subplots(figsize=(7,4))
    ax.boxplot([df.loc[df['Shift'].eq(s),'Defect_Rate']*100 for s in shifts],tick_labels=shifts)
    ax.set(title='Defect-rate distributions by shift',xlabel='Shift',ylabel='Defect rate (%)')
    ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(GRAPHS/filename,bbox_inches='tight');plt.close(fig)

def scatter_chart(df,filename):
    x=df['Output_Units'].to_numpy(dtype=float)
    y=df['Defects'].to_numpy(dtype=float)
    slope, intercept=np.polyfit(x,y,1)
    xp=np.linspace(x.min(),x.max(),100)
    fig,ax=plt.subplots(figsize=(8,4.4))
    ax.scatter(x,y,s=10,alpha=.32,label='Production records',color='#2f6e90')
    ax.plot(xp,slope*xp+intercept,label=f'Linear trend (slope={slope:.3f})',color='#b34434',linewidth=2)
    ax.set(title='Output volume versus defect counts',xlabel='Output (units/record)',ylabel='Defects (count)')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(GRAPHS/filename,bbox_inches='tight');plt.close(fig)
    return float(slope),float(intercept),float(np.corrcoef(x,y)[0,1])

def multipanel(df,filename):
    daily=df.groupby(['Date','Line'])['Output_Units'].sum().unstack(fill_value=0)
    means=(df.groupby('Machine_ID')['Defect_Rate'].mean()*100).sort_values(ascending=False)
    shifts=sorted(df['Shift'].unique())
    fig,axs=plt.subplots(2,2,figsize=(12,8))
    for line in daily.columns: axs[0,0].plot(daily.index,daily[line],label=line,lw=1)
    axs[0,0].set(title='(a) Daily total output',xlabel='Date',ylabel='Units/day')
    axs[0,0].xaxis.set_major_locator(mdates.WeekdayLocator(interval=3))
    axs[0,0].xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    axs[0,0].tick_params(axis='x',rotation=30);axs[0,0].legend(title='Line',fontsize=7)
    axs[0,1].bar(means.index,means.values,color='#2f6e90')
    axs[0,1].set(title='(b) Mean machine defect rate',xlabel='Machine',ylabel='Rate (%)');axs[0,1].set_ylim(bottom=0)
    axs[1,0].hist(df['Defect_Rate']*100,bins=25,color='#2f6e90',edgecolor='white')
    axs[1,0].set(title='(c) Record-level defect rates',xlabel='Rate (%)',ylabel='Frequency')
    axs[1,1].boxplot([df.loc[df['Shift'].eq(s),'Defect_Rate']*100 for s in shifts],tick_labels=shifts)
    axs[1,1].set(title='(d) Defect rate by shift',xlabel='Shift',ylabel='Rate (%)')
    for ax in axs.flat: ax.grid(axis='y',alpha=.19)
    fig.suptitle('Production quality review: four complementary views',fontsize=13,y=.99)
    fig.tight_layout();fig.savefig(GRAPHS/filename,bbox_inches='tight');plt.close(fig)

def misleading_axis(df,filename):
    rates=(df.groupby('Line')['Defect_Rate'].mean()*100).sort_index()
    low=float(rates.min())
    fig,axs=plt.subplots(1,2,figsize=(10,4.2),sharex=True)
    for ax in axs:
        ax.bar(rates.index,rates.values,color='#2f6e90')
        ax.set(xlabel='Production line',ylabel='Average defect rate (%)')
        ax.grid(axis='y',alpha=.2)
    axs[0].set_title('Misleading: truncated vertical axis')
    axs[0].set_ylim(max(0,low-.3),float(rates.max()*1.05))
    axs[1].set_title('Corrected: zero-baseline comparison')
    axs[1].set_ylim(0,float(rates.max()*1.12))
    fig.suptitle('Identical rates; changing the y-axis changes the visual impression')
    fig.tight_layout();fig.savefig(GRAPHS/filename,bbox_inches='tight');plt.close(fig)
    return rates.to_dict()

def main():
    df=read_prod()
    daily=line_chart(df,'Q5_daily_line_output.png')
    bar=bar_chart(df,'Q5_machine_rate_bar.png')
    hist_chart(df,'Q5_defect_rate_histogram.png')
    box_chart(df,'Q5_shift_boxplot.png')
    slope,intercept,r=scatter_chart(df,'Q5_output_defects_scatter.png')
    multipanel(df,'Q5_four_panel_review.png')
    line_rates=misleading_axis(df,'Q5_axis_before_after.png')
    res=dict(seed=20260503,figures=[p.name for p in sorted(GRAPHS.glob('Q5_*.png'))],
       plotted_lines=list(daily.columns), daily_days=len(daily),histogram_bins=25,
       machine_mean_rates_percent=bar.to_dict(),scatter_slope=slope,scatter_intercept=intercept,
       pearson_r=r, mean_rate_by_line_percent=line_rates,
       misleading_axis='Truncated y-axis exaggerates absolute differences between mean line defect rates',
       corrected_axis='Same data redrawn with y=0 baseline')
    save_json(5,res)
    print('Q5 GENERATED',len(res['figures']),'PLOTS:\n', '\n '.join(res['figures']))
    print('Daily index length:',len(daily),'lines',list(daily.columns))
    print('Machine average defect percentages:\n',bar.to_string())
    print('Trend slope/intercept/correlation:',slope,intercept,r)
    print('Line rates % used for misleading vs corrected chart:',line_rates)

if __name__=='__main__': main()


import pandas as pd 
import scipy.stats as st 
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.stats.mstats import gmean

def feature_ranks(z, name, method): 
    r = z[name].unique().tolist()
    r_counts = pd.DataFrame(z[name].value_counts()).sort_index()
    r_meds = []
    for ii in range(len(r)): 
        if method == 'Geom': 
            r_meds.append(np.round(gmean(z[z[name] == r[ii]]['AggRank']), 0))
        elif method == 'Median': 
            r_meds.append(np.round(z[z[name] == r[ii]]['AggRank'].median(), 0))
        elif method == 'Arith': 
            r_meds.append(np.round(z[z[name] == r[ii]]['AggRank'].mean(), 0))

    r_meds = round(pd.DataFrame(r_meds), 0)
    r_meds.index = r
    r_meds.columns = ['Rank']
    r_meds.sort_index(inplace=True)
    r_meds['Count'] = r_counts[name]
    r_meds.sort_values('Rank', inplace=True)
    
    return r_meds 


def violin(data_list, labels, colours, ax, box_size=12):

    positions = [x for x in range(len(data_list))] 
    jitter = 0.04 
    x_jittered = []
    for ii in range(len(data_list)): 
        x_jittered.append(st.t.rvs(df=6, scale=jitter, size=data_list[ii].shape[0]))

    medianprops = dict(linewidth=4, color="black", solid_capstyle="butt")
    boxprops = dict(linewidth=1.4, color="black")
    means = [np.round(np.mean(x), 0) for x in data_list]
    gmeans = [np.round(gmean(x), 0) for x in data_list]

    violins = ax.violinplot(data_list, positions=positions, widths=0.45, bw_method='silverman', 
    showmeans=False, showmedians=False, showextrema=False)
    for ii in range(len(data_list)): 
        violins['bodies'][ii].set_facecolor('none')
        violins['bodies'][ii].set_edgecolor('black')
        violins['bodies'][ii].set_linewidth(1.4)
        violins['bodies'][ii].set_alpha(0.75)

    ax.boxplot(data_list, positions=positions, widths=0.275, showfliers=False, showcaps=False, medianprops=medianprops, 
    whiskerprops=boxprops, boxprops=boxprops)
    for ii in range(len(data_list)): 
        ax.scatter(ii+x_jittered[ii], data_list[ii], s=80, color=colours[ii], edgecolor='black', alpha=0.4, zorder=0)
        ax.scatter(ii, means[ii], s=125, color='crimson', edgecolor='black', zorder=10)
        ax.scatter(ii, gmeans[ii], s=125, color='gold', edgecolor='black', zorder=10)
        ax.text(ii + 0.22, means[ii], r"A.Mean = " + str(int(round(means[ii], 0))), fontsize=box_size, va="center", 
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.15), zorder=10)
        ax.plot([ii, ii + 0.22], [means[ii], means[ii]], ls="dashdot", color="black", zorder=3)
        ax.text(ii + 0.22, gmeans[ii], r"G.Mean = " + str(int(round(gmeans[ii], 0))), fontsize=box_size, va="center", 
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.15), zorder=10)
        ax.plot([ii, ii + 0.22], [gmeans[ii], gmeans[ii]], ls="dashdot", color="black", zorder=3)

    newlabs = []
    for ii in range(len(data_list)): 
        newlabs.append(f'{labels[ii]}\n(n = {data_list[ii].shape[0]})')

    ax.set_xticks(range(len(data_list)))
    ax.set_xticklabels(labels=newlabs, fontsize=13)
    ax.set_facecolor('white')
    
    return ax


def compare_group(z, feature_name, figsize, colours, box_size=12): 

    feature_labels = z[feature_name].unique().tolist()
    features = z.groupby(feature_name)
    lst = {}
    for ii in range(len(feature_labels)): 
        lst[feature_labels[ii]] = features.get_group(feature_labels[ii])['AggRank'].tolist()

    data = [np.array(lst[group]) for group in feature_labels]

    fig, ax = plt.subplots(figsize=figsize)
    violin(data, feature_labels, colours, ax=ax, box_size=box_size)
    ax.invert_yaxis()
    ax.set_yticks([1, 100, 200, 300, 391])
    ax.set_yticklabels([1, 100, 200, 300, 391], fontsize=12)
    ax.set_ylabel('Agg. Rank', fontsize=14, loc='top')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()


def cont_tab(df, feature1, feature2): 

    index_names = {
        'selector': '.index_name',
        'props': 'font-style: italic; color: black; font-weight: normal; font-size: 1em;'
    }
    headers = {
        'selector': 'th:not(.index_name)',
        'props': 'background-color: #006600; color: white; font-weight:normal;'
    }

    gen_per = pd.crosstab(df[feature1], df[feature2], rownames=[f'{feature1}:'], colnames=[f'{feature2}:'], 
    margins=True, margins_name='Total')
    return gen_per.style.set_table_styles([index_names, headers, {'selector': 'td', 'props': 'text-align: center; font-weight: normal;'}])


def get_ranks(df, months, feature_name):
    feature_labels = df[feature_name].unique().tolist()
    features = df.groupby(feature_name)
    lst = {}
    for ii in range(len(feature_labels)): 
        lst[feature_labels[ii]] = gmean(features.get_group(feature_labels[ii]).loc[:, months], axis=0)

    data = [np.array(lst[group]) for group in feature_labels]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    for ii in range(len(data)): 
        ax.plot(months, data[ii], marker="o", label=feature_labels[ii], markerfacecolor='white', lw=2)
    ax.invert_yaxis()
    ax.set_xticks(months)
    ax.set_xticklabels(months, rotation=90)
    ax.legend(ncol=2, loc='center left', prop=dict(size=9))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()


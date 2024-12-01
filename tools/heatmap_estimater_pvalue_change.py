import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def plot_estimator_pvalue_change(data_main, data_split, estimate_columns, p_split, x_ticks, plot_name):

    data_split['ylabel'] = data_main['lval'] + data_main['op'] + data_main['rval']

    plt.figure(figsize=(35, 30))

    diff = data_main['Estimate'].values[:, None] - data_split[estimate_columns].values

    plt.imshow(diff, cmap='bwr', vmin=-5, vmax=5)

    for i in range(data_split.shape[0]):
        for j in range(3, data_split.shape[1] - 1):
            text = f'{round(data_split.iloc[i, j], 3)}'
            plt.text(j - 3, i, text, ha='center', va='center', fontsize=15,
                     color='black' if float(p_split.iloc[i, j]) < 0.05 else 'red')

    # Loop for adding outlines
    for i in range(data_split.shape[0] + 3):
        for j in range(3, data_split.shape[1] - 1):
            rect = patches.Rectangle((j - 3.5, i - 3.5), 1, 1, linewidth=2, edgecolor='black', facecolor='none')
            plt.gca().add_patch(rect)

    plt.xlabel(plot_name, weight='bold', fontsize=20, labelpad=10)
    plt.ylabel('Regression', weight='bold', fontsize=20)
    colorbar = plt.colorbar(fraction=0.02, pad=0.04)
    colorbar.ax.yaxis.set_tick_params(labelsize=20)
    colorbar.set_label('Difference to Baseline Estimators', labelpad=10, fontsize=15)

    plt.yticks(np.arange(data_split.shape[0]), data_split['ylabel'].astype(str), fontsize=15)
    plt.xticks(np.arange(len(x_ticks)), x_ticks, rotation=45, fontsize=15,
               ha="right")

    plt.tight_layout()

    plt.savefig('/Users/inagege/Documents/00_Uni/SeminarSocialSentimentInTimesOfCrisis/results/change_estimators_plots/' + plot_name)

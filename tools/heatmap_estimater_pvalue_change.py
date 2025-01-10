import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def plot_estimator_pvalue_change(data_main, data_split, estimate_columns, p_split, x_ticks, plot_name):

    plt.figure(figsize=(35, 30))

    initial_distance = np.abs(data_main['Estimate'].values[:, None])

    # Compute the updated distance from zero
    updated_distance = np.abs(data_split[estimate_columns].values)

    # Compute the difference in distances (positive = closer to zero, negative = further from zero)
    diff = updated_distance - initial_distance

    plt.imshow(diff, cmap='bwr', vmin=-5, vmax=5)

    for i in range(data_split.shape[0]):
        for j in range(3, data_split.shape[1]):
            text = f'{round(data_split.iloc[i, j], 3)} \n *{round(float(p_split.iloc[i, j]),3)}'
            plt.text(j - 3, i, text, ha='center', va='center', fontsize=15,
                     color='black')

    # Loop for adding outlines
    for i in range(data_split.shape[0] + 3):
        for j in range(3, data_split.shape[1]):
            rect = patches.Rectangle((j - 3.5, i - 3.5), 1, 1, linewidth=2, edgecolor='black', facecolor='none')
            plt.gca().add_patch(rect)

    data_split['ylabel'] = data_main['lval'] + data_main['op'] + data_main['rval']


    plt.xlabel(plot_name, weight='bold', fontsize=20, labelpad=10)
    plt.ylabel('Regression', weight='bold', fontsize=20)
    colorbar = plt.colorbar(fraction=0.02, pad=0.04)
    colorbar.ax.yaxis.set_tick_params(labelsize=20)
    colorbar.set_label(f'Difference of Absolute Estimator Weight', labelpad=10, fontsize=15)

    plt.yticks(np.arange(data_split.shape[0]), data_split['ylabel'].astype(str), fontsize=15)
    plt.xticks(np.arange(len(x_ticks)), x_ticks, rotation=45, fontsize=15,
               ha="right")

    plt.tight_layout()

    plt.savefig('/Users/inagege/Documents/00_Uni/SeminarSocialSentimentInTimesOfCrisis/results/change_estimators_plots/' + plot_name  + '.svg', format='svg')




def plot_all_pvalue_change(data_main, data_split, estimate_columns, p_split, x_ticks, plot_name):

    plt.figure(figsize=(35, 30))

    initial_distance = np.abs(data_main['Estimate'].values[:, None])

    # Compute the updated distance from zero
    updated_distance = np.abs(data_split[estimate_columns].values)

    # Compute the difference in distances (positive = closer to zero, negative = further from zero)
    diff = updated_distance - initial_distance

    plt.imshow(diff, cmap='bwr', vmin=-5, vmax=5)

    for i in range(data_split.shape[0]):
        for j in range(3, data_split.shape[1]):
            text = f'{round(data_split.iloc[i, j], 3)} \n *{round(float(p_split.iloc[i, j]),3)}'
            plt.text(j - 3, i, text, ha='center', va='center', fontsize=35,
                     color='black')

    # Loop for adding outlines
    for i in range(data_split.shape[0]):
        for j in range(3, data_split.shape[1]):
            rect = patches.Rectangle((j-3.5, i-0.5), 1, 1, linewidth=2, edgecolor='black', facecolor='none')
            plt.gca().add_patch(rect)

    data_split['ylabel'] = data_main['lval'] + data_main['op'] + data_main['rval']


    plt.xlabel(plot_name, weight='bold', fontsize=30, labelpad=10)
    plt.ylabel('Regression', weight='bold', fontsize=30)
    colorbar = plt.colorbar(fraction=0.02, pad=0.04)
    colorbar.ax.yaxis.set_tick_params(labelsize=30)
    colorbar.set_label('Difference of Absolute Estimator Weight', labelpad=10, fontsize=25, weight='bold')

    plt.yticks(np.arange(data_split.shape[0]), data_split['ylabel'].astype(str), fontsize=25)
    plt.xticks(np.arange(len(x_ticks)), x_ticks, rotation=45, fontsize=25,
               ha="right")

    plt.tight_layout()

    plt.savefig('/Users/inagege/Documents/00_Uni/SeminarSocialSentimentInTimesOfCrisis/results/change_estimators_plots/' + plot_name  + '.svg', format='svg')


def plot_all_data(data_main, data_split, estimate_columns, p_split, x_ticks, plot_name):

    plt.figure(figsize=(20, 30))

    initial_distance = np.abs(data_main['Estimate'].values[:, None])

    # Compute the updated distance from zero
    updated_distance = np.abs(data_split[estimate_columns].values)

    # Compute the difference in distances (positive = closer to zero, negative = further from zero)
    diff = updated_distance - initial_distance

    plt.imshow(diff, cmap='bwr', vmin=-5, vmax=5)

    for i in range(data_split.shape[0]):
        for j in range(3, data_split.shape[1]):
            text = f'{round(data_split.iloc[i, j], 3)} \n *{round(float(p_split.iloc[i, j]),3)}'
            plt.text(j - 3, i, text, ha='center', va='center', fontsize=15,
                     color='black')

    # Loop for adding outlines
    for i in range(data_split.shape[0]):
        for j in range(3, data_split.shape[1]):
            rect = patches.Rectangle((j-3.5, i-0.5), 1, 1, linewidth=2, edgecolor='black', facecolor='none')
            plt.gca().add_patch(rect)

    data_split['ylabel'] = data_main['lval'] + data_main['op'] + data_main['rval']


    plt.xlabel(plot_name, weight='bold', fontsize=30, labelpad=10)
    plt.ylabel('Regression', weight='bold', fontsize=30)
    colorbar = plt.colorbar(fraction=0.02, pad=0.04)
    colorbar.ax.yaxis.set_tick_params(labelsize=30)
    colorbar.set_label('Difference of Absolute Estimator Weight', labelpad=10, fontsize=25, weight='bold')

    plt.yticks(np.arange(data_split.shape[0]), data_split['ylabel'].astype(str), fontsize=25)
    plt.xticks(np.arange(len(x_ticks)), x_ticks, rotation=45, fontsize=25,
               ha="right")

    plt.tight_layout()

    plt.savefig('/Users/inagege/Documents/00_Uni/SeminarSocialSentimentInTimesOfCrisis/results/change_estimators_plots/All_Estimators_' + plot_name + '.svg', format='svg')


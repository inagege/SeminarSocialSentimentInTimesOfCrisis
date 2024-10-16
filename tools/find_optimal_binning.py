import numpy as np
from sklearn.preprocessing import KBinsDiscretizer


def optimal_bins_freedman_diaconis(data):
    """
    This function calculates the optimal number of bins for a histogram using the Freedman-Diaconis rule.
    :param data: The data for which to calculate the optimal number of bins.
    :return bins: The optimal number of bins for the histogram.
    """
    q25, q75 = np.percentile(data.dropna(), [25, 75])
    bin_width = 2 * (q75 - q25) * len(data.dropna()) ** (-1/3)
    if bin_width == 0:
        return 2  # Return 2 bins if bin_width is zero to avoid division by zero
    bins = int((data.max() - data.min()) / bin_width)
    return max(2, bins)  # Ensure at least two bins


# Function to determine the optimal number of bins for each column
def determine_optimal_bins(data):
    """
    This function determines the optimal number of bins for each column in the data.
    :param data: The data for which to determine the optimal number of bins.
    :return optimal_bins_dict: A dictionary containing the optimal number of bins for each column.
    """
    optimal_bins_dict = {}
    for column in data.columns:
        optimal_bins_dict[column] = optimal_bins_freedman_diaconis(data[column])
    return optimal_bins_dict


# Function to bin data using the optimal number of bins
def bin_data_with_optimal_bins(data, optimal_bins_dict):
    """
    This function bins the data using the optimal number of bins for each column.
    :param data: The data to bin.
    :param optimal_bins_dict: A dictionary containing the optimal number of bins for each column.
    :return binned_data: The binned data.
    """
    binned_data = data.copy()
    for column, n_bins in optimal_bins_dict.items():
        kbins = KBinsDiscretizer(n_bins=n_bins, encode='ordinal', strategy='uniform')
        binned_data[column] = kbins.fit_transform(data[[column]])
    return binned_data

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler


def _convert_data_datetime(data):
    """
    This function converts the columns i_START and i_END to datetime format.
        @return data: DataFrame with the columns i_START and i_END converted to datetime format
    """
    data['i_START'] = pd.to_datetime(data['i_START'])
    data['i_END'] = pd.to_datetime(data['i_END'])
    return data

def load_data():
    """
    This function loads the data from the file data_sample_700_SOSEC_dataset_germany.csv.
        @return data: DataFrame with the loaded data
    """
    return pd.read_csv("../Data/data_sample_700_SOSEC_dataset_germany.csv")


def encode_data_to_numeric(data=None):
    """
    The function encode_data_to_numeric takes a DataFrame as input and encodes the data to numeric format.
        @return data: DataFrame with encoded data
    """
    if data is None:
        data = load_data()

    data = _convert_data_datetime(data)
    # Step 2: Calculate the number of days since the minimum date for each timestamp
    min_date = data['i_START'].min()
    data['i_START'] = (data['i_START'].dt.floor('D') - min_date).dt.days
    data['i_END'] = (data['i_END'].dt.floor('D') - min_date).dt.days

    # Step 3: Convert unique_id and unique_ids to numeric by removing the first 4 characters
    data['unique_id'] = data['unique_id'].apply(lambda x: str(x)[4:] if pd.notna(x) else x).astype(float)
    data['unique_ids'] = data['unique_ids'].apply(lambda x: str(x)[4:] if pd.notna(x) else x).astype(float)

    # Step 4: Convert columns with strings containing commas to numeric
    columns_to_convert = ['F4aA1', 'F4aA2', 'F4bA1', 'F4bA2', 'F4bA3', 'F4bA4', 'F4bA5', 'F4bA6', 'F4bA7', 'F4bA8',
                          'F4bA9', 'F4bA10', 'F4bA11', 'F4bA12', 'F4bA13', 'F4bA14', 'F4i_neuA1', 'F4i_neuA2',
                          'F4i_neuA3', 'F4iA1']
    for col in columns_to_convert:
        #if col exists in the data
        if col in data.columns:
            #if the column is a string
            if data[col].dtype == str:
                data[col] = data[col].str.replace(',', '.')
                data[col] = pd.to_numeric(data[col], errors='coerce')

    # Step 5: Encode the boolean column migration_background into numeric
    data['migration_background'] = data['migration_background'].astype(int)

    # Step 6: Encode the categorical columns kitA6 and state into numeric
    label_encoder = LabelEncoder()
    cols_to_encode = ['kitA6', 'state', 'region', 'town_name']
    for col in cols_to_encode:
        data[col] = label_encoder.fit_transform(data[col].astype(str))

    # Step 7: Drop the columns Start_Datum and Ende_Datum
    data.drop(columns=['Start_Datum', 'Ende_Datum'], inplace=True)

    return data

def get_data_since_date(data=None, date='2022-11-08'):
    """
    This function filters the data since a specific date.
        @param data: DataFrame with the data
        @param date: Date since the data should be filtered
        @return data: DataFrame with the data since the specific date
    """
    if data is None:
        data = load_data()

    date = pd.to_datetime(date)

    data = _convert_data_datetime(data)

    data = data[data['i_START'] >= date]

    return data

def min_max_scale_data(data):
    """
    This function scales the data using the Min-Max scaling method.
        @param data: DataFrame with the data
        @return data: DataFrame with the scaled data
    """
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    data = pd.DataFrame(data_scaled, columns=data.columns)
    return data

def fill_nan_individually(data):
    """
    This function fills the NaN values in the columns.
    If the columns include binary values fill the nans with mod, if not fill them with mean.
        @param data: DataFrame with the data
        @return data: DataFrame with the filled NaN values
    """
    for col in data.columns:
        if data[col].notna().any():  # Check if the column has at least one non-NaN value
            data.fillna({col: data[col].mode()[0]}, inplace=True)
    return data
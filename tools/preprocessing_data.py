import pandas as pd
from sklearn.preprocessing import LabelEncoder


def load_data():
    """
    This function loads the data from the file data_sample_700_SOSEC_dataset_germany.csv.
        @return data: DataFrame with the loaded data
    """
    return pd.read_csv("../Data/data_sample_700_SOSEC_dataset_germany.csv")


def encode_data_to_numeric():
    """
    The function encode_data_to_numeric takes a DataFrame as input and encodes the data to numeric format.
        @return data: DataFrame with encoded data
    """
    data = load_data()

    # Step 1: Convert i_START and i_END to datetime
    data['i_START'] = pd.to_datetime(data['i_START'])
    data['i_END'] = pd.to_datetime(data['i_END'])

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

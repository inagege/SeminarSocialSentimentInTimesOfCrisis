import yfinance as yf
import pandas as pd


def add_finance_data(df_data):
    df_data = add_dax_data(df_data)
    df_data = add_interest_rate_data(df_data)
    df_data = add_inflation_data(df_data)
    df_data = add_consumer_price_index_data(df_data)
    df_data.drop(columns=['Date_x', 'Date_y'], inplace=True)

    return df_data


def add_dax_data(df_data):
    """
    This function downloads the DAX data from Yahoo Finance and merges it with the input DataFrame based on the
    'i_START' column.
    :param df_data: Input DataFrame with the 'i_START' column
    :return df_merged (pd.DataFrame): Merged DataFrame with the DAX data
    """
    # Ensure i_START is in datetime format
    df_data['i_START'] = pd.to_datetime(df_data['i_START'])

    # Define the ticker symbol for DAX
    ticker = "^GDAXI"

    # Download DAX data from the beginning of 2022 to the current date
    dax_data = yf.download(ticker, start="2022-01-01", end=pd.Timestamp.today().strftime('%Y-%m-%d'))

    # Resample the data to weekly frequency
    dax_weekly = dax_data['Close'].resample('W').last().reset_index()

    # Add a 'week' column to both DataFrames
    df_data['week'] = df_data['i_START'].dt.to_period('W').dt.start_time
    dax_weekly['week'] = dax_weekly['Date'].dt.to_period('W').dt.start_time

    # Merge the DataFrames on the 'week' column
    df_merged = pd.merge(df_data, dax_weekly[['week', 'Close']], on='week', how='left')

    # Rename the 'Close' column to 'dax_points'
    df_merged.rename(columns={'Close': 'dax_points'}, inplace=True)

    # Drop the 'week' column if not needed
    df_merged.drop(columns=['week'], inplace=True)

    # Display the merged DataFrame
    return df_merged


def add_inflation_data(df_data):
    """
    This function loads the inflation rate data from a CSV file and merges it with the input DataFrame based on the
     'i_START' column
    :param df_data: Input DataFrame with the 'i_START' column
    :return df_merged: Merged DataFrame with the inflation rate data
    """
    # Load the inflation rate CSV file
    inflation_df = pd.read_csv('../Data/statistic_id1045_monatliche-inflationsrate-in-deutschland.csv',
                               delimiter=';')

    # Convert the Year and Month columns to a datetime format
    inflation_df['Date'] = pd.to_datetime(inflation_df[['Year', 'Month']].assign(DAY=1))

    # Ensure i_START is in datetime format
    df_data['i_START'] = pd.to_datetime(df_data['i_START'])

    # Extract the year and month from i_START
    df_data['Year'] = df_data['i_START'].dt.year
    df_data['Month'] = df_data['i_START'].dt.month

    # Merge the inflation data with df_data based on Year and Month
    df_merged = pd.merge(df_data, inflation_df[['Date', 'Change compared to previous years month']],
                         left_on=['Year', 'Month'], right_on=[inflation_df['Date'].dt.year, inflation_df['Date'].dt.month],
                         how='left')

    # Rename the 'Change to previous years month' column to 'inflation_rate'
    df_merged.rename(columns={'Change compared to previous years month': 'inflation_rate'}, inplace=True)

    df_merged['inflation_rate'] = df_merged['inflation_rate'].str.replace(',', '.')
    df_merged['inflation_rate'] = pd.to_numeric(df_merged['inflation_rate'], errors='coerce')

    # Drop the temporary Year and Month columns
    df_merged.drop(columns=['Year', 'Month'], inplace=True)

    # Display the merged DataFrame
    return df_merged


def add_interest_rate_data(df_data):
    """
    This function loads the interest rate data from a CSV file and merges it with the input DataFrame based on the
     'i_START' column
    :param df_data: Input DataFrame with the 'i_START' column
    :return df_merged: Merged DataFrame with the interest rate data
    """
    # Load the inflation rate CSV file
    interest_df = pd.read_csv('../Data/Zinssatz_EZB.csv', delimiter=';')

    # Convert the Year and Month columns to a datetime format
    interest_df['Date'] = pd.to_datetime(interest_df['Date'], format='%Y-%m')
    # Ensure i_START is in datetime format
    df_data['i_START'] = pd.to_datetime(df_data['i_START'])

    # Extract the year and month from i_START
    df_data['Year'] = df_data['i_START'].dt.year
    df_data['Month'] = df_data['i_START'].dt.month

    # Extract the year and month from Date
    interest_df['Year'] = interest_df['Date'].dt.year
    interest_df['Month'] = interest_df['Date'].dt.month

    df_merged = pd.merge(df_data, interest_df[['Year', 'Month', 'Zinssatz der EZB']],
                         on=['Year', 'Month'], how='left')

    # Rename the 'Change to previous years month' column to 'inflation_rate'
    df_merged.rename(columns={'Zinssatz der EZB': 'interest_rate'}, inplace=True)

    df_merged['interest_rate'] = df_merged['interest_rate'].str.replace(',', '.')
    df_merged['interest_rate'] = pd.to_numeric(df_merged['interest_rate'], errors='coerce')

    # Drop the temporary Year and Month columns
    df_merged.drop(columns=['Year', 'Month'], inplace=True)

    # Display the merged DataFrame
    return df_merged


def add_consumer_price_index_data(df_data):
    """
    This function loads the consumer price index data from a CSV file and merges it with the input DataFrame based on the
     'i_START' column
    :param df_data: Input DataFrame with the 'i_START' column
    :return df_merged: Merged DataFrame with the cpi rate data
    """
    # Load the inflation rate CSV file
    cpi_df = pd.read_csv('../Data/VPI.csv', delimiter=';')

    # Convert the Year and Month columns to a datetime format
    cpi_df['Date'] = pd.to_datetime(cpi_df[['Year', 'Month']].assign(DAY=1))

    # Ensure i_START is in datetime format
    df_data['i_START'] = pd.to_datetime(df_data['i_START'])

    # Extract the year and month from i_START
    df_data['Year'] = df_data['i_START'].dt.year
    df_data['Month'] = df_data['i_START'].dt.month

    # Merge the inflation data with df_data based on Year and Month
    df_merged = pd.merge(df_data, cpi_df[['Date', 'Veränderung zum Vorjahresmonat in %']],
                         left_on=['Year', 'Month'], right_on=[cpi_df['Date'].dt.year, cpi_df['Date'].dt.month],
                         how='left')

    # Rename the 'Change to previous years month' column to 'inflation_rate'
    df_merged.rename(columns={'Veränderung zum Vorjahresmonat in %': 'consumer_price_index'}, inplace=True)

    df_merged['consumer_price_index'] = df_merged['consumer_price_index'].str.replace(',', '.')
    df_merged['consumer_price_index'] = pd.to_numeric(df_merged['consumer_price_index'], errors='coerce')

    # Drop the temporary Year and Month columns
    df_merged.drop(columns=['Year', 'Month'], inplace=True)

    # Display the merged DataFrame
    return df_merged

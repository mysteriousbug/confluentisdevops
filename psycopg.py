import numpy as np
import pandas as pd
import psycopg2
import statsmodels.api as sm
import matplotlib.pyplot as plt

try:
    connection = psycopg2.connect(
        dbname='rapidigital',
        user='postgreadmin',
        password='Testing@123456',
        host='eu-01-rapidigital-postgresql-01.postgres.database.azure.com',
        port='5432'
    )
    cursor = connection.cursor()
    print("Connected to the database successfully!")
except psycopg2.Error as e:
    print("Error: Could not connect to the database")
    print(e)

try:
    column_name = 'sales'  # Replace this with the actual column name
    query = f"SELECT {column_name} FROM public.financedata;"
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    column_data = np.array(rows).flatten()

    # Convert the data to a pandas Series with appropriate timestamps (assuming you have a timestamp column)
    index = pd.date_range(start='23-01-2014', periods=len(column_data), freq='D')
    series_data = pd.Series(column_data, index=index)

    # Fit the ARIMA model
    # Replace p, d, and q with appropriate values based on your data and ARIMA modeling requirements
    p, d, q = 1, 1, 1
    model = sm.tsa.ARIMA(series_data, order=(p, d, q))
    results = model.fit()

    # Print the summary of the ARIMA model
    print(results.summary())

    # Make predictions on the testing data
    # Replace 'start_date' and 'end_date' with appropriate dates for your testing data
    predictions = results.predict(start='23-01-2015', end='15-03-2015', dynamic=False)

    # Print the predictions
    print(predictions)
    plt.figure(figsize=(10, 6))
    plt.plot(series_data, label='Actual Data')
    plt.plot(predictions, label='Predictions')
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('ARIMA Model Predictions')
    plt.legend()
    plt.show()

     

except psycopg2.Error as e:
    print("Error: Could not fetch data from the table")
    print(e)

#Executing Queries



if connection:
    cursor.close()
    connection.close()
    print("Connection closed.")

import pandas as pd

import matplotlib.pyplot as plt
import psycopg2
import requests
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


from main import currency_dataframe
df = currency_dataframe()
def rodyti_meniu():
    print("\n----Meniu------")
    print("1.Peržiūrėti naujausius duomenis")
    print("2.Apskaiciuot vidurki keliu dienu")
    print("3.Grafiku spausdinimas")
    print("4.Išeit")

def get_all_data():
    try:
        pasirinkta_valiuta = input("Prasome nurodyti valiutos trumpini:")
        pasirinkta_valiuta2 = df.loc[df["Currency Code"] == pasirinkta_valiuta]
        print(f"Valiutos {pasirinkta_valiuta} 30 dienu informacija\n{pasirinkta_valiuta2}")
    except:
        print("Blogai ivestas trumpinys")

def norimos_valiutos_vidurkis():
    try:
        norima_valiuta = input("Prasome nurodyti valiutos trumpini: ")
        valiuta = df.loc[df['Currency Code'] == norima_valiuta]
        valiutos_vidurkis = valiuta['Proportion'].mean()
        print(f"30 dienu {norima_valiuta} valiutos vidurkis yra {valiutos_vidurkis}")
    except ValueError:
        print("Blogai ivestas valiutos kodas")


def get_prediction_and_plot():
    numerical_columns = df.select_dtypes(include=[np.number]).columns
    df[numerical_columns] = df[numerical_columns].fillna(df[numerical_columns].mean())

    X = df.drop(columns=['Date', 'Title', 'Currency Code', 'Change', 'Change %'], errors='ignore')
    y = df['Proportion']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Initialize the Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Calculate and print the Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")

    # Extract the currency title for the latest data
    currency_title = df.iloc[-1]['Currency Code']

    # Sort the test set and predictions for line plot
    sorted_indices = X_test.index.argsort()
    X_test_sorted = X_test.iloc[sorted_indices]
    y_test_sorted = y_test.iloc[sorted_indices]
    y_pred_sorted = y_pred[sorted_indices]

    # Plot the actual values and prediction as line charts
    plt.figure(figsize=(10, 5))
    plt.plot(X_test_sorted.index, y_test_sorted, color='blue', label='Actual values', marker='o')
    plt.plot(X_test_sorted.index, y_pred_sorted, color='red', label='Predicted values', linestyle='--', marker='o')
    plt.title(f'Actual vs Predicted Proportions for {currency_title}')
    plt.xlabel('Index')
    plt.ylabel('Proportion')
    plt.legend()
    plt.show()

    # Predict using the latest data entry
    latest_data = df.iloc[-1].drop(['Date', 'Title', 'Currency Code', 'Change', 'Change %'], errors='ignore').values.reshape(1, -1)
    latest_prediction = model.predict(latest_data)
    plt.axhline(y=latest_prediction, color='green', linestyle='--')
    plt.scatter(X_test_sorted.index[-1] + 1, latest_prediction, color='green', label='Latest prediction')
    plt.legend()
    plt.show()

    return latest_prediction[0]

def main():

    while True:
        rodyti_meniu()
        pasirinkimas = input("Pasirinkite operacijos numeri (1-4):->>")
        if pasirinkimas == "1":
            get_all_data()
        elif pasirinkimas == "2":
            norimos_valiutos_vidurkis()
        elif pasirinkimas == "3":
            get_prediction_and_plot()
        elif pasirinkimas == "4":
            print("Isejote is programos")
            break
        else:
            print("Neteisingas pasirinkimas. Pprasome pasirinkti nuo 1 iki 4 !!!")

# get_all_data(df)
# main()

# test  = get_all_data(df)
# print(test)
# def get_mean_of_last_two_entries(df)
#     return df.iloc[-2].mean()

# get_mean_of_last_two_entries(df)

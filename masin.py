# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error
# from sklearn import datasets
#
# iris = datasets.loads_iris()
# X = iris.data
# y = iris.target
# X_train, X_test, y_train, y_test = train_test_split(X,y, test_size= 0.3, random_state=42)
#
# ##--tiesines regresijos modelis
# model = LinearRegression()
# #pateikiame duomenis imokimui
# mode.fit(X_train, y_train)
# ##--bandome pateikti pragnozes
# y_predict = model.predict(X_test)
# mse = mean_squared_error(y_test, y_predict)
# print("Vidutine kvadratine paklaida:", mse)
#
# ##--is ko gaunami atsakymai
# # print(iris)
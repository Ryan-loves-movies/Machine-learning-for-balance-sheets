from prep_data_for_ml import prep_data_into_dataframe, add_balance_sheet_to_prices
from save_state.pickle_save import load_data_from_json, save_data_into_json
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing
import pandas as pd
from xgboost import XGBRegressor
import time

start = time.time()
# add_balance_sheet_to_prices("ml_finance.json")
print(time.time()-start)
ml_finance = load_data_from_json("ml_finance.json")
print(time.time()-start)
X,Y = prep_data_into_dataframe(ml_finance, drop_na = True)
print(time.time()-start)
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
print(x_train)
print(x_test)

def impute_values_for_empty_str(train, test):
    for i in train:
        for k in train[i]:
            if k=="":
                k = None
    for i in test:
        for k in test[i]:
            if k=="":
                k = None
    # imputer = SimpleImputer(strategy = 'constant', fill_value=0)
    # imputed_x_train = pd.DataFrame(imputer.fit_transform(train))
    # imputed_x_test = pd.DataFrame(imputer.transform(test))
    # imputed_x_train.columns = train.columns
    # imputed_x_test.columns = test.columns
    print(imputed_x_test)
    print(imputed_x_train)
    return imputed_x_train,imputed_x_test

# imputed_x_train, imputed_x_test = impute_values_for_empty_str(x_train,x_test)
# imputed_x_train = preprocessing.normalize(imputed_x_train)
# imputed_x_test = preprocessing.normalize(imputed_x_test)

# def optimise_random_forest(x_train,x_test,y_train,y_test):
#     mae = {}
#     for i in [100]:
#         random_forest = RandomForestRegressor(random_state = 0, n_estimators = i, min_samples_leaf = 2)
#         random_forest.fit(x_train,y_train)
#         predictions = random_forest.predict(x_test)
#         mae[i] = mean_absolute_error(predictions,y_test)
#     print(mae)
#     return mae
# dict_of_mae = optimise_random_forest(x_train,x_test,y_train,y_test)

def optimise_xgb(x_train,x_test,y_train,y_test):
    mae = {}
    for i in [100]:
        xgb = XGBRegressor(n_estimators=i, early_stopping_rounds=5, eval_set=[(x_test, y_test)])
        xgb.fit(x_train,y_train)
        predictions = xgb.predict(x_test)
        mae[i] = mean_absolute_error(predictions,y_test)
    return mae
dict_of_mae = optimise_xgb(x_train,x_test,y_train,y_test)

print(dict_of_mae)
print(time.time()-start)

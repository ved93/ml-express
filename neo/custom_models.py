
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
import numpy as np
from scipy.optimize import minimize

class MeanRegressor(BaseEstimator, RegressorMixin):
    def __init__(self):
        pass

    def fit(self, X, y):
        X,y =check_X_y(X, y)
        self.mean_ = y.mean()
        return self

    def predict(self,X):
        check_is_fitted(self)
        X= check_array(X)

        return np.array(X.shape[0]*self.mean_)


class LADRegression(BaseEstimator, RegressorMixin):
    def __init__(self):
        pass

    def fit(self, X,y):
        X,y = check_X_y(X,y)
        d = X.shape[1]
        mae_loss = lambda coefs: np.mean(np.abs(y-X@coefs[:-1]-coefs[-1]))
        *self.coef_, self.intercept_ = minimize(mae_loss, x0=np.array((d+1)*[0.])).x

        return self

    def predict(self,X):
        check_is_fitted(self)
        X= check_array(X)
        
        return X@self.coef_+self.intercept_ 






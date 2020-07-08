from scipy.stats import chi2_contingency
#stolen from https://stackoverflow.com/questions/46498455/categorical-features-correlation/46498792#46498792
#https://towardsdatascience.com/the-search-for-categorical-correlation-a1cf7f1888c9


from .imports import *

import warnings



def cramers_V(var1,var2) :
    crosstab =np.array(pd.crosstab(var1,var2, rownames=None, colnames=None)) # Cross table building
    stat = chi2_contingency(crosstab)[0] # Keeping of the test statistic of the Chi2 test
    obs = np.sum(crosstab) # Number of observations
    mini = min(crosstab.shape)-1 # Take the minimum value between the columns and the rows of the cross table
    return (stat/(obs*mini))


def correlation_ratio(categories, measurements):
#     we can use the Correlation Ratio (often marked using the greek letter eta). Mathematically, it is defined as the weighted variance of the mean of each category divided by the variance of all samples; in human language, the Correlation Ratio answers the following question: Given a continuous number, how well can you know to which category it belongs to? Just like the two coefficients we’ve seen before, here too the output is on the range of [0,1].
    
    
    
    fcat, _ = pd.factorize(categories)
    cat_num = np.max(fcat)+1
    y_avg_array = np.zeros(cat_num)
    n_array = np.zeros(cat_num)
    for i in range(0,cat_num):
        cat_measures = measurements[np.argwhere(fcat == i).flatten()]
        n_array[i] = len(cat_measures)
        y_avg_array[i] = np.average(cat_measures)
    y_total_avg = np.sum(np.multiply(y_avg_array,n_array))/np.sum(n_array)
    numerator = np.sum(np.multiply(n_array,np.power(np.subtract(y_avg_array,y_total_avg),2)))
    denominator = np.sum(np.power(np.subtract(measurements,y_total_avg),2))
    if numerator == 0:
        eta = 0.0
    else:
        eta = numerator/denominator
    return eta


def get_corr_df_cat(cat_cols,train_df_new):

    rows= []

    for var1 in cat_cols:
        col = []
        for var2 in cat_cols :
            cramers =cramers_V(train_df_new[var1], train_df_new[var2]) # Cramer's V test
            col.append(round(cramers,2)) # Keeping of the rounded value of the Cramer's V  
        rows.append(col)

    cramers_results = np.array(rows)
    dfcramers = pd.DataFrame(cramers_results, columns = cat_cols, index =cat_cols)

    return dfcramers


def get_corr_df_cat_cont(cat_cols,num_cols,train_df_new):

    rows= []

    for var1 in cat_cols:
        col = []
        for var2 in num_cols :
            cramers =correlation_ratio(train_df_new[var1], train_df_new[var2]) # Cramer's V test
            col.append(round(cramers,2)) # Keeping of the rounded value of the Cramer's V  
        rows.append(col)

    cramers_results = np.array(rows)
    dfcramers = pd.DataFrame(cramers_results, columns = num_cols, index =cat_cols)

    return dfcramers
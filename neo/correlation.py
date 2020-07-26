from scipy.stats import chi2_contingency
#stolen from https://stackoverflow.com/questions/46498455/categorical-features-correlation/46498792#46498792
#https://towardsdatascience.com/the-search-for-categorical-correlation-a1cf7f1888c9
#https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V
#http://www.people.vcu.edu/~pdattalo/702SuppRead/MeasAssoc/NominalAssoc.html
#for binary var, cramers v = phi so we will use always cramers v 


from .imports import *
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()

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



def get_corr_df_target(df,num_cols):
    
    # lets check correlation

    from scipy.stats import spearmanr
    import warnings
    warnings.filterwarnings("ignore")



    #let us first take the 'float' variables alone
    # and then get the correlation with the target variable to see how they are related.
    # Let us just impute the missing values with mean values to compute correlation coefficients #
    mean_values = df.mean(axis=0)
    train_df_new = df.fillna(mean_values )

    # Now let us look at the correlation coefficient of each of these variables #
    #logerror is the target var
    x_cols = [col for col in num_cols if col not in ['target','unique_id']] # if 'n' in col


    labels = []
    values = []
    for col in x_cols:
        labels.append(col)
        values.append(np.corrcoef(train_df_new[col].values, train_df_new.target.values)[0,1])
    corr_df = pd.DataFrame({'col_labels':labels, 'corr_values':values})
    corr_df = corr_df.sort_values(by='corr_values')
    print(corr_df)

    ind = np.arange(len(labels))
    width = 0.9
    fig, ax = plt.subplots(figsize=(8,6))
    # rects = ax.barh(ind, np.array(corr_df.corr_values.values), color='y')
    # # sns.barplot(x=ind, y=np.array(corr_df.corr_values.values))
    # ax.set_yticks(ind)
    # ax.set_yticklabels(corr_df.col_labels.values, rotation='horizontal')
    # ax.set_xlabel("Correlation coefficient")
    # ax.set_title("Correlation coefficient of the variables")
    # #autolabel(rects)
    # plt.show()



    ax=sns.barplot(y=ind, x=np.array(corr_df.corr_values.values) , orient='h')
    ax.set_yticks(ind)
    ax.set_yticklabels(corr_df.col_labels.values, rotation='horizontal')
    ax.set_xlabel("Correlation coefficient")
    ax.set_title("Correlation coefficient of the variables with Target")
    #autolabel(rects)
    plt.show()
    
    return corr_df

    


from sklearn.impute import SimpleImputer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


import scipy.stats as stats
import sklearn.preprocessing as preproc

def impute_plot(df,features, strategy='median'):
  impute_by_median = SimpleImputer(strategy=strategy)
  cleaned_features = impute_by_median.fit_transform(df[features])
  return cleaned_features



def remove_outlier_using_z_score (df, column):
  z_scores = stats.zscore(df[column])
  abs_z_scores = np.abs(z_scores)
  filtered_entries = (abs_z_scores < 3)
  return df[filtered_entries]

def compare_plot(df_list,x,y,subtitle,figsize=(25,10)):
  fig, axes = plt.subplots(nrows=len(df_list),figsize=figsize)
  fig.suptitle(subtitle, fontsize=16)
  for i,df in enumerate(df_list):
    sns.boxplot(x=x, y=y, data=df, ax=axes[i])
   

def scale_feature(df,features,strategy='minmax'):
  if strategy=='minmax':
    scale = preproc.minmax_scale(df[features])
  elif strategy=='standard':
    scale = preproc.StandardScaler().fit_transform(df[features])
  elif strategy == 'l2':
    scale = preproc.normalize(df[features],axis=0)
  return scale


if __name__ == "__main__":
    impute_plot()
    # clean_wine_df = remove_outlier_using_z_score(wine_df,'price')
    # compare_plot([wine_df,clean_wine_df],x='points',y='price',subtitle='Boxplot comparison (above:original,below:remove_outlier)',figsize=(25,10))
    # wine_df = clean_wine_df

    # salary_df['minmax_satisfaction_level'] = scale_feature(salary_df,['satisfaction_level'],strategy='minmax')
    # salary_df['standardized_satisfaction_level'] = scale_feature(salary_df,['satisfaction_level'],strategy='standard')
    # salary_df['l2_satisfaction_level'] = scale_feature(salary_df,['satisfaction_level'],strategy='l2')

    # draw_plot(salary_df,features=['minmax_satisfaction_level','standardized_satisfaction_level','l2_satisfaction_level']
    #         ,subtitle='Left:{},Mid:{},Right:{} satisfaction level'.format('minmax','standardized','l2')
    #         ,type='distplot')
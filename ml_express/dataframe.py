
##joins

def check_dim(df1,  df2):
    print(df1.shape,'   ', df2.shape)

    return True


def merge(df1,df2,how='left', on = cols):
    
    print(df1.shape,'   ', df2.shape)

    df = df1.merge(df2, how= how, on = cols)

    print(df.shape )

    return df




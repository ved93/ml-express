"""This script extracts rulesto understand the data bettter """




def build_model(X,y):
    # Load libraries
    from sklearn.tree import DecisionTreeClassifier
    from sklearn import datasets
    from IPython.display import Image  
    # Create decision tree classifer object
    clf = DecisionTreeClassifier(random_state=0,max_depth = 5, min_samples_split = 0.1, min_samples_leaf  = 0.05,
                                 criterion = 'entropy')   #, criterion = 'entropy'

    # Train model
    model = clf.fit(X, y)

    
    return model



def draw_tree(model,features):
    import pydotplus
    from IPython.display import Image  
    from sklearn import tree




    # Create DOT data
    tree.export_graphviz(model, out_file= "loan_default_tree.dot", filled=True,impurity  = False, precision =2,    #rotate  =True
                                    feature_names=features,proportion = True, label=None, rounded  =True
                                    ,class_names= ['Non-Default', 'Default'] 
                                   )


    graph = pydotplus.graph_from_dot_file("loan_default_tree.dot")
    # Show graph
    return Image(graph.create_png())







def value2prob(value):
    return value / value.sum(axis=1).reshape(-1, 1)



def get_rules(sample_id,X,model):
    
    from sklearn.tree import _tree
    feature_names   = X.columns.values

    node_indicator = model.decision_path(X)
    # n_nodes = model.tree_.node_count
    feature = model.tree_.feature
    threshold = model.tree_.threshold
    leave_id = model.apply(X)

    
    
    
#     print("WHEN", end=' ')
    rule = "WHEN" + ' ' 
    node_index = node_indicator.indices[node_indicator.indptr[sample_id]:
                                        node_indicator.indptr[sample_id + 1]]
    
#     print(node_index)
    for n, node_id in enumerate(node_index):
        if leave_id[sample_id] == node_id:
            values = model.tree_.value[node_id]
            probs = value2prob(values)
#             print('THEN Y={} (probability={}) (values={})'.format(
#                 probs.argmax(), probs.max(), values))
            
            rule = rule + '&& THEN Y={} (probability={}) (values={})'.format(
                probs.argmax(), probs.max(), values)
            
            continue
        if n > 0:
#             print('&& ', end='')
            
            rule  =rule+'&& '+''
            
        if (X.iloc[sample_id, feature[node_id]] <= threshold[node_id]):
            threshold_sign = "<="
        else:
            threshold_sign = ">"
        if feature[node_id] != _tree.TREE_UNDEFINED:
#             print(
#                 "%s %s %s" % (
#                     feature_names[feature[node_id]],
#                     #X.iloc[sample_id,feature[node_id]] # actual value
#                     threshold_sign,
#                     threshold[node_id]),
#                 end=' ')
            rule = rule + "%s %s %s" % (
                    feature_names[feature[node_id]],
                    #X.iloc[sample_id,feature[node_id]] # actual value
                    threshold_sign,
                    threshold[node_id]) + ' '
            
#             print(t)  
    return rule



# print_condition(1)

#  [print_condition(i) for i in (clf.predict(X) == 0).nonzero()[0]]

# [item[0] for item in df.rule.str.split('&&')]
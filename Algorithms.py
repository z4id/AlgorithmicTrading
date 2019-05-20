from sklearn.ensemble import RandomForestClassifier
from sklearn import neighbors
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
import pickle


def performRFClass(X_train, y_train, X_test, y_test, fout, savemodel):
    """
    Random Forest Binary Classification
    """
    clf = RandomForestClassifier(n_estimators=100, n_jobs=-1)
    clf.fit(X_train, y_train)
    
    if savemodel == True:
        fname_out = "Models/RF_"+fout + '.pickle'
        with open(fname_out, 'wb') as f:
            pickle.dump(clf, f)
    
    accuracy = clf.score(X_test, y_test)
    
    print accuracy


#     return accuracy,clf

def performSVMClass(X_train, y_train, X_test, y_test):
    """
    SVM binary Classification
    # """
    # c = parameters[0]
    # g = parameters[1]
    clf = SVC()
    clf.fit(X_train, y_train)
    
    accuracy = clf.score(X_test, y_test)
    
    print accuracy


def performAdaBoostClass(X_train, y_train, X_test, y_test):
    """
    Ada Boosting binary Classification
    """
    # n = parameters[0]
    # l = parameters[1]
    clf = AdaBoostClassifier()
    clf.fit(X_train, y_train)

    accuracy = clf.score(X_test, y_test)
    
    print accuracy


def performKNNClass(X_train, y_train, X_test, y_test):
    """
    KNN binary Classification
            """
    clf = neighbors.KNeighborsClassifier()
    clf.fit(X_train, y_train)
    
    accuracy = clf.score(X_test, y_test)
    
    print accuracy


def performGTBClass(X_train, y_train, X_test, y_test):
    """
    Gradient Tree Boosting binary Classification
    """
    clf = GradientBoostingClassifier(n_estimators=100)
    clf.fit(X_train, y_train)
    
    
    accuracy = clf.score(X_test, y_test)
    print accuracy
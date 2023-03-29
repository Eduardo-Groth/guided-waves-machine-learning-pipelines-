import numpy as np
exec(open('data_frame.py').read())

from sklearn import tree


clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)



# testing 
fname1 ='test.txt'



r1 = np.genfromtxt(fname1,delimiter=',',dtype=None, names=True);
test=np.zeros(len(r1))

for i in range(len(r1)):
    test[i]=float(r1[i][0])

result=clf.predict(test)
print('o modelo preve intervenção graus ' , result )


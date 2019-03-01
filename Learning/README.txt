1. Content of files
Programming language is Python, for python IDLE 3.6
There are 9 files
1) DT.py (Decision Tree)
2) LC.py (Linear Classifier)
3) NN.py (Neural Networks)
4) WillWait-data.csv (Decision Tree)
5) iris.data.discrete.csv (Decision Tree)
6) earthquake-clean.csv (Linear Classifier, Neural Networks)
7) earthquake-noisy.csv (Linear Classifier, Neural Networks)
8) iris.csv (Linear Classifier, Neural Networks)
9) wine.csv (Linear Classifier, Neural Networks)
libs which are used in programming
1) pandas
2) random
3) numpy
4) math
5) matplotlib
2. How to run files
Step1: go to the directory where you have all your source files
Step2: enter "python DT.py" or "python LC.py" or "python NN.py"
3. How to upload files and query

Decision Tree
DT.py
Step1: the system will ask you to input the name of the file, such as “WillWait-data.csv”
“iris.data.discrete.csv”
Step2: the system will upload the content of file
Step3: the system will ask you to input the name of classifier, for “WillWait-data.csv” which3 / 6
is “WillWait”, for “iris.data.discrete.csv” which is “class”
Step4: then the system will show you the training result as a decision tree
Step5: then the system will require you to input new example that you want to classify
1) The example has to be complete and include all attributes in the decision tree
2) Each attribute name and value should be separated by “,”
3) You can exit by inputting “end” if you want to quit
Step6: finally, the system will ask if you want to exit

Linear classifiers
LC.py
Step1: the system will ask you to input the name of the file, such as “earthquake-clean.csv”
“iris.csv”
Step2: the system will upload the content of file
Step3: the system will ask you to input the name of classifier, for “earthquake-clean.csv”
which is “class”, for “Iris.csv” which is “class”
Step5: then the system will ask you to input times of iteration
Step6: then the system will ask you to choose method, 1 for perceptron, 2 for logistic
Step7: then the system will show you the training result and accuracy of training dataset
and test dataset
Step8: then the system will require you to input new example that you want to classify
1) The example is the value for each attribute, be careful about the sequence
2) Each attribute name and value should be separated by “,”
3) You can exit by inputting “end” if you want to quit
Step9: finally, the system will ask if you want to exit

Neural networks
NN.py
Step1: the system will ask you to input the name of the file, such as “iris.csv”
Step2: the system will upload the content of file
Step3: the system will ask you to input the name of classifier, for “Iris.csv” which is “class”
for “wine.csv” which is “class”,
Step5: then the system will ask you to input units for hidden layer, times of iteration
Step6: then the system will show you the training result and accuracy of training dataset
and test dataset
Step7: then the system will require you to input new example that you want to classify
4) The example has to be complete and include all attributes in the decision tree
5) Each attribute name and value should be separated by “,”
6) You can exit by inputting “end” if you don’t want to input new example
Step8: finally, the system will ask if you want to exit
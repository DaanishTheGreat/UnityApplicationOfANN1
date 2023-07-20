import socket
import numpy as np
import tensorflow as tf
import pandas as pd

#Import Data Set 
dataset = pd.read_csv("TrainData.csv")
X = dataset.iloc[: , 1:5]
Y = dataset.iloc[:,  5:]

#Split Training and Test Set
from sklearn.model_selection import train_test_split
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size = 0.2, random_state = 0)


#Implement Feature Scaling (IDK what that is for) MAY NEED THIS
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
Xtrain = sc.fit_transform(Xtrain)
Xtest = sc.fit_transform(Xtest)

#Building Artificial Neural Network
ANN = tf.keras.models.Sequential()
#Add First Layer Output
ANN.add(tf.keras.layers.Dense(32, activation='relu', input_shape=(4,)))
#Add Second Hidden Layer
ANN.add(tf.keras.layers.Dense(32, activation='relu'))
#Add Output Layer
ANN.add(tf.keras.layers.Dense(2))

#Training Artificial Neural Network
ANN.compile(optimizer= 'adam', loss= 'mean_squared_error', metrics= ['accuracy'])
#Actual Training of the ANN
ANN.fit(Xtrain, Ytrain, batch_size= 32, epochs= 100)
print(ANN.predict([[8, 8, -7, -7]]))







server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 25565)) #Server socket listens on port 25565
server_socket.listen(1)
PreviousPositionData = ""
PreviousXMoveInstruction = ""
PreviousYMoveInstruction = ""
print("Ready For Testing!")
while(True):
    client_socket, address = server_socket.accept()
    data = client_socket.recv(1024)
    PositionData = data.decode("ascii")

    if PositionData != PreviousPositionData:
        PreviousPositionData = PositionData

        ListOfPositionData = PositionData.split(":")

        Prediction = ANN.predict([[int(ListOfPositionData[0]), int(ListOfPositionData[1]), int(ListOfPositionData[2]), int(ListOfPositionData[3])]])
        Prediction1 = Prediction.tolist()
        Prediction2 = Prediction1[0]
        print(str(Prediction2[0]) + " " + str(Prediction2[1]))
        SolutionXMove = 0
        SolutionYMove = 0
        if(float(Prediction2[0]) < 0):
            SolutionXMove = -1
        else:
            SolutionXMove = 1
        if(float(Prediction2[1]) < 0):
            SolutionYMove = -1
        else:
            SolutionYMove = 1
           

        client_socket.send(bytes(str(SolutionXMove) + ":" + str(SolutionYMove), "ascii"))

        PreviousXMoveInstruction = str(SolutionXMove)
        PreviousYMoveInstruction = str(SolutionYMove)
    else:
        client_socket.send(bytes(PreviousXMoveInstruction + ":" + PreviousYMoveInstruction, "ascii"))

    #client_socket.send(bytes("1:1", "ascii"))
    client_socket.close()


#It seems to work but its extremely laggy, fix the lag
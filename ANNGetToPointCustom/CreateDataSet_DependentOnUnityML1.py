import socket
import csv

#TCP Server Listening to Unity ML1 to obtain data and add to csv file for training
def DetermineGoal(PlayerPostion, GoalPosition):
    if PlayerPostion > GoalPosition:
        return -1
    elif PlayerPostion < GoalPosition:
        return 1
    else:
        return 0

#CSV format: Player X Position; Player Y Position; Goal X Position; Goal Y Position; Desired Move X Position[-1, 1]; Desired Move Y position[-1, 1, (Improbable)0] 
CSVRowList = []
CSVColumnList = ["Row Number" ,"PlayerXPosition", "PlayerYPosition", "GoalXPosition", "GoalYPosition", "DesiredMoveXPosition", "DesiredMoveYPosition"]
CSVRowList.append(CSVColumnList)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 25565)) #Server socket listens on port 25565
server_socket.listen(1)
PositionData = ""
while True:
    #print("Server is waiting for connection on port 25565")
    client_socket, address = server_socket.accept()
    #print("Client connected from", address)
    data = client_socket.recv(1024)
    
    PositionData = data.decode("ascii")
    PositionDataSplitByComma = PositionData.split(",")
    GoalPositionXYList = PositionDataSplitByComma[0].split(":")
    PositionDataSplitByComma.pop(0)
    PositionDataSplitByComma.pop(-1)
    for EachPositionData in PositionDataSplitByComma:
        EachPositionDataSplitByColon = EachPositionData.split(":")
        DesiredMoveXPosition = DetermineGoal(int(EachPositionDataSplitByColon[0]), int(GoalPositionXYList[0]))
        DesiredMoveYPosition = DetermineGoal(int(EachPositionDataSplitByColon[1]), int(GoalPositionXYList[1]))
        CSVRow = [len(CSVRowList), int(EachPositionDataSplitByColon[0]), int(EachPositionDataSplitByColon[1]), int(GoalPositionXYList[0]), int(GoalPositionXYList[1]), DesiredMoveXPosition, DesiredMoveYPosition]
        CSVRowList.append(CSVRow)

    with open('TrainData.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(CSVRowList)

    print(data.decode("ascii"))
    try:
        client_socket.send(bytes("Message Recieved", "ascii"))
    except:
        print("Connection Terminated by Client")
    client_socket.close()



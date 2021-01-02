import os
currentDir  = os.path.dirname(os.path.realpath(__file__))
UsersFiles = os.listdir(os.path.join(currentDir,"downloads"))
print(UsersFiles)
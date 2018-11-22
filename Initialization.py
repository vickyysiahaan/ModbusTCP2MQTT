from time import localtime, strftime
import json, time, os, inspect
from Constants import *

FolderPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

#MQTT Conf
with open(FolderPath + '/JSON/Config/MQTTConfig.json') as json_data:
    MQTT = json.load(json_data)
    #Create variable with name and value based in key and value in MQTT dictionary
    locals().update(MQTT)
#print(MQTT)

#Etc Conf
with open(FolderPath + '/JSON/Config/etc.json') as json_data:
    etc = json.load(json_data)
    #Create variable with name and value based in key and value in etc dictionary
    locals().update(etc)
#print(etc)

#Devices Identity
with open(FolderPath + '/JSON/Config/DevicesIdentity.json') as json_data:
    DevID = json.load(json_data)
DevNum = len(list(DevID.keys()))
Dev_ID = list(DevID.values())
#print(Dev_ID)

#### Classify variables based on their register types ####
VarsPerTopic = []
for i in range(0,len(TopicList)):
    VarsPerTopic.append([])
    for j in range(0, DevNum):
        VarsPerTopic[i].append([])

#Variables Identity
AllVar = list()
for i in range(1,DevNum+1):
    with open(FolderPath + '/JSON/Config/Device%dVariables.json' %i) as json_data:
        Var=json.load(json_data)
        VarID = list(Var.values())
        VarNum = len(VarID)

        _VarID = list()
        for j in range(0,VarNum):
            varid = list(VarID[j].values())
            _VarID.append(varid)
            varTopic = varid[6]
            varName = varid[0]
            for topic in varTopic:
                VarsPerTopic[topic-1][i-1].append(varName)
        AllVar.append(_VarID)
#print(AllVar)
#print(VarsPerTopic)
        
#### Classify variables based on their register type and data type ####
## Initialization ##
# Variable Name
Disc_In_VarName = list()
Disc_Out_VarName = list()

for _DataType in DataTypes:
    if _DataType != BIT:
        command = """Hold_Reg_VarName_%s = list()""" %_DataType
        exec(command)
        command = """In_Reg_VarName_%s = list()""" %_DataType
        exec(command)

# Multiplier
for _DataType in DataTypes:
    if _DataType != BIT:
        command = """Hold_Reg_Multiplier_%s = list()""" %_DataType
        exec(command)
        command = """In_Reg_Multiplier_%s = list()""" %_DataType
        exec(command)

# Register Address        
Disc_In_Address = list()
Disc_Out_Address = list()

for _DataType in DataTypes:
    if _DataType != BIT:
        command = """Hold_Reg_Address_%s = list()""" %_DataType
        exec(command)
        command = """In_Reg_Address_%s = list()""" %_DataType
        exec(command)

## Start to fill blank lists above ##
for i in range(0,DevNum):
    Disc_In_VarName.append(list())
    Disc_Out_VarName.append(list())

    for _DataType in DataTypes:
        if _DataType != BIT:
            command = """Hold_Reg_VarName_%s.append(list())""" %_DataType
            exec(command)
            command = """In_Reg_VarName_%s.append(list())""" %_DataType
            exec(command)

    for _DataType in DataTypes:
        if _DataType != BIT:
            command = """Hold_Reg_Multiplier_%s.append(list())""" %_DataType
            exec(command)
            command = """In_Reg_Multiplier_%s.append(list())""" %_DataType
            exec(command)
            
    Disc_In_Address.append(list())
    Disc_Out_Address.append(list())
    
    for _DataType in DataTypes:
        if _DataType != BIT:
            command = """Hold_Reg_Address_%s.append(list())""" %_DataType
            exec(command)
            command = """In_Reg_Address_%s.append(list())""" %_DataType
            exec(command)

    for j in range(0,len(AllVar[i])):
        VarName = AllVar[i][j][0]
        DataType = AllVar[i][j][4]
        Multiplier = AllVar[i][j][5]
        Reg = AllVar[i][j][1]
        RegType = AllVar[i][j][2]
        WordLength = AllVar[i][j][3]
        if RegType == DISCRETEIN:
            Disc_In_VarName[i].append(VarName)
            Disc_In_Address[i].append(list(range(Reg,Reg+WordLength)))
        elif RegType == DISCRETEOUT:
            Disc_Out_VarName[i].append(VarName)
            Disc_Out_Address[i].append(list(range(Reg,Reg+WordLength)))
        elif RegType == HOLDINGREG:
            command = """
Hold_Reg_VarName_%s[i].append(VarName)
Hold_Reg_Address_%s[i].append(list(range(Reg,Reg+WordLength)))
Hold_Reg_Multiplier_%s[i].append(Multiplier)
"""%(DataType,DataType,DataType)
            exec(command)
        elif RegType == INPUTREG:
            command = """
In_Reg_VarName_%s[i].append(VarName)
In_Reg_Address_%s[i].append(list(range(Reg,Reg+WordLength)))
In_Reg_Multiplier_%s[i].append(Multiplier)
"""%(DataType,DataType,DataType)
            exec(command)

    # Sort items in variable name list and register address list based on register address order from the smallest to the largest
    try:
        Disc_In_Address[i], Disc_In_VarName[i] = (list(t) for t in zip(*sorted(zip(Disc_In_Address[i], Disc_In_VarName[i]))))
    except Exception as e:
        #print(e)
        pass
    try:
        Disc_Out_Address[i], Disc_Out_VarName[i] = (list(t) for t in zip(*sorted(zip(Disc_Out_Address[i], Disc_Out_VarName[i]))))
    except Exception as e:
        #print(e)
        pass
    
    for _DataType in DataTypes:
        try:
            command = """
Hold_Reg_Address_%s[i], Hold_Reg_VarName_%s[i], Hold_Reg_Multiplier_%s[i] = (list(t) for t in zip(*sorted(zip(Hold_Reg_Address_%s[i], Hold_Reg_VarName_%s[i], Hold_Reg_Multiplier_%s[i]))))
""" %(_DataType,_DataType,_DataType,_DataType,_DataType,_DataType)
            exec(command)
        except Exception as e:
            #print(e)
            pass
        try:
            command = """
In_Reg_Address_%s[i], In_Reg_VarName_%s[i], In_Reg_Multiplier_%s[i] = (list(t) for t in zip(*sorted(zip(In_Reg_Address_%s[i], In_Reg_VarName_%s[i], In_Reg_Multiplier_%s[i]))))
""" %(_DataType,_DataType,_DataType,_DataType,_DataType,_DataType)
            exec(command)
        except Exception as e:
            #print(e)
            pass

############## Simplifier ##############
# Increase modbus polling efficiency to reduce polling time 
# how? some adjacent registers are unified into one sublist

DiscInVarName = Disc_In_VarName
DiscInAddress = []
for i in range(0, len(Disc_In_Address)):
    DiscInAddress.append([])
    for reg in Disc_In_Address[i]:
        if len(DiscInAddress[i])==0:
            DiscInAddress[i].append(reg)
        else:
            if (reg[0]-DiscInAddress[i][-1][-1])==1:
                DiscInAddress[i][-1]+=reg
            else:
                DiscInAddress[i].append(reg)
#print(DiscInAddress)
                
DiscOutVarName = Disc_Out_VarName
DiscOutAddress = []
for i in range(0, len(Disc_Out_Address)):
    DiscOutAddress.append([])
    for reg in Disc_Out_Address[i]:
        if len(DiscOutAddress[i])==0:
            DiscOutAddress[i].append(reg)
        else:
            if (reg[0]-DiscOutAddress[i][-1][-1])==1:
                DiscOutAddress[i][-1]+=reg
            else:
                DiscOutAddress[i].append(reg)
#print(DiscOutAddress)

for _DataType in DataTypes:
    if _DataType != BIT:
        if _DataType == STRING:
            command = """
HoldRegVarName_%s = Hold_Reg_VarName_%s
HoldRegMultiplier_%s = Hold_Reg_Multiplier_%s
HoldRegAddress_%s = Hold_Reg_Address_%s
""" %(_DataType,_DataType,_DataType,_DataType,_DataType,_DataType)
            exec(command)
        else:
            command = """
HoldRegVarName_%s = Hold_Reg_VarName_%s
HoldRegMultiplier_%s = Hold_Reg_Multiplier_%s
HoldRegAddress_%s = []
for i in range(0, len(Hold_Reg_Address_%s)):
    HoldRegAddress_%s.append([])
    for reg in Hold_Reg_Address_%s[i]:
        if len(HoldRegAddress_%s[i])==0:
            HoldRegAddress_%s[i].append(reg)
        else:
            if (reg[0]-HoldRegAddress_%s[i][-1][-1])==1:
                HoldRegAddress_%s[i][-1]+=reg
            else:
                HoldRegAddress_%s[i].append(reg)
#print(HoldRegAddress_%s)
""" %(_DataType,_DataType,_DataType,_DataType,_DataType,_DataType,_DataType
      ,_DataType,_DataType,_DataType,_DataType,_DataType,_DataType,_DataType)
            exec(command)

for _DataType in DataTypes:
    if _DataType != BIT:
        if _DataType == STRING:
            command = """
InRegVarName_%s = In_Reg_VarName_%s
InRegMultiplier_%s = In_Reg_Multiplier_%s
InRegAddress_%s = In_Reg_Address_%s
""" %(_DataType,_DataType,_DataType,_DataType,_DataType,_DataType)
            exec(command)
        else:
            command = """
InRegVarName_%s = In_Reg_VarName_%s
InRegMultiplier_%s = In_Reg_Multiplier_%s
InRegAddress_%s = []
for i in range(0, len(In_Reg_Address_%s)):
    InRegAddress_%s.append([])
    for reg in In_Reg_Address_%s[i]:
        if len(InRegAddress_%s[i])==0:
            InRegAddress_%s[i].append(reg)
        else:
            if (reg[0]-InRegAddress_%s[i][-1][-1])==1:
                InRegAddress_%s[i][-1]+=reg
            else:
                InRegAddress_%s[i].append(reg)
#print(InRegAddress_%s)
""" %(_DataType,_DataType,_DataType,_DataType,_DataType,_DataType,_DataType
      ,_DataType,_DataType,_DataType,_DataType,_DataType,_DataType,_DataType)
            exec(command)
    
        
#Slicer (for limitting the list length)
MaxWordLength = 50

for _DataType in DataTypes:
    if _DataType != BIT:
        command = """
_HoldRegAddress_%s = []
for i in range(0, len(HoldRegAddress_%s)):
    _HoldRegAddress_%s.append([])
    for j, item in enumerate(HoldRegAddress_%s[i]):
        if len(item) > MaxWordLength:
            div, mod = divmod(len(item), MaxWordLength)
            if mod != 0:
                SplitInto = div+1
            else:
                SplitInto = div
            for k in range(0, SplitInto):
                if k == SplitInto-1:
                    _HoldRegAddress_%s[i].append(item[k*MaxWordLength:])
                else:
                    _HoldRegAddress_%s[i].append(item[k*MaxWordLength:(k+1)*MaxWordLength])
        else:
            _HoldRegAddress_%s[i].append(item)
            
HoldRegAddress_%s= _HoldRegAddress_%s
""" %(_DataType,_DataType,_DataType,_DataType,_DataType,_DataType,_DataType,_DataType,_DataType)
        exec(command)

for _DataType in DataTypes:
    if _DataType != BIT:
        command = """
_InRegAddress_%s = []
for i in range(0, len(InRegAddress_%s)):
    _InRegAddress_%s.append([])
    for j, item in enumerate(InRegAddress_%s[i]):
        if len(item) > MaxWordLength:
            div, mod = divmod(len(item), MaxWordLength)
            if mod != 0:
                SplitInto = div+1
            else:
                SplitInto = div
            for k in range(0, SplitInto):
                if k == SplitInto-1:
                    _InRegAddress_%s[i].append(item[k*MaxWordLength:])
                else:
                    _InRegAddress_%s[i].append(item[k*MaxWordLength:(k+1)*MaxWordLength])
        else:
            _InRegAddress_%s[i].append(item)
            
InRegAddress_%s= _InRegAddress_%s
""" %(_DataType,_DataType,_DataType,_DataType,_DataType,_DataType,_DataType,_DataType,_DataType)
        exec(command)


print("Config JSONs Interpreter Has Finished")


###  For debugging
'''
print("============== Discrete Input Register ===============")
print(DiscInVarName)
print(DiscInAddress)

print("============== Discrete Output Register ===============")
print(DiscOutVarName)
print(DiscOutAddress)

print("============== Holding Register ===============")
for _DataType in DataTypes:
    if _DataType != BIT:
        command = """
print(_DataType)
print(HoldRegVarName_%s)
print(HoldRegMultiplier_%s)
print(HoldRegAddress_%s)""" %(_DataType,_DataType,_DataType)
        exec(command)

print("============== Input Register ===============")
for _DataType in DataTypes:
    if _DataType != BIT:
        command = """
print(_DataType)
print(InRegVarName_%s)
print(InRegMultiplier_%s)
print(InRegAddress_%s)""" %(_DataType,_DataType,_DataType)
        exec(command)
'''

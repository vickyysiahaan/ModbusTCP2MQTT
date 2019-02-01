import json, os, inspect, traceback, sys, argparse, ast
import MyDB, MyModbusTCP
from Initialization import *
from time import strftime,localtime
from Constants import *

db = MyDB.DataBase()

# Get Folder Path
FolderPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# Main Function
def main(args):
    try:
        DevNum = args.DeviceNo
        VarNameList = args.VarName.split(',')
        ValueList = args.Value.split(',')
    except:
        pass
    #print(AllVar)
    Write(DevNum,VarNameList,ValueList)

def Write(DevNum,keyList,valList):
    #check device
    try:
        Device_Identity = Dev_ID[DevNum-1]
    except:
        print("Device Number is not detected in list of device")
    #get device profile
    DevName = Device_Identity['Name']
    IPAddress = Device_Identity['IPAddress']
    Port = Device_Identity['Port']
    Timeout = Device_Identity['Timeout']
    ByteOrder = Device_Identity['ByteOrder']

    #connect to device
    try:
        device = MyModbusTCP.Device(IPAddress, Port, Timeout, ByteOrder)
        #print("Connected to ", DevName)
    except:
        tb = traceback.format_exc()
        #print(tb)
        print("FAILED Connection to", DevName)

    if (len(keyList)==len(valList)):
        Data = dict()
        for i,key in enumerate(keyList):
            value = ast.literal_eval(valList[i])
            try:
                index = AllVarName[DevNum-1].index(key)
                RegisterType = AllVar[DevNum-1][index][2]
                if RegisterType == DISCRETEOUT:
                    registerAddress = AllVar[DevNum-1][index][1]
                    if type(value) == int or type(value) == bool:
                        try:
                            device.write_bit(registerAddress, value)
                            Data[key]=value
                        except Exception as e:
                            print(e)
                    else:
                        print("value inserted for", key, "is not valid")
                    
                elif RegisterType == HOLDINGREG:
                    registerAddress = AllVar[DevNum-1][index][1]
                    wordlength = AllVar[DevNum-1][index][3]
                    dtype = AllVar[DevNum-1][index][4]
                    mul = AllVar[DevNum-1][index][5]

                    _val = value/mul
                    try:
                        device.write_num(registerAddress, _val, dtype)
                        Data[key]=value
                    except Exception as e:
                        print(e)
                else:
                    print(key, "Register cannot be written")
            except Exception as e:
                print(e)
                
        print("Successful")
        Timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
        Data['Timestamp'] = Timestamp
        
        db.InsertData(DevNum, DevName, Data)
        db.commit()
        db.close()
        
    else:
        raise ValueError("Length of Variable Name List and Value List are different") 
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--DeviceNo", type=int, help="Device Number", default=None)
    parser.add_argument("--VarName", type=str, help="List of variable name", default=None)
    parser.add_argument("--Value", type=str, help="List of variable value", default=None)
    
    args = parser.parse_args(sys.argv[1:]);
    
    main(args);

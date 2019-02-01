import paho.mqtt.client as mqtt
from Constants import *
from Initialization import *
from time import strftime, localtime
import json, time, os, inspect, MyModbusTCP, traceback, gc, threading, pprint, signal, psutil
import paho.mqtt.client as mqtt
import MyDB

FolderPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

_FINISH = False

def get_process_memory():
    process = psutil.Process(os.getpid())
    return [process.memory_info().rss,process.memory_full_info().rss]

#print(LoggingPeriod)
db = MyDB.DataBase()

def PollerPerDevice(did,Device_Identity):
    DevName = Device_Identity['Name']
    IPAddress = Device_Identity['IPAddress']
    Port = Device_Identity['Port']
    Timeout = Device_Identity['Timeout']
    ByteOrder = Device_Identity['ByteOrder']
    Token = Device_Identity['AccessToken']
    mqtt_client = mqtt.Client()

    isConnected = False
    InitialState = True

    tLog0 = 0
    
    mqtt_client.username_pw_set(Token)
    Trial = 1
    while(Trial <=3):
        try:
            mqtt_client.connect(BrokerHOST, MQTTPort, 60)
            mqtt_client.loop_start()
            isConnected = True
            print("Client-%s connected to MQTT Broker" %DevName)
            break
        except:
            Trial += 1
            print("Client-%s FAILED connected to MQTT Broker" %DevName)
            time.sleep(3)
            
    while(not _FINISH):
        try:
            tPoll0 = time.time()    #begin polling time
            if InitialState:
                tLog0 = tPoll0   
            if not isConnected:
                try:
                    mqtt_client.connect(BrokerHOST, MQTTPort, 60)
                    mqtt_client.loop_start()
                    isConnected = True
                    print("Client-%s connected to MQTT Broker" %DevName)
                    break
                except:
                    Trial += 1
                    print("Client-%s FAILED connected to MQTT Broker" %DevName)
                
            try:
                device = MyModbusTCP.Device(IPAddress, Port, Timeout, ByteOrder)
                print("Connected to ", DevName)
            except:
                tb = traceback.format_exc()
                #print(tb)
                print("FAILED Connection to", DevName)
                
            Data = {}
                
            ### Read Discrete Input Registers
            if len(DiscInVarName[did-1]) != 0:
                DiscInData = device.read_bits(DiscInVarName[did-1],DiscInAddress[did-1],functioncode=2)
                #print(DiscInData)
                Data.update(DiscInData)
                
            ### Read Discrete Output Registers
            if len(DiscOutVarName[did-1]) != 0:
                DiscOutData = device.read_bits(DiscOutVarName[did-1],DiscOutAddress[did-1],functioncode=1)
                #print(DiscOutData)
                Data.update(DiscOutData)
                    
            ### Read Input Registers
            for _DataType in DataTypes:
                if _DataType in [INT16, INT32, INT64]:
                    command = """
if len(InRegVarName_%s[did-1]) != 0:
    InRegData = device.read_%s(InRegVarName_%s[did-1], InRegAddress_%s[did-1], InRegMultiplier_%s[did-1], signed=True, functioncode=4)
    #print(InRegData)
    Data.update(InRegData)
"""%(_DataType,_DataType,_DataType,_DataType,_DataType)
                    exec(command)
                elif _DataType in [UINT16, UINT32, UINT64]:
                    command = """
if len(InRegVarName_%s[did-1]) != 0:
    InRegData = device.read_%s(InRegVarName_%s[did-1], InRegAddress_%s[did-1], InRegMultiplier_%s[did-1], signed=False, functioncode=4)
    #print(InRegData)
    Data.update(InRegData)
"""%(_DataType,_DataType[1:],_DataType,_DataType,_DataType)
                    exec(command)
                elif _DataType in [FLOAT16, FLOAT32, FLOAT64]:
                    command = """
if len(InRegVarName_%s[did-1]) != 0:
    InRegData = device.read_%s(InRegVarName_%s[did-1], InRegAddress_%s[did-1], InRegMultiplier_%s[did-1], functioncode=4)
    #print(InRegData)
    Data.update(InRegData)
"""%(_DataType,_DataType,_DataType,_DataType,_DataType)
                    exec(command)
                elif _DataType == STRING:
                    command = """
if len(InRegVarName_%s[did-1]) != 0:
    InRegData = device.read_%s(InRegVarName_%s[did-1], InRegAddress_%s[did-1], functioncode=4)
    #print(InRegData)
    Data.update(InRegData)
"""%(_DataType,_DataType,_DataType,_DataType)
                    exec(command)

            #Read Holding Registers
            for _DataType in DataTypes:
                if _DataType in [INT16, INT32, INT64]:
                    command = """
if len(HoldRegVarName_%s[did-1]) != 0:
    HoldRegData = device.read_%s(HoldRegVarName_%s[did-1], HoldRegAddress_%s[did-1], HoldRegMultiplier_%s[did-1], signed=True, functioncode=3)
    #print(HoldRegData)
    Data.update(HoldRegData)
"""%(_DataType,_DataType,_DataType,_DataType,_DataType)
                    exec(command)
                elif _DataType in [UINT16, UINT32, UINT64]:
                    command = """
if len(HoldRegVarName_%s[did-1]) != 0:
    HoldRegData = device.read_%s(HoldRegVarName_%s[did-1], HoldRegAddress_%s[did-1], HoldRegMultiplier_%s[did-1], signed=False, functioncode=3)
    #print(HoldRegData)
    Data.update(HoldRegData)
"""%(_DataType,_DataType[1:],_DataType,_DataType,_DataType)
                    exec(command)
                elif _DataType in [FLOAT16, FLOAT32, FLOAT64]:
                    command = """
if len(HoldRegVarName_%s[did-1]) != 0:
    HoldRegData = device.read_%s(HoldRegVarName_%s[did-1], HoldRegAddress_%s[did-1], HoldRegMultiplier_%s[did-1], functioncode=3)
    #print(HoldRegData)
    Data.update(HoldRegData)
"""%(_DataType,_DataType,_DataType,_DataType,_DataType)
                    exec(command)
                elif _DataType == STRING:
                    command = """
if len(HoldRegVarName_%s[did-1]) != 0:
    HoldRegData = device.read_%s(HoldRegVarName_%s[did-1], HoldRegAddress_%s[did-1], functioncode=3)
    #print(HoldRegData)
    Data.update(HoldRegData)
"""%(_DataType,_DataType,_DataType,_DataType)
                    exec(command)
                
            tPoll1 = time.time()    #end polling time
                
            #PollingDuration = round(tPoll1-tPoll0, 2)
            PollingDuration = tPoll1-tPoll0
            Data['PollingDuration'] = PollingDuration
            Timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
            Data['Timestamp'] = Timestamp

            #pprint.pprint(Data, width=1)
                
            with open(FolderPath + '/JSON/Data/Device%dData.json'%did, 'w') as file:
                file.write(json.dumps(Data, indent=4))

            tLog1 = tPoll1
            if InitialState or tLog1 - tLog0 >= LoggingPeriod:
                db.InsertData(did, DevName, Data)
                db.commit()
                InitialState = False
                #isAlreadyLogged = True
                print(Timestamp, ">>>", DevName, "Data are Logged")
                tLog0 = tPoll1
                    
            DataPerTopic = []
            for i in range(0,len(VarsPerTopic)):
                vals = []
                for name in VarsPerTopic[i][did-1]:
                    vals.append(Data[name])
                DataPerTopic.append(dict(zip(VarsPerTopic[i][did-1],vals)))
            #pprint.pprint(DataPerTopic, width=1)

            i = 0
            for topic in TopicList:
                if DataPerTopic[i] != {}:
                    mqtt_client.publish(topic, json.dumps(DataPerTopic[i]),0)
                    print(Timestamp, ">>>", DevName, "Data are Published in topic:", topic)
                i += 1
                
            time.sleep(PollingInterval)
            device.close()
        except KeyboardInterrupt:
            mqtt_client.loop_stop()
            print('Interrupted')
            break
        except:
            tb = traceback.format_exc()
            print(tb)
            time.sleep(PollingInterval)

class ServiceExit(Exception):
    pass

def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit

if __name__ == '__main__':
    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    try:    
        threads = []
        
        for i,dev in enumerate(Dev_ID):
            threads.append(threading.Thread(target=PollerPerDevice, args=[i+1,dev]))
            threads[i].setDaemon(True)
            threads[i].start()

        while(True):
            time.sleep(0.5)
            
    except ServiceExit:
        print("finished")
        _FINISH = True
        for _thread in threads:
            _thread.join()
        print('All Thread Stopped')
        db.close()  
    except:
        tb = traceback.format_exc()
        #print(tb)
        db.close()
        

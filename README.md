What you need to know:
1. I assume you: 
	- have a basic knowledge about Modbus TCP Communication (if you are a beginner, read this http://www.simplymodbus.ca/FAQ.htm)
	- use python3.6 or later.

   Python modules needed:
	- pyModbusTCP
	- numpy
	- MySQLdb
	- paho.mqtt
	- pprint
	- psutil

2. This program also requires MySQL database to be installed.
   Name, username, and the password of the database can be set in MyDB.py
   
3. Modbus TCP devices and their registers that want to be read can be configured through JSON files in directory JSON/Config

   a. DevicesIdentity.json 
      contains information about devices identity.
      - Name			: Name of the device
      - IPAddress		: device ip address
      - Port		: modbus tcp port of the device
      - ByteOrder		: byte order in the device memory system
      - AccessToken		: mqtt username (for authentication with mqtt broker),
      - Timeout			: timeout limit for the device
	  
	  
   b. MQTTConfig.json 
      contains settings for mqtt communication and polling interval.
      - PollingInterval	: interval of devices data polling 
      - BrokerHOST		: mqtt broker address
      - MQTTPort		: mqtt broker port
      - TopicList		: mqtt topic list. for example: ["v1/devices/me/telemetry", "v1/devices/me/attributes"]
	
	
   c. DeviceVariables.json
      contains list of variables in each device with its OID, Datatype, etc.
      - Name 		: 	name of the variable
      - RelativeRegAddress	: 	relative register address of the variable
	  - RegisterType	: Register Type. ("Discrete Input", "Discrete Output","Holding Register","Input Register")
	  - WordLength		: Number of register used to store the variable value
      - Datatype	: 	Variable data type ("INT16","INT32","INT64","UINT16","UINT32","UINT64","FLOAT16","FLOAT32","FLOAT64","STRING","BIT")
      - Multiplier	: 	Value of this variable will be multiplied with this value (if you need numerical data processing)
      - PublishTopic	: 	mqtt topic index in TopicList. The variable value will be published on this topic.
      
	
	
4. To begin data polling, just run the Poller.py. The program will automatically publish the data to mqtt topic periodically, based on the polling interval. The result can also be seen in JSON/Result


5. Device control via MQTT is still in development. But you can do device control by using Control.py directly.

   Run this command:
   
   python3.6 Control.py --DeviceNo [Device_Number_Index] --VarName [List_of_variable] --Value [List_of_Value]
   
   Device_Number_Index 	==> device index (based on the order in DevicesIdentity)
   
   List_of_variable		==> list of variable that want to be set
   
   List_of_Value		==> list of desired value of each variable
   
   for example:
   
   python3.6 Control.py --DeviceNo 1 --VarName Fast_Charge,Battery_Test --Value 0,1
   
   this command will set Fast_Charge to 0 and Battery_Test to 1 in the first Device
   


# MODBUSTCP2MQTT

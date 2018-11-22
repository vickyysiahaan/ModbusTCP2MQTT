from pyModbusTCP.client import ModbusClient
import json, serial, struct
import numpy as np
from Constants import *

# Method to convert UINT16 to INT16
def UINT16toINT16(val_list):
    # Arguments:
    # val_list  :   list of UINT16
    # Return    :   list of INT16

    # allocate list for int16
    result = [None] * len(val_list)
    # fill registers list with register items
    for i in range(0, len(val_list)):
        result[i] = struct.unpack("h", struct.pack("H", np.uint16(val_list[i])))[0]
    return result

# Method to convert UINT16 to INT16
def INT16toUINT16(val_list):
    # Arguments:
    # val_list  :   list of INT16
    # Return    :   list of UINT16

    # allocate list for UINT16
    result = [None] * len(val_list)
    # fill registers list with register items
    for i in range(0, len(val_list)):
        result[i] = struct.unpack("H", struct.pack("h", np.int16(val_list[i])))[0]
    return result

# Method to convert UINT16 to INT32
def UINT16toINT32(val_list, big_endian=True, signed=False):
    # Arguments:
    # val_list  :   list of uint16
    # signed    :   True  >> will return signed INT32
    #               False >> will return unsigned INT32
    # big_endian:   Byte order of the device memory structure
    #               True  >>  big endian
    #               False >>  little endian
    # Return    :   list of INT32
    
    # allocate list for int32
    int32_list = [None] * int(len(val_list) / 2)
    # fill registers list with register items
    for i, item in enumerate(int32_list):
        if big_endian:
            int32_list[i] = (val_list[i * 2] << 16) + val_list[(i * 2) + 1]
        else:
            int32_list[i] = (val_list[(i * 2) + 1] << 16) + val_list[i * 2]

    if signed:
        for i in range(0, len(int32_list)):
            int32_list[i] = struct.unpack("i", struct.pack("I", np.uint32(int32_list[i])))[0]
    # return int32 list
    return int32_list

# Method to convert INT32 to UINT16
def INT32toUINT16(int32_val, big_endian=True, signed=False):
    # Arguments:
    # int32_val :   INT32 value
    # signed    :   True  >> for signed INT32 val_list
    #               False >> for unsigned INT32 val_list
    # big_endian:   Byte order of the device memory structure
    #               True  >>  big endian
    #               False >>  little endian
    # Return    :   list of UINT16
    
    # convert int32 to uint16
    
    if signed:
        if big_endian:
            uint8_list = list(struct.pack(">i", np.int32(int32_val)))
        else:
            uint8_list = list(struct.pack("<i", np.int32(int32_val)))
    else:
        if big_endian:
            uint8_list = list(struct.pack(">I", np.uint32(int32_val)))
        else:
            uint8_list = list(struct.pack("<I", np.uint32(int32_val)))

    if big_endian:
        uint16_list = [(uint8_list[i]<<8) + uint8_list[i+1] for i in range(0, len(uint8_list),2)]
    else:
        uint16_list = [(uint8_list[i+1]<<8) + uint8_list[i] for i in range(0, len(uint8_list),2)]
        
     
    # return int16 list
    return uint16_list

# Method to convert UINT16 to INT64
def UINT16toINT64(val_list, big_endian=True, signed=False):
    # Arguments:
    # val_list  :   list of uint16
    # signed    :   True  >> will return signed INT64
    #               False >> will return unsigned INT64
    # big_endian:   Byte order of the device memory structure
    #               True  >>  big endian
    #               False >>  little endian
    # Return    :   list of INT64
    
    # allocate list for int64
    int64_list = [None] * int(len(val_list) / 4)
    # fill registers list with register items
    for i, item in enumerate(int64_list):
        if big_endian:
            int64_list[i] = (val_list[i * 2] << 48) + (val_list[(i * 2) + 1] << 32) + (val_list[(i * 2) + 2] << 16) + val_list[(i * 2) + 3]
        else:
            int64_list[i] = (val_list[(i * 2)+3] << 48) + (val_list[(i * 2) + 2] << 32) + (val_list[(i * 2) + 1] << 16) + val_list[i * 2]

    if signed:
        for i in range(0, len(int64_list)):
            int64_list[i] = struct.unpack("q", struct.pack("Q", np.uint64(int64_list[i])))[0]

    # return int64 list
    return int64_list

# Method to convert INT64 to UINT16
def INT64toUINT16(int64_val, big_endian=True, signed=False):
    # Arguments:
    # int64_val :   INT64 value
    # signed    :   True  >> for signed INT64 val_list
    #               False >> for unsigned INT64 val_list
    # big_endian:   Byte order of the device memory structure
    #               True  >>  big endian
    #               False >>  little endian
    # Return    :   list of UINT16
    
    # convert int64 to uint16  
    if signed:
        if big_endian:
            uint8_list = list(struct.pack(">q", np.int64(int64_val)))
        else:
            uint8_list = list(struct.pack("<q", np.int64(int64_val)))
    else:
        if big_endian:
            uint8_list = list(struct.pack(">Q", np.uint64(int64_val)))
        else:
            uint8_list = list(struct.pack("<Q", np.uint64(int64_val)))

    if big_endian:
        uint16_list = [(uint8_list[i]<<8) + uint8_list[i+1] for i in range(0, len(uint8_list),2)]
    else:
        uint16_list = [(uint8_list[i+1]<<8) + uint8_list[i] for i in range(0, len(uint8_list),2)]
          
    # return int16 list
    return uint16_list

# Method to convert UINT16 to FLOAT16
def UINT16toFLOAT16(val_list):
    # Arguments:
    # val_list  :   list of uint16
    # Return    :   list of FLOAT16

    # allocate list for FLOAT16
    result = [None] * len(val_list)
    # fill registers list with register items
    for i in range(0, len(val_list)):
        result[i] = struct.unpack("e", struct.pack("H", np.uint16(val_list[i])))[0]
    return result

# Method to convert FLOAT16 to UINT16
def FLOAT16toUINT16(val_list):
    # Arguments:
    # val_list  :   list of float16
    # Return    :   list of uint16

    # allocate list for uint16
    result = [None] * len(val_list)
    # fill registers list with register items
    for i in range(0, len(val_list)):
        result[i] = struct.unpack("H", struct.pack("e", np.float16(val_list[i])))[0]
    return result

# Method to convert UINT16 to FLOAT32
def UINT16toFLOAT32(val_list, big_endian=True):
    # Arguments:
    # val_list  :   list of uint16
    # Return    :   list of FLOAT32

    val_list = UINT16toINT32(val_list, big_endian)

    # allocate list for FLOAT32
    result = [None] * len(val_list)
    # fill registers list with register items
    for i in range(0, len(val_list)):
        if big_endian:
            result[i] = struct.unpack(">f", struct.pack(">I", np.uint32(val_list[i])))[0]
        else:
            result[i] = struct.unpack("<f", struct.pack("<I", np.uint32(val_list[i])))[0]
    return result

# Method to convert FLOAT32 to UINT16
def FLOAT32toUINT16(float32_val, big_endian=True):
    # Arguments:
    # float32_val   :   list of FLOAT32
    # Return        :   list of uint16

    if big_endian:
        uint32_val = struct.unpack(">I", struct.pack(">f", np.float32(float32_val)))[0]
    else:
        uint32_val = struct.unpack("<I", struct.pack("<f", np.float32(float32_val)))[0]
    
    result = INT32toUINT16(uint32_val, big_endian)

    return result

# Method to convert UINT16 to FLOAT64
def UINT16toFLOAT64(val_list, big_endian=True):
    # Arguments:
    # val_list  :   list of uint16
    # Return    :   list of FLOAT64

    val_list = UINT16toINT64(val_list, big_endian)
    
    # allocate list for FLOAT64
    result = [None] * len(val_list)
    # fill registers list with register items
    for i in range(0, len(val_list)):
        if big_endian:
            result[i] = struct.unpack(">d", struct.pack(">Q", np.uint64(val_list[i])))[0]
        else:
            result[i] = struct.unpack("<d", struct.pack("<Q", np.uint64(val_list[i])))[0]
    return result

# Method to convert FLOAT64 to UINT16
def FLOAT64toUINT16(float64_val, big_endian=True):
    # Arguments:
    # float64_val   :   list of FLOAT64
    # Return        :   list of uint16

    if big_endian:
        uint64_val = struct.unpack(">Q", struct.pack(">d", np.float64(float64_val)))[0]
    else:
        uint64_val = struct.unpack("<Q", struct.pack("<d", np.float64(float64_val)))[0]
        
    result = INT64toUINT16(uint64_val, big_endian)

    return result

# Method to convert UINT16 to STRING
def UINT16toSTRING(val_list, big_endian=True):
    # Arguments:
    # val_list  :   list of uint16
    # big_endian:   Byte order of the device memory structure
    #               True  >>  big endian
    #               False >>  little endian
    # Return    :   a String
    
    # list for uint8
    uint8_list = []

    # list for char
    char_list = []

    for item in val_list:
        _16bits = bin(item)[2:]

        if len(_16bits)<16:
            add = 16 - len(_16bits)
            _16bits = '0'*add + _16bits
            
        #reverse bit order if little endian
        if not big_endian:
            _16bits = _16bits[::-1]           
        _8bits1 = '0b'+ ''.join(_16bits[0:8])
        _8bits2 = '0b'+ ''.join(_16bits[8:])
        uint8_1 = np.uint8(int(_8bits1,2))
        uint8_2 = np.uint8(int(_8bits2,2))
        
        uint8_list.append(uint8_1)
        uint8_list.append(uint8_2)

        char_list.append(chr(uint8_1))
        char_list.append(chr(uint8_2))
    
    if not big_endian:
        uint8_list = uint8_list[::-1]
        char_list = char_list[::-1]
    
    result = ''.join(char_list)
    result = result.replace('\x00', ' ')
    # return string result list
    return result

# Method to convert STRING to UINT16
def STRINGtoUINT16(string_val, big_endian=True):
    # Arguments:
    # string_val    :   string value
    # big_endian    :   Byte order of the device memory structure
    #                   True  >>  big endian
    #                   False >>  little endian
    # Return        :   list of uint16

    uint8_list = [ord(x) for x in string_val]
    _8bits_list = []

    for x in uint8_list:
        _8bits = bin(x)[2:]
        if len(_8bits)<8:
            add = 8 - len(_8bits)
            _8bits = '0' *add + _8bits
            
        if not big_endian:
            _8bits = _8bits[::-1]
            
        _8bits_list.append(_8bits)

    if not big_endian:
        _8bits_list = _8bits_list[::-1]

    for i,x in enumerate(_8bits_list):
        uint8_list[i] = int('0b'+x, 2)
    
    uint16_list = []

    if big_endian:
        for i in range(0, len(uint8_list),2):
            try:
                uint16_val = (uint8_list[i]<<8) + uint8_list[i+1]
            except:
                uint16_val = (uint8_list[i]<<8)
            uint16_list.append(uint16_val)
    else:
        for i in range(len(uint8_list)-1, -1, -2):
            if i != 0:
                uint16_val = (uint8_list[i]<<8) + uint8_list[i-1]
            else:
                uint16_val = (uint8_list[i]<<8)
            uint16_list.append(uint16_val)
        uint16_list = uint16_list[::-1]
    return uint16_list
    
class Device():
    def __init__(self, host, port, timeout, byteorder=BE):       
        # big_endian        :   Byte order of the device memory structure
        #                       True  >>  big endian
        #                       False >>  little endian
        if byteorder == BE:
            self.big_endian=True
        else:
            self.big_endian=False
        
        self.dev = ModbusClient()
        self.dev.host(host)
        self.dev.port(port)
        self.dev.timeout(timeout)
        self.dev.open()
        #self.dev.debug = True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ READ METHODS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #Method to read binary variable
    def read_bits(self, VarNameList, AddressList, functioncode=2):
        # Arguments:
        # VarNameList       :   list of variable name
        # AddressList       :   list of variable register address in decimal (relative address)
        # functioncode      :   functioncode for modbus reading operation
        #                       1 >> for Discrete Output (Coils)
        #                       2 >> for Discrete Input
        # Return            :   dictionary of variable name and its value
        
        self.values = []
        if functioncode == 1:
            for address in AddressList:
                self.values.extend(self.dev.read_coils(address[0], len(address)))
        elif functioncode == 2:
            for address in AddressList:
                self.values.extend(self.dev.read_discrete_inputs(address[0], len(address)))    
        self.Result = dict(zip(VarNameList, self.values))
        return self.Result

    #Method to read INT16 or UINT16 variable
    def read_INT16(self, VarNameList, AddressList, MultiplierList, signed=False, roundto=3, functioncode=3):
        # Arguments:
        # VarNameList       :   list of variable name
        # AddressList       :   list of variable register address in decimal (relative address)
        # MultiplierList    :   list of multiplier
        # roundto           :   number of digits after decimal point
        #                       any positive integer number >> to limit the number of digits after decimal point
        #                       None                        >> to disable
        # signed            :   True  >> for signed values
        #                       False >> for unsigned values
        # functioncode      :   functioncode for modbus reading operation
        #                       3 >> for Holding Register
        #                       4 >> for Input Register
        # Return            :   dictionary of variable name and its value
        
        self.values = []

        if functioncode == 3:
            for address in AddressList:
                self.values.extend(self.dev.read_holding_registers(address[0],len(address)))
        elif functioncode == 4:
            for address in AddressList:
                self.values.extend(self.dev.read_input_registers(address[0],len(address)))
        
        if signed:
            self.values = UINT16toINT16(self.values)
        
        for i in range(0, len(self.values)):
            self.values[i] = round(self.values[i]*MultiplierList[i],roundto)

        self.Result = dict(zip(VarNameList, self.values))
        return self.Result


    #Method to read INT32 or UINT32 variable
    def read_INT32(self, VarNameList, AddressList, MultiplierList, signed=False, roundto=3, functioncode=3):
        # Arguments:
        # VarNameList       :   list of variable name
        # AddressList       :   list of variable register address in decimal (relative address)
        # MultiplierList    :   list of multiplier
        # roundto           :   number of digits after decimal point
        #                       any positive integer number >> to limit the number of digits after decimal point
        #                       None                        >> to disable
        # signed            :   True  >> for signed values
        #                       False >> for unsigned values
        # functioncode      :   functioncode for modbus reading operation
        #                       3 >> for Holding Register
        #                       4 >> for Input Register
        # Return            :   dictionary of variable name and its value

        self.values = []

        if functioncode == 3:
            for address in AddressList:
                self.values.extend(self.dev.read_holding_registers(address[0],len(address)))
        elif functioncode == 4:
            for address in AddressList:
                self.values.extend(self.dev.read_input_registers(address[0],len(address)))

        self.values = UINT16toINT32(self.values, self.big_endian, signed)
        for i in range(0, len(self.values)):
            self.values[i] = round(self.values[i]*MultiplierList[i], roundto)

        self.Result = dict(zip(VarNameList, self.values))
        return self.Result
    
    #Method to read INT64 or UINT64 variable
    def read_INT64(self, VarNameList, AddressList, MultiplierList, signed=False, roundto=3, functioncode=3):
        # Arguments:
        # VarNameList       :   list of variable name
        # AddressList       :   list of variable register address in decimal (relative address)
        # MultiplierList    :   list of multiplier
        # roundto           :   number of digits after decimal point
        #                       any positive integer number >> to limit the number of digits after decimal point
        #                       None                        >> to disable
        # signed            :   True  >> for signed values
        #                       False >> for unsigned values
        # functioncode      :   functioncode for modbus reading operation
        #                       3 >> for Holding Register
        #                       4 >> for Input Register
        # Return            :   dictionary of variable name and its value
        
        self.values = []

        if functioncode == 3:
            for address in AddressList:
                self.values.extend(self.dev.read_holding_registers(address[0],len(address)))
        elif functioncode == 4:
            for address in AddressList:
                self.values.extend(self.dev.read_input_registers(address[0],len(address)))

        self.values = UINT16toINT64(self.values, self.big_endian, signed)
        for i in range(0, len(self.values)):
            self.values[i] = round(self.values[i]*MultiplierList[i], roundto)

        self.Result = dict(zip(VarNameList, self.values))
        return self.Result

    #Method to read FLOAT16 variable
    def read_FLOAT16(self, VarNameList, AddressList, MultiplierList, roundto=3, functioncode=3):
        # Arguments:
        # VarNameList       :   list of variable name
        # AddressList       :   list of variable register address in decimal (relative address)
        # MultiplierList    :   list of multiplier
        # roundto           :   number of digits after decimal point
        #                       any positive integer number >> to limit the number of digits after decimal point
        #                       None                        >> to disable
        # functioncode      :   functioncode for modbus reading operation
        #                       3 >> for Holding Register
        #                       4 >> for Input Register
        # Return            :   dictionary of variable name and its value
        
        self.values = []

        if functioncode == 3:
            for address in AddressList:
                self.values.extend(self.dev.read_holding_registers(address[0],len(address)))
        elif functioncode == 4:
            for address in AddressList:
                self.values.extend(self.dev.read_input_registers(address[0],len(address)))

        self.values = UINT16toFLOAT16(self.values)
        
        for i in range(0, len(self.values)):
            self.values[i] = round(self.values[i]*MultiplierList[i], roundto)

        self.Result = dict(zip(VarNameList, self.values))
        return self.Result
    
    #Method to read FLOAT32 variable
    def read_FLOAT32(self, VarNameList, AddressList, MultiplierList, roundto=3, functioncode=3):
        # Arguments:
        # VarNameList       :   list of variable name
        # AddressList       :   list of variable register address in decimal (relative address)
        # MultiplierList    :   list of multiplier
        # roundto           :   number of digits after decimal point
        #                       any positive integer number >> to limit the number of digits after decimal point
        #                       None                        >> to disable
        # functioncode      :   functioncode for modbus reading operation
        #                       3 >> for Holding Register
        #                       4 >> for Input Register
        # Return            :   dictionary of variable name and its value
        
        self.values = []

        if functioncode == 3:
            for address in AddressList:
                self.values.extend(self.dev.read_holding_registers(address[0],len(address)))
        elif functioncode == 4:
            for address in AddressList:
                self.values.extend(self.dev.read_input_registers(address[0],len(address)))

        self.values = UINT16toFLOAT32(self.values, self.big_endian)
        for i in range(0, len(self.values)):
            self.values[i] = round(self.values[i]*MultiplierList[i], roundto)
        
        self.Result = dict(zip(VarNameList, self.values))
        return self.Result
    
    #Method to read FLOAT64 variable
    def read_FLOAT64(self, VarNameList, AddressList, MultiplierList, roundto=3, functioncode=3):
        # Arguments:
        # VarNameList       :   list of variable name
        # AddressList       :   list of variable register address in decimal (relative address)
        # MultiplierList    :   list of multiplier
        # roundto           :   number of digits after decimal point
        #                       any positive integer number >> to limit the number of digits after decimal point
        #                       None                        >> to disable
        # functioncode      :   functioncode for modbus reading operation
        #                       3 >> for Holding Register
        #                       4 >> for Input Register
        # Return            :   dictionary of variable name and its value
        
        self.values = []

        if functioncode == 3:
            for address in AddressList:
                self.values.extend(self.dev.read_holding_registers(address[0],len(address)))
        elif functioncode == 4:
            for address in AddressList:
                self.values.extend(self.dev.read_input_registers(address[0],len(address)))

        self.values = UINT16toFLOAT64(self.values, self.big_endian)
        for i in range(0, len(self.values)):
            self.values[i] = round(self.values[i]*MultiplierList[i], roundto)

        self.Result = dict(zip(VarNameList, self.values))
        return self.Result

    #Method to read STRING variable
    def read_STRING(self, VarNameList, AddressList, functioncode=3):
        # Arguments:
        # VarNameList       :   list of variable name
        # AddressList       :   list of variable register address in decimal (relative address)
        # functioncode      :   functioncode for modbus reading operation
        #                       3 >> for Holding Register
        #                       4 >> for Input Register
        # Return            :   dictionary of variable name and its value
        
        self.values = []
        if functioncode == 3:
            for address in AddressList:
                _uint16Val = self.dev.read_holding_registers(address[0],len(address))
                self.values.append(UINT16toSTRING(_uint16Val, self.big_endian))
        elif functioncode == 4:
            for address in AddressList:
                _uint16Val = self.dev.read_input_registers(address[0],len(address))
                self.values.append(UINT16toSTRING(_uint16Val, self.big_endian))
        
        self.Result = dict(zip(VarNameList, self.values))
        return self.Result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ WRITE METHODS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # Method to write binary value on discrete output register (Coil)
    def write_bit(self, registerAddress, value):
        # Arguments:
        # registerAddress   :   register address in decimal (relative address)
        # value             :   0 or 1
        
        self.dev.write_single_coil(registerAddress, value)

    # Method to write numeric value on holding register
    def write_num(self, registerAddress, value, valueType):
        # Arguments:
        # registerAddress   :   register START address in decimal (relative address)
        # value             :   numerical value
        # valueType         :   UINT16, UINT32, UINT64, INT16, INT32, INT64, FLOAT16,
        #                       FLOAT32, FLOAT64, STRING

        startAddress = registerAddress
        val = None
        
        if valueType == UINT16:
            val = [value]
        elif valueType == INT16:
            val = INT16toUINT16([value])
        elif valueType == UINT32:
            val = INT32toUINT16(value, self.big_endian, signed=False)
        elif valueType == INT32:
            val = INT32toUINT16(value, self.big_endian, signed=True)
        elif valueType == UINT64:
            val = INT64toUINT16(value, self.big_endian, signed=False)
        elif valueType == INT64:
            val = INT64toUINT16(value, self.big_endian, signed=True)
        elif valueType == FLOAT16:
            val = FLOAT16toUINT16([value])
        elif valueType == FLOAT32:
            val = FLOAT32toUINT16(value, self.big_endian)
        elif valueType == FLOAT64:
            val = FLOAT64toUINT16(value, self.big_endian)
        elif valueType == STRING:
            val = STRINGtoUINT16(value, self.big_endian)
    
        # write multiple registers
        self.dev.write_multiple_registers(startAddress, val)

    def close(self):
        self.dev.close()
        
#Cek EIO
"""
a = Device('192.168.1.201', 502, 0.2, BE)
VarName = ['Temperature']
Reg = [[33]]
Mul = [1,1,1,1]
#print(a.read_INT16(VarName, Reg, Mul, functioncode=3))
a.write_num(0, 3.45678, FLOAT32)
"""

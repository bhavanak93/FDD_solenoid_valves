# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 16:20:22 2019

@author: krishnamurthy
"""

# Import modules.
# ---------------------------------------------------------
import visa
import struct
import datetime
import pandas as pd
from time import sleep

# Global variables (booleans: 0 = False, 1 = True).
# ---------------------------------------------------------
debug = 0
InfiniiVision = 0
SIX_V_VALVE = 0
TWELVE_V_VALVE = 1
# =========================================================
# Initialize:
# =========================================================
def initialize():
    
    # Get and display the device's *IDN? string.
    idn_string = do_query_string("*IDN?")
    print ("Identification string: ", idn_string)
   
    # Clear status 
    do_command("*CLS")
#    do_command("*RST")
    do_command(":DISPlay:LABel ON")
    qres = do_query_string("*ESR?")
    print ("ESR (event status register): ", qres)
    do_command(":FUNCtion1:DISPlay OFF") 

    
def genWaveform():
    print("Trying to mimic wavegen functionality:")
    print("Setup info of WGEN1", do_query_string(":WGEN1?"))
    
    print("WGEN1 function", do_query_string(":WGEN1:FUNCtion?"))
    
    # Set the params of Wavegen to desired values
    do_command(":WGEN1:FUNCtion SQUare")
    do_command(":WGEN1:FREQuency 2.00E+1")   #for normal data without pressure
#    do_command(":WGEN1:FREQuency 5.00E-1")  #for pressure data
    do_command(":WGEN1:VOLTage 1.00E+1")
    
    do_command(":WGEN1:VOLTage:LOW 0.00E+0")
    do_command(":WGEN1:VOLTage:HIGH 5.00E+0")
    
    #do_command(":WGEN1:VOLTage:OFFSet 0.00E+0")
    do_command(":WGEN1:FUNCtion:SQUare:DCYCle 50")
    
    # Finally turn on Wave Generator
    do_command(":WGEN1:OUTPut ON")


def getDiffVoltWave():
    # do math of ch1 - ch2
    do_command(":FUNCtion1:OPERation SUBTract")
    do_command(":FUNCtion1:SOURce1 CHANnel2")
    do_command(":FUNCtion1:SOURce2 CHANnel1")
    do_command(":FUNCtion1:SCALe 2.00E-1[V]")
    do_command(":FUNCtion1:OFFSet 0")
    do_command(":FUNCtion1:DISPlay ON")
   

def setAcquireValues():
    # change settings to get a smooth waveform without much distortion
    do_command(":ACQuire:COUNt 8")
    do_command(":ACQuire:MODE ETIMe")
    do_command(":ACQuire:TYPE AVERage")
    #print("Acquire points analog is : "+ do_query_string(":ACQuire:POINts[:ANALog]?"))


def getWaveformSettingVals():
    qresult = do_query_string(":WAVeform:SOURce?")
    print ("Waveform source: %s" % qresult)
    
    qresult = do_query_string(":WAVeform:POINts:MODE?")
    print ("Waveform points mode: ", qresult)
    
    qresult = do_query_string(":WAVeform:POINts?")
    print ("Waveform points available:", qresult)
    
    print ("Waveform format: ", do_query_string(":WAVeform:FORMat?"))
    
    # Display the waveform settings from preamble:
    wav_form_dict = {
    0 : "BYTE",
    1 : "WORD",
    4 : "ASCii",
    }
    acq_type_dict = {
    0 : "NORMal",
    1 : "PEAK",
    2 : "AVERage",
    3 : "HRESolution",
    }
    preamble_string = do_query_string(":WAVeform:PREamble?")
    (wav_form, acq_type, wfmpts, avgcnt, x_increment, x_origin,
    x_reference, y_increment, y_origin, y_reference) = preamble_string.split(',')
    print ("Waveform format: ", wav_form_dict[int(wav_form)])
    print ("Acquire type: ", acq_type_dict[int(acq_type)])
    print ("Waveform points desired: ", wfmpts)
    print ("Waveform average count: ", avgcnt)
    print ("Waveform X increment: ", x_increment)
    print ("Waveform X origin: ", x_origin)
    print ("Waveform X reference: ", x_reference) # Always 0.
    print ("Waveform Y increment: ", y_increment)
    print ("Waveform Y origin: ", y_origin)
    print ("Waveform Y reference: ", y_reference)

    
def setWaveformSettingVals():
    # Set the waveform source.
    do_command(":WAVeform:SOURce FUNCtion1")
    print("Waveform source : "+do_query_string(":WAVeform:SOURce?"))
    
    # Set the waveform points mode.
    do_command(":WAVeform:POINts:MODE RAW")
    print("Waveform points mode : "+do_query_string(":WAVeform:POINts:MODE?"))
    
    # Set the number of waveform points.
    # It gives 4000, 5333, 8000, 16000
    do_command(":WAVeform:POINts 2000")
    print("Waveform points : "+do_query_string(":WAVeform:POINts?"))
    
    # Choose the format of the data returned
    do_command(":WAVeform:FORMat BYTE")
    
    
def setDispWindow(valveType):
    #delay set as + or - 20 ms
    do_command(":CHANnel1:SCALe 5.00E+0")
    do_command(":CHANnel2:SCALe 5.00E+0")
    
    # for 12V valves:
    if (valveType == TWELVE_V_VALVE):
        do_command(":TIMebase:DELay 2.0E-03")
        do_command(":TIMebase:SCALe 2.0E-03")
        
        do_command(":FUNCtion1:SCALe 500.0E-03")
        do_command(":FUNCtion1:OFFSet 0.0E+0")
    elif (valveType == SIX_V_VALVE):
        # for 6V valve:
#        do_command(":TIMebase:DELay 1002.0E-03")    #for pressure data with 0.5Hz
        do_command(":TIMebase:DELay 2.0E-03")    #for normal data without pressure
        do_command(":TIMebase:SCALe 2.0E-03")
        
        do_command(":FUNCtion1:SCALe 1.0E+0")
        do_command(":FUNCtion1:OFFSet 2.0E+0")
    else:
        print("Incorrect valve type.")
        
#def setTriggerSettings():
#    do_command(":TRIGger:LEVel:ASETup")
    
    
def getData():
    do_command(":DIGitize [FUNCtion1];*OPC?")
    
    # Get numeric values for later calculations.
    x_increment = do_query_number(":WAVeform:XINCrement?")
    x_origin = do_query_number(":WAVeform:XORigin?")
    y_increment = do_query_number(":WAVeform:YINCrement?")
    y_origin = do_query_number(":WAVeform:YORigin?")
    y_reference = do_query_number(":WAVeform:YREFerence?")
    
    sData = do_query_ieee_block(":WAVeform:DATA?")
    
    # Unpack unsigned byte data.
    values = struct.unpack("%dB" % len(sData), sData)
#    print ("Number of data values: %d" % len(values))
    
    # save voltage values at each time instant in the form of a list and return it.
    timeBase = []
    voltValues = []
    
    for i in range(0, len(values)):
        time_val = x_origin + (i * x_increment)
        voltage = ((values[i] - y_reference) * y_increment) + y_origin

        timeBase.append(time_val)
        voltValues.append(voltage)

#    print ("Waveform format BYTE data stored as dict. Len values = ", len(voltValues))
    return timeBase, voltValues
    
    
def saveDataToCsv(numReadings):
    # get current time 
    print(datetime.datetime.now().time())
    # generating data files in .csv format
    
    for i in range(0,numReadings):
        # turn off the wave generator for coping up with heating issues
#        if (i != 0 and i%10 == 0 and i != numReadings):
#            do_command(":WGEN1:OUTPut OFF")
#            sleep(100)
#            do_command(":WGEN1:OUTPut ON")
        
        # Get list of voltage values for each reading and store them as a dictionary
        timeVals, voltage = getData()
        print("reading ", i)
        if (i == 0):
            dataDict = {'time': timeVals, 'reading0': voltage}
        else:
            dataDict['reading'+str(i)] = voltage
        df = pd.DataFrame(dataDict)
        df.to_csv(r'Z:/User/KrishnaMurthy/Work/data/exp_data/trial_data/1021_03_6000readings.csv', header = True)
    
#    df = pd.DataFrame(dataDict)
#    df.to_csv(r'Z:/User/KrishnaMurthy/Work/data/exp_data/trial_data/1021-03_100readings.csv', header = True)
    print(datetime.datetime.now().time())

def prepDataCollection():
    genWaveform()
    getDiffVoltWave()
    setAcquireValues()
    setWaveformSettingVals()
    setDispWindow(SIX_V_VALVE)

def startDataCollection(numReadings):
    saveDataToCsv(numReadings)
    do_command(":WGEN1:OUTPut OFF")

# =========================================================
# Send a command and check for errors:
# =========================================================
def do_command(command, hide_params=False):
    if hide_params:
#        (header, data) = string.split(command, " ", 1)
        (header, data) = command.split(" ")
        if debug:
            print ("\nCmd = '%s'" % header)
    else:
        if debug:
            print ("\nCmd = '%s'"% command)
            
    InfiniiVision.write("%s" % command)
    
#    if hide_params:
#        check_instrument_errors(header)
#    else:
#        check_instrument_errors(command)


# =========================================================
# Send a command and binary values and check for errors:
# =========================================================
def do_command_ieee_block(command, values):
    if debug:
        print ("Cmb = '%s'", command)
    
    InfiniiVision.write_binary_values("%s ", command, values, datatype='c')
#    check_instrument_errors(command)


# =========================================================
# Send a query, check for errors, return string:
# =========================================================
def do_query_string(query):
    if debug:
        print ("Qys = '%s'" % query)
    
#    result = InfiniiVision.query("%s" % query)
    result = InfiniiVision.query(query)
#    check_instrument_errors(query)
    return result


# =========================================================
# Send a query, check for errors, return floating-point value:
# =========================================================
def do_query_number(query):
    if debug:
        print ("Qyn = '%s'" % query)

    results = InfiniiVision.query("%s" % query)
#    check_instrument_errors(query)
    return float(results)


# =========================================================
# Send a query, check for errors, return binary values:
# =========================================================
def do_query_ieee_block(query):
    if debug:
        print ("Qys = '%s'" % query)

    result = InfiniiVision.query_binary_values("%s" % query, datatype='s')
#    check_instrument_errors(query)
    return result[0]


# =========================================================
# Check for instrument errors:
# =========================================================
#def check_instrument_errors(command):
#    while True:
#        error_string = InfiniiVision.query(":SYSTem:ERRor?")
##        print("-----Error string: ", error_string)
#        if error_string: # If there is an error string value.
#            if error_string.find("+0,", 0, 3) == -1: # Found Error!!.
#                print ("ERROR: %s, command: '%s'" % (error_string, command))
#                print ("Exited because of error.")
#                sys.exit(1)
#            else: # "No error"
#                break
#        else: # :SYSTem:ERRor? should always return string.
#            print ("ERROR: :SYSTem:ERRor? returned nothing, command: '%s'" % command)
#            print ("Exited because of error.")
#            sys.exit(1)

# =========================================================
# Main program:
# =========================================================
rm = visa.ResourceManager('C:/Windows/system32/visa64.dll')
InfiniiVision = rm.open_resource("USB0::2391::6064::MY53390449::INSTR")
#InfiniiVision.timeout = 15000
InfiniiVision.timeout = 25000

# Initialize the oscilloscope, capture data, and analyze.
initialize()

#do_command(":WGEN1:OUTPut OFF")

prepDataCollection()
startDataCollection(6000)

#visa.log_to_screen()
print ("End of program.")
pyLabInstruments/lib
=============

A simple library for controlling USB and Serial based measurement instruments in Linux. It does not have a gui but provides a wrapper around instruments controlled via usb or serial interface.
It does not rely on Agilent/NI VISA libraries.
No docmunetation exists as yet.

## Supported instruments

### usb_instruments:
* Agilent 3320A Arbitrary Waveform Generator (view [usage example](http://markjones112358.co.nz/projects/Python-Controlled-Function-Generator/))

### serial_instruments:
* Tektronix TPS2024B Digital Storage Oscilloscope (view [usage example](http://markjones112358.co.nz/projects/Python-Controlled-Oscilloscope/))
* Tested osc: Tektronix TPS2024B, Tektronix TPS2022B, Tektronix TPS2024C.
* Should work for: TDS210, TDS220, TDS224, TDS1002, TDS1012, TDS2002, TDS2012, TDS2014, TDS2022, TDS2024, TPS2012, TPS2014, TPS2024, TDS1001, TDS2004, TDS1001B, TDS1002B, TDS1012B, TDS2002B, TDS2004B, TDS2012B, TDS2014B, TDS2022B, TDS2024B, TDS2001C, TDS2002C, TDS2004C, TDS2012C, TDS2014C, TDS2022C, TDS1001C EDU, TDS1002C EDU, TDS1012C EDU, TPS2012B, TPS2014B, TPS2024B, TBS1022, TBS1042, TBS1062, TBS1102, TBS1152, TBS1052B EDU, TBS1052B, TBS1072B EDU, TBS1072B, TBS1102B, TBS1102B EDU, TBS1152B, TBS1152B EDU, TBS1202B, TBS1202B EDU 


## Usage

    import serial_instruments
    import usb_instruments
    
    scope = serial_instruments.tek2024('/dev/ttyS0')
    wavegen = usb_instruments.agilent33220A('/dev/usbtmc0')
    channel1 = serial_instruments.channel(scope,1)
    channel2 = serial_instruments.channel(scope,2)
    
    wavegen.mode('sine')  # Enable sinusodal output
    wavegen.frequency(1000)  # Set the frequency to 1kHz
    wavegen.voltage(2)  # Set the output amplitude to 2V
    wavegen.output(True)  # Enable the output
    
    scope.set_hScale(frequency=1000, cycles=8)  # Set the time scale to the mimimum that contains 8 waveforms
    scope.set_averaging(16)  # Set the scope to do 16X averaging
    channel1.set_vScale(1)  # Set the voltage scale to 
    channel2.set_vScale(1)
    
    data_voltage = channel1.get_waveform()  # Download the waveform from channel 1
    data_current = channel2.get_waveform()  # Download the waveform from channel 2


Custom Scripts
=============

##pygasdet.py
To perform custom acquisition on ion gas detector. 
Make sure the osciloscope is mounted on /dev/usbtmc0.
### to-do
 - add conf() to get data from user input channels
 - add conf() which detector we are using
 - add CAEN HV control based on: 1) which detector 2) field to be applied (Td)

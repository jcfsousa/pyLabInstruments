import serial_instruments
import usb_instruments
import matplotlib.pyplot as plt

#scope = serial_instruments.tek2024('/dev/usbtmc0')
scope = serial_instruments.tek2024('/dev/usbtmc0')
channel1 = serial_instruments.channel(scope,1)
channel2 = serial_instruments.channel(scope,2)

period = 1 * 10**-6
frequency = 1/period

scope.set_hScale(frequency=frequency, cycles=8)  # Set the time scale to the mimimum that contains 8 waveforms
#breakpoint()
scope.set_averaging(128)  # Set the scope to do 16X averaging
channel1.set_vScale(0.01, debug=True)  # Set the voltage scale to 
#channel2.set_vScale(1)

data_voltage = channel1.get_waveform(debug=True)  # Download the waveform from channel 1
data_current = channel2.get_waveform()  # Download the waveform from channel 2

#print(data_voltage)
#print(data_current)


test = True

if test:
    fig, ax1 = plt.subplots(figsize=(10,6))
    line1, = ax1.plot(data_voltage[0], data_voltage[1], color = 'k', label='channel 1')
    ax1.set_ylabel('Voltage (V)')
    ax1.set_xlabel('Time (s)')

    ax2 = ax1.twinx()

    line2, = ax2.plot(data_current[0], data_current[1], color='b', label='channel 2')
    ax2.set_ylabel('Voltage (V)')

    lines = [line1, line2]
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc = 'best')


    plt.tight_layout()
    plt.show()

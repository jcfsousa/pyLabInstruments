from numpy import average
import csv
import serial_instruments
import os
import usb_instruments
import matplotlib.pyplot as plt
import cmd
import sys



class MyCLI(cmd.Cmd):
    prompt = 'pyoscli> '
    intro = "Welcome to my CLI. Type ? to list commands."
    completekey = 'tab'

    def __init__(self):
        super().__init__()
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.scope = serial_instruments.tek2024('/dev/usbtmc0')
        self.channel1 = serial_instruments.channel(self.scope,1)
        self.channel2 = serial_instruments.channel(self.scope,2)
        self.output_folder = os.path.dirname(os.path.realpath(__file__))

    def do_hscale(self, div):
        '''
        to se the horizontal division size, in seconds
        usage: > set_hscale 2
        
        '''
        try:
            # Evaluate math expression safely
            period = float(eval(div, {"__builtins__": None}, {}))
            frequency = 1 / period
            self.scope.set_hScale(frequency=frequency, cycles=8)
            print(f'Horizontal time division set to {period} s')

        except Exception as e:
            print(f'Error setting horizontal scale: {e}')


    def do_averaging(self, n):
        try:
            n = int(n)
            self.scope.set_averaging(n)
        except Exception as e:
            print(f'Please provide an int: {e}')

    def do_vscale(self, arg):
        '''
        vscale ch div

        ch - int(), channel ID

        div - float(), vertical div in Volt
        '''

        try:
            ch, div = arg.split()
            if int(ch) == 1:
                div = float(eval(div, {"__builtins__": None}, {}))
                self.channel1.set_vScale(div)
            elif int(ch) == 2:
                div = float(eval(div, {"__builtins__": None}, {}))
                self.channel2.set_vScale(div)
        except Exception as e:
            print(f'Channel number is int() and div is float(): {e}')

    def do_custom_acquisition(self, line):
        acq_name = input('    Acquisition name > ')
        save_folder = f'{self.output_folder}/{acq_name}'
        try:
            os.mkdir(save_folder)
        except Exception as e:
            print(e)

        avrg = input('    set_average > ')
        if avrg != 0:
            self.do_averaging(avrg)

        reps = input('    n acquitions > ')
        i=0 

        while i < int(reps):
            ch1_data = self.channel1.get_waveform()
            i += 1
            times, voltages = ch1_data[0], ch1_data[1]

            with open(f'{save_folder}/acq_{i}.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Time', 'Voltage'])
                writer.writerows(zip(times, voltages))


    def do_conf(self):
        self.output_folder = input('    Base output folder > ')

    def do_exit(self, line):
        "Exit the CLI"
        print("Goodbye!")
        return True

if __name__ == '__main__':
    

    MyCLI().cmdloop()


#scope = serial_instruments.tek2024('/dev/usbtmc0')


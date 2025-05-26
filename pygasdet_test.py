from numpy import average
from datetime import datetime
import csv
import lib.serial_instruments as serial_instruments
import os
import lib.usb_instruments as usb_instruments
import matplotlib.pyplot as plt
import cmd
import sys



class MyCLI(cmd.Cmd):
    prompt = 'pyoscli> '
    
    intro = "Welcome to pygasdet. Type ? to list commands."
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

    def do_timemainposition(self, line):
        reference = self.scope.get_timeMainPosition()
        print(f'Time main reference: {reference}')
        print(type(reference))

    def do_averaging(self, n):
        try:
            n = int(n)
            check = self.scope.set_averaging(n)
            if check == 0:
                print('Try again...')
                n = input('    n average > ')
                n = int(n)
                check = self.scope.set_averaging(n)
                if check == 0:
                    print('Seems like you dont know how to read')
                    print('You got kicked from the script for beeing dumb')
                    sys.exit(1)
        except Exception as e:
            print(f'Please provide an int: {e}')
            n = input('    n average > ')
            n = int(n)
            check = self.scope.set_averaging(n)
            if check == 0:
                print('Try again...')
                n = input('    n average > ')
                n = int(n)
                check = self.scope.set_averaging(n)
                if check == 0:
                    print('Seems like you dont know how to read')
                    print('You got kicked from the script for beeing dumb')
                    sys.exit(1)

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
        '''
        custom_acquisition – run and save oscilloscope acquisitions with metadata.
        This function captures oscilloscope waveforms and saves them to a .csv file with experiment details. You can change base output_folder path on the > conf command.
            - You will be prompted for metadata: field1, vgem, field2, field3.
            - You can set oscilloscope averaging.
            - You can choose how many acquisitions to perform.
            - Data and metadata are saved to a CSV file for each acquisition on ~/{output_folder}/{read_charge_from}/{filename}.csv
        '''
        
        save_folder = f'{self.output_folder}/output'
        try:
            os.mkdir(save_folder)
            print(f'        Saving data on: {save_folder}')
        except Exception as e:
            print(f'        Warning: {e}')

        vgem_study = input('  Are you doing a field study? (y/n) > ')

        if vgem_study not in ('y', 'n'):
            print("Invalid input. Please enter 'y' or 'n'.")
            return

        read_from = input('    read charge from > ')
        read_from_folder = f'{save_folder}/{read_from}'
        try:
            os.mkdir(read_from_folder)
            print(f'        Saving data on: {read_from_folder}')
        except Exception as e:
            print(f'        Warning: {e}')

        continue_loop = True
        first_loop = True

        while continue_loop:
            if vgem_study == 'y' and first_loop or vgem_study == 'n':
                resist = input('    resist  > ')
                conden = input('    conden  > ') 
                field1 = input('    field 1 > ').replace('.', '-')
                field2 = input('    field 2 > ').replace('.', '-')
                field3 = input('    field 3 > ').replace('.', '-')
                avrg = input('    set osc average > ')
                if avrg != 0:
                    self.do_averaging(avrg)

                try:
                    reps = int(input('    n acquisitions > '))
                    if reps <= 0:
                        raise ValueError
                except:
                    print('You should learn how to read....')
                    print('You got kicked from the script for being dumb....')
                    sys.exit(1)
            else:
                # Mantém os campos anteriores
                try:
                    self.do_averaging(avrg)
                    reps = int(input('    n acquisitions > '))
                    if reps <= 0:
                        raise ValueError
                except:
                    print('You should learn how to read....')
                    print('You got kicked from the script for being dumb....')
                    sys.exit(1)

            vgem = input('    vgem > ').replace('.', '-')
            input('    press ENTER to start acquisition')

            i = 0
            while i < int(reps):
                ch2_data = self.channel2.get_waveform()
                i += 1
                times, voltages = ch2_data[0], ch2_data[1]

                now = datetime.now()
                timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
                with open(f'{read_from_folder}/{read_from}_{resist}M_{conden}pF_{field1}td_{vgem}v_{field2}td_{field3}td_{timestamp}.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['date', f'{timestamp}'])
                    writer.writerow(['resist', f'{resist}'])
                    writer.writerow(['conden', f'{conden}'])
                    writer.writerow(['field1', f'{field1}', 'Td'])
                    writer.writerow(['vgem', f'{vgem}', 'V'])
                    writer.writerow(['field2', f'{field2}', 'Td'])
                    writer.writerow(['field3', f'{field3}', 'Td'])
                    writer.writerow(['Time', 'Voltage'])
                    writer.writerows(zip(times, voltages))

            if vgem_study == 'y':
                choice = input('    Continue with new vgem? (y/n) > ').lower()
                if choice != 'y':
                    continue_loop = False
                first_loop = False
            else:
                continue_loop = False
    

    def do_conf(self):
        '''
        Configure base output folder. The default is the script directory.
        '''
        self.output_folder = input('    Base output folder > ')

    def do_exit(self, line):
        "Exit the CLI"
        print("Goodbye!")
        return True

if __name__ == '__main__':
    

    MyCLI().cmdloop()


#scope = serial_instruments.tek2024('/dev/usbtmc0')


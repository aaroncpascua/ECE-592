'''IMPORTANT: For this program to work, the user needs to have SSH keys onto the default location ~/.ssh'''

from cgitb import small
from multiprocessing.sharedctypes import Value
from stat import S_ISREG
import sys
import paramiko
from scp import SCPClient
from matplotlib.ticker import MaxNLocator
import numpy as np
import pylab as plt
import csv
import re
import os.path
import os
import threading

def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s

def natural_keys(s):
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]


def scp(ip, input_file):
    client = paramiko.SSHClient()
    client.load_system_host_keys() # use ssh keys stored onto default location in client computer
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 

    try:
        print("Connecting to host")
        client.connect(hostname=ip, username='pi') # create client object
    except TimeoutError:
        print("Cannot connect to " + ip)
        sys.exit()

    scp = SCPClient(client.get_transport()) # create scp object
    sftp = client.open_sftp() # create sftp object

    file_names = []
    client_directory = r'./DataFiles'

    try:
        # if the user input a file name, see if it exists, and if it does not, retrieve it from host
        if input_file != "":
            if not os.path.exists("./DataFiles/" + input_file):
                print("Retreiving " + input_file)

                host_directory = r'/home/pi/Documents/{}'.format(input_file)
                scp.get(host_directory, client_directory)
                file_names.append(input_file)

                print('Done.')
            
            # else file exists and do nothing
            else:
                print(input_file + " exists. Not overwriting.")
                file_names.append(input_file)
        
        else:
            # if the user did not input a file, gather all the files in the host directory, if the file exists, skip retrieving it
            for df in sftp.listdir_attr(r'/home/pi/Documents/'):
                if not os.path.exists("./DataFiles/" + df.filename):
                    print("Retreiving " + df.filename)

                    mode = df.st_mode
                    if S_ISREG(mode):
                        host_directory = r'/home/pi/Documents/{}'.format(df.filename)
                        scp.get(host_directory, client_directory)
                        file_names.append(df.filename)
                    
                else:
                    print(df.filename + " exists. Not overwriting.")
                    file_names.append(df.filename)
                        
            file_names.sort(key=natural_keys) # sort files because i thought i had to make a graph if the user did not input a file, but this isn't true, so it's here
            print('Done.')
    except:
        print("No such file or directory")
        sys.exit()

    client.close() # close client
    return(file_names)

def plot_data(files):
    # for each file name in files[] read the data and create plots
    for fname in files:
        fname = "./DataFiles/" + fname
        file = open(fname, "r")
        reader = csv.DictReader(file, delimiter=",")

        data_dict = {}
        for row in reader:
            for column, value in row.items():
                data_dict.setdefault(column, []).append(value)

        # read data and store into data_dict{}
        data_to_plot = {} # dictionary of converted values to plot
        for key in data_dict:
            if key == 'Timestamp':
                time_data1 = []
                for data in data_dict[key]:
                    str1 = data.split(' ')
                    str2 = str1[1].split(':')
                    hours = float(str2[0])
                    minutes = float(str2[1])
                    seconds = float(str2[2])
                    time = (hours*3600) + (minutes*60) + seconds
                    time_data1.append(time)
                
                time_data2 = []
                for t in time_data1:
                    time_offset = t - time_data1[0]
                    time_offset = round(time_offset, 3)
                    time_data2.append(time_offset)
                data_to_plot[key] = time_data2

            elif 'RGB' in key:
                red_data = []
                green_data = []
                blue_data = []

                for data in data_dict[key]:
                    color = data.split('-')
                    if color[0] == "None":
                         red_data.append(np.nan)

                    if color[1] == "None":
                        green_data.append(np.nan)

                    if color[2] == "None":
                        blue_data.append(np.nan)

                    else:
                        red_data.append(int(color[0]))
                        green_data.append(int(color[1]))
                        blue_data.append(int(color[2]))
                
                data_to_plot['Red'] = red_data
                data_to_plot['Green'] = green_data
                data_to_plot['Blue'] = blue_data

            elif 'Frequency' in key:
                temp_freq = []
                for data in data_dict[key]:
                    if data == "None":
                        temp_freq.append(np.nan)

                    else:
                        temp_freq.append(float(data))

                key = key.split(' ')[0]

                data_to_plot[key] = temp_freq

            else:
                temp_data = []
                for data in data_dict[key]:
                    temp_data.append(float(data))
                if " " in key:
                    key = key.split(' ')[0] # some headers have a space in them, this takes the space out to make the keys in data_to_plot{} easier to use
                data_to_plot[key] = temp_data

        # create subplots
        fig = plt.figure()
        keys = []
        for key in data_to_plot:
            keys.append(key)

        rgb_fig_num = 234
        for k in keys[1:]: # couldn't think of a better way to skip the first key (Timestamp)
            x = np.array(data_to_plot['Timestamp'])
            y = np.array(data_to_plot[k])
            # place the plots in specific locations in main plot
            if k == 'Distance':
                ax = fig.add_subplot(231)
                ax.set_ylabel("Distance (cm)")
            if k == 'Frequency':
                ax = fig.add_subplot(232)
                ax.set_ylabel("Frequency (Hz)")
            if k == 'Potentiometer':
                ax = fig.add_subplot(233)
                ax.set_ylabel("Potentiometer %")
            if k == 'Red' or k == 'Green' or k == 'Blue':
                ax = fig.add_subplot(rgb_fig_num)
                ax.set_ylabel(k + " value")
                rgb_fig_num += 1

            ax.plot(x, y)

            ax.set_xlabel("Time (ms)")

            if k == 'Red' or k == 'Green' or k == 'Blue':
                ax.set_title("RGB " + k + " value")
            else:
                ax.set_title(k + " vs time")

            # create y limits based on the data's smallest/largest value -/+ a scalar of 10 to fit all data
            try:
                smallest_value = sorted(data_to_plot[k])[0]
                if smallest_value == 0 or smallest_value == 0.0:
                    smallest_value = -1
            except TypeError: # if value shows up as nan
                smallest_value = -1

            try:
                largest_value = sorted(data_to_plot[k])[-1]
                if largest_value == 0 or largest_value == 0.0:
                    largest_value = 1
            except TypeError: # if value shows up as nan
                largest_value = 1
            ymin = smallest_value - (largest_value / 10)
            ymax = (largest_value / 10) + largest_value
            
            # this is to account for nan values in the middle of the data set
            if True in np.isnan(y): 
                values = []
                for value in y:
                    if value != np.nan:
                        values.append(value)
                ymin = min(values)
                ymax = max(values)
                ymin = ymin - (ymax / 10)
                ymax = (ymax / 10) + ymax
            
            # really bad fix if here is no data to plot
            if ymin == 0:
                ymin = -1
            
            if ymax == 0:
                ymax = 1

            try:
                plt.ylim(ymin, ymax)
            except ValueError:
                values = []
                for value in y:
                    if value != np.nan:
                        values.append(value)
                ymin = min(values)
                ymax = max(values)
                ymin = ymin - (ymax / 10)
                ymax = (ymax / 10) + ymax
                
            ax.xaxis.set_major_locator(MaxNLocator(5))
            ax.yaxis.set_major_locator(MaxNLocator(5))
            
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
    
    # get figure names to save for file later
    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums] 
    
    # thread to handle if the user wants to save the plot or not
    save_thread = threading.Thread(target=save_plot, args=[files, figs], daemon=True)
    save_thread.start()

    plt.tight_layout() # space out the plots
    plt.show()

def save_plot(files, figs):
    # if user wants to save the file
    true_input = False
    
    split_str = files[0].split('.')[0] # get data file name before file extension
    fig = figs[0] # matplotlib figure object
    
    while not true_input: # keep having user input something until program likes it 
        user_input = input("Do you want to save the plot(s)? (Y/N) ")
        try:
            # if user type y or Y, then save file as <data file name>.png
            if user_input.upper() == "Y":
                if not os.path.exists("./DataFiles/" + split_str + ".png"):
                    fig.savefig("./DataFiles/" + split_str + ".png")
                    print("Saving " + split_str + ".png")
                    print("Done.")

                else:
                    print(split_str + ".png exists. Not overwriting.")

                true_input = True

            elif user_input.upper() == "N":
                true_input = True

            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Invalid Input.")

        except ValueError:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid Input.")      

if __name__ == '__main__':
    if sys.argv[1:]:
        ip = sys.argv[1] # ip address

        try:
            plot_bit = sys.argv[2] # bit flip if user wants to plot a file or not
            plot_bit_int = int(plot_bit)
            if plot_bit_int not in [0,1]:
                print("Invalid input: Invalid plot mode")
                sys.exit()
        except (ValueError, IndexError):
            print("Invalid input: Invalid plot mode")
            sys.exit()

        try:
            input_file = sys.argv[3] # file that user wants to receive/plot
        except IndexError:
            input_file = ""
    
    else:
        print("Invalid Input: Missing all arguments")
        sys.exit()

    files = scp(ip, input_file) # connect to scp via ssh

    if plot_bit_int == 1:
        if input_file != "":
            plot_data(files)
    
        else:
            print("Input file name is needed for plotting")
            sys.exit()

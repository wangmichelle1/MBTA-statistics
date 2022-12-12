'''
     Michelle Wang 
     mbta.py
     Goal -- Informs user about average riders per line of different MBTA
     lines, ridership on all lines over different times of the day,
     and plots this information
'''

import csv
import matplotlib.pyplot as plt

MBTA_FILE = "mbta_data.csv"
LINE_COL = 3
TOTAL_ON = 12
TOTAL_OFF = 13
TIME_OF_DAY = 8

def read_file(filename):
    ''' Function: read_file
        Parameters: filename (string) for a CSV file
        Returns: 2d list of what the file contains, w/o the header
    '''
    data = []
    
    with open(filename, "r") as csvfile: 
        file = csv.reader(csvfile, delimiter = ",")
        next(file)
        for row in file: 
            data.append(row)
            
    return data 
    
def get_col(data, col):
    ''' Function: get_col
        Parameters 2d list of anything, a column number (int)
        Returns: one column of the 2d list, turned into a list of its own
    '''
    column_lst = []
    
    for i in range(len(data)):
        for j in range(len(data[i])): 
            column_data = data[i][col]
        column_lst.append(column_data)
    
    return column_lst

def riders_per_line(all_data, line, line_col, on_col):
    ''' Function: riders_per_line
        Parameters: 2d list of strings (original data from csv), the line to 
                    look for (a string), the column number where the line is,
                    and column number where the # of riders getting on is
        Returns: the average number of riders on that line
    '''
    target_line_nums = []
    
    for i in range(len(all_data)):
        for j in range(len(all_data[i])):
            if all_data[i][line_col] == line:
                target_line_num = int(all_data[i][on_col])
                target_line_nums.append(target_line_num)
                
    average = sum(target_line_nums) / len(target_line_nums)
    
    return average 

def split_by_time(all_data, time, timecol):
    ''' Function: split_by_time
        Parameters: 2d list of strings (original data from csv),
                    time we care about (string), and column where the time is
        Returns: New 2d list that contains the data just for that time
    '''
    time_period = []
    
    for i in range(len(all_data)):
        if all_data[i][timecol] == time: 
            time_period.append(all_data[i])
    
    return time_period

def plot_ridership(ridership, lines):
    ''' Function: plot_ridership
        Parameters: one list of ints: t-riders getting on,
                    one list of strings: the lines we care about
        Returns: nothing, just generates a plot
    '''
    pos = [i for i in range(len(lines))]    
    plt.bar(pos, ridership, color = lines)
    plt.title("MBTA average ridership")
    plt.xticks(pos, lines)

def plot_time_ridership(ridership_by_time, lines):
    ''' Function: plot_time_ridership
        Parameters: 2d list of floats; each sublist is the ridership of
                    all 4 lines at a certain time of day
                    [[greenam, blue-am, red-am, orange-am], [green-pm,...]]
                    plus
        Returns: nothing, just creates a plot
    '''
    for i in range(len(lines)):
        curr_line = get_col(ridership_by_time, i)
        plt.plot(curr_line, color = lines[i])
    plt.title("Ridership on all lines over the day")
    plt.xticks([i for i in range(0, len(ridership_by_time), 3)],
                ["Early morning", "Midday", "PM Peak", "Night"])
    
def main():
    # Step One: Gathering data
    # Get the data as a 2d list of ints
    data = read_file(MBTA_FILE)

    # Step Two: Computations 
    # Compute the average number of riders getting on each line
    lines = ["Green", "Blue", "Red", "Orange"]
    ridership = []
    for i in range(len(lines)):
        on_riders = riders_per_line(data, lines[i], LINE_COL, TOTAL_ON)
        ridership.append(on_riders)
    
    # Step Two: Computations
    # Count the average number of total riders at each time of day
    # We can reuse the ridership functions above, but first we
    # split the data into each separate part of day
    ridership_time = []
    for i in range(1, 12):
        time_period = "time_period_{:02d}".format(i)
        time_data = split_by_time(data, time_period, TIME_OF_DAY)
        curr_riders = []
        for j in range(len(lines)):
            riders = riders_per_line(time_data, lines[j], LINE_COL, TOTAL_ON)
            curr_riders.append(riders)
        ridership_time.append(curr_riders)
        
    # Step Three: Communicate! 
    # Plot the average number of riders getting on each line
    print("Average ridership per line:")
    for i in range(len(lines)):
        print("\t", lines[i], ": ", round(ridership[i]), " avg riders.",
              sep = "")
    plot_ridership(ridership, lines)
    plt.show()
    
    # Step Three: Communicate
    # Plot each line's ridership over the day as a line chart
    plot_time_ridership(ridership_time, lines)
    
main()  
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
import datetime
import time
import csv
import numpy as np
from scipy import integrate

# Use computer modern font in plots:
"""
plt.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.serif': ['Computern Modern Roman'],
})
"""

# Change default font sizes for plot
SMALL_SIZE = 20
MEDIUM_SIZE = 30
BIGGER_SIZE = 40

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

# Change default plot size
mpl.rcParams['figure.figsize'] = (20, 10)

# Set max plot size
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()

# Set plot style
#plt.style.use('fivethirtyeight')


index = count()

# Set today's filename
startTime = datetime.datetime.today()
startTimeFileName = startTime.strftime("%Y-%m-%d")
fileName = "../Data/Data" + "_" + startTimeFileName + ".csv"    # Set name of created .csv file

# Set current electricity price
priceperkWh = 27e-2    # [CHF/kWh]

# Get date
date = datetime.datetime.today()
dateFileName = date.strftime("%Y-%m-%d")

# Create plot
fig, ax = plt.subplots()

# Set plot name
plotName = "../Plots/Plot" + "_" + dateFileName + ".pdf"    # Set name of created .csv file

def plot_myStrom(i):
    # Read CSV file
    with open(fileName) as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        data_read = [row for row in reader]

    nrows = np.shape(data_read)[0]

    Power = np.zeros(nrows)
    Energy = np.zeros(nrows)
    Temp = np.zeros(nrows)
    time = ["" for row in range(nrows)]
    timeInt = np.zeros(nrows)

    # Assign data to variables
    for row in range(nrows):
        Power[row] = data_read[row][0]
        Energy[row] = data_read[row][1]
        Temp[row] = data_read[row][3]
        time[row] = data_read[row][4][11:19]
        timeInt[row] = int(time[row][0:2]) * 3600 + int(time[row][3:5]) * 60 + \
                       int(time[row][6:8])

    # Numerical integration to get kWh
    kWh = integrate.simpson(Power, timeInt)/(3.6 * 1e6)
    cost = kWh * priceperkWh

    # Clear previous axes
    plt.cla()

    # Create plot
    ax.plot(timeInt, Power, color='gray', alpha=0.8, linestyle='solid')

    # Shade area under curve
    ax.fill_between(timeInt, Power, facecolor='gray', alpha=0.2)

    # Beautify the x-labels
    # ax.set_xticks(timeFloat)
    freq = int(timeInt[1]-timeInt[0]*np.max(timeInt))
    print(max(timeInt)- np.min(timeInt))
    ax.set_xticks(timeInt[::freq])
    ax.set_xticklabels(time[::freq])
    deltat = np.max(timeInt) - np.min(timeInt)
    #plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.15 * deltat))

    # Add labels
    ax.set_xlabel(r'Time')
    ax.set_ylabel(r'Power [W]')

    # Set axis limits
    ax.set_ylim([0, 1.3 * np.max(Power)])

    # Add text
    text = 'Energy = {:.6f} kWh \nCost = {:.6f} CHF = {:.1f} mRp'\
            .format(kWh, cost, cost*1e5)
    xpos = np.max(timeInt) - 0.38 * (np.max(timeInt) - np.min(timeInt))
    ypos = 1.15*np.max(Power)
    ax.text(xpos, ypos, text)

    # Set title
    ax.set_title(r'Power Consumption', y=1.01)

    # Titles
    fig.suptitle('MyStrom Data ' + dateFileName, fontsize=30, y=0.99)

    # Save plot (w/o title)
    #plt.savefig(plotName, bbox_inches='tight')


def animate_myStrom():
    time.sleep(2)

    ani = FuncAnimation(plt.gcf(), plot_myStrom, interval=200)

    plt.show()


animate_myStrom()

exit()

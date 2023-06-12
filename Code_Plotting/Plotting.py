import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime
import csv
import numpy as np
import matplotlib.ticker as plticker
from scipy import integrate
import warnings
warnings.filterwarnings("ignore")

# Use computer modern font in plots:
plt.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.serif': ['Computern Modern Roman'],
})


def plot_myStrom(fileName):

    # Set current electricity price
    priceperkWh = 27e-2    # [CHF/kWh]

    # Get date
    date = datetime.datetime.today()
    dateFileName = date.strftime("%Y-%m-%d")

    # Set plot name
    plotName = "../Plots/Plot" + "_" + dateFileName + ".pdf"    # Set name of created .csv file

    # Read CSV file
    with open(fileName) as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        data_read = [row for row in reader]

    nrows = np.shape(data_read)[0]
    ncols = np.shape(data_read)[1]

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
        timeInt[row] = int(time[row][0:2])*3600 + int(time[row][3:5])*60 + \
                       int(time[row][6:8])

    # Numerical integration to get kWh
    kWh = integrate.simpson(Power, timeInt)/(3.6*1e6)
    kWhperYear = kWh * 365
    costperYear = kWhperYear * priceperkWh

    # Create plot
    fig, ax = plt.subplots()
    ax.plot(timeInt, Power, color='gray', alpha=0.8, linestyle='solid')

    # Shade area under curve
    ax.fill_between(timeInt, Power, facecolor='gray', alpha=0.2)

    # Beautify the x-labels
    # ax.set_xticks(timeFloat)
    ax.set_xticks(timeInt[::15])
    ax.set_xticklabels(time[::15])
    deltat = np.max(timeInt) - np.min(timeInt)
    #plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.15 * deltat))

    # Add labels
    ax.set_xlabel(r'Time')
    ax.set_ylabel(r'Power [W]')

    # Set axis limits
    ax.set_ylim([0, 1.2 * np.max(Power)])

    # Add text
    # print('{:.3f}'.format(kWh))
    text = 'Energy = {:.3f} kWh \n Per Year: {:.1f} kWh \n Annual Cost = {:.2f} CHF'\
            .format(kWh, kWhperYear, costperYear)
    xpos = np.max(timeInt) - 0.4 * (np.max(timeInt) - np.min(timeInt))
    ypos = 1.2 * np.max(Power) - 0.2 * (np.max(Power) - np.min(Power))
    ax.text(xpos, ypos, text)

    # Set title
    ax.set_title(r'Power Consumption')

    # Titles
    fig.suptitle('MyStrom Data ' + dateFileName, fontsize=16, y=0.98)   # Set overall title

    # Save plot (w/o title)
    plt.savefig(plotName, bbox_inches='tight')

    plt.show()


plot_myStrom('/Users/eduardmeier/Desktop/Python/Projects_meiered/Mystrom/Data/Data_2022-12-26_fixed.csv')

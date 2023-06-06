# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
from numpy import *
import numpy as np


# Libraries for plotting
import matplotlib.pyplot as plt

import cufflinks as cf
cf.set_config_file(offline=True)

#RM TODO - check this
pd.options.plotting.backend = "plotly"

# Set max row to 300
pd.set_option('display.max_rows', 300)

class PricePath:
    def __init__(self):
        pass


class OneStepPricePath(PricePath):
    #May be appropriate for simple, non-path-dependent derivatives

    def __init__(self):
        pass


class MultiStepPricePath(PricePath):
    #Simulate a full price path for the assset
    def __init__(self, s0, mu, sigma, time_horizon, n_timesteps, n_sims):
        self.s0 = s0 #initial spot level
        self.r = mu #asset drift rate
        self.sigma = sigma #std deviation of the asset
        self.time_horizon = time_horizon #time horizon for the sim, i.e. T
        self.n_timesteps = n_timesteps #number of timesteps between t0 and T
        self.n_sims = n_sims #number of price paths to simulate

    def simulate_path(self):
        #Define the length of the time interval, dt
        dt = self.time_horizon/self.n_timesteps

        #This array will hold the simulated prices
        #Dimensions: t+1, n
        #Initialise with zeros
        S = zeros((self.n_timesteps + 1, self.n_sims))

        S[0] = self.s0

        for i in range(1, self.n_timesteps+1):
            #get n random numbers
            #RM TODO abstract this away!
            #Make it a class or at least use enums or something
            z = random.standard_normal(self.n_sims)

            #RM TODO make sure all these calcs are CORRECT!!!!
            exponentialTerm = exp((self.r - 0.5 * self.sigma **2) * dt + self.sigma * sqrt(dt) * 2)

            S[i] = S[i-1] * exponentialTerm

        return S


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    #RM TODO sort this
    plt.interactive(True)
    plt.show()

    pricePath = MultiStepPricePath(100, 0.05, 0.2, 1, 252, 100000)
    spath = pricePath.simulate_path()

    #Now let's print it, see what it looks like
    #RM TODO - pull this away in to a function or somesuch
    #first pop it in to a dataframe for convenience
    spath_df = pd.DataFrame(spath)

    print(spath_df.shape)
    print(spath_df.head())

    x = np.linspace(0,252, 253)
    y = spath_df.iloc[:,2:3].values

    print(x.shape)
    print(y.shape)


    #x1 = array([1,2,3,4,5,6,7,8])
    #x2 = array([5,6,7,8,9,1,2,3])
    #y = array([0.1, 0.2, 0.5, 0.7, 0.1, 2.1, 1.2, 2.2 ])

    #print(x1.shape)
    #print(x2.shape)

    #print(y.shape)


    plt.plot(x, y)
    #plt.plot(x2, y)
    plt.show()

    #spath_df.iloc[:,100].plot()
    #plt.show()

    cf.go_offline()

    spath_df.iloc[:, :100].iplot(title='Simulated Geometric Brownian Motion Paths', \
                                   xTitle='Time Steps', yTitle='Index Levels')

    print("this is the last line of the program - exiting")







# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# Imports
import time

import pandas
import pandas as pd
from numpy import *

from enum import Enum

# Imports for the visualisation side of things...
import matplotlib
import matplotlib.pyplot as plt

# Some pyplot settings
# RM TODO this should live somewhere
plt.style.use('ggplot')
matplotlib.rcParams['figure.figsize'] = [12.0, 8.0]
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['lines.linewidth'] = 2.0

# set pandas settings:
# RM TODO this should live somewhere
pd.set_option('display.max_rows', 300)

def printstars():
    print('*********************************************************************')

class MCENUM(Enum):
    # In a proper implementation one should really have enums broken out by category, each group
    # in it's own class, to stop accidentally using the wrong one in the wrong place.
    # However, in a toy implementation such as this this doesn't really make sense - I'm really just
    # trying to stop myself from passing around text strings or whatever

    # Do NOT assume that all of these features are fully implemented! :)

    # RM TODO this is just an outline right now

    # Pseudorandom numbers
    PSEUDO_STD_NORMAL = 11
    PSEUDO_UNIFORM = 12
    PSEUDO_WILMOTT = 13 # Paul's special quickie excel trick

    # Variance Reduction Methods
    ANTITHETIC_VARIATES = 21 #see Joshi p93
    CONTROL_VARIATES = 22
    MOMENT_MATCHING = 23

    # Processing tweaks, such as, run to a max error size, or for a particular period?
    TIMED_EXECUTION = 31
    MAX_ERROR = 32

    # Low Discrepancy, Sobol, etc.  Potentially highly experimental!
    LOW_DISCREPANCY = 41
    SOBOL = 42
    BROWNIAN_BRIDGE = 43

    # Option values
    OPT_CALL = 51
    OPT_PUT = 52

class Timer:
    def __init__(self):
        self.start = time.perf_counter()

    #def stop(self):
    #    return str(time.perf_counter() - self.start

    def elapsed(self):
        return str(f'{(time.perf_counter() - self.start):0.4f}')

    def elapsedastime(self):
        return time.perf_counter() - self.start

class RandomNumberGenerator:
    # Must return a VECTOR of values
    # This is just to abstract away the mechanism of creating the asset path simulations
    # and allow customisation if required

    # RM TODO:  Do we want to generate a bunch of timesteps here, or just one?
    def __init__(self, seed, num_sims, variance_reduction_strategy = 'None'):
        # do init
        self.seed = seed
        self.num_sims = num_sims

        #use the variance reduction strategy to decide which RNs to create
        # blah
        pass

    def get_rns(self, rntype):
        # for the moment just use random.standard_normal()
        # but RM TODO abstract this away
        t = Timer()

        typeasstring = ''

        if rntype == MCENUM.PSEUDO_STD_NORMAL:
        #    typeasstring = "Standard Normal"
            retval = random.standard_normal(self.num_sims)
        elif rntype == MCENUM.PSEUDO_UNIFORM:
        #    typeasstring = "Uniform"
            retval = random.random()
        else:
        #    typeasstring = "Something else!"
            # Not implemented yet.  RM todo!
            raise (Exception('Not implemented yet!'))

        #print(f'Generated {self.num_sims:,} asset prices in {t.elapsed()} '
        #      f'seconds from {typeasstring} distribution.  ', end='')
        return retval

class BrownianBridge:
    # RM TODO
    pass


class Option:
    # not much to do here yet
    def __init__(self, K, r, T, putcall):
        # again, not much to do yet
        self.K = K
        self.r = r
        self.T = T
        self.putcall = putcall
        pass

    def GetPayOff(self):
        # RM TODO - this should never be called - not yet anyway
        raise Exception("this this shouldn't get called- not yet anyway")

class PathDependentOption(Option):
    def __init__(self, K, r, T, putcall):
        Option(K, r, T, putcall).__init__()

    def GetPayOff(self, asset_val):
        raise (Exception("this shoudln't be called!"))
        pass

class AsianOption(PathDependentOption):
    def __init__(self):
        pass

    def GetPayOff(self, asset_val):
        pass

class LookBackOption(PathDependentOption):
    def __init__(self):
        pass

    def GetPayOff(self, asset_val):
        pass

class PathIndependentOption(Option):
    def __init__(self, K, r, T, putcall):
        super().__init__(K, r, T, putcall)

    def GetPayOff(self, asset_val):
        if self.putcall == MCENUM.OPT_CALL:
            C0 = exp(-self.r * self.T) * mean(maximum(asset_val[-1] - self.K, 0))
            return C0
        if self.putcall == MCENUM.OPT_PUT:
            P0 = exp(-self.r * self.T) * mean(maximum(self.K - asset_val[-1], 0))
            return P0
        pass


class Visualiser():
    # not sure what to do here yet
    pass

class MonteCarloEngine():
    def __init__(self, S0, mu, sigma, horizon, timesteps, n_sims, seed = 10_000):
        # RM TODO perhaps run the price path sim here, and store for later
        self.S0 = S0                    # initial value of the asset for the simulation
        self.r = mu                     # r = mu, as we are using RN valuation
        self.sigma = sigma              # vol
        self.T = horizon                # How far out should we simulate
        self.timesteps = timesteps      # number of timesteps
        self.n_sims = n_sims            # How many asset paths to simulate

        self.seed = seed                # seed for random number generator

        # Pre-calculate some bits and pieces
        self.dt = self.T / self.timesteps   #size of each timestep

        # Create the initial (empty) space for the data
        # and pre-populate the first value with S0
        self.S = zeros((self.timesteps, self.n_sims))
        self.S[0] = self.S0

        return

    def visualise_histogram(self, w, standardise = True):
        # rm todo - not working!
        if standardise == True:
            plt.hist(pd.DataFrame( ( w - w.mean()) / w.std()), bins = 100, color='cornflowerblue')
        else:
            # RM TODO - implement this once you're happy the one above looks right
            pass

        return

        plt.show()

    def simulate_price_paths(self):
        # RM TODO, is this even neeeded?
        # this is where much of the meat goes
        pass

    def run_sim(self, timed_execution = False, howlongtorun = 0):
        # RM TODO all of this
        # Create an option object - this is what you want to price
        # Visualise the payoff
        # Get the price paths.  Decide (here or elsewhere) if you want to
        # do one big jump or the full timestep treatment.  Visualise the price paths
        # Price the Option
        # Do the averaging and all that
        # check convergence / whatever

        RNG = RandomNumberGenerator(self.seed, num_sims=self.n_sims)

        t = Timer()

        printstars()
        print(f'Beginning Monte Carlo simulation with parameters:\nseed = {self.seed:,}, '
              f'\nnumber of simulations = {self.n_sims:,}, \ntime horizon = {self.T}, \nnumber of timesteps: {self.timesteps:,}')
        printstars()

        # If the timed_execution parameter is set to true, then it means the job should
        # execute until the timer is up
        for i in range(0, self.timesteps - 1):
            # get a vector of random numbers
            w = RNG.get_rns(MCENUM.PSEUDO_STD_NORMAL)

            # have a look at the first set of random numbers we get
            #if i == 0:
            #    self.visualise_histogram(w, standardise=True)

            # Then populate the asset prices for the next timestep
            # RM TODO document this mathematically
            self.S[i + 1] = self.S[i] * (1 + self.r * self.dt + self.sigma * sqrt(self.dt) * w)

            # every 1000 timesteps, check to see if we've run out of time
            # Given that we are in a non-production setting, to be honest this is unlikely
            # to be particularly useful.  However if we were valuing an entire trader book
            # and wanted to get absolute minimum error in the allotted time, this could be a
            # lightweight way to do it
            # RM TODO document this in the notebook
            # RM TODO we should also return standard error, perhaps
            if timed_execution == True and i % 1_000 == 0:
                if t.elapsedastime() > howlongtorun:
                    print(f'Timed execution:  exiting after {i} iterations and {t.elapsed()} seconds')
                    return

            print(f'Generated {w.shape:,} asset prices in {t.elapsed()} seconds')

        # RM TODO Now visualise what we got, and perform some initial statistical analysis too

        return

    def PriceVanillaOption(self, putcall, optiontype):
        #This is really just a wee test right now
        #RM TODO - sort this out and pull together with the rest of the stuff

        # Get the Random numbers:

        RNG = RandomNumberGenerator(self.seed, num_sims=self.n_sims)

        t = Timer()
        print(f'Beginning Monte Carlo simulation with parameters:\nseed = {self.seed:,}, '
              f'\nnumber of simulations = {self.n_sims:,}, \ntime horizon = {self.T}, \nnumber of timesteps: {self.timesteps:,}')

        #And form in to an asset path:

        for i in range(0, self.timesteps - 1):
            # get a vector of random numbers
            w = RNG.get_rns(MCENUM.PSEUDO_STD_NORMAL)

            # Then populate the asset prices for the next timestep
            # RM TODO document this mathematically
            self.S[i + 1] = self.S[i] * (1 + self.r * self.dt + self.sigma * sqrt(self.dt) * w)

        #Create an Option Class first, with all the right bits:
        myOption = PathIndependentOption(K = 100, r = 0.05, T = 1, putcall = optiontype)


        # And finally price it:
        jim = myOption.GetPayOff(self.S)

        print(f'priced option with value {jim}')

    def calculate_pi(self, numsims):
        #rng = RandomNumberGenerator(seed = 10000, num_sims=100000)

            x = random.random(numsims)
            y = random.random(numsims)

        print(x)
        print(y)

        xy = pandas.DataFrame(zip(x, y), columns=['x','y'])
        print(xy)

        xydf = pd.DataFrame(xy)
        xydf['xsqplusysq'] = (xydf['x'] - 0.5) **2 + (xydf['y'] - 0.5)**2
        xydf['InOrOut'] = where(xydf['xsqplusysq'] < 0.5 **2, 4, 0)


        #xydf['InOrOut'] = xydf['x']

        print(xydf)

        print()

        avg = xydf['InOrOut'].mean()
        stddev = xydf['InOrOut'].std()

        print(f'average: {avg}, std dev: {stddev}')

        return avg




class Statistics:
    # intent here is to have just a bunch of stats about
    # the monte carlo sim, but perhaps also the price paths?
    # Like RM TODO the shape, mean, standard deviation, perhaps other moments

    # Joshi: "One standard method of checking the
    # convergence is to examine the standard error of the simulation; that is measure the
    # SAMPLE standard deviation and divide by the square root of the number of paths. If
    # one is using low-discrepancy numbers this measure does not take account of their
    # special properties and, in fact, it predicts the same error as for a pseudo-random
    # simulation.  One alternative method is therefore to use a convergence table. Rather than re-
    # turning statistics for the entire simulation, we instead return them for every power
    # of two to get an idea of how the numbers are varying"

    # Lots of useful stuff in JOSHI!  around p66 - p80 ish

    def __init__(self):
        # do something
        pass




if __name__ == '__main__':

    print(f'starting!')


    #RM TODO - have a think about if we should be passing in T here
    #Surely we want that to be aligned with the maturity of the oprion?

    MyMC = MonteCarloEngine(S0 = 100,
                            mu = 0.05,
                            sigma = 0.2,
                            horizon = 1,
                            timesteps=252,
                            n_sims= 100_000,
                            seed = 10_000)

    ###############################################
    ### Calculating Pi
    ###############################################

    #t = Timer()
    #results = pd.DataFrame(columns=['numsims', 'pi_est'])
    #for i in range(1_000_000, 30_000_000, 1_000_000):

    #    pi_est = MyMC.calculate_pi(numsims=i)

        #this doesn't work
    #    results = results.append({'numsims': i, 'pi_est': pi_est}, ignore_index=True)

    #    print (results)

    #    print(f'Value of Pi calculated using {i} simulations is: {pi_est}')

    #print(f'complete in {t.elapsed()} seconds')
    #print (results)

    #results.plot()

    #MyMC.run_sim(timed_execution=True, howlongtorun=5)

    #MyMC.run_sim(timed_execution=True, howlongtorun=60)


    ################################################
    ### Performing a timed execution
    ################################################

    #t = Timer()
    #howlongtorun = 5
    #while t.elapsedastime() < howlongtorun:
    #    print(f'still waiting at {t.elapsed()}')

    ################################################
    ### Pricing a vanilla Option - for backward testing
    ################################################

    printstars()
    print(f'Attempting to price Vanilla Options x2')
    MyMC.PriceVanillaOption(MCENUM.OPT_CALL)
    MyMC.PriceVanillaOption(MCENUM.OPT_PUT)
    printstars()
    print('\n')

    printstars()
    print(f'Attempting to price Asian Option x1')
    MyMC.run_sim()




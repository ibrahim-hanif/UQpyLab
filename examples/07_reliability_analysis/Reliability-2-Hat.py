# %% [markdown]
# # RELIABILITY: TWO-DIMENSIONAL HAT FUNCTION
# 
# This example showcases the application of various reliability analysis
# methods in UQ[Py]Lab to a two-dimensional hat function.
# 
# ## 1 - INITIALIZATION
# ### Package imports

# %%
from uqpylab import sessions
import pprint; pp = pprint.PrettyPrinter(depth=2)

# %% [markdown]
# ### Start a remote UQCloud session

# %%
# Start the session
mySession = sessions.cloud()
# (Optional) Get a convenient handle to the command line interface
uq = mySession.cli
# Set the timeout
mySession.timeout = 2000
# Reset the session
mySession.reset()


# %% [markdown]
# ### Set the random seed for reproducibility

# %%
uq.rng(100,'twister');

# %% [markdown]
# ## 2 - COMPUTATIONAL MODEL
# The two-dimensional hat function is defined as follows:
# $$g(x_1, x_2) = 20 - (x_1 - x_2)^2 - 8 (x_1 + x_2 - 4)^3$$
# 
# ### Create a limit state function model based on the hat function using a string, written below in a vectorized operation:
# 

# %%
ModelOpts = { 
    'Type': 'Model', 
    'ModelFun':'Hat.model',
    'isVectorized': True
}
myModel = uq.createModel(ModelOpts)

# %% [markdown]
# ## 3 - PROBABILISTIC INPUT MODEL
# The probabilistic input model consists of two independent and identically-distributed Gaussian random variables:
# $$X_i \sim \mathcal{N}(0.25, 1), \quad i = 1, 2$$
# 
# ### Specify the marginals of the two input random variables:

# %%
InputOpts = {
    "Marginals": [
        {"Name":"X1",
         "Type":"Gaussian",
         "Parameters":[0.25,1]
        },
        {"Name":"X2",
         "Type":"Gaussian",
         "Parameters":[0.25,1]
        }
    ]
}

# %% [markdown]
# ### Create an INPUT object based on the specified marginals and print its properties

# %%
myInput = uq.createInput(InputOpts)
uq.print(myInput)

# %% [markdown]
# ## 4 - STRUCTURAL RELIABILITY
# 
# Failure event is defined as $g(\mathbf{x}) \leq 0$. The failure probability is then defined as $P_f = P[g(\mathbf{x})\leq 0]$.
# Reliability analysis is performed with the following methods:
# 
# * Monte Carlo simulation (MCS)
# * Subset simulation
# * Adaptive-Kriging-Monte-Carlo-Simulation (AK-MCS)
# * Adaptive-Polynomial-Chaos-Kriging-Monte-Carlo-Simulation (APCK-MCS)
# * Stochastic spectral embedding-based reliability (SSER)
# * First-order reliability method (FORM)
# * Importance sampling (IS)

# %% [markdown]
# ### 4.1 Monte Carlo simulation (MCS)
# Define a `Reliability` analysis using Monte Carlo simulation (MCS) by specifying the maximum sample size, the size of the batches, and the target coefficient of variation:

# %%
MCSOpts = {
    "Type":"Reliability",
    "Method":"MCS",
    "Simulation": { 
        "MaxSampleSize":1.0E+6,
        "BatchSize":1.0E+5,
        "TargetCoV":0.01
    }
}

# %% [markdown]
# Run the Monte Carlo simulation and print out a report of the results:

# %%
MCSAnalysis = uq.createAnalysis(MCSOpts)

# %% [markdown]
# Print out a report of the results:

# %%
uq.print(MCSAnalysis)

# %% [markdown]
# Create a graphical representation of the results (convergence of $P_f$, convergence of $\beta$, and MCS samples):

# %%
uq.display(MCSAnalysis);

# %% [markdown]
# ### 4.2 Subset Simulation
# Define a `Reliability` analysis using subset simulation by specifying the batch size:

# %%
SubsetSimOpts = {
    "Type":"Reliability",
    "Method":"Subset",
    "Simulation": {
        "BatchSize": 10000
    }
}


# %% [markdown]
# Run reliability analysis with Subset simulation:

# %%
SubsetSim = uq.createAnalysis(SubsetSimOpts)

# %% [markdown]
# Print out a report of the results:

# %%
uq.print(SubsetSim)

# %% [markdown]
# Create a graphical representation of the results (plot the subsets):

# %%
uq.display(SubsetSim);

# %% [markdown]
# ### 4.3 Adaptive-Kriging-Monte-Carlo-Simulation (AKMCS)
# Select the `Reliability` module and the AK-MCS method:

# %%
AKMCSOpts = {
    "Type": "Reliability",
    "Method":"AKMCS",
    "Simulation": {
        "MaxSampleSize": 1e6    # Specify the size of the Monte Carlo sample set used for the Monte Carlo simulation
    },
    "AKMCS": {
        "MaxAddedED": 20,       # Specify the maximum number of sample points added to the experimental design
        "IExpDesign": {         # Specify the initial experimental design
            "N": 20,  
            "Sampling": "LHS"
        },
        "Kriging": {            # Specify the options for the Kriging metamodel (note that all Kriging options are supported)
            "Corr": {
                "Family": "Gaussian"
                }
        },
        "Convergence": "stopPf",  # Specify the convergence criterion for the adaptive experimental design algorithm (here, it is based on the failure probability estimate):
        "LearningFunction": "EFF" # Specify the learning function (here, it is the expected feasibility function (EFF))
    }
}

# %% [markdown]
# Run the AK-MCS simulation:

# %%
AKMCSAnalysis = uq.createAnalysis(AKMCSOpts)

# %% [markdown]
# Print out a report of the results:

# %%
uq.print(AKMCSAnalysis)

# %% [markdown]
# Create a graphical representation of the results (plot AKMCS convergence and the AKMCS experimental design and the limit state surface):

# %%
uq.display(AKMCSAnalysis);

# %% [markdown]
# ## 4.4 Adaptive-Polynomial-Chaos-Kriging-Monte-Carlo-Simulation (APCK-MCS)
# 
# APCK-MCS is a variation of AK-MCS in which the Kriging model is replaced by a PC-Kriging (PCK) model.
# 
# Select the `Reliability` module and the APCK-MCS method:

# %%
APCKOpts = {
    "Type": "Reliability",
    "Method": "AKMCS",
    "AKMCS": {
        "MetaModel": "PCK",
        "PCK": {
            "Kriging": {
                "Corr": {
                    "Family": "Gaussian"
                }
            }
        },
        "IExpDesign": {
            "N": 5
        }
    },
    "Simulation": {
        "MaxSampleSize": 1.0E+6
    }
}


# %% [markdown]
# Run the APCK-MCS simulation:

# %%
myAPCKMCSAnalysis = uq.createAnalysis(APCKOpts)

# %% [markdown]
# Print out a report of the results:

# %%
uq.print(myAPCKMCSAnalysis)

# %% [markdown]
# Create a graphical representation of the results (plot APCK-MCS convergence and the APCK-MCS experimental design and the limit state surface):

# %%
uq.display(myAPCKMCSAnalysis);

# %% [markdown]
# ## 4.5 Stochastic spectral embedding-based reliability (SSER)
# 
# SSER is an active learning reliability method that constructs a stochastic spectral embedding of the limit state function with smart refinement, partitioning, and sample enrichment strategies.
# 
# Select the `Reliability` module and the SSER method:

# %%
SSEROpts = {
    "Type": "Reliability",
    "Method": "SSER",
    "SSER": {
        "ExpDesign": {
            "NEnrich": 20    # Set the number of samples to be added in every refinement domain
        },
        "ExpOptions": {
            "Degree": [0, 1, 2, 3, 4]   # Select the polynomial degree of the residual expansion
        }
    }
}

# %% [markdown]
# Run the SSER analysis:

# %%
mySSERAnalysis = uq.createAnalysis(SSEROpts)

# %% [markdown]
# Print out a report of the results:

# %%
uq.print(mySSERAnalysis)

# %% [markdown]
# Visualize the results of the analysis:

# %%
uq.display(mySSERAnalysis);

# %% [markdown]
# ## 4.6 First-order reliability method (FORM)
# Select FORM as the reliability analysis method:

# %%
FORMOpts = {
    "Type": "Reliability",
    "Method":"FORM"
}

# %% [markdown]
# Run the FORM analysis:

# %%
FORMAnalysis = uq.createAnalysis(FORMOpts)

# %% [markdown]
# Print out a report of the results:

# %%
uq.print(FORMAnalysis)

# %% [markdown]
# #### Create a graphical representation of the results:

# %%
uq.display(FORMAnalysis);

# %% [markdown]
# ### 4.7 Importance sampling (IS)
# Select importance sampling (IS) as the reliability analysis method:

# %%
ISOpts = {
    "Type": "Reliability",
    "Method":"IS"
}

# %% [markdown]
# Run the IS reliability analysis:

# %%
ISAnalysis = uq.createAnalysis(ISOpts)

# %% [markdown]
# Print out a report of the results:

# %%
uq.print(ISAnalysis)

# %% [markdown]
# #### Create a graphical representation of the results:

# %%
uq.display(ISAnalysis);

# %% [markdown]
# ## Terminate the remote UQCloud session:

# %%
mySession.quit()

# %%

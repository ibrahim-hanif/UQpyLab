# %% [markdown]
# # RELIABILITY: RESISTANCE VS. STRESS (R-S)
# 
# This example showcases the application of different reliability analysis methods available in UQLab to the simple R-S example.

# %% [markdown]
# ## Package imports

# %%
from uqpylab import sessions
import numpy as np

# %% [markdown]
# ## Start a remote UQCloud session

# %%
# Start the session
mySession = sessions.cloud()
# (Optional) Get a convenient handle to the command line interface
uq = mySession.cli
# Reset the session
mySession.reset()

# %% [markdown]
# ## Set the random seed for reproducibility

# %%
uq.rng(100,'twister');

# %% [markdown]
# ## COMPUTATIONAL MODEL
# The R-S function is defined as:
# $$g(\mathbf{x}) = R - S,$$
# 
# where $\mathbf{x} = \{R,S\}$.
# $R$ and $S$ are the resistance and stress variables, respectively.

# %% [markdown]
# Create a limit state function model using a string, written below in a vectorized operation:

# %%
ModelOpts = { 
    'Type': 'Model', 
    'mString': 'X(:,1) - X(:,2)',
    'isVectorized': 1
}
myModel = uq.createModel(ModelOpts)

# %% [markdown]
# ## PROBABILISTIC INPUT MODEL
# The probabilistic input model consists of two independent Gaussian random variables:
# $$R \sim \mathcal{N}(5, 0.8), \; S \sim \mathcal{N}(2, 0.6)$$

# %% [markdown]
# Specify the probabilistic input model for $R$ and $S$:

# %%
InputOpts = {
    "Marginals": [
        {"Name": "R",               # Resistance
         "Type": "Gaussian",
         "Moments": [5.0 , 0.8]
        },
        {"Name": "S",               # Stress
         "Type": "Gaussian",
         "Moments": [2.0 , 0.6]
        }
    ]
}

# %% [markdown]
# Create an INPUT object based on the specified marginals:

# %%
myInput = uq.createInput(InputOpts)

# %% [markdown]
# ## RELIABILITY ANALYSIS
# 
# Failure event is defined as $g(\mathbf{x}) \leq 0$. The failure probability is then defined as $P_f = P[g(\mathbf{x}) \leq 0]$.
# 
# Reliability analysis is performed with the following methods:
# 
# * Monte Carlo simulation
# * First-order reliability method (FORM)
# * Importance sampling (IS)
# * Subset simulation
# * Adaptive Kriging-Monte Carlo Simulation (AK-MCS)

# %% [markdown]
# ### Monte Carlo simulation (MCS)

# %% [markdown]
# Select the Reliability module and the Monte Carlo simulation (MCS) method:

# %%
MCSOpts = {
    "Type": "Reliability",
    "Method":"MCS"
}

# %% [markdown]
# Specify the maximum sample size:

# %%
MCSOpts["Simulation"] = {
    "MaxSampleSize":1e5
}

# %% [markdown]
# Run reliability analysis with MCS:

# %%
MCSAnalysis = uq.createAnalysis(MCSOpts)

# %% [markdown]
# Print out a report of the results:

# %%
uq.print(MCSAnalysis)

# %% [markdown]
# #### Create a graphical representation of the results:
# 

# %%
uq.display(MCSAnalysis);

# %% [markdown]
# ### FORM

# %% [markdown]
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
# ### Importance sampling (IS)

# %% [markdown]
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
# ### Subset simulation

# %% [markdown]
# Select subset simulation as the reliability analysis method:

# %%
SubsetSimOpts = {
    "Type": "Reliability",
    "Method":"Subset"
}

# %% [markdown]
# Run the subset simulation:

# %%
SubsetSimAnalysis = uq.createAnalysis(SubsetSimOpts)

# %% [markdown]
# Print out a report of the results:

# %%
uq.print(SubsetSimAnalysis)

# %% [markdown]
# #### Create a graphical representation of the results:

# %%
uq.display(SubsetSimAnalysis);

# %% [markdown]
# ### Adaptive Kriging-Monte Carlo Simulation (AK-MCS)

# %% [markdown]
# Select subset simulation as the reliability analysis method:

# %%
AKMCSOpts = {
    "Type": "Reliability",
    "Method":"AKMCS"
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
# #### Create a graphical representation of the results:

# %%
uq.display(AKMCSAnalysis);

# %% [markdown]
# ### Stochastic spectral embedding-based reliability (SSER)
# 
# Select stochastic spectral embedding-based reliability as the reliability analysis method

# %%
SSEROpts = {
    "Type": "Reliability",
    "Method": "SSER"
}

# %% [markdown]
# Run the SSER simulation:

# %%
SSERAnalysis = uq.createAnalysis(SSEROpts)

# %% [markdown]
# Print out a report of the results:

# %%
uq.print(SSERAnalysis)

# %% [markdown]
# #### Create a graphical representation of the results:

# %%
uq.display(SSERAnalysis);

# %% [markdown]
# ## Terminate the remote UQCloud session:

# %%
mySession.quit()

# %%

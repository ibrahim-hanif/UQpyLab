# %% [markdown]
# # RELIABILITY: PARALLEL SYSTEM
# 
# In this example, the failure probability of a parallel system is computed using a plain Monte Carlo simulation (MCS) and the First-Order Reliability Method (FORM). The results are then compared.
# 
# 

# %% [markdown]
# ## Package imports

# %%
from uqpylab import sessions
import numpy as np
from scipy.stats import multivariate_normal as mvn

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
uq.rng(2,'twister');

# %% [markdown]
# ## COMPUTATIONAL MODEL
# 
# The parallel system consists of two 2-dimensional Resistance-Stress (R-S) limit state functions that are defined as follows:
# $$ g_1(r, s) = 1.2 r - 0.9 s; \quad g_2(r, s) = r - s $$
# 
# Create two MODEL objects based on the limit state functions using string with vectorized operation:

# %%
Model1Opts = { 
    'Type': 'Model', 
    'mString': '1.2*X(:,1) - 0.9*X(:,2)',
    'isVectorized': 1
}
myLimitState1 = uq.createModel(Model1Opts)

Model2Opts = { 
    'Type': 'Model', 
    'mString': 'X(:,1) - X(:,2)',
    'isVectorized': 1
}
myLimitState2 = uq.createModel(Model2Opts)

# %% [markdown]
# The full parallel system limit state function can be calculated by just taking the maximum of the two limit state functions:

# %%
ModelFullOpts = { 
    'Type': 'Model', 
    'mString': 'max(X(:,1) - X(:,2), 1.2*X(:,1) - 0.9*X(:,2))',
    'isVectorized': 1
}
myLimitStateFull = uq.createModel(ModelFullOpts)

# %% [markdown]
# ## PROBABILISTIC INPUT MODEL
# 
# The probabilistic input model consists of two independent Gaussian random variables:
# 
# $$ R \sim \mathcal{N} (3, 0.3),\, S \sim \mathcal{N} (2, 0.4) $$
# 
#  Specify the marginals of the two input random variables:

# %%
InputOpts = {
    "Marginals": [
        {"Name": "R",               # Resistance
         "Type": "Gaussian",
         "Moments": [3.0 , 0.3]
        },
        {"Name": "S",               # Stress
         "Type": "Gaussian",
         "Moments": [2.0 , 0.4]
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

# %% [markdown]
# ### Monte Carlo simulation (MCS)
# 
# Select the Reliability module and the Monte Carlo simulation (MCS) method:

# %%
MCSOpts = {
    "Type": "Reliability",
    "Method":"MCS"
}

# %% [markdown]
# MCS is performed on the full parallel system limit state function.
# 
# Select the function:

# %%
uq.selectModel(myLimitStateFull['Name'])

# %% [markdown]
# Specify the maximum sample size:

# %%
MCSOpts["Simulation"] = {
    "MaxSampleSize": 2e6
}

# %% [markdown]
# Run the Monte Carlo simulation:

# %%
myMCSAnalysis = uq.createAnalysis(MCSOpts)

#%% 
# post-process: report and plot
uq.print(myMCSAnalysis)
uq.display(myMCSAnalysis);

# %% [markdown]
# Store the probality of failure in a variable:

# %%
Pf_MC = myMCSAnalysis['Results']['Pf']

# %% [markdown]
# ## First-order reliability method (FORM)
# 
# Select the Reliability module and the FORM method:

# %%
FORMOpts = {
    "Type": "Reliability",
    "Method":"FORM"
}

# %% [markdown]
# FORM is performed on each component of the system.
# 
#  First, select the first component (i.e., the first limit state function):

# %%
uq.selectModel(myLimitState1['Name'])

# %% [markdown]
# Run the FORM analysis on the first limit state function:

# %%
myFORMAnalysis1 = uq.createAnalysis(FORMOpts)

#%% 
# post-process: report and plot
uq.print(myFORMAnalysis1)
uq.display(myFORMAnalysis1);

# %% [markdown]
# Then, perform the FORM analysis on the second limit state function:

# %%
uq.selectModel(myLimitState2['Name'])
myFORMAnalysis2 = uq.createAnalysis(FORMOpts)

#%% 
# post-process: report and plot
uq.print(myFORMAnalysis2)
uq.display(myFORMAnalysis2);

# %% [markdown]
# Retrieve the reliability index of each component:

# %%
betaHL1 = myFORMAnalysis1['Results']['BetaHL']
betaHL2 = myFORMAnalysis2['Results']['BetaHL']

# %% [markdown]
# Calculate the unit vectors ($\alpha$) in the direction of the design point for each system component:

# %%
alpha1 = np.array(myFORMAnalysis1['Results']['Ustar']) / betaHL1 
alpha2 = np.array(myFORMAnalysis2['Results']['Ustar']) / betaHL2

# %% [markdown]
# The failure probability of the parallel system is calculated by:
# 
# $P_f = \Phi_2(-\beta, 0, R),$
# 
# where $\Phi_2$ is a bivariate Gaussian distribution, with zero mean, unit variance, and correlation matrix $R$, evaluated at point $-\beta$.
# 
# The correlation matrix $R$ is defined as follows:
# 
# $R= \left[\begin{matrix} 1 & \alpha_1 \cdot \alpha_2 \\ \alpha_1 \cdot \alpha_2 & 1 \end{matrix} \right]$
# 
# Finally, the failure probability based on the FORM method is computed as follows:

# %%
B = np.array([betaHL1, betaHL2])
mu = np.zeros(2)
R = np.array([[1, alpha1@alpha2],
              [alpha1@alpha2, 1]])
dist = mvn(mean=mu, cov=R)
Pf_FORM = dist.cdf(-B)

# %% [markdown]
# For more details about the derivation of the formula see, for example, Chapter 15 of Engineering Design Reliability Handbook, CRC Press 2004.

# %% [markdown]
# ## RESULTS COMPARISON
# 
# Compare the failure probabilities obtained by the MCS and FORM:

# %%
print(f'Results:\n Pf[MC]   = {Pf_MC}\n Pf[FORM] = {Pf_FORM}')

# %% [markdown]
# ## Terminate the remote UQCloud session:

# %%
mySession.quit()

# %%

# %% [markdown]
# # INPUT MODULE: MARGINALS AND PAIR COPULA
# 
# This example showcases how to define a probabilistic input model with a pair copula dependence structure. In order to display the copula density, the marginals are kept as uniform distributions in $[0,1]$. In this way, the joint probabilty density function (PDF) and the copula density are equivalent.

# %% [markdown]
# ## Package imports

# %%
from uqpylab import sessions

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
uq.rng(100, 'twister');

# %% [markdown]
# ## Probabilistic input model
# 
# The probabilistic input model consists of two variables:
# 
# $X_1 \sim \mathcal{U}(0, 1)$
# 
# and 
# 
# $X_2 \sim \mathcal{U}(0, 1)$

# %%
InputOpts = {
    'Marginals': [
        {
            'Type': 'Uniform',
            'Parameters': [0,1]
        },
        {
            'Type': 'Uniform',
            'Parameters': [0,1]
        }
    ]
}

# %% [markdown]
# Define the copula between the two variables as a Gumbel pair copula:
# 
# $C_{12} = \text{Gumbel}(1.5)$

# %%
InputOpts['Copula'] = {
    'Type': 'Pair',
    'Family': 'Gumbel',
    'Parameters': 1.5
}

# %% [markdown]
# Create an INPUT object based on the specified marginals and copula:

# %%
myInput = uq.createInput(InputOpts)

# %% [markdown]
# Print a report of the INPUT object:

# %%
uq.print(myInput)


# %% [markdown]
# Display a visualization of the INPUT object:

# %%
uq.display(myInput)

# %% [markdown]
# Alternatively, the copula of the input model can be specified using the function `uq_PairCopula(Type, Parameters, Rotation)` as follows:

# %%
InputOpts['Copula'] = uq.PairCopula('Gumbel', 1.5)

# %% [markdown]
# Create the INPUT object:

# %%
myInput2 = uq.createInput(InputOpts)

# %% [markdown]
# Display a visualization of the INPUT object:

# %%
uq.display(myInput2)

# %% [markdown]
# ## Dependence properties of the input model
# 
# The dependence properties of the input model are fully determined by the input copula.
# 
# For instance, a popular measure of the global dependence between two random variables is their Kendall's tau, defined as the probability that two realizations from the random variables are concordant minus the probability that they are discordant.
# 

# %%
Tau_K = uq.PairCopulaKendallTau(myInput['Copula'])
Tau_K

# %% [markdown]
# The probability of joint extremes is also of interest, for instance in reliability and fragility analysis. The Gumbel copula defined above models the upper tail dependence, that is, a positive probability $\lambda_u$ that the random variables it couples take jointly high values:

# %%
Lambda_U = uq.PairCopulaUpperTailDep(myInput['Copula'])
Lambda_U

# %% [markdown]
# This makes the Gumbel copula different from the Gaussian copula, which instead never assigns upper or lower tail dependence, even for high values of its correlation parameter:

# %%
GaussianCopula = uq.PairCopula('Gaussian',0.99)
Lambda_U_Gaussian = uq.PairCopulaUpperTailDep(GaussianCopula)
Lambda_U_Gaussian

# %% [markdown]
# Different parametric pair copula families have different dependence properties (Kendall's tau, upper/lower tail dependence). These properties should be considered when deciding which pair copula to use to model the input! For summary, refer to the UQLab's Input Manual, Chapter "Theory".

# %% [markdown]
# ## Copula rotation
# 
# The PDF of a copula distribution can be rotated by $90$, $180$, or $270$ degrees to model different types of dependencies. For instance:

# %%
InputOpts['Copula'] = {
    'Type': 'Pair',
    'Family': 'Gumbel',
    'Parameters': 1.5,
    'Rotation': 180
}

# %% [markdown]
# creates a version of the Gumbel copula rotated by $180$ degrees. Mathematically, this is obtained by flipping the original copula density $c(u,v)$ around both axes: $c_{180}(u,v) = c(1-u,1-v)$.
# 
# Create an INPUT object based on the rotated copula:

# %%
myInput_rot180 = uq.createInput(InputOpts)

# %% [markdown]
# Display a visualization of the object:

# %%
uq.display(myInput_rot180)

# %% [markdown]
# This new copula has different dependence properties. For instance, it has no upper tail dependence anymore:

# %%
uq.PairCopulaUpperTailDep(myInput_rot180['Copula'])

# %% [markdown]
# but has lower tail one:

# %%
uq.PairCopulaLowerTailDep(myInput_rot180['Copula'])

# %% [markdown]
# Analogously, the copula PDF can be rotated by $90$ and $270$ degrees:

# %%
InputOpts['Copula']['Rotation'] = 90

myInput_rot90 = uq.createInput(InputOpts)

uq.display(myInput_rot90)

# %%
InputOpts['Copula']['Rotation'] = 270

myInput_rot270 = uq.createInput(InputOpts)

uq.display(myInput_rot270)

# %% [markdown]
# ## Terminate the remote UQCloud session

# %%
mySession.quit()

# %%

# %% [markdown]
# # INPUT MODULE: MARGINALS AND GAUSSIAN COPULA
# 
# This example showcases how to define a probabilistic input model with or without a copula dependency.

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
# ## Probabilistic input model (without dependency)
# 
# The probabilistic input model consists of two variables:
# 
# $X_1 \sim \mathcal{N}(0, 1)$
# 
# and 
# 
# $X_2 \sim \mathcal{B}(1, 3)$

# %%
InputOpts = {
    'Marginals': [
        {
            'Type': 'Gaussian',
            'Parameters': [0,1]
        },
        {
            'Type': 'Beta',
            'Parameters': [1,3]
        }
    ]
}

# %% [markdown]
# By default, the variables are considered independent.
# 
# Create an INPUT object based on the specified marginals:

# %%
myInputIndependent = uq.createInput(InputOpts)

# %% [markdown]
# Print a report of the INPUT object:

# %%
uq.print(myInputIndependent)

# %% [markdown]
# ## Probabilistic input model (with dependency: Gaussian copula)
# 
# The marginal distributions of the probabilistic input model are already defined inside the structure `InputOpts`. A dependency following a Gaussian copula is added as follows:

# %%
InputOpts['Copula'] = {
    'Type': 'Gaussian',
    'RankCorr': [[1, 0.8],[0.8, 1]] # the Spearman corr. matrix
}

# %% [markdown]
# Create an INPUT object based on the specified marginals and copula:

# %%
myInputDependent = uq.createInput(InputOpts)

# %% [markdown]
# Print a report of the INPUT object:

# %%
uq.print(myInputDependent)

# %% [markdown]
# ## Comparison of the input models
# 
# Each of the generated INPUT objects can be quickly visualized using the function `uq.display`.
# 
# For the independent INPUT object:

# %%
uq.display(myInputIndependent)


# %% [markdown]
# For the dependent INPUT object:

# %%
uq.display(myInputDependent)

# %% [markdown]
# ## Terminate the remote UQCloud session

# %%
mySession.quit()



# %%

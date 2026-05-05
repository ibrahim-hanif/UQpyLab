# %% [markdown]
# # INPUT MODULE: MARGINALS AND VINE COPULA
# 
# This example showcases how to define a probabilistic input model in three dimension or higher with a vine copula dependence structure.

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
uq.rng(100, 'twister');

# %% [markdown]
# ## Probabilistic input model
# 
# The probabilistic input model consists of three variables:
# 
# * $X_1 \sim \mathcal{N}(0,1)$
# * $X_2 \sim \mathcal{B}(1,3)$
# * $X_3 \sim \mathcal{G}(1,3)$
# 
# Specify the marginals of these variables:

# %%
InputOpts = {
    'Marginals': [
        {
            'Type': 'Gaussian',
            'Parameters': [0,1],
        },
        {
            'Type': 'Beta',
            'Parameters': [1,3]
        },
        {
            'Type': 'Gumbel',
            'Parameters': [1,3]
        }
    ]
}

# %% [markdown]
# The variables are coupled by a Canonical Vine (CVine). A vine in dimension $M$ requires the specification of $M \cdot (M-1)/2$ pair copulas (here, there are three pair copulas):

# %%
InputOpts['Copula'] = {
    'Type': 'CVine',
    'Families': ['Gumbel', 'Gaussian', 'Frank'],
    'Parameters': [1.5, -.4, .3],
    'Rotations': [180, 0, 270],
    'Structure': [1, 2, 3]
}

# %% [markdown]
# Create an INPUT object based on the specified marginals and copula:

# %%
myInput = uq.createInput(InputOpts)

# %% [markdown]
# ## Print and visualize the output
# 
# Print a summary of the input model:

# %%
uq.print(myInput)

# %% [markdown]
# Display a visualization of the input model:

# %%
uq.display(myInput);

# %% [markdown]
# ## How to assign the pair copulas in the vine?
# 
# The pair copulas composing the vine can be a difficult beast to tame.
# 
# Some (the first $M-1$ ones, for an input of dimension $M$) are unconditional pair copulas, the rest are conditional on other variables. But which variables do they couple? It all depends on the vine type and structure!
# 
# If unsure, call the function `uq_CopulaSummary`: when fed with a vine copula type and a vine copula structure, it prints a report of the meaning of the pair copulas of that vine:

# %%
uq.CopulaSummary('CVine',[1,2,3])

# %% [markdown]
# The same function, when fed with an actual copula, prints the same copula information as provided by `uq_print`:

# %%
uq.CopulaSummary(myInput['Copula'])

# %% [markdown]
# Furthermore, a visual representation of the pair copulas composition in a vine can be obtained using the uq_drawVineCopula function:

# %%
uq.display(myInput, show_vine=True);

# %% [markdown]
# ## Vine truncation
# 
# Sometimes, due to lack of information, specifying conditional pair copulas in a vine may be hard or impossible. In these case, it may be reasonable to assume conditional independence from a certain conditioning order. This is called truncation of a vine.
# 
# For instance, truncating a vine at the 1st level means that only the unconditional pair copulas are retained, and the rest are set to the independence copula:

# %%
InputOpts['Copula']['Truncation'] = 1

# %% [markdown]
# Create an INPUT object based on the truncated vine copula:

# %%
myInput_Truncated = uq.createInput(InputOpts)

# %% [markdown]
# Print a summary of the input with truncated vine:

# %%
uq.print(myInput_Truncated)

# %% [markdown]
# Display a visualization of the input model with truncated vine:

# %%
uq.display(myInput_Truncated);

# %% [markdown]
# ## Terminate the remote UQCloud session

# %%
mySession.quit()



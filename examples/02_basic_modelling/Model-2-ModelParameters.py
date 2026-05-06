# %% [markdown]
# # MODEL MODULE: COMPUTATIONAL MODEL PARAMETERS
# 
# This example showcases how to pass parameters in a computational model.

# %% [markdown]
# ## INITIALIZE UQ[PY]LAB
# ### Package imports

# %%
from uqpylab import sessions, display_general, display_util
import numpy as np
import matplotlib.pyplot as plt

# %% [markdown]
# ### Initialize common plotting parameters

# %%
display_util.load_plt_defaults()
uq_colors = display_util.get_uq_color_order()

# %% [markdown]
# ### Start a remote UQCloud session

# %%
# Start the session
mySession = sessions.cloud()
# (Optional) Get a convenient handle to the command line interface
uq = mySession.cli
# Reset the session
mySession.reset()

# %% [markdown]
# ### Set the random seed for reproducibility

# %%
uq.rng(100,'twister');

# %% [markdown]
# ## COMPUTATIONAL MODEL
# 
# The Ishigami function is defined as:
# 
# $$Y(\mathbf{x}) = \sin(x_1) + a \sin^2(x_2) + b x_3^4 \sin(x_1)$$
# 
# where $x_i \in [-\pi, \pi], \; i = 1,2,3$; and $a$ and $b$ are model parameters.
# 
# ### Using a Python script
# 
# This computation is carried out by the function `model` supplied within `ishigami_parametric.py`.The inputs and model parameters of this function are gathered into $N \times M$ list of lists `X` and into a dictionary `P`, respectively; and where $N$ and $M$ are the numbers of realizations and inputs, respectively.
# 
# Specify the function in the options for MODEL object:
# 

# %%
ModelOpts = {
    'Type': 'Model', 
    'ModelFun':'ishigami_parametric.model',
    'isVectorized': True
}

# %% [markdown]
# First, a typical parameter set is chosen, $[a, b] = [7, 0.1]$:

# %%
ModelOpts['Parameters'] = {
    'a': 7,
    'b': 0.1
}

# %% [markdown]
# Create the MODEL object:

# %%
myModel = uq.createModel(ModelOpts)

# %% [markdown]
# ## PROBABILISTIC INPUT MODEL
# 
# The probabilistic input model consists of three independent uniform random variables:
# 
# $$X_i \sim \mathcal{U}(-\pi, \pi), \quad i = 1,2,3$$

# %% [markdown]
# Specify the marginals:

# %%
InputOpts = {
    "Marginals": [
        {"Type": "Uniform",
         "Parameters": [-np.pi, np.pi]
        },
        {"Type": "Uniform",
         "Parameters": [-np.pi, np.pi]
        },
        {"Type": "Uniform",
         "Parameters": [-np.pi, np.pi]
        }
    ]
}

# %% [markdown]
# Create an INPUT object based on the specified marginals:

# %%
myInput = uq.createInput(InputOpts)

# %% [markdown]
# ## COMPARISON OF THE MODEL RESPONSES FOR VARIOUS PARAMETER SETS
# 
# ### Using a fixed parameter set
# 
# Create a validation sample of size $10^4$ from the input model using latin hypercube sampling (LHS):

# %%
X = uq.getSample(Method='LHS', N=1e4)

# %% [markdown]
# Evaluate the corresponding responses of the computational model at the validation sample points:

# %%
Y = uq.evalModel(myModel,X)

# %% [markdown]
# Plot a histogram of the model responses:

# %%
Y_dict = {'Y': Y.squeeze()}
display_general.display_histogram(Y_dict, xaxis_title='Y', yaxis_title='Frequency')

# %% [markdown]
# ### Using different parameter sets
# 
# Create multiple combinations of model parameters values in a matrix:

# %%
parameterValues = [[7, 0.1], [ 7, 0.2], [6, 0.1], [6, 0.2]]
numParameters = len(parameterValues)

# %% [markdown]
# Create the histograms of the model responses for each set of model parameter values by looping through each parameter set:

# %%
fig, axs = plt.subplots(nrows=2, ncols=2)

# adjust the spacing between subplots
fig.subplots_adjust(hspace=0.5, wspace=0.5)

for ii in range(numParameters):
    # Assign the corresponding parameters
    ModelOpts['Parameters'] = {
        'a': parameterValues[ii][0],
        'b': parameterValues[ii][1]
    }

    # Evaluate the computational model's responses
    Y =  uq.evalModel(ModelOpts,X)

    # Plot the histogram of the responses in a separate subplot
    row = ii // 2
    col = ii % 2
    axs[row,col].hist(Y, bins=20, color=uq_colors[ii])
    axs[row,col].set_title(f'a={parameterValues[ii][0]}, b={parameterValues[ii][1]}')

# Set labels for all subplots
for ax in axs.flat:
    ax.set(xlabel='Y', ylabel='Frequency')
plt.show()

# %% [markdown]
# ## Terminate the remote UQCloud session

# %%
mySession.quit()

# %%

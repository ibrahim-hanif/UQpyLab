# %% [markdown]
# # MODEL MODULE: COMPUTATIONAL MODEL DEFINITION
# 
# This example showcases the various ways to define a computational model in UQ[py]Lab using the analytical Ishigami function as the computational model.

# %% [markdown]
# ## INITIALIZE UQ[PY]LAB
# ### Package imports

# %%
from uqpylab import sessions, display_general, display_util
import numpy as np

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
# $$Y(\mathbf{x}) = \sin(x_1) + 7 \sin^2(x_2) + 0.1 x_3^4 \sin(x_1)$$
# 
# where $x_i \in [-\pi, \pi], \; i = 1,2,3.$
# 
# The Model module in UQ[py]Lab offers two ways to define a computational model:
# 
# * using a Python script, and
# * using a string.
# 
# Each of these will be illustrated next to define the Ishigami function as a computational model in UQ[py]Lab. 
# 
# ### Using a Python script
# 
# This computation is carried out by the function `model` supplied within `ishigami.py`. The input parameters of this function are gathered into the vector `X`.
# 
# The function evaluates the inputs given in the $N \times M$ matrix `X`, where $N$ and $M$ are the numbers of realizations and inputs, respectively.
# 
# Specify the `ishigami` function in the options for the MODEL object:
# 

# %%
Model1Opts = {
    'Type': 'Model', 
    'ModelFun':'ishigami.model'
}

# %% [markdown]
# Create the MODEL object:

# %%
myModel_pyFile = uq.createModel(Model1Opts)

# %% [markdown]
# ### Using a function handle
# It is possible to define the `ishigami` function using text strings that are executed on UQCloud, in addition to its existing implementation. To write a function string in UQ[py]Lab, the convention is to represent random variables using the letter `X`. The function strings are interpreted by the `MATLAB` engine on UQCloud.

# %%
Model2Opts = {
    'Type': 'Model', 
    'mString': 'sin(X(:,1)) + 7*(sin(X(:,2)).^2)+ 0.1*(X(:,3).^4).* sin(X(:,1))' 
}

# %% [markdown]
# The `MATLAB` expression in the string is vectorized, hence vectorization can be activated:

# %%
Model2Opts['isVectorized'] = True

# %% [markdown]
# Create the MODEL object:

# %%
myModel_mString = uq.createModel(Model2Opts)

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
# ## COMPARISON OF THE MODELS
# 
# To compare models created using the two different ways, create a sample of size $10^4$ from the input model using the latin hypercube sampling (LHS):

# %%
X = uq.getSample(Method='LHS', N=1e4)

# %% [markdown]
# Evaluate the corresponding responses
#  for each of the two computational models created:

# %%
YmFile = uq.evalModel(myModel_pyFile,X)
YmString = uq.evalModel(myModel_mString,X)

# %% [markdown]
# It can be observed that the results are identical

# %%
Diff_MFileMString = np.max(np.abs(YmFile-YmString))
Diff_MFileMString

# %% [markdown]
# To visually show that the responses are indeed identical, create a histogram of the responses from the different models:

# %%
myColors = display_util.colorOrder()
YmFile_dict = {'YmFile': YmFile.squeeze()}

display_general.display_histogram(YmFile_dict, xaxis_title='Y', yaxis_title='Frequency',title='mFile', color=myColors[0])

# %%
YmString_dict = {'YmString': YmString.squeeze()}
display_general.display_histogram(YmString_dict, xaxis_title='Y', yaxis_title='Frequency',title='mString', color=myColors[3])

# %% [markdown]
# ## Terminate the remote UQCloud session

# %%
mySession.quit()

# %%

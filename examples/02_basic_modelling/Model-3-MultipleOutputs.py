# %% [markdown]
# # MODEL MODULE: MULTIPLE OUTPUTS
# 
# This example showcases the modeling of the deflection of a simply supported beam subjected to a uniform random load at several points along its length.

# %% [markdown]
# ## INITIALIZE UQ[PY]LAB
# ### Package imports

# %%
from uqpylab import sessions, display_util
import numpy as np
import matplotlib.pyplot as plt

# %% [markdown]
# ## Initialize common plotting parameters

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
# The simply supported beam model is shown in the following figure:
# 
# <div>
# <img src="SimplySupportedBeam.png" width="500"/>
# </div>
# 
# 
#%%
from IPython.display import Image
Image(filename='SimplySupportedBeam.png') 

# %% [markdown]
# The (negative) deflection of the beam at any longitudinal coordinate $s$ is given by:
# 
# $$V(s) = -\frac{p \,s (L^3 - 2\, s^2 L + s^3) }{2E b h^3}$$
# 
# This computation is carried out by the function `simply_supported_beam_9points`. The function evaluates the inputs gathered in the $N \times M$ matrix X, where $N$ and $M$ are the numbers of realizations and inputs, respectively. The inputs are given in the following order:
# 
# * $b$: beam width $(m)$
# * $h$: beam height $(m)$
# * $L$: beam length $(m)$
# * $E$: Young's modulus $(Pa)$
# * $p$: uniform load $(N/m)$
# 
# The function returns the beam deflection $V(s_i)$ at nine equally-spaced points along the length $s_i = i \cdot L/10, \; i=1,\ldots,9.$
# 
# Create a MODEL object from the `simply_supported_beam_9points` function:

# %%
ModelOpts = {
    'Type': 'Model',
    'ModelFun': 'simply_supported_beam_9points.model',
    'isVectorized': 'true'
}

myModel = uq.createModel(ModelOpts)

# %% [markdown]
# ## PROBABILISTIC INPUT MODEL
# 
# The simply supported beam model has five independent input parameters modeled by lognormal random variables. The parameters of the distributions are given in the following table:
# 
# |Variable |Description |Distribution |Mean |Std. deviation|
# | --- | :-: | :-: | :-: | -: |
# |b |Beam width |Lognormal|0.15 m| 7.5 mm|
# |h |Beam height|Lognormal |0.3 m |15 mm|
# |L |Length|Lognormal |5 m |50 mm|
# |E|Young modulus|Lognormal|30000 MPa |4500 MPa|
# |p|Uniform load|Lognormal |10 kN/m|2 kN/m|
# 
# Define an INPUT object with the following marginals:

# %%
InputOpts = {
    'Marginals': [
        {
        'Name': 'b', # beam width
        'Type': 'Lognormal',
        'Moments': [0.15, 0.0075] # (m)
        },
        {
        'Name': 'h', # beam height
        'Type': 'Lognormal',
        'Moments': [0.3, 0.015] # (m)
        },
        {
        'Name': 'L', # beam length
        'Type': 'Lognormal',
        'Moments': [5, 0.05] # (m)
        },
        {
        'Name': 'E', # Young's modulus
        'Type': 'Lognormal',
        'Moments': [3e10, 4.5e9] # (Pa)
        },
        {
        'Name': 'p', # uniform load
        'Type': 'Lognormal',
        'Moments': [1e4, 1e3] # (N/m)
        }]
}


# %% [markdown]
# Create an INPUT object based on the specified marginals:

# %%
myInput = uq.createInput(InputOpts)

# %% [markdown]
# ## VISUALIZATION OF MODEL RESPONSES
# 
# Generate 7 sample points:

# %%
N = 7
X = uq.getSample(Method='LHS', N=N)
X.shape

# %% [markdown]
# Evaluate the corresponding computational model responses:

# %%
Y = uq.evalModel(myModel,X)
Y.shape

# %% [markdown]
# The output |Y| is a $N \times N_{out}$ and consists of seven realizations $(N = 7)$, each with $N_{\mathrm{out}} = 9$ values:

# %%
Ysize = Y.shape
Ysize

# %% [markdown]
# The deflections $V(s_i)$ at the nine points are plotted for three realizations of the random inputs. Relative length units are used for comparison, because $L$ is one of the random inputs:

# %%
li = np.arange(0,1.01,0.1)  # use normalized positions

# %% [markdown]
# Loop over the realizations and plot with a different color:

# %%
fig, ax = plt.subplots()

for ii in range(Ysize[0]):
    YY = np.concatenate(([0], Y[ii,:], [0]))
    ax.plot(li, YY, 'x-', color=uq_colors[ii], label=f'Realization {ii+1}')

ax.set_ylim(-0.013, 0.005)
ax.set_xlabel('$\\mathrm{L_{rel}}$ (-)')
ax.set_ylabel('$\\mathrm{V}$ (m)')
ax.legend()
plt.show()

# %% [markdown]
# ## Terminate the remote UQCloud session

# %%
mySession.quit()

# %%

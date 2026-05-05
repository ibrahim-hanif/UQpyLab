# %% [markdown]
# # INPUT MODULE: SAMPLING STRATEGIES
# 
# This example showcases how to define a probabilistic input model and then use it to draw samples using various sampling strategies.

# %% [markdown]
# ## Package imports

# %%
from uqpylab import sessions
import matplotlib.pyplot as plt
from uqpylab.display_util import get_uq_color_order


# %% [markdown]
# ## Parameters

# %%
UQ_colors = get_uq_color_order(4)

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
uq.rng(1, 'twister');

# %% [markdown]
# ## Probabilistic input model
# 
# The probabilistic input model consists of two uniform random variables $$X_i \sim \mathcal{U}(0, 1) \qquad i = 1,2 $$
# Specify the marginals:
# 

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
# Create an INPUT object based on the specified marginals:

# %%
myInput = uq.createInput(InputOpts)

# %% [markdown]
# Print a report on the created INPUT object:

# %%
uq.print(myInput)

# %% [markdown]
# ## Drawing samples
# 
# Different samples from the INPUT object are drawn using various sampling strategies.

# %% [markdown]
# ### 1) Monte Carlo sampling

# %%
X_MC = uq.getSample(N=80, Method='MC')

# %%
fig_mc, ax_mc = plt.subplots()
ax_mc.scatter(X_MC[:,0], X_MC[:,1], color=UQ_colors[0])
ax_mc.set_xlabel("$X_1$")
ax_mc.set_ylabel("$X_2$")
ax_mc.set_title("MCS")
ax_mc.grid()


# %% [markdown]
# ### 2) Latin hypercube sampling

# %%
X_LHS = uq.getSample(N=80, Method='LHS');

# %%
fig_lhs, ax_lhs = plt.subplots()
ax_lhs.scatter(X_LHS[:,0], X_LHS[:,1], color=UQ_colors[1])
ax_lhs.set_xlabel("$X_1$")
ax_lhs.set_ylabel("$X_2$")
ax_lhs.set_title("LHS")
ax_lhs.grid()


# %% [markdown]
# ### 3) Sobol' sequence sampling

# %%
X_Sobol = uq.getSample(N=80, Method='Sobol');

# %%
fig_sobol, ax_sobol = plt.subplots()
ax_sobol.scatter(X_Sobol[:,0], X_Sobol[:,1], color=UQ_colors[2])
ax_sobol.set_xlabel("$X_1$")
ax_sobol.set_ylabel("$X_2$")
ax_sobol.set_title("Sobol")
ax_sobol.grid()

# %% [markdown]
# ### 4) Halton sequence sampling

# %%
X_Halton = uq.getSample(N=80, Method='Halton');

# %%
fig_halton, ax_halton = plt.subplots()
ax_halton.scatter(X_Halton[:,0], X_Halton[:,1], color=UQ_colors[3])
ax_halton.set_xlabel("$X_1$")
ax_halton.set_ylabel("$X_2$")
ax_halton.set_title("Halton")
ax_halton.grid()

# %% [markdown]
# ## Comparison of sampling strategies

# %%
fig_all, axs_all = plt.subplots(2, 2, figsize=(10, 8), layout='constrained')

axs_all[0,0].scatter(X_MC[:,0], X_MC[:,1], color=UQ_colors[0])
axs_all[0,0].set_title("MCS")

axs_all[0,1].scatter(X_LHS[:,0], X_LHS[:,1], color=UQ_colors[1])
axs_all[0,1].set_title("LHS")

axs_all[1,0].scatter(X_Sobol[:,0], X_Sobol[:,1], color=UQ_colors[2])
axs_all[1,0].set_title("Sobol'")

axs_all[1,1].scatter(X_Halton[:,0], X_Halton[:,1], color=UQ_colors[3])
axs_all[1,1].set_title("Halton")

for ax in axs_all.flatten():
    ax.grid()

plt.setp(axs_all[-1, :], xlabel="$X_1$")
plt.setp(axs_all[:, 0],  ylabel="$X_2$")



# %% [markdown]
# ## Terminate the remote UQCloud session

# %%
mySession.quit()



# %%

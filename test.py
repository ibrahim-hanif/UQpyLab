#%%
from uqpylab import sessions
import numpy as np
from access_UQCloud import Endpoint, Token
# %%
# Initialize session with your credentials
mySession = sessions.cloud(host=Endpoint, 
                          token=Token)

# Now you can use UQ[py]Lab features
# Polynomial Chaos Expansions, sensitivity analysis, etc.
# %%

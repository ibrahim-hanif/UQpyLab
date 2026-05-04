#%%
from uqpylab import sessions
from access_UQCloud import Endpoint, Token
# The user's token to access the UQCloud API
# The UQCloud instance to use
#%%​​
# Start the session
mySession = sessions.cloud(host=Endpoint, token=Token)
# (Optional) Get a convenient handle to the command line interface
uq = mySession.cli
# Reset the session
mySession.reset()

# Specify the options for a bivariate normal random vector
InputOpts = {
    'Marginals': [
        {
            'Type': 'Gaussian',
            'Parameters': [0,1]
        },
        {
            'Type': 'Gaussian',
            'Parameters': [0,1]
        }
    ]
}

# Create the bivariate normal random vector
myInput = uq.createInput(InputOpts)

# Draw 10 samples from the bivariate normal distribution
theSamples = uq.getSample(myInput, 10)

# %%[markdown]
# Storing your UQCloud credentials
#%%
mySession.save_config()
# %%
mySession = sessions.cloud()
uq = mySession.cli
mySession.reset()
mySession.quit()
# %%

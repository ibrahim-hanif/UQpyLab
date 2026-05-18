# %% [markdown]
# # RELIABILITY: TIME VARIANCE
# 
# In this example, UQ[py]Lab is used to compute the outcrossing rate $\nu^+$ in a non-stationary time-variant reliability problem using the so-called PHI2 method.
# 
# For details, see:
# Sudret, B. (2008). 
# Analytical derivation of the outcrossing rate in time-variant reliability problems. Structure and Infrastructure Engineering, 4 (5), 353-362 (Section 5). <https://doi.org/10.1080/15732470701270058 DOI:10.1080/15732470701270058>
# 
# 

# %% [markdown]
# ## THEORY
# ### Problem statement
# 
# The limit state function is defined as the difference between a degrading
# resistance $r(t) = R - b\, t$ and a time-varying load $S(t)$:
# 
# $$g(t, R, S) = R-bt-S(t)$$
# 
# where:
# 
# * $R$: the resistance, modeled by a Gaussian random variable
#        of mean value $\mu_R$ and standard deviation $\sigma_R$
# * $b$: (deterministic) deterioration rate of the resistance
# * $t$: time
# * $S(t)$: time-varying stress, which is modeled by a stationary
#           Gaussian process of mean value $\mu_S$,
#           standard deviation $\sigma_S$ and square-exponential
#           autocorrelation function $\rho_S(t) = \exp(- (t/\ell)^2)$
# 
# ### PHI2 Method
# 
# The outcrossing rate from the safe to the failure domain is then defined
# by:
# 
# $$\nu^+(t) =\lim_{\Delta t \rightarrow 0}  \frac{P[(g(t)>0)\cap (g(t+\Delta t)\leq 0)]}{\Delta t}$$
# 
# The limit state functions at two different times can be written as
# $g(t) = R-bt-S_1$ and $g(t+\Delta t) = R-b(t+\Delta t)-S_2$, where the
# two stress variables $S_1$ and $S_2$ are correlated:
# 
# $$\rho_{S_1,S_2} = \exp(- (\Delta t/\ell)^2)$$
# 
# THE PHI2 method solves two FORM analysis at time instant $t$ and
# $t+\Delta t$, then estimates the outcrossing rate from the parallel
# system probability of failure defined above:
# 
# $$\nu^+_{PHI2}(t) = \frac{\Phi_2(\beta(t), -\beta(t+ \Delta t ), -\alpha(t) \cdot \alpha(t+\Delta t))}{\Delta t}$$
# 
# where:
# 
# * $\beta(t)$ (resp. $\beta(t+ \Delta t)$): the time-invariant
#   Hasofer-Lind reliability index at time instant $t$ (resp. $t+ \Delta t$)
# * $\alpha(t)$: unit vector to the design point in the standard
#   normal space.
# 
# ### Analytical reference solution
# 
# According to Sudret (2008), for the example under consideration,
# an analytical expression of the outcrossing rate can be derived:
# 
# $$\nu^+(t) = \omega_0 \Psi\left( \frac{-b}{\omega_0 \sigma_S} \right) \frac{\sigma_S}{\sqrt{\sigma_R^2+\sigma_S^2}}\ \varphi\left(  \frac{\mu_R-bt-\mu_S}{\sqrt{\sigma_R^2+\sigma_S^2}} \right)$$
# 
# where:
# 
# * $\omega_0$ is the cycle rate defined as
#   $\omega_0^2= - \rho_S''(0) = \sqrt{2}/\ell$,
# * $\Psi(x) = \varphi(x) - x \Phi(-x)$, and $\varphi$ and $\Phi$ are
#   the PDF and CDF values of a standard Gaussian variable.
# 
# In this example, pairs of FORM analyses are carried out at different time
# instants so as to compute the outcrossing rate as a function of time.
# The PHI2 solution is compared to the analytical solution.
# Note that another Eq.(41) of Sudret (2008) is implemented
# in this example.
# The more stable Eq. (40) of the same reference could be also used.

# %% [markdown]
# ## INITIALIZE UQ[PY]LAB
# ### Package imports

# %%
from uqpylab import sessions, display_util
import numpy as np
from scipy.stats import norm
from scipy.stats import multivariate_normal as mvn
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
uq.rng(1,'twister');

# %% [markdown]
# ## APPLICATION
# 
# Assume the following:
# 
# * Resistance: $\mu_R=5$, $\sigma_R = 0.3$
# * Stress: $\mu_S = 3$, $\sigma_S = 0.5$
# * Deterioration rate $b=0.01$
# * Time $t$ = [0:1:50], $\Delta t =10^{-3}$
# * Squared exponential correlation model with correlation length of $\ell=10$

# %%
muR, sigmaR = 5, 0.3
muS, sigmaS = 3, 0.5
b = 0.01
t = 0
deltat = 0.001
l = 10

# %% [markdown]
# The assumptions above lead to a correlation between $S_1$ and $S_2$ of

# %%
rho_12 = np.exp(-deltat**2/l**2)
rho_12

# %% [markdown]
# and a cycle rate of 

# %%
omega_0 = np.sqrt(2/l**2)
omega_0

# %% [markdown]
# Then, the analytical outcrossing rate is (Sudret, 2008, Eq.(46)):

# %%
PSI = lambda x: norm.pdf(x) - x* norm.cdf(-x)
v = omega_0 * PSI(-b/(omega_0*sigmaS)) * \
    (sigmaS/np.sqrt(sigmaR**2+sigmaS**2)) * \
    norm.pdf((muR-b*t-muS)/np.sqrt(sigmaR**2+sigmaS**2))
v

# %% [markdown]
# ## PROBABILISTIC INPUT MODEL
# 
# In order to account for the correlation of $S_1$ and $S_2$, define a three-dimensional input vector as follows:

# %%
InputOpts = {
    "Marginals": [
        {"Name": "R",               # Resistance
         "Type": "Gaussian",
         "Moments": [muR, sigmaR]
        },
        {"Name": "S_1",               # Gaussian process at t
         "Type": "Gaussian",
         "Moments": [muS, sigmaS]
        },
        {"Name": "S_2",               # Gaussian process at t+Delta_t
         "Type": "Gaussian",
         "Moments": [muS, sigmaS]
        },        
    ]
}

# %% [markdown]
# The computed correlation coefficient is used:

# %%
InputOpts["Copula"] = {
    "Type": 'Gaussian',
    "Parameters": [[1, 0, 0], [0, 1, rho_12], [0, rho_12, 1]]
}

# %% [markdown]
# Create an INPUT object based on the defined marginals and copula:

# %%
myInput = uq.createInput(InputOpts)

uq.print(myInput)

# %% [markdown]
# ## LIMIT STATE FUNCTION
# 
# The limit state function returns a two-dimensional output related to:
# 
# $$g_1(\mathbf{x}) = R-b\, t - S_1 ,\quad g_2(\mathbf{x}) = R-b\, (t+\Delta t) - S_2$$
# 
# where $\mathbf{x} = \{R, S_1, S_2\}$ is the vector of input variables.
# 
# Define the limit state function using a string
# in a vectorized expression.
# The values of time instants are passed as parameters P(1) and P(2):

# %%
LSOpts = {
    'Type': 'Model',
    'mString': '[(X(:,1)-'+str(b)+'*P(1)-X(:,2)) X(:,1)-'+ str(b)+'*P(2)-X(:,3) ]',
    'Parameters': [t, t+deltat]
}

# %% [markdown]
# Create a MODEL object of the limit state function:

# %%
myLimitState = uq.createModel(LSOpts)

# %% [markdown]
# ## RELIABILITY ANALYSIS
# 
# A FORM analysis is conducted to estimate the two failure probabilities at time instants $t$ and $t+\Delta t$. Note that FORM can carry out several analysis related to each output limit state function in a single call.
# 
# Select FORM as the reliability analysis method:

# %%
FORMOpts = {
    "Type": "Reliability",
    "Method":"FORM"
}

# %% [markdown]
# Run the FORM analysis:

# %%
myFORM = uq.createAnalysis(FORMOpts)

#%%
uq.print(myFORM)
uq.display(myFORM);

# %% [markdown]
# ## ESTIMATION OF THE OUTCROSSING RATE
# 
# Using the same equations as in |Reliability-4-ParallelSystem|, the parallel system failure probability can be estimated as follows:

# %%
betaS1 = myFORM['Results']['BetaHL'][0]
betaS2 = myFORM['Results']['BetaHL'][1]

alpha1 = (-np.array(myFORM['Results']['Ustar'])[:,0] / betaS1).flatten() #(v) TODO: why -ve?
alpha2 =  (np.array(myFORM['Results']['Ustar'])[:,1] / betaS2).flatten()

mu = np.zeros(2)
B = np.array([-betaS1, betaS2]) #(v) TODO: why -ve?
R = np.array([[ 1, alpha1@alpha2],
              [alpha1@alpha2, 1]])
dist = mvn(mean=mu, cov=R)
Pf_FORM = dist.cdf(-B)
Pf_FORM

# %% [markdown]
# And finally, compute the outcrossing rate:

# %%
v_FORM = Pf_FORM / deltat
v_FORM

# %% [markdown]
# ## COMPARISON TO THEORETICAL RESULTS

# %%
print('Outcrossing rate (t=0)')
print('-------------------------------------')
print('Theoretical       : {:11.4e}'.format(v))
print('FORM approximation: {:11.4e}'.format(v_FORM))


# %% [markdown]
# ## EVOLUTION IN TIME OF THE OUTCROSSING RATE
# 
#  Set time varying between $t = 0$ and $t = 50$ and compute the analytical outcrossing rate for each time instant:

# %%
tt = np.arange(0, 51, 1)
vv = omega_0 * PSI(-b/(omega_0*sigmaS)) * \
    (sigmaS/np.sqrt(sigmaR**2+sigmaS**2)) * \
    norm.pdf((muR-b*tt-muS)/np.sqrt(sigmaR**2+sigmaS**2))
# vv

# %% [markdown]
# Use the same limit state function and FORM options as before

# %%
LSiOpts = LSOpts.copy()
FORMiOpts = FORMOpts.copy()
FORMiOpts['Display'] = 0

# %% [markdown]
# Compute the approximated outcrossing rate by the PHI2 method at each time instant:

# %%
# Run FORM at each time instance and compute the outcrossing rate

# Initialize output variable to zeros
vv_FORM = np.zeros((len(tt),1)) 

# Loop over all time steps
for ii in range(len(tt)):
    LSiOpts['Parameters'] = [tt[ii].item(), tt[ii].item()+deltat]  
    myLimitStatei = uq.createModel(LSiOpts)
    myFORMi = uq.createAnalysis(FORMiOpts)
    betaS1i = myFORMi['Results']['BetaHL'][0]
    betaS2i = myFORMi['Results']['BetaHL'][1]
    alpha1i = (-np.array(myFORMi['Results']['Ustar'])[:,0] / betaS1i).flatten()
    alpha2i = (np.array(myFORMi['Results']['Ustar'])[:,1] / betaS2i).flatten()
    mui = np.zeros(2)
    Bi = np.array([-betaS1i, betaS2i])
    Ri = np.array([[1, alpha1i@alpha2i],
                   [alpha1i@alpha2i,1]])
    disti = mvn(mean=mui, cov=Ri)
    Pf_FORMi = disti.cdf(-Bi)
    vv_FORM[ii] = Pf_FORMi / deltat

# %% [markdown]
# Plot the outcrossing rate as a function of time  (analytical versus PHI2 values):

# %%
fontsize=16
plt.plot(tt, vv, '-', linewidth=2, color=uq_colors[0], label='Analytical result')
plt.plot(tt[::2], vv_FORM[::2], 'o', markeredgecolor=uq_colors[1], 
         markerfacecolor=uq_colors[1], markersize=5, label='PHI2 approximation')
plt.xlim([0, 50])
plt.ylim([0, 9e-4])
plt.xticks(np.arange(0,51,10))
plt.yticks(np.arange(0,1e-3,1e-4))
plt.legend(fontsize=fontsize)
plt.xlabel('t',fontsize=fontsize)
plt.ylabel('$\\mathrm{\\nu^+}$',fontsize=fontsize)
plt.tick_params(axis='both', labelsize=fontsize)

# %% [markdown]
# ## TERMINATE THE REMOTE UQCLOUD SESSION

# %%
mySession.quit()

# %%

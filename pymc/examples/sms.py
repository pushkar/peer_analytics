import pymc as pm
from numpy import *
from pymc.Matplot import plot
from pylab import *
from pprint import *

def plot_artificial_sms_dataset():
    tau = pm.rdiscrete_uniform(0, 80)
    alpha = 1./20.
    lambda_1, lambda_2 = pm.rexponential(alpha, 2)
    data = np.r_[pm.rpoisson(lambda_1, tau), pm.rpoisson(lambda_2, 80-tau)]
    plt.bar(np.arange(80), data, color="#348ABD")
    plt.bar(tau - 1, data[tau - 1], color="r", label="user behaviour changed")
    plt.xlim(0, 80)

plt.title("More example of artificial datasets")
for i in range(4):
    plt.subplot(4, 1, i)
    plot_artificial_sms_dataset()

show()

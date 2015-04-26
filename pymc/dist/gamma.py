import scipy.stats as stats
import pymc as pm
import numpy as np
from pymc.Matplot import plot
from pylab import *
from pprint import *

dist = stats.gamma
x = np.linspace(-2, 25, 150)
alpha = (2, 5, 10)
beta = (0.01, 0.01, 0.01)
colors = ["#348ABD", "#A60628", "#7A68A6"]
parameters = zip(alpha, beta, colors)

for _a, _b, _color in parameters:
    plt.plot(x, dist.pdf(x, _a, _b), label="$a = %d,\; b = %.1f$" % (_a, _b), color=_color)
    plt.fill_between(x, dist.pdf(x, _a, _b), color=_color, alpha=.33)

plt.legend(loc="upper right")
plt.xlabel("$x$")
plt.ylabel("density function at $x$")
plt.title("Probability distribution of Gamma Dist");


show()

from pymc import *

with Model() as model:
    x = Normal('x', 1, 1)
    x2 = Potential('x2', -x ** 2)

    start = model.test_point
    h = find_hessian(start)
    step = Metropolis(model.vars, h)


M = MCMC(model)
M.sample(iter=10000, burn=0, thin=1)
plot(M)
show()

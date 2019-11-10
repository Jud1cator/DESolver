import matplotlib.pyplot as plt
from Functions.var18 import Var18
from NumericalMethods.euler import Euler
from NumericalMethods.improved_euler import ImprovedEuler
from NumericalMethods.runge_kutta import RungeKutta
from managers import PlotManager, WidgetManager


x0 = 1
y0 = 0.5
X = 9
h = 1

ivp = Var18(x0, y0, X, h)

pm = PlotManager(ivp)

euler = Euler(ivp)
ieuler = ImprovedEuler(ivp)
rkutta = RungeKutta(ivp)
num_methods = [euler, ieuler, rkutta]

pm.plot_exact()
for nm in num_methods:
    pm.plot_numerical(nm)
pm.plot_errors()

wm = WidgetManager('lightgoldenrodyellow', pm)
wm.show()
plt.text(0.05, 0.3, 'test')
plt.draw()


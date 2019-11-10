import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, TextBox, Button
from NumericalMethods.num_method import NumericalMethod
from Functions.ivp import IVP


class PlotManager:

    def __init__(self, f: IVP):
        self.f = f
        self.plots = []
        self.num_methods = {}
        self.errors = {}

        self.fig = plt.figure()
        plt.subplots_adjust(left=0.25)

        gs = self.fig.add_gridspec(5, 2)
        self.ax_sol = self.fig.add_subplot(gs[:3, :], title='Solutions')
        self.ax_sol.set_ylabel('y')
        self.ax_sol.set_xlabel('x')
        self.ax_err1 = self.fig.add_subplot(gs[3:, 0], title='Local errors')
        self.ax_err1.set_ylabel('error')
        self.ax_err1.set_xlabel('step')
        self.ax_err2 = self.fig.add_subplot(gs[3:, 1], title='Global errors')
        self.ax_err2.set_xlabel('step')

        self.axes = [self.ax_sol, self.ax_err1, self.ax_err2]

        # self.labels = plt.axis([0.05, 0.25, 0.15, 0.05])

        self.fig.tight_layout()

    def plot_exact(self):
        x, y = self.f.solution()
        p, = self.ax_sol.plot(x, y, label='Exact')
        self.plots.append(p)
        return p

    def plot_numerical(self, nm: NumericalMethod):
        x, y = nm.solution()
        p, = self.ax_sol.plot(x, y, label=nm.label)
        self.plots.append(p)
        self.num_methods[nm.label] = nm
        return p

    def plot_errors(self):
        x_exact, y_exact = self.f.solution()
        x = range(len(x_exact))
        for plot in self.plots:
            if plot.get_label() == self.f.label:
                continue
            y1 = abs(y_exact - plot.get_ydata())
            y2 = np.zeros(len(x))
            for i in x[1:]:
                y2[i] = y2[i-1] + y1[i]
            self.errors[plot.get_label()] = (self.ax_err1.plot(x, y1, label=plot.get_label(), c=plot.get_c())[0],
                                             self.ax_err2.plot(x, y2, label=plot.get_label(), c=plot.get_c())[0])


class WidgetManager:
    def __init__(self, color, pm: PlotManager):
        self.pm = pm

        plt.subplots_adjust(left=0.3)

        # Initialize checkboxes

        labels = [str(plot.get_label()) for plot in pm.plots]
        visibility = [plot.get_visible() for plot in pm.plots]
        self.checkboxes = CheckButtons(plt.axes([0.05, 0.75, 0.15, 0.15], facecolor=color, title='Plots'),
                                       labels, visibility)

        def checkbox_update(label):
            index = labels.index(label)
            pm.plots[index].set_visible(not pm.plots[index].get_visible())
            pm.errors[label][0].set_visible(pm.plots[index].get_visible())
            pm.errors[label][1].set_visible(pm.plots[index].get_visible())
            plt.draw()

        self.checkboxes.on_clicked(checkbox_update)

        # Initialize textboxes

        self.x0 = TextBox(plt.axes([0.05, 0.65, 0.15, 0.05], title='Parameters'), label='x0', initial=str(pm.f.x0))
        self.y0 = TextBox(plt.axes([0.05, 0.55, 0.15, 0.05]), label='y0', initial=str(pm.f.y0))
        self.X = TextBox(plt.axes([0.05, 0.45, 0.15, 0.05]), label='X', initial=str(pm.f.X))
        self.h = TextBox(plt.axes([0.05, 0.35, 0.15, 0.05]), label='h', initial=str(pm.f.h))

        self.textboxes = {'x0': self.x0, 'y0': self.y0, 'X' : self.X, 'h': self.h}

        def x0_callback(box):
            def x0_submit(text):
                try:
                    float(text)
                except ValueError:
                    print('x0: Please, enter numerical value')
                    box.set_val(pm.f.x0)
                    return
                if float(text) == 0:
                    print('x0: Function is not defined at x0 = 0. Please, use another value')
                    box.set_val(pm.f.x0)
                    return
                pm.f.x0 = float(text)
                pm.f.pdscnt = -pm.f.x0 / (1 / pm.f.y0 - 1)
            return x0_submit

        def y0_callback(box):
            def y0_submit(text):
                try:
                    float(text)
                except ValueError:
                    print('y0: Please, enter numerical value')
                    box.set_val(pm.f.y0)
                    return
                if float(text) == 0:
                    print('y0: y0 = 0 exists only for trivial solution. Please, use another value')
                    box.set_val(pm.f.y0)
                    return
                pm.f.y0 = float(text)
                pm.f.pdscnt = -pm.f.x0 / (1 / pm.f.y0 - 1)
            return y0_submit

        def X_callback(box):
            def X_submit(text):
                try:
                    float(text)
                except ValueError:
                    print('X: Please, enter numerical value')
                    box.set_val(pm.f.X)
                    return
                if float(text) < pm.f.x0:
                    print('X: Please, enter value greater than ', pm.f.x0)
                    box.set_val(pm.f.X)
                    return
                pm.f.X = float(text)
            return X_submit

        def h_callback(box):
            def h_submit(text):
                try:
                    float(text)
                except ValueError:
                    print('h: Please, enter numerical value')
                    box.set_val(pm.f.h)
                    return
                if float(text) > pm.f.X-pm.f.x0:
                    print('h: It is recommended to use step size less than or equal to ', pm.f.X-pm.f.x0)
                    box.set_val(pm.f.h)
                    return
                pm.f.h = float(text)
            return h_submit

        self.x0.on_submit(x0_callback(self.x0))
        self.y0.on_submit(y0_callback(self.y0))
        self.X.on_submit(X_callback(self.X))
        self.h.on_submit(h_callback(self.h))

        # Initialize button

        self.plot_button = Button(plt.axes([0.05, 0.25, 0.15, 0.05]), color=color, label='Plot')

        def plot_click(self):
            if pm.f.x0 <= 0 <= pm.f.X:
                print('Interval contains discontinuity for first derivative. Please, use another interval')
                return
            if pm.f.x0 <= pm.f.pdscnt <= pm.f.X:
                print('Warning: function has discontinuity at point {0}. Please, change X correspondingly'
                      .format(pm.f.pdscnt))
                return
            print()
            print('Total approximation errors:')
            print()
            for plot in pm.plots:
                if plot.get_visible():
                    flag = True
                    if plot.get_label() == 'Exact':
                        x, y = pm.f.solution()
                    else:
                        x, y = pm.num_methods[plot.get_label()].solution()
                        x_err = range(len(pm.f.get_interval()))
                        y_err1 = abs(pm.f.solution()[1] - y)
                        y_err2 = np.zeros(len(x_err))
                        for i in x_err[1:]:
                            y_err2[i] = y_err2[i - 1] + y_err1[i]
                        pm.errors[plot.get_label()][0].set_data(x_err, y_err1)
                        pm.errors[plot.get_label()][1].set_data(x_err, y_err2)
                        if np.isnan(y_err1[-1]) or y_err1[-1] > pm.f.h:
                            print(plot.get_label() + ': diverged')
                            flag = False
                        else:
                            print(plot.get_label() + ': ' + str(y_err2[-1]))

                    if flag:
                        plot.set_data(x, y)
                    for ax in pm.axes:
                        ax.relim()
                        ax.autoscale_view()
                    plt.draw()

        self.plot_button.on_clicked(plot_click)

    def show(self):
        self.pm.ax_sol.legend()
        for ax in self.pm.axes:
            ax.grid()
        plt.show()

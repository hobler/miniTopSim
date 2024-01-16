import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # hard coded date
    n = np.array([0, 50, 101, 202, 303, 404, 505, 606, 707, 808, 909, 1010, 1111, 1212, 1313, 1414, 1515, 1616, 1717,
                  1818, 1919, 2020, 3030, 4040, 5050, 6060, 7070, 8080, 9090])
    time = np.array([0, 0.0156, 0.0469, 0.1719, 0.391, 0.719, 1.14, 1.625, 2.1719, 2.875, 3.6719, 4.421875, 5.265625,
                     6.296875, 7.4219, 8.61, 10.4219, 11.25, 12.78125, 14.453125, 18.61, 20.953125, 47.265625,
                     72.71875, 107.91, 157.171875, 222.17, 286.17, 352.17])

    # plotting
    fig, axs = plt.subplots(3)
    fig.suptitle("Time of one execution of the deloop() depending on the number of points")

    axs[0].plot(n, time, "orange")

    axs[1].plot(n, time, "b")
    axs[1].semilogx()

    axs[2].plot(n, time, "g")
    axs[2].loglog()

    for ax in axs.flat:
        ax.set(xlabel='Number of points, n', ylabel='time, s')

    for ax in axs.flat:
        ax.label_outer()

    plt.show()

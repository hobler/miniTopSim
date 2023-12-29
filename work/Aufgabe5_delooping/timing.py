import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # hard coded date
    n = np.array([0, 50, 101, 202, 303, 404, 505, 606, 707, 808, 909, 1010, 1111, 1212, 1313, 1414, 1515, 1616, 1717,
                  1818, 1919, 2020, 3030, 4040, 5050, 6060, 7070, 8080, 9090])
    time = np.array([0, 0.0156, 0.0469, 0.1875, 0.5, 0.875, 1.3593, 1.96875, 2.71875, 3.578125, 4.5, 5.421875, 5.890625,
                     6.90625, 8.0625, 9.5, 12.65625, 14.265625, 16.34375, 18.140625, 20.1875, 22.265625, 51.5156,
                     83.453125, 132.59, 190.2343, 257.75, 350.625, 461.75])

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

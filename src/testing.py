import math
import matplotlib.pyplot as plt

num = int(input("num: "))

columns = math.ceil(math.sqrt(num))
base_rows = num // columns
extra_row_columns = num % columns

total_rows = base_rows + (extra_row_columns > 0)

fig, axs = plt.subplots(total_rows, columns)

plot_num = 1
for row in range(base_rows):
    for column in range(columns):
        plt.subplot(total_rows, columns, plot_num) 
        plt.plot([0, 1], [0, 1])
        plot_num += 1
if extra_row_columns > 0:
    for column in range(extra_row_columns):
        plt.subplot(total_rows, columns, plot_num) 
        plt.plot([0, 1], [0, 1])
        plot_num += 1

# remove unused axes
for i in range(plot_num, total_rows*columns + 1):
    fig.delaxes(axs.flatten()[i-1])

plt.show()
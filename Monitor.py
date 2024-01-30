import psutil
import GPUtil
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import os
import pynvml
import configparser

config = configparser.RawConfigParser() #fix that url include %
config.read("config.ini")

pynvml.nvmlInit()
# Initial value
update_count = 1
output_path = "img"
os.makedirs(output_path, exist_ok=True)

# Diagram
x_axis = int(config["Variable"]["x-axis"])
init_range = x_axis

fig, axs = plt.subplots(4, 1, figsize=(10, 8), gridspec_kw={'right': 0.8})  # 4 rows, 1 column
fig.suptitle("CPU and GPU Usage")

axs[0].set(xlim=[0, init_range])  # x-axis range
axs[0].set(ylim=[0, 100], ylabel='%')  # y-axis range
axs[1].set(xlim=[0, init_range])  # x-axis range
axs[1].set(ylim=[0, 100], ylabel='%')  # y-axis range
axs[2].set(xlim=[0, init_range])  # x-axis range
axs[2].set(ylim=[0, 30], ylabel='GB')  # y-axis range
axs[3].set(xlim=[0, init_range])  # x-axis range
axs[3].set(ylim=[0, 100], xlabel='Seconds(s)', ylabel='%')  # y-axis range

# Diagram Initialization
cpu_line, = axs[0].plot([], [], label='CPU Usage', color='blue')
gpu_line, = axs[1].plot([], [], label='GPU CUDA Usage', color='green')
gpu_memory_line, = axs[2].plot([], [], label='GPU Dedicated Memory', color='red')
gpu_decode_line, = axs[3].plot([], [], label='GPU Video Decode', color='orange')

y_cpu_list = deque([0] * init_range)
y_gpu_list = deque([0] * init_range)
y_gpu_mem_list = deque([0] * init_range)
y_gpu_decode_list = deque([0] * init_range)

# Variables to store max CPU usage information
max_cpu_index_temp = 0
max_cpu_value_temp = 0
max_gpu_cuda_index_temp = 0
max_gpu_cuda_value_temp = 0
max_gpu_mem_index_temp = 0
max_gpu_mem_value_temp = 0
max_gpu_decode_index_temp = 0
max_gpu_decode_value_temp = 0

sum_cpu_usage = 0
sum_gpu_usage = 0
sum_gpu_memory = 0
sum_gpu_decode = 0

# Variables to store min CPU usage information
min_cpu_index_temp = 0
min_cpu_value_temp = 100 # Start with a high value

min_gpu_cuda_index_temp = 0
min_gpu_cuda_value_temp = 100  # Start with a high value

min_gpu_mem_index_temp = 0
min_gpu_mem_value_temp = 100  # Start with a high value

min_gpu_decode_index_temp = 0
min_gpu_decode_value_temp = 100  # Start with a high value

# List to store text annotations for min values
min_cpu_annotations = []
min_gpu_cuda_annotations = []
min_gpu_mem_annotations = []
min_gpu_decode_annotations = []

# List to store text annotations
max_cpu_annotations = []
max_gpu_cuda_annotations = []
max_gpu_mem_annotations = []
max_gpu_decode_annotations = []

# List to store text annotations
avg_cpu_annotations = []
avg_gpu_cuda_annotations = []
avg_gpu_mem_annotations = []
avg_gpu_decode_annotations = []

# # Maximize the window
# plt.get_current_fig_manager().window.showMaximized()

def init():
    for line in [cpu_line, gpu_line, gpu_memory_line, gpu_decode_line]:
        line.set_data([], [])
    return cpu_line, gpu_line, gpu_memory_line, gpu_decode_line

def animate(i):
    global update_count, max_cpu_index_temp, max_cpu_value_temp, max_cpu_annotations, \
           max_gpu_cuda_index_temp, max_gpu_cuda_value_temp, max_gpu_cuda_annotations, \
           max_gpu_mem_index_temp, max_gpu_mem_value_temp, max_gpu_decode_index_temp, \
           max_gpu_decode_value_temp, max_gpu_mem_annotations, max_gpu_decode_annotations, \
           min_cpu_index_temp, min_cpu_value_temp, min_cpu_annotations,\
           min_gpu_cuda_index_temp, min_gpu_cuda_value_temp, min_gpu_cuda_annotations,\
           min_gpu_mem_index_temp, min_gpu_mem_value_temp, min_gpu_mem_annotations,\
           min_gpu_decode_index_temp, min_gpu_decode_value_temp, min_gpu_decode_annotations,\
           sum_cpu_usage, sum_gpu_usage, sum_gpu_memory, sum_gpu_decode,\
           avg_cpu_annotations, avg_gpu_cuda_annotations, avg_gpu_mem_annotations, avg_gpu_decode_annotations
                   
    # cpu
    y_cpu_list.popleft()
    cpu_percent = psutil.cpu_percent(None, False)
    y_cpu_list.append(cpu_percent)

    # gpu_usage
    GPUs = GPUtil.getGPUs()
    gpu_usage = GPUs[0].load * 100
    y_gpu_list.popleft()
    y_gpu_list.append(gpu_usage)

    # gpu_memory
    gpu_memory = round(GPUs[0].memoryUsed / 1000, 2)
    #gpu_proportion = round(GPUs[0].memoryUtil * 100, 2)
    y_gpu_mem_list.popleft()
    y_gpu_mem_list.append(gpu_memory)

    # gpu_decode
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    gpu_decode = pynvml.nvmlDeviceGetDecoderUtilization(handle)
    y_gpu_decode_list.popleft()
    y_gpu_decode_list.append(gpu_decode[0])

    # update data
    cpu_line.set_xdata(range(len(y_cpu_list)))
    cpu_line.set_ydata(y_cpu_list)

    gpu_line.set_xdata(range(len(y_gpu_list)))
    gpu_line.set_ydata(y_gpu_list)

    gpu_memory_line.set_xdata(range(len(y_gpu_mem_list)))
    gpu_memory_line.set_ydata(y_gpu_mem_list)

    gpu_decode_line.set_xdata(range(len(y_gpu_decode_list)))
    gpu_decode_line.set_ydata(y_gpu_decode_list)
    

    # Find index of max value in ylist
    max_index_cpu = y_cpu_list.index(max(y_cpu_list))
    max_value_cpu = max(y_cpu_list)
    
    max_index_gpu_cuda = y_gpu_list.index(max(y_gpu_list))
    max_value_gpu_cuda = max(y_gpu_list)
    
    max_index_gpu_mem = y_gpu_mem_list.index(max(y_gpu_mem_list))
    max_value_gpu_mem = max(y_gpu_mem_list)
    
    max_index_gpu_decode = y_gpu_decode_list.index(max(y_gpu_decode_list))
    max_value_gpu_decode = max(y_gpu_decode_list)
    
    # Find index of min value in ylist
    min_index_cpu = y_cpu_list.index(min(y_cpu_list))
    min_value_cpu = min(y_cpu_list)
    
    min_index_gpu_cuda = y_gpu_list.index(min(y_gpu_list))
    min_value_gpu_cuda = min(y_gpu_list)
    
    min_index_gpu_mem = y_gpu_mem_list.index(min(y_gpu_mem_list))
    min_value_gpu_mem = min(y_gpu_mem_list)
    
    min_index_gpu_decode = y_gpu_decode_list.index(min(y_gpu_decode_list))
    min_value_gpu_decode = min(y_gpu_decode_list)
    
    #Find average value
    sum_cpu_usage += cpu_percent
    sum_gpu_usage += gpu_usage
    sum_gpu_memory += gpu_memory
    sum_gpu_decode += gpu_decode[0]
    #sum_gpu_decode += pynvml.nvmlDeviceGetDecoderUtilization(pynvml.nvmlDeviceGetHandleByIndex(0))[0]
    
    average_cpu_usage = round(sum_cpu_usage / update_count, 2)
    average_gpu_usage = round(sum_gpu_usage / update_count, 2)   
    average_gpu_memory = round(sum_gpu_memory / update_count, 2)
    average_gpu_decode = round(sum_gpu_decode / update_count, 2)
    
    # Average CPU Usage
    if (average_cpu_usage > 0):
        for annotation_avg_cpu_usage in avg_cpu_annotations:
            annotation_avg_cpu_usage.remove()
        annotation_avg_cpu_usage = axs[0].annotate(f'Avg CPU Usage: {average_cpu_usage}%',
                                                xy=(min_cpu_index_temp, min_cpu_value_temp),
                                                xytext=(init_range + init_range/100, 40))
        avg_cpu_annotations = [annotation_avg_cpu_usage]
        
    # Average GPU Usage
    if (average_gpu_usage > 0):
        for annotation_avg_gpu_usage in avg_gpu_cuda_annotations:
            annotation_avg_gpu_usage.remove()
        annotation_avg_gpu_usage = axs[1].annotate(f'Avg GPU CUDA Usage: {average_gpu_usage}%',
                                                xy=(min_gpu_cuda_index_temp, max_gpu_cuda_value_temp),
                                                xytext=(init_range + init_range/100, 40))
        avg_gpu_cuda_annotations = [annotation_avg_gpu_usage]
        
    # Average GPU Memory Usage
    if (average_gpu_memory > 0):
        for annotation_avg_gpu_mem_usage in avg_gpu_mem_annotations:
            annotation_avg_gpu_mem_usage.remove()
        annotation_avg_gpu_mem_usage = axs[2].annotate(f'Avg GPU Memory Usage: {average_gpu_memory}GB',
                                                xy=(min_gpu_mem_index_temp, max_gpu_mem_value_temp),
                                                xytext=(init_range + init_range/100, 12))
        avg_gpu_mem_annotations = [annotation_avg_gpu_mem_usage]
        
    # Average GPU Decode Usage
    if (average_gpu_decode > 0):
        for annotation_avg_gpu_decode_usage in avg_gpu_decode_annotations:
            annotation_avg_gpu_decode_usage.remove()
        annotation_avg_gpu_decode_usage = axs[3].annotate(f'Avg GPU CUDA Usage: {average_gpu_decode}%',
                                                xy=(min_gpu_decode_index_temp, max_gpu_decode_value_temp),
                                                xytext=(init_range + init_range/100, 40))
        avg_gpu_decode_annotations = [annotation_avg_gpu_decode_usage]
        
    
    
    # If the current min CPU value is smaller than the stored min value, update the stored values
    non_cpu_zero_values = [value for value in y_cpu_list if value > 0]
    if non_cpu_zero_values:
        min_index_cpu = y_cpu_list.index(min(non_cpu_zero_values))
        min_value_cpu = min(non_cpu_zero_values)
        min_cpu_index_temp = min_index_cpu
        min_cpu_value_temp = min_value_cpu

        # Clear previous annotations
        for annotation_cpu_usage in min_cpu_annotations:
            annotation_cpu_usage.remove()

        # Annotate min value in the plot
        annotation_cpu_usage = axs[0].annotate(f'Min CPU Usage: {min_cpu_value_temp}%',
                                    xy=(min_cpu_index_temp, min_cpu_value_temp),
                                    xytext=(init_range + init_range/100, 20))
        min_cpu_annotations = [annotation_cpu_usage]
        
    # # If the current min GPU value is smaller than the stored min value, update the stored values
    non_gpu_zero_values = [value for value in y_gpu_list if value > 0]
    if non_gpu_zero_values:
        min_index_gpu_cuda = y_gpu_list.index(min(non_gpu_zero_values))
        min_value_gpu_cuda = min(non_gpu_zero_values)
        min_gpu_cuda_index_temp = min_index_gpu_cuda
        min_gpu_cuda_value_temp = min_value_gpu_cuda

        # Clear previous annotations
        for annotation_gpu_cuda_usage in min_gpu_cuda_annotations:
            annotation_gpu_cuda_usage.remove()

        # Annotate min value in the plot
        annotation_gpu_cuda_usage = axs[1].annotate(f'Min GPU CUDA Usage: {round(min_gpu_cuda_value_temp, 2)}%',
                                    xy=(min_gpu_cuda_index_temp, min_gpu_cuda_value_temp),
                                    xytext=(init_range + init_range/100, 20))
        min_gpu_cuda_annotations = [annotation_gpu_cuda_usage]
        
    # # If the current min GPU mem value is smaller than the stored min value, update the stored values
    non_gpu_mem_zero_values = [value for value in y_gpu_mem_list if value > 0]
    if non_gpu_mem_zero_values:
        min_index_gpu_mem = y_gpu_mem_list.index(min(non_gpu_mem_zero_values))
        min_value_gpu_mem = min(non_gpu_mem_zero_values)
        min_gpu_mem_index_temp = min_index_gpu_mem
        min_gpu_mem_value_temp = min_value_gpu_mem

        # Clear previous annotations
        for annotation_gpu_mem_usage in min_gpu_mem_annotations:
            annotation_gpu_mem_usage.remove()

        # Annotate min value in the plot
        annotation_gpu_mem_usage = axs[2].annotate(f'Min GPU Mmeory Usage: {min_gpu_mem_value_temp}GB',
                                    xy=(min_gpu_mem_index_temp, min_gpu_mem_value_temp),
                                    xytext=(init_range + init_range/100, 6))
        min_gpu_mem_annotations = [annotation_gpu_mem_usage]
        
    # # If the current min GPU decode value is smaller than the stored min value, update the stored values
    non_gpu_decode_zero_values = [value for value in y_gpu_decode_list if value > 0]
    if non_gpu_decode_zero_values:
        min_index_gpu_decode = y_gpu_decode_list.index(min(non_gpu_decode_zero_values))
        min_value_gpu_decode = min(non_gpu_decode_zero_values)
        min_gpu_decode_index_temp = min_index_gpu_decode
        min_gpu_decode_value_temp = min_value_gpu_decode

        # Clear previous annotations
        for annotation_gpu_decode_usage in min_gpu_decode_annotations:
            annotation_gpu_decode_usage.remove()

        # Annotate min value in the plot
        annotation_gpu_decode_usage = axs[3].annotate(f'Min GPU Decode Usage: {min_gpu_decode_value_temp}%',
                                    xy=(min_gpu_decode_index_temp, min_gpu_decode_value_temp),
                                    xytext=(init_range + init_range/100, 20))
        min_gpu_decode_annotations = [annotation_gpu_decode_usage]

    # If the current max CPU value is greater than the stored max value, update the stored values
    if max_value_cpu > max_cpu_value_temp:
        max_cpu_index_temp = max_index_cpu
        max_cpu_value_temp = max_value_cpu

        # Clear previous annotations
        for annotation_cpu_usage in max_cpu_annotations:
            annotation_cpu_usage.remove()

        # Annotate max value in the plot
        annotation_cpu_usage = axs[0].annotate(f'Max CPU Usage: {max_cpu_value_temp}%',
                                     xy=(max_cpu_index_temp, max_cpu_value_temp),
                                     xytext=(init_range + init_range/100, 60))
        max_cpu_annotations = [annotation_cpu_usage]
        
    # If the current max GPU value is greater than the stored max value, update the stored values
    if max_value_gpu_cuda > max_gpu_cuda_value_temp:
        max_gpu_cuda_index_temp = max_index_gpu_cuda
        max_gpu_cuda_value_temp = max_value_gpu_cuda

        # Clear previous annotations
        for annotation_gpu_usage in max_gpu_cuda_annotations:
            annotation_gpu_usage.remove()

        # Annotate max value in the plot
        annotation_gpu_usage = axs[1].annotate(f'Max GPU CUDA Usage: {round(max_gpu_cuda_value_temp,2)}%',
                                     xy=(max_gpu_cuda_index_temp, max_gpu_cuda_value_temp),
                                     xytext=(init_range + init_range/100, 60))
        max_gpu_cuda_annotations = [annotation_gpu_usage]
        
    # If the current max GPU memory value is greater than the stored max value, update the stored values
    if max_value_gpu_mem > max_gpu_mem_value_temp:
        max_gpu_mem_index_temp = max_index_gpu_mem
        max_gpu_mem_value_temp = max_value_gpu_mem

        # Clear previous annotations
        for annotation_gpu_mem_usage in max_gpu_mem_annotations:
            annotation_gpu_mem_usage.remove()

        # Annotate max value in the plot
        annotation_gpu_mem_usage = axs[2].annotate(f'Max GPU Memory Usage: {max_gpu_mem_value_temp}GB',
                                     xy=(max_gpu_mem_index_temp, max_gpu_mem_value_temp),
                                     xytext=(init_range + init_range/100, 18))
        max_gpu_mem_annotations = [annotation_gpu_mem_usage]
        
    # If the current max GPU decode value is greater than the stored max value, update the stored values
    if max_value_gpu_decode > max_gpu_decode_value_temp:
        max_gpu_decode_index_temp = max_index_gpu_decode
        max_gpu_decode_value_temp = max_value_gpu_decode

        # Clear previous annotations
        for annotation_gpu_decode_usage in max_gpu_decode_annotations:
            annotation_gpu_decode_usage.remove()

        # Annotate max value in the plot
        annotation_gpu_decode_usage = axs[3].annotate(f'Max GPU Decode Usage: {max_gpu_decode_value_temp}%',
                                     xy=(max_gpu_decode_index_temp, max_gpu_decode_value_temp),
                                     xytext=(init_range + init_range/100, 60))
        max_gpu_decode_annotations = [annotation_gpu_decode_usage]
    
    update_count += 1
    
    if update_count % init_range == 0:
        file_path = os.path.join(output_path, f"combined_plot_{update_count}.png")
        plt.savefig(file_path)
    # Pause to allow the plot to update
    plt.pause(0.01)  
    
    return cpu_line, gpu_line, gpu_memory_line, gpu_decode_line

# Add legends
axs[0].legend(loc='upper left')
axs[1].legend(loc='upper left')
axs[2].legend(loc='upper left')
axs[3].legend(loc='upper left')

# Show the plot
ani = animation.FuncAnimation(fig, animate, init_func=init, repeat=True, frames=init_range, blit=True, interval=config['Variable']['frequency'])
plt.show()
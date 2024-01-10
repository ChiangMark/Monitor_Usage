import GPUtil
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import os

update_count = 0
output_path = "img"
os.makedirs(output_path, exist_ok=True)


# Diagram
fig, ax = plt.subplots()
ax.set(title = "GPU Usage")
ax.set(xlim = [0, 1000], xlabel = 'Times')  # x-axis range
ax.set(ylim = [0, 100], ylabel = '%')  # y-axis range
line, = ax.plot([], [])

# Initialization
y_list = deque([0] * 1000)

def GPU_Animate(i):
    global update_count
    y_list.popleft()  
    GPUs = GPUtil.getGPUs()
    gpu_usage = GPUs[0].load * 100
    y_list.append(gpu_usage) 
    # for i, gpu in enumerate(GPUs):
    #     pass
    # y1_list.append(gpu.load * 100) 
    
    # update data
    line.set_xdata(range(len(y_list)))
    line.set_ydata(y_list)
    update_count += 1
    
    if gpu_usage > 80:
        line.set_color('red')
    else:
        line.set_color('blue')
        
    if update_count % 1000 == 0:
        file1_path = os.path.join(output_path, f"gpu_usage_plot_{update_count}.png")
        plt.savefig(file1_path)
        
    return line,

# result
ani1 = animation.FuncAnimation(fig, GPU_Animate, blit=True)
plt.show()
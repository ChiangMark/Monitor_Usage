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
ax.set(title = "Dedicated GPU Memory")
ax.set(xlim = [0, 10000], xlabel = 'Times')  # x-axis range
ax.set(ylim = [0, 16], ylabel = 'GB')  # y-axis range
line1, = ax.plot([], [])

def snapshot():
    file1_path = os.path.join(output_path, f"gpu_memory_plot_{update_count}.png")
    plt.savefig(file1_path)
    

# Initialization
y_list = deque([0] * 10000)

def GPU_Memory_Animate(i):
    global update_count
    y_list.popleft()  
    GPUs = GPUtil.getGPUs()
    gpu_memory = round(GPUs[0].memoryUsed/1000, 2)
    #gpu_total_memory = round(GPUs[0].memoryTotal/1000, 2)
    gpu_proportion = round(GPUs[0].memoryUtil*100, 2)
    y_list.append(gpu_memory) 
    
    
    # update data
    line1.set_xdata(range(len(y_list)))
    line1.set_ydata(y_list)
    update_count += 1
    
    if gpu_proportion > 80:
        line1.set_color('red')
        snapshot()
        if update_count % 10000 == 0:
            snapshot()
    else:
        line1.set_color('blue')
        if update_count % 10000 == 0:
            snapshot()
        
    return line1,

# result
ani1 = animation.FuncAnimation(fig, GPU_Memory_Animate, blit=True)
plt.show()
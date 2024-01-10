import psutil
import GPUtil
import time

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f'CPU Usage: {cpu_usage}%')

def get_gpu_usage():
    try:
        GPUs = GPUtil.getGPUs()
        for i, gpu in enumerate(GPUs):
            print(f'GPU {i + 1} - GPU Usage: {gpu.load * 100}%')
    except Exception as e:
        print(f'Error getting GPU usage: {e}')
        
def get_gpu_memory_usage():
    try:
        GPUs = GPUtil.getGPUs()
        for i, gpu in enumerate(GPUs):
            print(f'GPU {i + 1} - GPU Memory Used: {gpu.memoryUsed} MB / {gpu.memoryTotal} MB ({gpu.memoryUtil*100:.2f}%)')
    except Exception as e:
        print(f'Error getting GPU memory usage: {e}')

if __name__ == "__main__":
    try:
        while True:
            get_cpu_usage()
            get_gpu_usage()
            get_gpu_memory_usage()
            time.sleep(2)  # 每隔2秒更新一次
    except KeyboardInterrupt:
        print("Monitoring stopped.")
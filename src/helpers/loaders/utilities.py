import torch

def print_gpu_memory_usage():
    allocated_memory = torch.cuda.memory_allocated('cuda') / (1024 ** 2)
    reserved_memory = torch.cuda.memory_reserved('cuda') / (1024 ** 2)
    print(f"Allocated Memory: {allocated_memory:.2f} MB")
    print(f"Reserved Memory: {reserved_memory:.2f} MB")
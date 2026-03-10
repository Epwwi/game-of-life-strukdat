import random

# Insertion Sort
def insertion_sort(arr):
    arr = arr.copy()
    comparisons = 0
    swaps = 0

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                swaps += 1
                j -= 1
            else:
                break

        arr[j + 1] = key

    return arr, comparisons + swaps


# Selection Sort
def selection_sort(arr):
    arr = arr.copy()
    comparisons = 0
    swaps = 0

    n = len(arr)
    for i in range(n):
        min_idx = i

        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j

        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1

    return arr, comparisons + swaps


# Hybrid Sort
def hybridSort(arr, threshold=10):
    if len(arr) <= threshold:
        return insertion_sort(arr)
    else:
        return selection_sort(arr)


# Pengujian
sizes = [50, 100, 500]

print("Size | Hybrid Ops | Insertion Ops | Selection Ops")
print("-----------------------------------------------")

for size in sizes:
    data = [random.randint(1, 1000) for _ in range(size)]

    _, hybrid_ops = hybridSort(data)
    _, insertion_ops = insertion_sort(data)
    _, selection_ops = selection_sort(data)

    print(f"{size:4} | {hybrid_ops:10} | {insertion_ops:13} | {selection_ops:13}")
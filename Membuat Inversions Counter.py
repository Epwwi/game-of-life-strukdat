import time
import random

# --- Bagian A: Pendekatan Brute Force O(n^2) ---
def countInversionsNaive(arr):
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count

# --- Bagian B: Pendekatan Merge Sort O(n log n) ---
def countInversionsSmart(arr):
    # Kita gunakan fungsi pembantu untuk rekursi agar tidak merusak array asli
    temp_arr = [0] * len(arr)
    return _mergeSortAndCount(arr.copy(), temp_arr, 0, len(arr) - 1)

def _mergeSortAndCount(arr, temp_arr, left, right):
    inv_count = 0
    if left < right:
        mid = (left + right) // 2

        # Hitung inversi di bagian kiri, kanan, dan saat proses penggabungan (merge)
        inv_count += _mergeSortAndCount(arr, temp_arr, left, mid)
        inv_count += _mergeSortAndCount(arr, temp_arr, mid + 1, right)
        inv_count += _merge(arr, temp_arr, left, mid, right)
        
    return inv_count

def _merge(arr, temp_arr, left, mid, right):
    i = left    # Indeks awal untuk subarray kiri
    j = mid + 1 # Indeks awal untuk subarray kanan
    k = left    # Indeks awal untuk array hasil merge
    inv_count = 0

    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp_arr[k] = arr[i]
            i += 1
        else:
            # Jika arr[i] > arr[j], maka terjadi inversi.
            # Karena subarray sudah terurut, semua elemen setelah arr[i] 
            # di bagian kiri juga pasti > arr[j].
            temp_arr[k] = arr[j]
            inv_count += (mid - i + 1)
            j += 1
        k += 1

    # Salin sisa elemen jika ada
    while i <= mid:
        temp_arr[k] = arr[i]
        i += 1
        k += 1
    while j <= right:
        temp_arr[k] = arr[j]
        j += 1
        k += 1

    # Kembalikan elemen ke array asli
    for loop_var in range(left, right + 1):
        arr[loop_var] = temp_arr[loop_var]
        
    return inv_count

# --- Fungsi Pengujian dan Pengukuran Waktu ---
def run_test(size):
    test_arr = [random.randint(1, 100000) for _ in range(size)]
    
    print(f"--- Menguji Array Berukuran {size} ---")
    
    # Uji Naive
    start_time = time.time()
    result_naive = countInversionsNaive(test_arr)
    end_time = time.time()
    time_naive = end_time - start_time
    
    # Uji Smart (Merge Sort)
    start_time = time.time()
    result_smart = countInversionsSmart(test_arr)
    end_time = time.time()
    time_smart = end_time - start_time
    
    print(f"Hasil Naive: {result_naive} | Waktu: {time_naive:.4f} detik")
    print(f"Hasil Smart: {result_smart} | Waktu: {time_smart:.4f} detik")
    print(f"Apakah hasil sama? {'YA' if result_naive == result_smart else 'TIDAK'}")
    print("-" * 40)

# Menjalankan pengujian sesuai instruksi
sizes = [1000, 5000, 10000]
for s in sizes:
    run_test(s)
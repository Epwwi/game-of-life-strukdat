"""
AdvancedSorter - Implementasi lengkap sesuai Bab 12
"""
import math
from typing import List, Optional

class ListNode:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class AdvancedSorter:
    def __init__(self):
        pass

    # =========================================================
    # 1. ARRAY MERGE SORT (Virtual Sublists + Single tmpArray)
    # =========================================================
    def sort_array(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr
        tmp_array = [0] * len(arr)  # Single temporary array - hanya 1 kali alokasi
        self._rec_merge_sort(arr, 0, len(arr) - 1, tmp_array)
        return arr

    def _rec_merge_sort(self, arr, first, last, tmp_array):
        if first >= last:
            return
        mid = (first + last) // 2
        # Rekursi pada sublist kiri
        self._rec_merge_sort(arr, first, mid, tmp_array)
        # Rekursi pada sublist kanan
        self._rec_merge_sort(arr, mid + 1, last, tmp_array)
        # Gabungkan dua virtual sublist yang sudah terurut
        self._merge_virtual(arr, first, mid, last, tmp_array)

    def _merge_virtual(self, arr, left_start, mid, right_end, tmp_array):
        """
        Penggabungan dua virtual sublist yang bersebelahan.
        Virtual sublist kiri : arr[left_start..mid]
        Virtual sublist kanan: arr[mid+1..right_end]
        Operasi STABLE: jika sama, ambil dari kiri terlebih dahulu (<=)
        """
        a = left_start      # indeks untuk sublist kiri
        b = mid + 1         # indeks untuk sublist kanan
        m = 0               # indeks untuk tmp_array

        # Gabungkan dua sublist sampai salah satu habis
        while a <= mid and b <= right_end:
            # STABLE: gunakan <= agar elemen bernilai sama dari kiri diambil dulu
            if arr[a] <= arr[b]:
                tmp_array[m] = arr[a]
                a += 1
            else:
                tmp_array[m] = arr[b]
                b += 1
            m += 1

        # Sisa sublist kiri (jika ada)
        while a <= mid:
            tmp_array[m] = arr[a]
            a += 1
            m += 1

        # Sisa sublist kanan (jika ada)
        while b <= right_end:
            tmp_array[m] = arr[b]
            b += 1
            m += 1

        # Salin kembali hasil dari tmp_array ke arr
        for i in range(right_end - left_start + 1):
            arr[left_start + i] = tmp_array[i]

    # =========================================================
    # 2. LINKED LIST MERGE SORT (Fast-Slow + Dummy Merge)
    # =========================================================
    def sort_linked_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Base case: list kosong atau hanya 1 node
        if head is None or head.next is None:
            return head

        # Split menggunakan fast-slow pointer
        right_head = self._split_linked_list(head)
        left_head = head

        # Rekursi pada kedua sublist
        left_sorted = self.sort_linked_list(left_head)
        right_sorted = self.sort_linked_list(right_head)

        # Gabungkan dua sublist yang sudah terurut
        return self._merge_linked_lists(left_sorted, right_sorted)

    def _split_linked_list(self, head: ListNode) -> Optional[ListNode]:
        """
        Temukan titik tengah menggunakan teknik fast-slow pointer.
        midPoint bergerak 1 langkah, curNode bergerak 2 langkah.
        Ketika curNode mencapai akhir, midPoint berada di tengah.
        Hanya perlu SATU traversal - O(n) tanpa menghitung panjang.
        """
        midPoint = head          # bergerak lambat (1 langkah)
        curNode = head.next      # bergerak cepat (2 langkah)

        # Loop: curNode bergerak 2x lebih cepat dari midPoint
        while curNode is not None and curNode.next is not None:
            midPoint = midPoint.next
            curNode = curNode.next.next

        # midPoint sekarang berada di node tengah (akhir sublist kiri)
        right_head = midPoint.next   # simpan head sublist kanan
        midPoint.next = None         # putus link - pisahkan dua sublist

        return right_head

    def _merge_linked_lists(self, listA: Optional[ListNode], listB: Optional[ListNode]) -> Optional[ListNode]:
        """
        Gabungkan dua sorted linked list menggunakan dummy node & tail reference.
        - dummy node: eliminasi special case untuk node pertama
        - tail reference: append O(1) tanpa traversal
        - STABLE: jika sama, ambil dari listA terlebih dahulu (<=)
        - Tidak ada alokasi node baru (kecuali 1 dummy node statis)
        """
        # Dummy node: node sementara untuk menyederhanakan logika
        dummy = ListNode(0)
        tail = dummy  # tail selalu menunjuk ke node terakhir

        # Gabungkan sampai salah satu list habis
        while listA is not None and listB is not None:
            # STABLE: jika sama, ambil dari listA dulu
            if listA.data <= listB.data:
                tail.next = listA
                listA = listA.next
            else:
                tail.next = listB
                listB = listB.next
            tail = tail.next
            tail.next = None  # putus link lama untuk keamanan

        # Sambungkan sisa yang masih ada (tanpa loop - O(1))
        if listA is not None:
            tail.next = listA
        else:
            tail.next = listB

        # dummy.next adalah head dari list hasil (dummy tidak masuk list final)
        return dummy.next

    # =========================================================
    # 3. QUICK SORT PARTITION (Median-of-Three Pivot)
    # =========================================================
    def partition_quick(self, arr: List[int], first: int, last: int) -> int:
        """
        Pilih pivot menggunakan Median-of-Three:
        Bandingkan arr[first], arr[mid], arr[last]
        Tukar median ke posisi 'first' sebagai pivot
        
        Catatan: Quick Sort inherently unstable karena swap jarak jauh.
        Untuk stabilitas penuh, gunakan Merge Sort.
        """
        mid = (first + last) // 2

        # Urutkan arr[first], arr[mid], arr[last] agar median ke arr[first]
        # Langkah 1: pastikan arr[first] <= arr[mid]
        if arr[first] > arr[mid]:
            arr[first], arr[mid] = arr[mid], arr[first]
        # Langkah 2: pastikan arr[first] <= arr[last]
        if arr[first] > arr[last]:
            arr[first], arr[last] = arr[last], arr[first]
        # Langkah 3: pastikan arr[mid] <= arr[last]
        if arr[mid] > arr[last]:
            arr[mid], arr[last] = arr[last], arr[mid]
        # Sekarang arr[mid] adalah median, tukar ke posisi first sebagai pivot
        arr[first], arr[mid] = arr[mid], arr[first]

        # Logika partisi standar (dari Listing 12.5)
        pivot = arr[first]
        left = first + 1
        right = last

        while left <= right:
            # Cari elemen pertama >= pivot dari kiri
            while left <= right and arr[left] < pivot:
                left += 1
            # Cari elemen pertama < pivot dari kanan
            while right >= left and arr[right] >= pivot:
                right -= 1
            # Tukar jika belum selesai
            if left < right:
                arr[left], arr[right] = arr[right], arr[left]

        # Tempatkan pivot di posisi finalnya
        if right != first:
            arr[first], arr[right] = arr[right], arr[first]

        return right  # posisi pivot setelah partisi

    def quick_sort_recursive(self, arr: List[int], first: int, last: int, depth: int = 0):
        """Quick Sort dengan fallback ke Merge Sort jika kedalaman rekursi berlebihan."""
        if first >= last:
            return

        n = last - first + 1
        max_depth = int(2 * math.log2(max(n, 2)))

        # Fallback ke Merge Sort jika kedalaman rekursi melebihi 2*log2(n)
        if depth > max_depth:
            sub_arr = arr[first:last+1]
            self.sort_array(sub_arr)
            arr[first:last+1] = sub_arr
            return

        pos = self.partition_quick(arr, first, last)
        self.quick_sort_recursive(arr, first, pos - 1, depth + 1)
        self.quick_sort_recursive(arr, pos + 1, last, depth + 1)


# =========================================================
# TEST SUITE
# =========================================================
def list_to_linked(lst):
    if not lst:
        return None
    head = ListNode(lst[0])
    cur = head
    for val in lst[1:]:
        cur.next = ListNode(val)
        cur = cur.next
    return head

def linked_to_list(head):
    result = []
    while head:
        result.append(head.data)
        head = head.next
    return result

def run_tests():
    sorter = AdvancedSorter()
    
    # Test 1: Array Merge Sort
    print("=" * 60)
    print("TEST 1: Array Merge Sort (Virtual + Single tmpArray)")
    print("=" * 60)
    test_cases = [
        [10, 23, 51, 18, 4, 31, 13, 5],
        [5, 4, 3, 2, 1],  # descending
        [1, 2, 3, 4, 5],  # already sorted
        [3, 3, 3, 1, 2],  # duplicates (stability test)
        [42],              # single element
        [],                # empty
    ]
    for tc in test_cases:
        original = tc.copy()
        result = sorter.sort_array(tc)
        expected = sorted(original)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"  {status}: {original} → {result}")

    # Test 2: Linked List Merge Sort
    print("\n" + "=" * 60)
    print("TEST 2: Linked List Merge Sort (Fast-Slow + Dummy)")
    print("=" * 60)
    ll_tests = [
        [23, 51, 2, 18, 4, 31],
        [5, 4, 3, 2, 1],
        [1],
        [],
        [3, 3, 1, 2, 3],  # duplicates
    ]
    for tc in ll_tests:
        head = list_to_linked(tc)
        sorted_head = sorter.sort_linked_list(head)
        result = linked_to_list(sorted_head)
        expected = sorted(tc)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"  {status}: {tc} → {result}")

    # Test 3: Quick Sort dengan Median-of-Three
    print("\n" + "=" * 60)
    print("TEST 3: Quick Sort Median-of-Three (dengan Fallback)")
    print("=" * 60)
    qs_tests = [
        [10, 23, 51, 18, 4, 31, 13, 5],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],  # worst case untuk naive QS
        [1, 2, 3, 4, 5, 6, 7, 8, 9],  # already sorted
        [42],
    ]
    for tc in qs_tests:
        original = tc.copy()
        sorter.quick_sort_recursive(tc, 0, len(tc)-1)
        expected = sorted(original)
        status = "✓ PASS" if tc == expected else "✗ FAIL"
        print(f"  {status}: {original} → {tc}")

    print("\n✓ Semua test selesai!")

run_tests()

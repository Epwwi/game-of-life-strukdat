"""
ExprHeapSorter - Implementasi lengkap sesuai Bab 13
"""
from typing import List, Optional
from collections import deque

class ExprHeapSorter:
    def __init__(self, expr_str: str):
        self.expr = expr_str
        self.values = []

    def parse_and_evaluate(self) -> int:
        """Membangun pohon ekspresi, mengevaluasi, mengembalikan nilai integer."""
        tokens = deque(self.expr.replace(' ', ''))
        root = self._build_tree(tokens)
        result = self._eval_tree(root)
        return result

    def _build_tree(self, tokens: deque) -> Optional[dict]:
        """
        Implementasi rekursif sesuai Listing 13.9.
        Node: {'val': operator/operand, 'left': node, 'right': node}
        
        Aturan:
        - '(' → buat node kiri (rekursi), ambil operator, buat node kanan (rekursi), ambil ')'
        - operand (digit/huruf) → return node leaf
        """
        if not tokens:
            return None

        token = tokens.popleft()

        if token == '(':
            # Buat node kosong sementara
            node = {'val': None, 'left': None, 'right': None}
            # Bangun subpohon kiri
            node['left'] = self._build_tree(tokens)
            # Token berikutnya adalah operator
            node['val'] = tokens.popleft()
            # Bangun subpohon kanan
            node['right'] = self._build_tree(tokens)
            # Ambil dan buang ')'
            tokens.popleft()
            return node
        else:
            # token adalah operand (digit atau variabel)
            return {'val': token, 'left': None, 'right': None}

    def _eval_tree(self, node: Optional[dict]):
        """
        Evaluasi postorder (kiri → kanan → root).
        Leaf node: kembalikan nilai integer.
        Interior node: evaluasi operasi aritmetika.
        """
        if node is None:
            return 0

        # Leaf node: berisi operand
        if node['left'] is None and node['right'] is None:
            try:
                return int(node['val'])
            except ValueError:
                raise ValueError(f"Token tidak valid: '{node['val']}'")

        # Interior node: evaluasi kedua subtree terlebih dahulu (postorder)
        left_val = self._eval_tree(node['left'])
        right_val = self._eval_tree(node['right'])

        # Lakukan operasi berdasarkan operator
        op = node['val']
        if op == '+':
            return left_val + right_val
        elif op == '-':
            return left_val - right_val
        elif op == '*':
            return left_val * right_val
        elif op == '/':
            if right_val == 0:
                raise ValueError("Division by zero!")
            return left_val // right_val  # integer division
        elif op == '%':
            if right_val == 0:
                raise ValueError("Modulo by zero!")
            return left_val % right_val
        else:
            raise ValueError(f"Operator tidak dikenal: '{op}'")

    def heapsort_inplace(self, arr: List[int]) -> List[int]:
        """Mengurutkan array secara ascending menggunakan in-place heapsort."""
        n = len(arr)
        if n <= 1:
            return arr

        # FASE 1: Bangun max-heap in-place (dari daun ke atas)
        # Mulai dari node interior terakhir (index n//2 - 1) sampai root (index 0)
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(arr, n, i)

        # FASE 2: Ekstrak nilai terbesar satu per satu
        for end in range(n - 1, 0, -1):
            # Swap root (max) dengan elemen terakhir
            arr[0], arr[end] = arr[end], arr[0]
            # Sift-down root pada heap yang ukurannya berkurang 1
            self._sift_down(arr, end, 0)

        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int):
        """
        Implementasi sift-down berdasarkan Listing 13.10 & 13.12.
        Rumus: left = 2*idx+1, right = 2*idx+2
        Swap dengan anak terbesar jika anak > parent, lalu rekursi ke bawah.
        """
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            largest = idx  # asumsikan root adalah yang terbesar

            # Cek apakah anak kiri lebih besar dari current largest
            if left < heap_size and arr[left] > arr[largest]:
                largest = left

            # Cek apakah anak kanan lebih besar dari current largest
            if right < heap_size and arr[right] > arr[largest]:
                largest = right

            # Jika largest sudah di posisi yang benar, hentikan
            if largest == idx:
                break

            # Tukar dan lanjutkan sift-down ke bawah
            arr[idx], arr[largest] = arr[largest], arr[idx]
            idx = largest  # pindah ke posisi anak yang ditukar

    def is_complete_tree(self, arr: List[int]) -> bool:
        """
        Validasi apakah array memenuhi properti complete binary tree.
        
        Dalam complete binary tree yang dipetakan ke array:
        - Semua elemen indeks 0..n-1 harus terisi tanpa "lubang"
        - Setelah menemukan node pertama yang tidak memiliki 2 anak penuh,
          semua node berikutnya harus merupakan leaf node.
        
        Untuk array biasa dengan n elemen, properti ini selalu terpenuhi
        karena tidak ada "gap" dalam pengisian indeks 0..n-1.
        """
        n = len(arr)
        if n == 0:
            return True

        # Cek: setiap node internal harus memiliki anak yang valid
        # Node pada indeks i memiliki anak kiri di 2i+1 dan kanan di 2i+2
        found_incomplete = False
        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2

            if left >= n and right < n:
                # Ada anak kanan tapi tidak ada anak kiri - TIDAK VALID
                return False

            if found_incomplete:
                # Setelah node incomplete pertama, semua berikutnya harus leaf
                if left < n:
                    return False
            
            if left < n and right >= n:
                # Node ini hanya memiliki anak kiri (node incomplete)
                found_incomplete = True

        return True

    def _inorder_to_string(self, node, result):
        """Helper untuk menampilkan pohon ekspresi."""
        if node is None:
            return
        if node['left'] is None and node['right'] is None:
            result.append(str(node['val']))
            return
        result.append('(')
        self._inorder_to_string(node['left'], result)
        result.append(str(node['val']))
        self._inorder_to_string(node['right'], result)
        result.append(')')

    def _postorder_to_string(self, node, result):
        """Postorder traversal menghasilkan notasi postfix."""
        if node is None:
            return
        self._postorder_to_string(node['left'], result)
        self._postorder_to_string(node['right'], result)
        result.append(str(node['val']))


# =========================================================
# TEST SUITE BAB 13
# =========================================================
def run_tests_bab13():
    print("=" * 60)
    print("TEST BAB 13: ExprHeapSorter")
    print("=" * 60)

    # Test 1: Expression Tree Evaluation
    print("\n--- Test 1: Expression Tree Builder & Evaluator ---")
    test_exprs = [
        ("(5+8)", 13),
        ("((8*5)+(9/(7-4)))", 43),  # dari bab 13: 8*5=40, 7-4=3, 9/3=3, 40+3=43
        ("((2*7)+8)", 22),
        ("(9+3)", 12),
    ]
    for expr, expected in test_exprs:
        try:
            sorter = ExprHeapSorter(expr)
            result = sorter.parse_and_evaluate()
            status = "✓ PASS" if result == expected else f"✗ FAIL (expected {expected})"
            print(f"  {status}: {expr} = {result}")
        except Exception as e:
            print(f"  ✗ ERROR: {expr} → {e}")

    # Test Division by zero
    print("\n  Division by zero test:")
    try:
        sorter = ExprHeapSorter("(5/0)")
        sorter.parse_and_evaluate()
        print("  ✗ FAIL: Should have raised exception")
    except ValueError as e:
        print(f"  ✓ PASS: Correctly caught: {e}")

    # Test 2: In-Place Heapsort
    print("\n--- Test 2: Heapsort In-Place ---")
    heapsort_tests = [
        [10, 51, 2, 18, 4, 31, 13, 5, 23, 64, 29],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [5],
        [],
        [3, 3, 1, 2, 3],
    ]
    sorter = ExprHeapSorter("(1+1)")
    for tc in heapsort_tests:
        original = tc.copy()
        result = sorter.heapsort_inplace(tc)
        expected = sorted(original)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"  {status}: {original} → {result}")

    # Test 3: Complete Tree Validator
    print("\n--- Test 3: Complete Binary Tree Validator ---")
    ct_tests = [
        ([1, 2, 3, 4, 5, 6, 7], True),    # perfect complete tree
        ([1, 2, 3, 4, 5, 6], True),         # complete tree (last level partial)
        ([1, 2, 3, 4, 5], True),
        ([1], True),
        ([], True),
    ]
    for arr, expected in ct_tests:
        result = sorter.is_complete_tree(arr)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"  {status}: {arr} → complete={result}")

    # Test 4: Postorder traversal menghasilkan postfix
    print("\n--- Test 4: Postorder = Postfix Notation ---")
    sorter_ex = ExprHeapSorter("((8*5)+(9/(7-4)))")
    tokens = deque("((8*5)+(9/(7-4)))".replace(' ', ''))
    tree = sorter_ex._build_tree(tokens)
    
    postfix = []
    sorter_ex._postorder_to_string(tree, postfix)
    print(f"  Ekspresi  : ((8*5)+(9/(7-4)))")
    print(f"  Postfix   : {' '.join(postfix)}")
    print(f"  (Diharapkan: 8 5 * 9 7 4 - / +)")
    
    infix = []
    sorter_ex._inorder_to_string(tree, infix)
    print(f"  Infix     : {''.join(infix)}")

    print("\n✓ Semua test Bab 13 selesai!")

from collections import deque
run_tests_bab13()

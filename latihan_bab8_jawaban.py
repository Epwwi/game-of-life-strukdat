# ============================================================
#  LATIHAN BAB 8 — JAWABAN LENGKAP
#  Soal 4: Implementasi metode _handleArrival, _handleBeginService,
#           _handleEndService pada TicketCounterSimulation
#  Soal 5: Versi detik + tabel eksperimen
#  Soal 6: Fungsi reverseQueue
# ============================================================

import random


# ------------------------------------------------------------------
# Queue ADT (linked-list based, O(1) enqueue & dequeue)
# ------------------------------------------------------------------
class _Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def enqueue(self, item):
        node = _Node(item)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self):
        assert not self.isEmpty(), "dequeue dari queue kosong"
        data = self._head.data
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return data

    def isEmpty(self):
        return self._size == 0

    def __len__(self):
        return self._size


# ------------------------------------------------------------------
# Array (fixed-size)
# ------------------------------------------------------------------
class Array:
    def __init__(self, size):
        self._data = [None] * size
        self.size = size

    def __getitem__(self, idx):
        return self._data[idx]

    def __setitem__(self, idx, val):
        self._data[idx] = val

    def __iter__(self):
        return iter(self._data)


# ------------------------------------------------------------------
# TicketAgent dan Passenger
# ------------------------------------------------------------------
class Passenger:
    def __init__(self, arriveTime):
        self._arriveTime = arriveTime

    def timeArrived(self):
        return self._arriveTime


class TicketAgent:
    def __init__(self, idNum):
        self._idNum = idNum
        self._passenger = None   # None → agen idle
        self._stopTime = 0

    def isFree(self):
        return self._passenger is None

    def isFinished(self, curTime):
        return (self._passenger is not None) and (self._stopTime == curTime)

    def startService(self, passenger, stopTime):
        self._passenger = passenger
        self._stopTime = stopTime

    def stopService(self):
        passenger = self._passenger
        self._passenger = None
        return passenger


# ============================================================
# SOAL 4: Implementasi metode yang tersisa (versi MENIT)
# ============================================================
class TicketCounterSimulation:
    """Simulasi antrian loket tiket (satuan: menit)."""

    def __init__(self, numAgents, numMinutes, betweenTime, serviceTime):
        self._arriveProb = 1.0 / betweenTime
        self._serviceTime = serviceTime
        self._numMinutes = numMinutes

        self._passengerQ = Queue()
        self._theAgents = Array(numAgents)
        for i in range(numAgents):
            self._theAgents[i] = TicketAgent(i + 1)

        self._totalWaitTime = 0
        self._numPassengers = 0

    def run(self):
        for curTime in range(self._numMinutes + 1):
            self._handleArrival(curTime)
            self._handleBeginService(curTime)
            self._handleEndService(curTime)

    def printResults(self):
        numServed = self._numPassengers - len(self._passengerQ)
        if numServed == 0:
            avgWait = 0.0
        else:
            avgWait = float(self._totalWaitTime) / numServed
        print("")
        print("Number of passengers served =", numServed)
        print("Number of passengers remaining in line = %d" % len(self._passengerQ))
        print("The average wait time was %4.2f minutes." % avgWait)
        return numServed, len(self._passengerQ), avgWait

    # --- Aturan #1: Kedatangan penumpang ---
    def _handleArrival(self, curTime):
        """Setiap menit, penumpang datang dengan probabilitas arriveProb."""
        if random.random() <= self._arriveProb:
            passenger = Passenger(curTime)
            self._passengerQ.enqueue(passenger)
            self._numPassengers += 1

    # --- Aturan #2: Mulai pelayanan ---
    def _handleBeginService(self, curTime):
        """Jika ada agen idle dan antrian tidak kosong, mulai layani penumpang."""
        for agent in self._theAgents:
            if agent.isFree() and not self._passengerQ.isEmpty():
                passenger = self._passengerQ.dequeue()
                agent.startService(passenger, curTime + self._serviceTime)
                self._totalWaitTime += curTime - passenger.timeArrived()

    # --- Aturan #3: Selesai pelayanan ---
    def _handleEndService(self, curTime):
        """Jika agen selesai melayani, bebaskan agen tersebut."""
        for agent in self._theAgents:
            if agent.isFinished(curTime):
                agent.stopService()


# ============================================================
# SOAL 5: Versi DETIK + tabel eksperimen
# ============================================================
class TicketCounterSimulationSec:
    """
    Modifikasi TicketCounterSimulation agar menggunakan satuan DETIK.
    Parameter:
        numAgents    : jumlah agen (loket)
        numSeconds   : durasi simulasi dalam detik
        betweenTime  : rata-rata jarak kedatangan (detik)
        serviceTime  : waktu pelayanan per penumpang (detik)
    """

    def __init__(self, numAgents, numSeconds, betweenTime, serviceTime):
        self._arriveProb = 1.0 / betweenTime
        self._serviceTime = serviceTime
        self._numSeconds = numSeconds

        self._passengerQ = Queue()
        self._theAgents = Array(numAgents)
        for i in range(numAgents):
            self._theAgents[i] = TicketAgent(i + 1)

        self._totalWaitTime = 0
        self._numPassengers = 0

    def run(self):
        for curTime in range(self._numSeconds + 1):
            self._handleArrival(curTime)
            self._handleBeginService(curTime)
            self._handleEndService(curTime)

    def printResults(self, unit="seconds"):
        numServed = self._numPassengers - len(self._passengerQ)
        avgWait = float(self._totalWaitTime) / numServed if numServed else 0.0
        print("")
        print("Number of passengers served =", numServed)
        print("Number of passengers remaining in line = %d" % len(self._passengerQ))
        print("The average wait time was %4.2f %s." % (avgWait, unit))
        return numServed, len(self._passengerQ), avgWait

    def _handleArrival(self, curTime):
        if random.random() <= self._arriveProb:
            self._passengerQ.enqueue(Passenger(curTime))
            self._numPassengers += 1

    def _handleBeginService(self, curTime):
        for agent in self._theAgents:
            if agent.isFree() and not self._passengerQ.isEmpty():
                p = self._passengerQ.dequeue()
                agent.startService(p, curTime + self._serviceTime)
                self._totalWaitTime += curTime - p.timeArrived()

    def _handleEndService(self, curTime):
        for agent in self._theAgents:
            if agent.isFinished(curTime):
                agent.stopService()


def runExperimentSec():
    """Jalankan eksperimen seperti Tabel 8.1 tetapi dalam satuan detik."""
    configs = [
        # (numSeconds, numAgents, serviceTime, betweenTime)
        (6000,  2, 180, 120),
        (30000, 2, 180, 120),
        (60000, 2, 180, 120),
        (6000,  2, 240, 120),
        (30000, 2, 240, 120),
        (60000, 2, 240, 120),
        (6000,  3, 240, 120),
        (30000, 3, 240, 120),
        (60000, 3, 240, 120),
    ]

    print("\n{'Num Sec':>10} {'Num Agents':>10} {'Svc (s)':>8} "
          "{'Between':>8} {'Avg Wait':>10} {'Served':>8} {'Remain':>8}")
    print("-" * 68)
    random.seed(42)
    for numSec, agents, svc, btw in configs:
        sim = TicketCounterSimulationSec(agents, numSec, btw, svc)
        sim.run()
        served, remain, avgWait = sim.printResults.__func__(sim, "seconds")
        # print baris tabel tanpa panggil printResults agar rapi
        print(f"{numSec:>10} {agents:>10} {svc:>8} {btw:>8} "
              f"{avgWait:>10.2f} {served:>8} {remain:>8}")


# ============================================================
# SOAL 6: Fungsi reverseQueue
# ============================================================
def reverseQueue(q):
    """
    Membalik urutan item dalam queue.
    Hanya menggunakan operasi Queue ADT (enqueue, dequeue, isEmpty, len).
    Struktur data tambahan yang dibolehkan: Python list sebagai stack.

    Algoritma:
        1. Pindahkan semua item dari queue ke stack (list).
        2. Pop stack (LIFO) lalu enqueue kembali ke queue → urutan terbalik.

    Kompleksitas: O(n) waktu, O(n) ruang.
    """
    stack = []
    # Langkah 1: kosongkan queue ke stack
    while not q.isEmpty():
        stack.append(q.dequeue())
    # Langkah 2: masukkan kembali dalam urutan terbalik
    while stack:
        q.enqueue(stack.pop())
    return q   # kembalikan queue yang sama (in-place)


# ------------------------------------------------------------------
# Demo / pengujian
# ------------------------------------------------------------------
if __name__ == "__main__":
    random.seed(0)

    print("=" * 60)
    print("SOAL 4 — Simulasi loket tiket (satuan menit)")
    print("=" * 60)
    sim = TicketCounterSimulation(
        numAgents=2, numMinutes=100, betweenTime=2, serviceTime=3
    )
    sim.run()
    sim.printResults()

    print("\n" + "=" * 60)
    print("SOAL 5 — Simulasi loket tiket (satuan detik)")
    print("=" * 60)
    sim2 = TicketCounterSimulationSec(
        numAgents=2, numSeconds=6000, betweenTime=120, serviceTime=180
    )
    sim2.run()
    sim2.printResults(unit="seconds")
    print("\nTabel eksperimen lengkap (satuan detik):")
    runExperimentSec()

    print("\n" + "=" * 60)
    print("SOAL 6 — reverseQueue")
    print("=" * 60)
    q = Queue()
    for v in [10, 20, 30, 40, 50]:
        q.enqueue(v)
    print("Queue awal (front→rear): [10, 20, 30, 40, 50]")
    reverseQueue(q)
    hasil = []
    while not q.isEmpty():
        hasil.append(q.dequeue())
    print("Queue setelah reverseQueue:", hasil)
    # Expected: [50, 40, 30, 20, 10]

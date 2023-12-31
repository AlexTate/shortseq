import unittest
import psutil
import time
import os

from collections import Counter
from pympler.asizeof import asizeof
from random import randint

import shortseq as sq
from shortseq import ShortSeqCounter, read_and_count_fastq
from .util import rand_sequence

resources = "./testdata"

# For now, you must first generate these files using the make_data() helper function.
# These files will be several hundred megabytes in size.
ten_m_wo_repeat = f"{resources}/10m_no_rep.txt"
one_m_w_repeats = f"{resources}/1m.txt"


class Profiling(unittest.TestCase):

    def make_data(self, n, file=f"{resources}/test_data.txt", repeats=False):
        dups = lambda: randint(1, 100) if repeats else lambda: 1
        mapr = ["A", "T", "G", "C"]
        seqs = []

        for i in range(n):
            length = randint(15, 32)
            new_seq = [mapr[randint(0, 3)] for _ in range(length)]
            seqs.extend(["".join(new_seq)] * dups())

        with open(file, 'w') as f:
            f.write('\n'.join(seqs))

        print("Wrote %d sequences to %s" % (len(seqs), file))

    def read_data(self, file="test_data.txt", n=None):
        with open(file, 'rb') as f:
            seqs = f.readlines()

        length = n if n is not None else len(seqs)
        result = [seqs[i][:-1] for i in range(length)]

        return result

    def benchmark_unicode_tp_hash(self, seqs, decode=False):
        start = time.time()
        count = Counter(seqs)
        end = time.time()
        diff = end - start
        print(f"Time to count bytes: {diff:.6f}s")

        if decode:
            start2 = time.time()
            for seq in count.keys():
                seq.decode()
            end2 = time.time()
            diff = end2 - start
            print(f"Time to decode: {end2 - start2:.6f}")
            print(f"Unicode total: {diff:.6f}")

        print(f"{len(count)} unique sequences")
        return count, diff

    def benchmark_ShortSeq(self, seqs, unmarshall=False):
        start = time.time()
        count = ShortSeqCounter(seqs)
        end = time.time()
        diff = end - start
        print(f"Time to count ShortSeqs: {diff:.6f}")

        if unmarshall:
            start2 = time.time()
            for seq in count.keys():
                seq.__str__()
            end2 = time.time()
            diff = end2 - start
            print(f"Time to unmarshall: {end2 - start2:.6f}")
            print(f"ShortSeq total: {diff:.6f}")

        print(f"{len(count)} unique sequences")
        return count, diff

    def print_compression_ratio(self, old_ctr, new_ctr):
        t1, t2 = 0, 0
        for c1, c2 in zip(old_ctr.keys(), new_ctr.keys()):
            t1 += asizeof(c1)
            t2 += asizeof(c2)

        print(f"Compression Ratio: {t2 / t1}")

    def print_time_diff(self, old_t, new_t):
        fastest = min(old_t, new_t)
        slowest = max(old_t, new_t)
        diff = slowest - fastest
        if new_t == fastest:
            direction = "faster"
            pct = (diff / slowest) * 100
        else:
            direction = "slower"
            pct = (diff / fastest) * 100

        print(f"Time difference: {diff:.5f} ({pct:.1f}% {direction})")

    @unittest.skip("Long running benchmark test")
    def test_benchmark(self):
        mem = []
        process = psutil.Process(os.getpid())
        t1 = time.time()
        # counts = read_and_count_fastq(one_m_w_repeats)
        counts = read_and_count_fastq(ten_m_wo_repeat)
        t2 = time.time()
        print(t2 - t1)
        # sys.exit(0)

        seqs = self.read_data(ten_m_wo_repeat)
        # seqs = self.read_data(one_m_w_repeats)
        mem.append(process.memory_info().rss)

        counts1, t1 = self.benchmark_unicode_tp_hash(seqs, decode=True)
        mem.append(process.memory_info().rss)
        print('=' * 35)
        counts2, t2 = self.benchmark_ShortSeq(seqs, unmarshall=True)

        mem.append(process.memory_info().rss)
        print('=' * 35)
        print(f"Size of PyUnicode dictionary: {asizeof(counts1) / 1024 / 1024:.1f}mb")
        print(f"Size of ShortSeqCounter dict: {asizeof(counts2) / 1024 / 1024:.1f}mb")
        print([f"{int(m / 1024 / 1024):d}mb" for m in mem])
        print('=' * 35)

        self.print_compression_ratio(old_ctr=counts1, new_ctr=counts2)
        self.print_time_diff(t1, t2)
        print(f"Count values match: {sorted(counts1.values()) == sorted(counts2.values())}")

    """A primitive benchmark for PyBytes to ShortSeqVar vs PyUnicode runtime."""

    @unittest.skip("Long running benchmark test")
    def test_benchmark(self):
        sample_size = 10000
        min_len, max_len = 65, 1023
        samples = [rand_sequence(min_len, max_len, as_bytes=True) for _ in range(sample_size)]
        print("samples done")

        start = time.time()
        uni = [seq.decode() for seq in samples]
        end = time.time()
        print(f"{end - start:.8f}s unicode")

        start = time.time()
        seq = [sq.from_bytes(seq) for seq in samples]
        end = time.time()
        print(f"{end - start:.8f}s ShortSeq")


if __name__ == '__main__':
    unittest.main()

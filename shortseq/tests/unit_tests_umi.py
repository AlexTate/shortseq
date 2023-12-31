import unittest

from shortseq.umi import *

class MyTestCase(unittest.TestCase):
    def test_construct(self):
        u = UMI()
        u5 = UMI5p()
        u3 = UMI3p()
        ub = UMIboth()

    def test_factory_construct(self):
        f_5p = UMIFactory(len_5p=1)
        f_3p = UMIFactory(len_3p=1)
        f_bo = UMIFactory(len_5p=1, len_3p=1)

        self.assertIsInstance(f_5p.from_bytes(b"ATGC"), UMI5p)
        self.assertIsInstance(f_3p.from_bytes(b"ATGC"), UMI3p)
        self.assertIsInstance(f_bo.from_bytes(b"ATGC"), UMIboth)

    def test_seq_basic(self):
        #                             remain: GCGTAATA GGGGGTTT CGCTGTGG GGCGGCT
        # GCGTAATA GGGGGTTT CGCTGTGG GGCGGCTA GCGTAATA GGGGGTTT CGCTGTGG GGCGGCT
        # seq = b"GCGTAATAGGGGGTTTCGCTGTGGGGCGGCTAGCGTAATAGGGGGTTTCGCTGTGGGGCGGCT"
        # UMIFactory(len_5p=5).from_bytes(seq)

        # GCGTAATA GGGGGTTT CGCTGTGG GGCGGCTA G
        seq = b"GCGTAATAGGGGGTTTCGCTGTGGGGCGGCTAG"
        UMIFactory(len_5p=5).from_bytes(seq)


if __name__ == '__main__':
    unittest.main()

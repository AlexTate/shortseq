import cython

from cpython.bytes cimport PyBytes_AsString
from cpython.dict cimport PyDict_GetItem, PyDict_SetItem
from cpython.exc cimport PyErr_Occurred
from cpython.list cimport PyList_GET_ITEM
from cpython.long cimport PyLong_FromSize_t
from cpython.unicode cimport PyUnicode_AsASCIIString

from libcpp.vector cimport vector

from .short_seq_var cimport *
from .short_seq_128 cimport *
from .short_seq_64 cimport *
from .fast_read cimport *
from .util cimport *

from shortseq import MAX_64_NT, MAX_128_NT, MAX_VAR_NT

"""
Private dictionary fast-path methods not currently offered by the Cython wrapper
"""

cdef extern from "Python.h":
    dict _PyDict_NewPresized(int minused)
    PyObject* _PyDict_GetItem_KnownHash(object mp, object key, Py_hash_t hash)
    PyObject* _PyDict_Pop_KnownHash(object mp, object key, Py_hash_t hash, object deflt)
    int _PyDict_SetItem_KnownHash(object mp, object key, object item, Py_hash_t hash)
    int _PyDict_DelItem_KnownHash(object mp, object key, Py_hash_t hash)
    bint _PyDict_Contains_KnownHash(object mp, object key, Py_hash_t hash)


"""
Importable constructor functions for Cython space
"""

cdef object _from_py_str(str seq_str)
cdef object _from_py_bytes(bytes seq_bytes)
cdef object _from_chars(char* sequence)
cdef object _new(char* sequence, size_t length)


cdef class ShortSeqCounter(dict):
    cdef _count_short_seq_vector(self, vector[PyObject *])
    cdef _count_chars_vector(self, vector[char*] it)
    cdef _count_py_bytes_list(self, list it)
    cdef _count_sequence(self, object seq)


cpdef ShortSeqCounter read_and_count_fastq(object filename)
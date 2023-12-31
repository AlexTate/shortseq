import random
import math
import re


def print_var_seq_pext_chunks(seq):
    """Prints the specified sequence with the block and pext boundaries of ShortSeqVar indicated.
    This is useful for visualizing and debugging the ShortSeqVar marshalling algorithm."""

    block_count = math.ceil(len(seq) / 32)
    blocks = [seq[i*32:(i+1)*32] for i in range(block_count)]
    out = []

    for block in blocks:
        np64, rem = divmod(len(block), 8)
        np32, ser = divmod(rem, 4)
        chunks = []

        if np64: chunks.extend(block[i*8:(i+1)*8] for i in range(np64))
        if np32: chunks.append(block[np64*8:np64*8+4])
        if ser: chunks.append(block[-1 * ser:])

        out.append("|".join(chunks))

    print(" -> ".join(out))


def rand_sequence(min_length=None, max_length=None, as_bytes=False):
    """Returns a randomly generated sequence of the specified type, with a length in the specified range"""

    assert (min_length, max_length) != (None, None)
    bases = ("A", "C", "T", "G")

    if min_length and max_length:
        assert min_length <= max_length
        seq = ''.join(random.choice(bases) for _ in range(min_length, max_length))
    else:
        seq = ''.join(random.choice(bases) for _ in range(min_length))

    return seq.encode() if as_bytes else seq


def sorted_natural(lines, key=None, reverse=False):
    """Sorts alphanumeric strings with entire numbers considered in the sorting order,
    rather than the default behavior which is to sort by the individual ASCII values
    of the given number. Returns a sorted copy of the list, just like sorted().

    Not sure who to credit... it seems this snippet has been floating around for quite
    some time. Strange that there isn't something in the standard library for this."""

    convert = lambda text: int(text) if text.isdigit() else text.lower()
    extract = (lambda data: key(data)) if key is not None else lambda x: x
    alphanum_key = lambda elem: [convert(c) for c in re.split(r'(\d+)', extract(elem))]
    return sorted(lines, key=alphanum_key, reverse=reverse)
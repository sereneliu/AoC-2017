# --- Day 10: Knot Hash ---

puzzle_list = list(range(256))
puzzle_input = '''88,88,211,106,141,1,78,254,2,111,77,255,90,0,54,205'''
puzzle_lengths = [int(num) for num in puzzle_input.split(",")]

class KnotHashState(object):
    def __init__(self, size):
        self._pos = 0
        self._skip = 0
        self._list = range(size)
        pass
    
    def one_round(self, length):
        reversed_elements = []
        if length <= len(self._list[self._pos:]):
            i = self._list[self._pos:self._pos + length]
        else:
            i = self._list[self._pos:] + self._list[0:length - len(self._list[self._pos:])]
        if i != []:
            for element in reversed(i):
                reversed_elements.append(element)
        j = self._pos
        for element in reversed_elements:
            self._list[j] = element
            if j < len(self._list) - 1:
                j += 1
            else:
                j = 0
        self._pos = (self._pos + length + self._skip) % len(self._list)
        self._skip += 1
        return self._list

    def many_rounds(self, lengths):
        for length in lengths:
            self.one_round(length)
        return self._list
        
def dense_hash(list_of_num):
    x = list_of_num[0]
    for i in range(len(list_of_num) - 1):
        x = x ^ list_of_num[i + 1]
    return x
    
def knot_hash(key):
    lengths = [ord(c) for c in key] + [17, 31, 73, 47, 23]
    hash_state = KnotHashState(256)
    for _ in range(64):
        sparse_hash = hash_state.many_rounds(lengths)
    dense_hash_result = []
    i = 0
    while i < len(sparse_hash):
        dense_hash_result.append(dense_hash(sparse_hash[i:i + 16]))
        i += 16
    return dense_hash_result
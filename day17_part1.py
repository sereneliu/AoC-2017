def spinlock(steps):
    circular_buffer = []
    pos = 0
    value = 0
    for n in range(2018):
        if len(circular_buffer) == 0:
            circular_buffer.insert(pos + steps + 1, value)
        else:
            circular_buffer.insert(((pos + steps) % len(circular_buffer)) + 1, value)
        pos = circular_buffer.index(value)
        value += 1
    return circular_buffer[circular_buffer.index(2017) + 1]

print spinlock(335)
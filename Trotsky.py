def local_insertion_sort(block):
    for i in range(1, len(block)):
        key = block[i]
        j = i - 1
        while j >= 0 and block[j] > key:
            block[j + 1] = block[j]
            j -= 1
        block[j + 1] = key


def trotsky_sort(data, block_size=32):
    n = len(data)

    for i in range(0, n, block_size):
        end = min(i + block_size, n)
        block = data[i:end]
        local_insertion_sort(block)
        data[i:end] = block

    current_size = block_size
    while current_size < n:
        for start in range(0, n, 2 * current_size):
            mid = start + current_size
            end = min(start + 2 * current_size, n)

            left = data[start:mid]
            right = data[mid:end]

            i = j = 0
            k = start

            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    data[k] = left[i]
                    i += 1
                else:
                    data[k] = right[j]
                    j += 1
                k += 1

            while i < len(left):
                data[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                data[k] = right[j]
                j += 1
                k += 1

        current_size *= 2

    return data

def trotsky_sort(data, block_size=32):
    n = len(data)

    for i in range(0, n, block_size):
        end = min(i + block_size, n)
        chunk = data[i:end]
        trotsky_sort_v2(chunk)
        data[i:end] = chunk

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

class TrotskySort:
    def __init__(self, block_size=16, disorder_threshold=0.2):
        self.data = []
        self.block_size = block_size
        self.disorder_threshold = disorder_threshold

    def insert(self, value):
        self.data.append(value)

    def revolution_step(self):
        n = len(self.data)
        if n < 2:
            return

        for start in range(0, n, self.block_size):
            end = min(start + self.block_size, n)
            if end - start > 1:  # Garante que o bloco tenha pelo menos 2 elementos
                disorder = self._local_disorder(start, end)
                if disorder > self.disorder_threshold:
                    self._local_reorder(start, end)

    def _local_disorder(self, start, end):
        if end - start < 2:
            return 0.0

        disorder = 0
        total = end - start - 1

        for i in range(start, end - 1):
            if self.data[i] > self.data[i + 1]:
                disorder += 1

        return disorder / total

    def _local_reorder(self, start, end):
        # Implementação do insertion sort no intervalo [start, end)
        for i in range(start + 1, end):
            key = self.data[i]
            j = i - 1
            while j >= start and self.data[j] > key:
                self.data[j + 1] = self.data[j]
                j -= 1
            self.data[j + 1] = key

    def snapshot(self):
        return list(self.data)

    def sorted_prefix(self):
        if not self.data:
            return []

        prefix = [self.data[0]]
        for i in range(1, len(self.data)):
            if self.data[i] >= self.data[i - 1]:
                prefix.append(self.data[i])
            else:
                break
        return prefix

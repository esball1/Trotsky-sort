import asyncio
import threading
import queue
import time


class AsyncTrotskyAdapter:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.input = asyncio.Queue()
        self.running = False

    async def produce(self, event):
        await self.input.put(event)

    async def consume_loop(self, handler):
        self.running = True
        while self.running:
            while not self.input.empty():
                self.scheduler.push(await self.input.get())

            self.scheduler.revolution_step()

            event = self.scheduler.pop()
            if event:
                await handler(event)
            else:
                await asyncio.sleep(0.01)

    def stop(self):
        self.running = False


class ThreadedTrotskyAdapter(threading.Thread):
    def __init__(self, scheduler):
        super().__init__(daemon=True)
        self.scheduler = scheduler
        self.input = queue.Queue()
        self.output = queue.Queue()

    def run(self):
        while True:
            try:
                while True:
                    self.scheduler.push(self.input.get_nowait())
            except queue.Empty:
                pass

            self.scheduler.revolution_step()

            event = self.scheduler.pop()
            if event:
                self.output.put(event)

            time.sleep(0.001)

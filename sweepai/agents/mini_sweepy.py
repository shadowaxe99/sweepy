import logging
from multiprocessing import Process, Queue


class MiniSweepy:
    def __init__(self, identifier):
        self.identifier = identifier
        self.logger = logging.getLogger(__name__)
        self.message_queue = Queue()

    def execute_task(self, task):
        try:
            task()
        except Exception as e:
            self.logger.error(f"Error executing task: {e}")

    def communicate(self, message):
        self.message_queue.put(message)


# Unit tests
import pytest


def test_execute_task():
    sweepy = MiniSweepy(1)
    task = lambda: 1 + 1
    sweepy.execute_task(task)

def test_execute_task_with_error():
    sweepy = MiniSweepy(1)
    task = lambda: 1 / 0
    with pytest.raises(Exception):
        sweepy.execute_task(task)

def test_communicate():
    sweepy = MiniSweepy(1)
    message = "Hello, Taskmaster!"
    sweepy.communicate(message)
    assert sweepy.message_queue.get() == message

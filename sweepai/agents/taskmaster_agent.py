import os
import spacy
from collections import defaultdict
import queue
import logging
from multiprocessing import Process, Queue
from mini_sweepy import MiniSweepy
from base_agent import BaseAgent

class TaskmasterAgent(BaseAgent):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.task_queue = queue.PriorityQueue()
        self.logger = logging.getLogger(__name__)
        self.developer_agents = []  # This will be replaced by mini_sweepys
        self.mini_sweepys = []  # List to hold MiniSweepy instances
        self.message_queue = None

    def analyze_task(self, task_description):
        doc = self.nlp(task_description)
        tasks = defaultdict(list)
        for token in doc:
            if token.dep_ in ("ROOT", "acl", "advcl"):
                tasks[token.lemma_].append(token.text)
        return tasks

    def assign_tasks(self):
        while not self.task_queue.empty():
            priority, task = self.task_queue.get()
            for mini_sweepy in self.mini_sweepys:
                # Assume MiniSweepy has an is_available method
                if mini_sweepy.is_available():
                    mini_sweepy.execute_task(task)  # Changed method to execute_task
                    break

    def start_developer_agents(self):
        for _ in range(6):
            agent_process = Process(target=self.assign_tasks)
            self.developer_agents.append(agent_process)
            agent_process.start()

    def manage_communication(self):
        self.message_queue = Queue()
        for agent in self.developer_agents:
            agent.set_message_queue(self.message_queue)

    def log_error(self, error):
        self.logger.error(error)

    def create_file(self, file_path):
        try:
            with open(file_path, 'w') as file:
                file.write('')  # Create an empty file
            self.logger.info(f'File created at {file_path}')
        except Exception as e:
            self.log_error(f'Error creating file {file_path}: {e}')

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
            self.logger.info(f'File deleted at {file_path}')
        except Exception as e:
            self.log_error(f'Error deleting file {file_path}: {e}')


# Unit tests
import pytest

def test_task_analysis():
    agent = TaskmasterAgent()
    tasks = agent.analyze_task("Refactor the retrieve_relevant function to be more modular.")
    assert len(tasks) > 0

def test_task_assignment():
    agent = TaskmasterAgent()
    agent.task_queue.put((1, "Refactor function"))
    agent.assign_tasks()
    # Assert that the task has been assigned
    
def test_create_file():
    agent = TaskmasterAgent()
    temp_file_path = '/tmp/test_file.txt'
    agent.create_file(temp_file_path)
    assert os.path.exists(temp_file_path)
    os.remove(temp_file_path)  # Clean up after test

def test_delete_file():
    temp_file_path = '/tmp/test_file.txt'
    with open(temp_file_path, 'w') as file:  # Create a file to delete
        file.write('Test')
    agent = TaskmasterAgent()
    agent.delete_file(temp_file_path)
    assert not os.path.exists(temp_file_path)


def test_communication_management():
    agent = TaskmasterAgent()
    agent.manage_communication()
    # Assert that the message queue is set up correctly
    # ...
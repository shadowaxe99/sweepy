import spacy
from collections import defaultdict
import queue
import logging
from multiprocessing import Process, Queue
from base_agent import BaseAgent

class TaskmasterAgent(BaseAgent):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.task_queue = queue.PriorityQueue()
        self.logger = logging.getLogger(__name__)
        self.developer_agents = []
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
            for agent in self.developer_agents:
                if agent.is_available():
                    agent.assign_task(task)
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
    # ...

def test_communication_management():
    agent = TaskmasterAgent()
    agent.manage_communication()
    # Assert that the message queue is set up correctly
    # ...
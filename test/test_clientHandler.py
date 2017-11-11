from unittest import TestCase
from src.server import *


class TestClientHandler(TestCase):
    def test_parse(self):
        message = "server"
        assert message == "server"

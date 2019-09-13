from invoke import Context
import unittest

from testfixtures import LogCapture

import tasks

class TestTasks(unittest.TestCase):
    def test_say_hello(self):
        tasks.say_hello(Context(), "Tua", 10)
        assert True, 'We must reach here'


if __name__ == '__main__':
    unittest.main()

import unittest
from decorator import log2mongo

class TestDecorator01(unittest.TestCase):
    def test_log2mongo_returned_value(self):
        def testee(abc):
            return abc

        INP = 'something'
        EXP = testee(INP)
        OUT = log2mongo(testee)(INP)
        assert EXP == OUT, 'Decorator log2mongo should return exactly the original function'



if __name__ == '__main__':
    unittest.main()

from main import speak, sing
import unittest


class TestMain(unittest.TestCase):

    def test_speak(self):
        INP = EXP ='OK'
        OUT = speak(INP)
        assert OUT == EXP, 'It must speak exactly what I asked'

    def test_sing(self):
        INP = EXP = 'Lala land'
        OUT = sing(INP)
        assert OUT == EXP, 'It must sing exactly what I asked'


if __name__ == '__main__':
    unittest.main()

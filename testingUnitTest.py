import unittest
import testingUnitTest_sample as theThing

def additionExample(i):
    return(i + i)


class MyTest(unittest.TestCase):
    def test_additionExample(self):
        self.assertEqual(additionExample(2), 4)
        self.assertEqual(additionExample(0), 0)
        self.assertNotEqual(additionExample(-2), -3)
        self.assertEqual(additionExample(-5), -10)
    @unittest.skip("Skipping this bad boy")
    def test_testingUnitTestSample(self):
        self.assertEqual(theThing.addToTen(5), 15)
        self.assertEqual(theThing.divideByTen(20), 2)
        self.assertEqual(theThing.lowerCaseText("Hi There"), "hi there")

unittest.main()
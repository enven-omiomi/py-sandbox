import time


def test_1():
	time.sleep(0.1)
	expected = (0, 1, 2, 3)
	actual = tuple(i for i in range(4))
	assert expected == actual

def test_2():
	time.sleep(0.2)
	expected = [0, 1, 2, 3]
	actual = [i for i in range(4)]
	assert expected == actual

def test_3():
	time.sleep(0.3)
	expected = {'1': 1, '2': 2}
	actual = {str(i): i for i in range(1,3)}
	assert expected == actual

def test_4():
	time.sleep(0.4)
	expected = {0, 1, 2, 3}
	actual = {i for i in range(4)}
	assert expected == actual

def test_5():
	time.sleep(0.5)
	expected = [0, 2, 4, 6, 8]
	actual = [i for i in range(10) if i % 2 == 0]
	assert expected == actual

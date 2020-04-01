import time
import pytest
import sys


@pytest.fixture(scope='module')
def expected():
  return [i for i in range(1, 1000000)]


def test_1_1(expected):
  actual = [i for i in range(1, 1000000)]
  assert expected == actual

def test_1_2(expected):
  actual = []
  for i in range(1, 1000000):
    actual.append(i)
  assert expected == actual

def test_1_3(expected):
  def total(n):
    if n < 1:
      return [i for i in range(1, n)]
    return total(n - 100) + [i for i in range(n - 99, n)]
  actual = total(100000)
  assert expected == actual

def test_2():
  expected = [0, 1, 2, 3]
  actual = [i for i in range(4)]
  assert expected == actual

def test_3():
  expected = {'1': 1, '2': 2}
  actual = {str(i): i for i in range(1,3)}
  assert expected == actual

def test_4():
  expected = {0, 1, 2, 3}
  actual = {i for i in range(4)}
  assert expected == actual

def test_5():
  expected = [0, 2, 4, 6, 8]
  actual = [i for i in range(10) if i % 2 == 0]
  assert expected == actual

import time
import pytest
import sys


COUNT = 10000000

@pytest.fixture(scope='module')
def expected():
  return [i for i in range(1, COUNT)]

@pytest.fixture(scope='function', autouse=True)
def setup():
  time.sleep(0.1)
  yield
  time.sleep(0.2)

def test_1_1(expected):
  actual = [i for i in range(1, COUNT)]
  assert expected == actual


def test_1_2(expected):
  actual = list({i for i in range(1, COUNT)})
  assert expected == actual


def test_1_3(expected):
  actual = []
  for i in range(1, COUNT):
    actual.append(i)
  assert expected == actual


def test_1_4(expected):
  actual = []
  for i in range(1, COUNT):
    # actual = actual + [i] とすると死ぬほど時間かかる
    actual += [i]
  assert expected == actual

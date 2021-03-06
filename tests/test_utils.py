import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import fxpmath as fxp
from fxpmath.utils import *

import numpy as np

def test_strbin2int():
    assert strbin2int('0000') == 0
    assert strbin2int('0001') == 1
    assert strbin2int('1000', signed=False) == 8
    assert strbin2int('0b0010') == 2
    assert strbin2int('0b0100 1101') == 77
    assert strbin2int('0b1000 0000') == -128
    assert strbin2int('0b1111 1111') == -1
    assert strbin2int('0b1111 1110') == -2
    assert strbin2int('0b0111 1111') == 127
    assert strbin2int('0b1000 0000', signed=False) == 128
    assert strbin2int('0b0000', n_word=8) == 0
    assert strbin2int('0b0100', n_word=8) == 4
    assert strbin2int('0b1111', n_word=8) == -1
    assert strbin2int('0b1000', n_word=8) == strbin2int('0b1111 1000', n_word=8)

def test_strbin2float():
    assert strbin2float('0001') == 1.0
    assert strbin2float('0b1000 0000') == -128.0
    assert strbin2float('0b0111 1111') == 127.0
    assert strbin2float('000.1') == 0.5
    assert strbin2float('b010.101') == 2.625
    assert strbin2float('111.1') == -0.5
    assert strbin2float('0001', n_frac=1) == 0.5
    assert strbin2float('0001', n_frac=2) == 0.25
    assert strbin2float('000.1', n_frac=4) == 0.5

def test_strhex2int():
    assert strhex2int('0x00') == 0
    assert strhex2int('0x0A') == 10
    assert strhex2int('0x7F') == 127
    assert strhex2int('0xFF') == -1
    assert strhex2int('0x0F') == 15
    assert strhex2int('0x80') == -128
    assert strhex2int('0x80', signed=False) == 128
    assert strhex2int('0xFF', signed=False) == 255
    assert strhex2int('0x100') == 256

def test_strhex2float():
    assert strhex2float('0x00') == 0.0
    assert strhex2float('0x0A') == 10.0
    assert strhex2float('0x7F') == 127.0
    assert strhex2float('0xFF') == -1.0
    assert strhex2float('0x0F') == 15.0
    assert strhex2float('0x80') == -128.0

    assert strhex2float('0x00', n_frac=2) == 0.0
    assert strhex2float('0x0A', n_frac=2) == 2.5
    assert strhex2float('0x7F', n_frac = 3) == 16.0 - 0.125
    assert strhex2float('0xFF', n_frac = 4) == 0 - 0.0625
    assert strhex2float('0x0F', n_frac = 4) == 1 - 0.0625
    assert strhex2float('0x80', n_frac = 4) == -8.0

def test_str2num():
    # int
    assert str2num('0') == 0
    assert str2num('10') == 10
    assert str2num('253') == 253
    assert str2num('-5') == -5
    # floats
    assert str2num('7.2') == 7.2
    assert str2num('-7.2') == -7.2
    # binary
    assert str2num('0b0110') == 6
    assert str2num('0b1110') == -2
    # hex
    assert str2num('0x7F') == 127
    assert str2num('0x80') == -128.0
    assert str2num('0x0A', n_frac=2) == 2.5
    # list
    assert str2num(['10', '-7.2', '0b0110', '0x7F']) == [10, -7.2, 6, 127]
    # transparent types
    assert str2num(np.array([0,1,2,3])).all() == np.array([0,1,2,3]).all()
    assert str2num(None) is None

def test_binary_repr():
    assert binary_repr(6, n_word=8) == '00000110'
    assert binary_repr(6, n_word=8, n_frac=3) == '00000.110'
    assert binary_repr(6, n_word=8, n_frac=0) == '00000110.'
    assert binary_repr(6, n_word=8, n_frac=-2) == '00000110##.'
    assert binary_repr(6, n_word=8, n_frac=8) == '.00000110'

    assert binary_repr(-1, n_word=4) == '1111'

def test_base_repr():
    assert base_repr(6) == '110'
    assert base_repr(6, base=2, n_frac=3) == '.110'
    assert base_repr(6, n_frac=0) == '110.'
    assert base_repr(6, n_frac=-2) == '110##.'
    assert base_repr(6, n_frac=8) == '.00000110'

    assert base_repr(-1,) == '-1'
    assert base_repr(-6,) == '-110'
    assert base_repr(-6, n_frac=1) == '-11.0'

    assert base_repr(30, base=16) == '1E'
    assert base_repr(-30, base=16) == '-1E'


def test_bits_len():
    assert bits_len(1) == 1
    assert bits_len(-1) == 1
    assert bits_len(1, signed=True) == 2
    assert bits_len(31) == 5
    assert bits_len(32) == 6
    assert bits_len(-32) == 6
    assert bits_len(-33) == 7

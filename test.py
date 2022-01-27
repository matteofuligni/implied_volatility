import func as f
import pytest
from hypothesis import given, settings
import hypothesis
import hypothesis.strategies as st
from hypothesis.extra import numpy as enp
import numpy as np

@given(S0 = st.just(1),
       VOL = st.floats(min_value=0.01,max_value=0.99,
                       allow_nan=False, allow_infinity=False))
def test_sigma(S0, VOL):
    assert f.sigma(S0, VOL) == VOL
    assert type(f.sigma(S0, VOL)) is float

#T_array = st.lists(elements=st.floats(), min_size=1, max_size=20)
#K_array = st.lists(elements=st.floats(), min_size=1, max_size=20)
#T_array = np.linspace(0.5, TIME, T_INT)
#K_array = np.linspace(0.5, STRIKE, K_INT)
#N_INTER = st.integers(min_value=1, max_value=1000)
#N_SIM = st.integers(min_value=1, max_value=1000)
#N_INTER = 100
#N_SIM = 100
#S0 = st.floats(allow_nan=False, allow_infinity=False)
#R = st.floats(allow_nan=False, allow_infinity=False)
#VOL = st.floats(allow_nan=False, allow_infinity=False)
#CC = enp.arrays(dtype=np.int16,shape=(T_array, K_array))

#@given(T_array, K_array, N_INTER, N_SIM, S0, R, VOL, CC)
#def test_price(T_array, K_array, N_INTER, N_SIM, S0, R, VOL, CC):
#    price = f.price(T_array, K_array, N_INTER, N_SIM, S0, R, VOL, CC)
#    assert type(price) is np.array()

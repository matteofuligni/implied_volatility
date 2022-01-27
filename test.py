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

@given(T_array = st.just(np.linspace(0.5, 2, 10)),
       K_array = st.just(np.linspace(0.5, 1.5, 10)),
       N_INTER = st.just(100),
       N_SIM = st.just(100),
       S0 = st.just(1),
       R = st.floats(min_value=0.05,max_value=0.99,
                     allow_nan=False, allow_infinity=False),
       VOL = st.floats(min_value=0.01,max_value=0.99,
                       allow_nan=False, allow_infinity=False))
def test_price(T_array, K_array, N_INTER, N_SIM, S0, R, VOL):
    price = f.price(T_array, K_array, N_INTER, N_SIM, S0, R, VOL)
    assert type(price) is np.ndarray
    assert np.any(price)

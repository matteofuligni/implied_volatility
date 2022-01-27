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
       N_INTER = st.just(10),
       N_SIM = st.just(10),
       S0 = st.just(1),
       R = st.floats(min_value=0.05,max_value=0.99,
                     allow_nan=False, allow_infinity=False),
       VOL = st.floats(min_value=0.01,max_value=0.99,
                       allow_nan=False, allow_infinity=False))
def test_price(T_array, K_array, N_INTER, N_SIM, S0, R, VOL):
    price = f.price(T_array, K_array, N_INTER, N_SIM, S0, R, VOL)
    assert type(price) is np.ndarray
    assert np.any(price)


@given(S = st.floats(min_value=0.01, allow_nan=False, allow_infinity=False),
       K = st.floats(min_value=0.01, allow_nan=False, allow_infinity=False),
       T = st.floats(min_value=0.01, allow_nan=False, allow_infinity=False),
       r = st.floats(min_value=0.01,max_value=0.99,
                     allow_nan=False, allow_infinity=False),
       vol = st.floats(min_value=0.01,max_value=0.99,
                       allow_nan=False, allow_infinity=False))
def test_bs_call_01(S, K, T, r, vol):
    price = f.bs_call(S, K, T, r, vol)
    assert type(price) is np.float64


@given(S = st.just(1),
       K = st.just(1.5),
       T = st.just(1),
       r = st.just(0.05),
       vol = st.just(0.2))
def test_bs_call_02(S, K, T, r, vol):
    price = f.bs_call(S, K, T, r, vol)
    assert price == 0.0035962982615292335


@given(S = st.floats(min_value=0.01, allow_nan=False, allow_infinity=False),
       K = st.floats(min_value=0.01, allow_nan=False, allow_infinity=False),
       T = st.floats(min_value=0.01, allow_nan=False, allow_infinity=False),
       r = st.floats(min_value=0.01,max_value=0.99,
                     allow_nan=False, allow_infinity=False),
       sigma = st.floats(min_value=0.01,max_value=0.99,
                       allow_nan=False, allow_infinity=False))
def test_vega(S, K, T, r, sigma):
    vega = f.bs_vega(S, K, T, r, sigma)
    assert type(vega) is np.float64

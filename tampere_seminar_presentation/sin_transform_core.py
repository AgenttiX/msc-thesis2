<@\textcolor{red}{@numba.njit(parallel=True)}@>
def sin_transform(t: np.ndarray, f: np.ndarray, freq: np.ndarray) -> np.ndarray:
    integral = np.zeros_like(freq)
    for i in <@\textcolor{red}{numba.prange(freq.size)}@>:
        integrand = f * np.sin(freq[i] * t)
        integral[i] = np.trapz(integrand, t)
    return integral

import numpy
import pytest
from matchms.filtering import select_by_mz
from .builder_Spectrum import SpectrumBuilder


@pytest.mark.parametrize("peaks, mz_from, mz_to, expected", [
    [
        [numpy.array([10, 20, 30, 40], dtype="float"),
         numpy.array([1, 10, 100, 1000], dtype="float")],
        0, 1000,
        [numpy.array([10, 20, 30, 40], dtype="float"),
         numpy.array([1, 10, 100, 1000], dtype="float")]
    ], [
        [numpy.array([998, 999, 1000, 1001, 1002], dtype="float"),
         numpy.array([1, 10, 100, 1000, 10000], dtype="float")],
        0, 1000,
        [numpy.array([998, 999, 1000], dtype="float"),
         numpy.array([1, 10, 100], dtype="float")]
    ], [
        [numpy.array([10, 20, 30, 40], dtype="float"),
         numpy.array([1, 10, 100, 1000], dtype="float")],
        15, 1000,
        [numpy.array([20, 30, 40], dtype="float"),
         numpy.array([10, 100, 1000], dtype="float")]
    ], [
        [numpy.array([10, 20, 30, 40], dtype="float"),
         numpy.array([1, 10, 100, 1000], dtype="float")],
        0, 35,
        [numpy.array([10, 20, 30], dtype="float"),
         numpy.array([1, 10, 100], dtype="float")]
    ], [
        [numpy.array([10, 20, 30, 40], dtype="float"),
         numpy.array([1, 10, 100, 1000], dtype="float")],
        15, 35,
        [numpy.array([20, 30], dtype="float"),
         numpy.array([10, 100], dtype="float")]
    ]
])
def test_select_by_mz(peaks, mz_from, mz_to, expected):
    spectrum_in = SpectrumBuilder().with_mz(peaks[0]).with_intensities(peaks[1]).build()
    spectrum = select_by_mz(spectrum_in, mz_from=mz_from, mz_to=mz_to)

    assert spectrum.peaks.mz.size == len(expected[0])
    assert spectrum.peaks.mz.size == spectrum.peaks.intensities.size
    assert numpy.array_equal(spectrum.peaks.mz, expected[0])
    assert numpy.array_equal(spectrum.peaks.intensities, expected[1])

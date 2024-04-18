import pytest
from matchms.filtering.metadata_processing.repair_adduct_based_on_smiles import \
    repair_adduct_based_on_smiles
from tests.builder_Spectrum import SpectrumBuilder


@pytest.mark.parametrize("precursor_mz, expected_adduct, ionmode",
                         [(17.0, "[M+H]+", "positive"),
                          (17.5, "[M+H+NH4]2+", "positive"),
                          (74.0, "[2M+ACN+H]+", "positive"),
                          (15.0, "[M-H]-", "negative"),
                          (51.0, "[M+Cl]-", "negative"),
                          (4.33333, "[M-3H]3-", "negative"),
                          ])
def test_repair_adduct_based_on_smiles_not_mol_wt(precursor_mz, expected_adduct, ionmode):
    pytest.importorskip("rdkit")

    # CH4 is used as smiles, this has a mass of 16
    spectrum_in = SpectrumBuilder().with_metadata({"smiles": "C",
                                                   "precursor_mz": precursor_mz,
                                                   "ionmode": ionmode}).build()
    spectrum_out = repair_adduct_based_on_smiles(spectrum_in, mass_tolerance=0.1)
    assert spectrum_out.get("adduct") == expected_adduct
    assert abs(spectrum_out.get("parent_mass") - 15.9589) < 0.1


@pytest.mark.parametrize("precursor_mz, ionmode",
                         # Should not be repaired as [M]+, since this could also be a mistake with the precursor mz
                         # being the parent mass
                         [(16.04, "positive"),
                          # Should not be repaired as [M]-, since this could also be a mistake with the precursor mz
                          # being the parent mass
                          (16.04, "negative"),
                          (1000, "positive")
                          ])
def test_repair_adduct_based_on_smiles_not_repaired(precursor_mz, ionmode):
    pytest.importorskip("rdkit")

    # CH4 is used as smiles, this has a mass of 16
    spectrum_in = SpectrumBuilder().with_metadata({"smiles": "C",
                                                   "precursor_mz": precursor_mz,
                                                   "ionmode": ionmode}).build()
    spectrum_out = repair_adduct_based_on_smiles(spectrum_in, mass_tolerance=0.1)
    assert spectrum_out.get("adduct") is None

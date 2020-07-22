import numpy as np
import pandas as pd
import numpy.testing as npt
import tardis
import os
from astropy import units as u
from tardis.io.config_reader import Configuration
from tardis.model import Radial1DModel
import pytest

DATA_PATH = os.path.join(tardis.__path__[0], "model", "tests", "data")


@pytest.fixture(
    scope="module",
    params=[
        "model_full",
        "branch85",
        "uniform",
        "powerlaw",
        "exponential",
        "radiative",
    ],
)
def model_config_files(request):
    """Function to retrieve filenames of target data for tests"""
    filename = request.param
    csvy_config_file = os.path.join(DATA_PATH, filename + "_csvy.yml")
    old_config_file = os.path.join(DATA_PATH, filename + "_old_config.yml")
    return csvy_config_file, old_config_file


def test_compare_models(model_config_files):
    """Compare identical models produced by .from_config and 
       .from_csvy to check that velocities, densities and abundances 
       (pre and post decay) are the same"""
    csvy_config_file, old_config_file = model_config_files
    tardis_config = Configuration.from_yaml(csvy_config_file)
    tardis_config_old = Configuration.from_yaml(old_config_file)
    csvy_model = Radial1DModel.from_csvy(tardis_config)
    config_model = Radial1DModel.from_config(tardis_config_old)
    csvy_model_props = csvy_model.get_properties().keys()
    config_model_props = config_model.get_properties().keys()
    npt.assert_array_equal(csvy_model_props, config_model_props)
    for prop in config_model_props:
        csvy_model_val = csvy_model.get_properties()[prop]
        config_model_val = config_model.get_properties()[prop]
        if prop == "homologous_density":
            npt.assert_array_almost_equal(
                csvy_model_val.density_0.value, config_model_val.density_0.value
            )
            npt.assert_array_almost_equal(
                csvy_model_val.time_0.value, config_model_val.time_0.value
            )
        else:
            if hasattr(config_model_val, "value"):
                config_model_val = config_model_val.value
                csvy_model_val = csvy_model_val.value
            npt.assert_array_almost_equal(csvy_model_val, config_model_val)

    assert csvy_model.raw_abundance.shape == config_model.raw_abundance.shape
    assert (
        csvy_model.raw_isotope_abundance.shape
        == config_model.raw_isotope_abundance.shape
    )
    assert csvy_model.abundance.shape == config_model.abundance.shape
    npt.assert_array_almost_equal(
      csvy_model.raw_abundance.to_numpy(), config_model.raw_abundance.to_numpy()
    )
    npt.assert_array_almost_equal(
        csvy_model.raw_isotope_abundance.to_numpy(),
        config_model.raw_isotope_abundance.to_numpy(),
    )
    npt.assert_array_almost_equal(
        csvy_model.abundance.to_numpy(), config_model.abundance.to_numpy()
    )


@pytest.fixture(scope="module")
def csvy_model_to_test_abundances():
    """Returns Radial1DModel to use to test abundances dataframes"""
    csvypath = os.path.join(DATA_PATH, "csvy_model_to_test_abundances.yml")
    config = Configuration.from_yaml(csvypath)
    csvy_model_to_test_abundances = Radial1DModel.from_csvy(config)
    return csvy_model_to_test_abundances


def test_read_csvy_abundances(csvy_model_to_test_abundances):
    """Test if model reads abundances and isotope abundances 
       and constructs dataframes appropiatly before applying decay"""
    #rows in input_abundance are abundances for a fixed element,columns 
    #represent different shells
    abundance_index = pd.Index([1, 2], name="atomic_number")
    input_abundance = pd.DataFrame(
        [[0.0, 0.33, 0.3, 0.5, 0.4, 0.2], [0.98, 0.64, 0.6, 0.4, 0.55, 0.79]],
        index=abundance_index,
    )

    model_abundance_shape = csvy_model_to_test_abundances.raw_abundance.shape
    input_shape = input_abundance.shape
    assert model_abundance_shape == input_shape
    npt.assert_array_almost_equal(
      input_abundance.to_numpy(), csvy_model_to_test_abundances.raw_abundance.to_numpy()
    )

    # rows in input_isotopes represent isotope abundance in each of the 6 shells
    arrays = [[28], [56]]
    isotope_index = pd.MultiIndex.from_arrays(
        arrays, names=["atomic_number", "mass_number"]
    )
    input_isotopes = pd.DataFrame(
        [[0.02, 0.03, 0.1, 0.1, 0.05, 0.01]], 
        columns=np.arange(6), index=isotope_index
    )

    model_isotopes_shape = csvy_model_to_test_abundances.raw_isotope_abundance.shape
    input_isotopes_shape = input_isotopes.shape
    assert model_isotopes_shape == input_isotopes_shape
    npt.assert_array_almost_equal(
        input_isotopes.to_numpy(),
        csvy_model_to_test_abundances.raw_isotope_abundance.to_numpy(),
    )


def test_csvy_model_decay(csvy_model_to_test_abundances):
    """Compare model abundance decay against and decay calculations 
    done by hand.
    For the calculations decay calulculations the following procedure is used:
    Ni_halflife = 6.075 * u.d
    Co_halflife = 77.233 * u.d

    lambda_Ni = np.log(2) / Ni_halflife
    lambda_Co = np.log(2) / Co_halflife

    t = 4 * u.d means 4 days have passed since the explosion

    def N1(N0, lambda1, t=4.0 * u.d):
        return N0 * np.exp(-lambda1 * t)

    
    def N2(N1_0, lambda_1, lambda_2, t=4.0 * u.d):
        return (lambda_1 * N1_0 
                * (np.exp(-lambda_1 * t) / (lambda_2 - lambda_1)
                + np.exp(-lambda_2 * t) / (lambda_1 - lambda_2)))

     if the original Ni56 abundance for a given shell is 0.05, after 4 days:

     cobalt_abundace_after_4_days = N2(0.05, lambda_Ni, lambda_Co)
     nickel_abundace_after_4_days = N1(0.05, lambda_Ni)
     iron_abundance_after_4_days = 0.05 - cobalt_abundace_after_4_days 
                                    - nickel_abundace_after_4_days
     In the hand_decayed_dataframe every row represents a specific element
     and every column represent a shell"""

    decay_index = pd.Index([1, 2, 26, 27, 28], name="atomic_number")
    hand_decayed_abundance = pd.DataFrame(
        [
            [0.0, 0.33, 0.3, 0.5, 0.4, 0.2],
            [0.98, 0.64, 0.6, 0.4, 0.55, 0.79],
            [
                0.00013977843354947162,
                0.00020966765032420787,
                0.0006988921677473642,
                0.0006988921677473642,
                0.0003494460838736821,
                6.988921677473581e-05,
            ],
            [
                0.007188928223953217,
                0.010783392335929825,
                0.035944641119766085,
                0.035944641119766085,
                0.017972320559883043,
                0.0035944641119766084,
            ],
            [
                0.012671293342497312,
                0.019006940013745966,
                0.06335646671248656,
                0.06335646671248656,
                0.03167823335624328,
                0.006335646671248656,
            ],
        ],
        index=decay_index,
    )

    model_decayed_abundance_shape = csvy_model_to_test_abundances.abundance.shape
    hand_decayed_abundance_shape = hand_decayed_abundance.shape
    assert model_decayed_abundance_shape == hand_decayed_abundance_shape
    npt.assert_array_almost_equal(
        hand_decayed_abundance.to_numpy(), 
        csvy_model_to_test_abundances.abundance.to_numpy()
    )

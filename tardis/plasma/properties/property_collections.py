from tardis.plasma.properties import *


class PlasmaPropertyCollection(list):
    pass


basic_inputs = PlasmaPropertyCollection(
    [
        TRadiative,
        Abundance,
        Density,
        TimeExplosion,
        AtomicData,
        DilutionFactor,
        LinkTRadTElectron,
        HeliumTreatment,
        ContinuumInteractionSpecies,
    ]
)
basic_properties = PlasmaPropertyCollection(
    [
        BetaRadiation,
        Levels,
        Lines,
        AtomicMass,
        PartitionFunction,
        GElectron,
        IonizationData,
        NumberDensity,
        LinesLowerLevelIndex,
        LinesUpperLevelIndex,
        TauSobolev,
        StimulatedEmissionFactor,
        SelectedAtoms,
        ElectronTemperature,
    ]
)
lte_ionization_properties = PlasmaPropertyCollection([PhiSahaLTE])
lte_excitation_properties = PlasmaPropertyCollection([LevelBoltzmannFactorLTE])
macro_atom_properties = PlasmaPropertyCollection(
    [BetaSobolev, TransitionProbabilities, MacroAtomData]
)
nebular_ionization_properties = PlasmaPropertyCollection(
    [PhiSahaNebular, ZetaData, BetaElectron, RadiationFieldCorrection]
)
dilute_lte_excitation_properties = PlasmaPropertyCollection(
    [LevelBoltzmannFactorDiluteLTE]
)
non_nlte_properties = PlasmaPropertyCollection([LevelBoltzmannFactorNoNLTE])
nlte_properties = PlasmaPropertyCollection(
    [
        LevelBoltzmannFactorNLTE,
        NLTEData,
        PreviousElectronDensities,
        PreviousBetaSobolev,
        BetaSobolev,
    ]
)
helium_nlte_properties = PlasmaPropertyCollection(
    [
        HeliumNLTE,
        RadiationFieldCorrection,
        ZetaData,
        BetaElectron,
        LevelNumberDensityHeNLTE,
        IonNumberDensityHeNLTE,
    ]
)
helium_lte_properties = PlasmaPropertyCollection(
    [LevelNumberDensity, IonNumberDensity]
)
helium_numerical_nlte_properties = PlasmaPropertyCollection(
    [HeliumNumericalNLTE]
)
detailed_j_blues_inputs = PlasmaPropertyCollection(
    [JBluesEstimator, RInner, TInner, Volume]
)
detailed_j_blues_properties = PlasmaPropertyCollection(
    [JBluesDetailed, JBluesNormFactor, LuminosityInner, TimeSimulation]
)
continuum_interaction_inputs = PlasmaPropertyCollection(
    [
        StimRecombRateCoeffEstimator,
        PhotoIonRateCoeffEstimator,
        RInner,
        TInner,
        Volume,
        BfHeatingRateCoeffEstimator,
        StimRecombCoolingRateCoeffEstimator,
        YgData,
    ]
)
continuum_interaction_properties = PlasmaPropertyCollection(
    [
        PhotoIonizationData,
        SpontRecombRateCoeff,
        PhotoIonRateCoeff,
        ThermalLevelBoltzmannFactorLTE,
        ThermalLTEPartitionFunction,
        BetaElectron,
        ThermalGElectron,
        ThermalPhiSahaLTE,
        SahaFactor,
        TimeSimulation,
        PhotoIonEstimatorsNormFactor,
        LuminosityInner,
        StimRecombRateCoeff,
        CorrPhotoIonRateCoeff,
        SpontRecombCoolingRateCoeff,
        RawRecombTransProbs,
        RawPhotoIonTransProbs,
        RawRadBoundBoundTransProbs,
        MarkovChainTransProbs,
        NonContinuumTransProbsMask,
        YgInterpolator,
        CollExcRateCoeff,
        CollDeexcRateCoeff,
        RawCollisionTransProbs,
        MarkovChainIndex,
        MarkovChainTransProbsCollector,
        NonMarkovChainTransitionProbabilities,
        MonteCarloTransProbs,
        FreeFreeCoolingRate,
        FreeBoundCoolingRate,
        BoundFreeOpacity,
        LevelNumberDensityLTE,
        PhotoIonBoltzmannFactor,
        FreeBoundEmissionCDF,
        LevelIdxs2LineIdx,
        LevelIdxs2TransitionIdx,
        CollIonRateCoeffSeaton,
        CollRecombRateCoeff,
        RawCollIonTransProbs,
        ContinuumInteractionHandler,
        BoundFreeOpacityInterpolator,
        FreeFreeOpacity,
        ContinuumOpacityCalculator,
        BetaSobolev,
        FreeFreeFrequencySampler,
        FreeBoundFrequencySampler,
    ]
)
adiabatic_cooling_properties = PlasmaPropertyCollection([AdiabaticCoolingRate])
two_photon_properties = PlasmaPropertyCollection(
    [
        RawTwoPhotonTransProbs,
        TwoPhotonData,
        TwoPhotonEmissionCDF,
        TwoPhotonFrequencySampler,
    ]
)

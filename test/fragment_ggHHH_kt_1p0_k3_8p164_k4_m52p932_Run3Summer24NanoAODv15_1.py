import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer(
    "ExternalLHEProducer",
    args=cms.vstring(
        "/eos/home-s/smeriano/gridPacks_HHH_HEFT_bases_and_more/"
        "ggHHH_kt_1p0_k3_8p164_k4_m52p932_"
        "el8_amd64_gcc11_CMSSW_13_0_14_tarball.tar.xz"
    ),
    nEvents=cms.untracked.uint32(5000),
    generateConcurrently=cms.untracked.bool(False),
    numberOfParameters=cms.uint32(1),
    outputFile=cms.string("cmsgrid_final.lhe"),
    scriptName=cms.FileInPath(
        "GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh"
    ),
)

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter(
    "Pythia8ConcurrentHadronizerFilter",
    maxEventsToPrint=cms.untracked.int32(1),
    pythiaPylistVerbosity=cms.untracked.int32(1),
    filterEfficiency=cms.untracked.double(1.0),
    pythiaHepMCVerbosity=cms.untracked.bool(False),
    comEnergy=cms.double(13600.0),

    PythiaParameters=cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,

        processParameters=cms.vstring(
            # Higgs mass
            "25:m0 = 125.0",

            # Allow each Higgs to decay only to bb or tau tau.
            "25:onMode = off",
            "25:onIfMatch = 5 -5",
            "25:onIfMatch = 15 -15",

            # Require exactly:
            #   gg -> HHH -> (H -> bb)(H -> bb)(H -> tau tau)
            "ResonanceDecayFilter:filter = on",
            "ResonanceDecayFilter:exclusive = on",
            "ResonanceDecayFilter:eMuTauAsEquivalent = off",
            "ResonanceDecayFilter:mothers = 25",
            "ResonanceDecayFilter:daughters = 5,5,5,5,15,15",
        ),

        parameterSets=cms.vstring(
            "pythia8CommonSettings",
            "pythia8CP5Settings",
            "pythia8PSweightsSettings",
            "processParameters",
        ),
    ),
)

ProductionFilterSequence = cms.Sequence(generator)
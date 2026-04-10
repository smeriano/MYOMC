import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring(
        '/eos/home-s/smeriano/ttHH_EFT_LO_undecayed_SM_output_v1/ttHH_EFT_LO_undecayed_kl_1p0_kt_1p0_ct2_0p0_slc7_amd64_gcc700_CMSSW_12_4_8_tarball.tar.xz'
    ),
    nEvents = cms.untracked.uint32(5000),
    generateConcurrently = cms.untracked.bool(True),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13600.),

    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,

        processParameters = cms.vstring(
            # --------------------------------------------------
            # Higgs decays: allow only H -> bb and H -> tautau
            # --------------------------------------------------
            '25:onMode = off',
            '25:oneChannel = 1 0.0 100 5 -5',
            '25:addChannel = 1 0.0 100 15 -15',

            # Optional: let top quarks decay normally
            # (remove or modify only if you want specific top decays)
            '6:onMode = on',
        ),

        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'pythia8PSweightsSettings',
            'processParameters',
        )
    )
)
import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer(
    "ExternalLHEProducer",
    args = cms.vstring(
        '/eos/home-s/smeriano/private_gridpacks_ttHH/ttHH_EFT_LO_undecayed_kl_17p54_kt_1p824_ct2_7p422_el8_amd64_gcc11_CMSSW_13_0_14_tarball.tar.xz'
    ),
    nEvents = cms.untracked.uint32(5000),
    generateConcurrently = cms.untracked.bool(False),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter(
    "Pythia8ConcurrentHadronizerFilter",
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
            # Basic particle settings
            # --------------------------------------------------

            '25:m0 = 125.0',         # Set Higgs mass to 125 GeV

            # --------------------------------------------------
            # Higgs decay configuration
            # --------------------------------------------------

            '25:onMode = off',       # Turn OFF all Higgs decays first
            '25:onIfMatch = 5 -5',   # Allow H -> b b̄
            '25:onIfMatch = 15 -15', # Allow H -> τ+ τ-

            # Result: each Higgs can decay either to bb or ττ

            # --------------------------------------------------
            # Top quark decays
            # --------------------------------------------------

            '6:onMode = on',         # Let top quarks decay inclusively (no constraint)

            # NOTE:
            # This means the tt system is NOT restricted.
            # Only the Higgs decays are constrained by the filter below.

            # --------------------------------------------------
            # Resonance decay filter
            # --------------------------------------------------

            'ResonanceDecayFilter:filter = on',      # Activate decay-based event filter
            'ResonanceDecayFilter:exclusive = on',   # Require EXACT match to daughters list

            # Treat particle categories as equivalent for filtering
            'ResonanceDecayFilter:eMuTauAsEquivalent = on', # e, μ, τ treated as equivalent
                                                        # not strictly needed here, since we request τ explicitly
            # 'ResonanceDecayFilter:wzAsEquivalent = on',     # W/Z treated as equivalent (irrelevant here)
            # 'ResonanceDecayFilter:allNuAsEquivalent = on',  # all neutrinos equivalent (irrelevant here)
            # 'ResonanceDecayFilter:udscAsEquivalent = on',   # u, d, s, c quarks equivalent (irrelevant here)

            # Define which resonances we are filtering on
            'ResonanceDecayFilter:mothers = 25',     # Look only at Higgs bosons

            # --------------------------------------------------
            # Target final state: ttHH → bbττ
            # --------------------------------------------------

            'ResonanceDecayFilter:daughters = 5,5,15,15',

            # Interpretation:
            #   5,5     → one Higgs → b b̄
            #   15,15   → one Higgs → τ+ τ-
            #
            # So this enforces:
            #   ttHH → (H→bb) + (H→ττ)
            #
            # The top quarks remain fully inclusive:
            #   t  -> W b
            #   t̄ -> W b̄
            # with no restriction on the W decays
        ),

        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'pythia8PSweightsSettings',
            'processParameters',
        )
    )
)

ProductionFilterSequence = cms.Sequence(generator)
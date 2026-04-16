import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer(
    "ExternalLHEProducer",
    args = cms.vstring(
        '/eos/home-s/smeriano/ttHH_EFT_LO_undecayed_SM_output_el8_amd64_gcc11_CMSSW_13_0_14/ttHH_EFT_LO_undecayed_kl_1p0_kt_1p0_ct2_0p0_el8_amd64_gcc11_CMSSW_13_0_14_tarball.tar.xz'
    ),
    nEvents = cms.untracked.uint32(5000),
    generateConcurrently = cms.untracked.bool(False),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
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

            '24:mMin = 0.05',        # Avoid extremely low-mass W* (off-shell protection)
            '24:onMode = on',        # Allow W bosons to decay (default, but explicit for clarity)

            '25:m0 = 125.0',         # Set Higgs mass to 125 GeV

            # --------------------------------------------------
            # Higgs decay configuration
            # --------------------------------------------------

            '25:onMode = off',       # Turn OFF all Higgs decays first
            '25:onIfMatch = 5 -5',   # Allow H -> b b̄
            '25:onIfMatch = 24 -24', # Allow H -> W+ W-

            # Result: each Higgs can decay either to bb or WW

            # --------------------------------------------------
            # Top quark decays
            # --------------------------------------------------

            '6:onMode = on',         # Let top quarks decay inclusively (no constraint)

            # NOTE:
            # This means the tt system is NOT restricted.
            # "Fully hadronic" only applies to the Higgs → WW part.

            # --------------------------------------------------
            # Resonance decay filter
            # --------------------------------------------------

            'ResonanceDecayFilter:filter = on',        # Activate decay-based event filter
            'ResonanceDecayFilter:exclusive = on',     # Require EXACT match to daughters list

            # Treat particle categories as equivalent for filtering
            'ResonanceDecayFilter:eMuTauAsEquivalent = on',   # e, μ, τ treated the same (not used here, but harmless)
            'ResonanceDecayFilter:wzAsEquivalent = on',       # W/Z treated the same (irrelevant here since only WW is allowed)
            'ResonanceDecayFilter:allNuAsEquivalent = on',    # all neutrinos equivalent (not used here)
            'ResonanceDecayFilter:udscAsEquivalent = on',     # u, d, s, c quarks treated the same → important for hadronic W

            # Define which resonances we are filtering on
            'ResonanceDecayFilter:mothers = 24,25',    # Look at W bosons and Higgs bosons

            # --------------------------------------------------
            # Target final state: ttHH → bbWW with both W → qq (FH)
            # --------------------------------------------------

            'ResonanceDecayFilter:daughters = 5,5,1,1,1,1',

            # Interpretation:
            #   5,5       → one Higgs → b b̄
            #   1,1,1,1   → two W bosons → q q' and q q'
            #
            # With udscAsEquivalent = on:
            #   "1" stands for any light quark (u, d, s, c)
            #
            # So this enforces:
            #   ttHH → (H→bb) + (H→WW→qq qq)
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
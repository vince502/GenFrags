#Using cmsDriver command in CMSSW_14_1_6 cmsDriver.py Configuration/GenProduction/python/ShowerJPsitoMuMu_pTHatMin10_Pythia8TuneCP5_cfi.py --python_filename PsiToMuMuPiPi_GEN.py --eventcontent RAWSIM --datatier GEN-SIM --fileout file:Jpsi_GEN.root --conditions 141X_mcRun3_2024_realistic_ppRef5TeV_v7 --beamspot Realistic25ns13p6TeVEarly2023Collision --step GEN,SIM --geometry DB:Extended --era Run3_2024_ppRef --mc 

#------------------------------------
#GenXsecAnalyzer:
#------------------------------------
#Before Filter: total cross section = 1.811e+09 +- 1.021e+07 pb
#Filter efficiency (taking into account weights)= (210) / (10000) = 2.100e-02 +- 1.434e-03
#Filter efficiency (event-level)= (210) / (10000) = 2.100e-02 +- 1.434e-03    [TO BE USED IN MCM]
#
#After filter: final cross section = 3.802e+07 +- 2.605e+06 pb
#After filter: final fraction of events with negative weights = 0.000e+00 +- 0.000e+00
#After filter: final equivalent lumi for 1M events (1/fb) = 2.630e-05 +- 1.802e-06

# event size 406 kB/evt, 16 ms/evt in AMD EPIC Genoa CPU

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *

# see https://www.pythia.org/latest-manual/OniaShowers.html

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(5362.0),
                         maxEventsToPrint = cms.untracked.int32(0),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'HardQCD:all = on',
            'CharmoniumShower:all = on', # turn on for parton shower mode
            'OniaShower:ldmeFac = 100.',
            '443:onMode = off',
            '443:onIfAny = 13 -13', # dimuon decay
            'PhaseSpace:pTHatMin = 10.'
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
        )
)

oniafilter = cms.EDFilter("PythiaFilter",
    Status = cms.untracked.int32(2),
    MaxEta = cms.untracked.double(4),
    MinEta = cms.untracked.double(-4),
    MinPt = cms.untracked.double(0.0),
    ParticleID = cms.untracked.int32(443)
)

mumugenfilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(1, 1),
    MinPt = cms.untracked.vdouble(1., 1.),
    MinP = cms.untracked.vdouble(2.5, 2.5),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
    ParticleCharge = cms.untracked.int32(-1),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(13)
)

ProductionFilterSequence = cms.Sequence(generator*oniafilter*mumugenfilter)

#Benchmark with command line options in CMSSW_14_1_6: Configuration/GenProduction/python/Psi2StoMuMuPiPi_pTHatMin4_5p36TeV_Pythia8TuneCP5_cfi.py --python_filename PsiToMuMuPiPi_GEN.py --eventcontent RAWSIM --datatier GEN-SIM --fileout file:Jpsi_GEN.root --conditions 141X_mcRun3_2024_realistic_ppRef5TeV_v7 --beamspot Realistic25ns13p6TeVEarly2023Collision --step GEN,SIM --geometry DB:Extended --era Run3_2024_ppRef --mc

#------------------------------------
#GenXsecAnalyzer:
#------------------------------------
#Before Filter: total cross section = 4.042e+06 +- 1.950e+04 pb
#Filter efficiency (taking into account weights)= (255.763) / (1653.15) = 1.547e-01 +- 4.040e-03
#Filter efficiency (event-level)= (1829) / (10000) = 1.829e-01 +- 3.866e-03    [TO BE USED IN MCM]
#
#After filter: final cross section = 6.254e+05 +- 1.661e+04 pb
#After filter: final fraction of events with negative weights = 0.000e+00 +- 0.000e+00
#After filter: final equivalent lumi for 1M events (1/fb) = 1.599e-03 +- 4.249e-05

# 0.510 sec/event in AMD EPYC-Genoa Processor, 332 kB/event

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(5362.0),
                         maxEventsToPrint = cms.untracked.int32(0),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'Charmonium:states(3S1) = 100443', # filter on 100443 and prevents other onium states decaying to 100443, so we should turn the others off
            'Charmonium:O(3S1)[3S1(1)] = 1.16',
            'Charmonium:O(3S1)[3S1(8)] = 0.0119',
            'Charmonium:O(3S1)[1S0(8)] = 0.01',
            'Charmonium:O(3S1)[3P0(8)] = 0.01',
            'Charmonium:gg2ccbar(3S1)[3S1(1)]g = on',
            'Charmonium:gg2ccbar(3S1)[3S1(8)]g = on',
            'Charmonium:qg2ccbar(3S1)[3S1(8)]q = on',
            'Charmonium:qqbar2ccbar(3S1)[3S1(8)]g = on',
            'Charmonium:gg2ccbar(3S1)[1S0(8)]g = on',
            'Charmonium:qg2ccbar(3S1)[1S0(8)]q = on',
            'Charmonium:qqbar2ccbar(3S1)[1S0(8)]g = on',
            'Charmonium:gg2ccbar(3S1)[3PJ(8)]g = on',
            'Charmonium:qg2ccbar(3S1)[3PJ(8)]q = on',
            'Charmonium:qqbar2ccbar(3S1)[3PJ(8)]g = on',
            'Charmonium:gg2ccbar(3S1)[3S1(1)]gm = on',
            '100443:onMode = off',            # ignore cross-section re-weighting (CSAMODE=6) since selecting wanted decay mode
            '100443:onIfAny = 443 211 -211',
            '443:onMode = off',
            '443:onIfMatch = 13 -13',
            'PhaseSpace:pTHatMin = 2.0',
            'PhaseSpace:bias2Selection = on',
            'PhaseSpace:bias2SelectionPow = 1.3',
            'PhaseSpace:bias2SelectionRef = 1'
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
        )
)

psi2SIDfilter = cms.EDFilter("PythiaFilter",
    Status = cms.untracked.int32(2),
    MaxEta = cms.untracked.double(3.0),
    MinEta = cms.untracked.double(-3.0),
    MinPt = cms.untracked.double(0.0),
    ParticleID = cms.untracked.int32(100443)
)

jpsiIDfilter = cms.EDFilter("PythiaFilter",
    ParticleID = cms.untracked.int32(443),
    MinPt = cms.untracked.double(0.0),
    MinEta = cms.untracked.double(-3.0),
    MaxEta = cms.untracked.double(3.0),
    Status = cms.untracked.int32(2)
)

mumugenfilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(1, 1),
    MinPt = cms.untracked.vdouble(1., 1.),
    MinP = cms.untracked.vdouble(0.0, 0.0),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
    ParticleCharge = cms.untracked.int32(-1),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(13)
)
piminusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(0),
    MinPt = cms.untracked.vdouble(0.0),
    ParticleID = cms.untracked.int32(100443),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(-3.0),
    MaxEta = cms.untracked.vdouble(3.0),
    NumberDaughters = cms.untracked.int32(1),
    DaughterIDs = cms.untracked.vint32(-211)
)
piplusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(0),
    MinPt = cms.untracked.vdouble(0.0),
    ParticleID = cms.untracked.int32(100443),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(-2.4),
    MaxEta = cms.untracked.vdouble(2.4),
    NumberDaughters = cms.untracked.int32(1),
    DaughterIDs = cms.untracked.vint32(211)
)

ProductionFilterSequence = cms.Sequence(generator*psi2SIDfilter*jpsiIDfilter*mumugenfilter*piminusfilter*piplusfilter)

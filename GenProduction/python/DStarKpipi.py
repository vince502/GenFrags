import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

_generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(5360.0),
    maxEventsToPrint = cms.untracked.int32(0),

    ExternalDecays = cms.PSet(
                           EvtGen130 = cms.untracked.PSet(
                           decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
                           particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_0.1kpilifetime.pdl'),
                           user_decay_embedded = cms.vstring(
"""
Alias      MyDstar   D*+
Alias      Myanti-Dstar   D*-
ChargeConj MyDstar     Myanti-Dstar

Alias      MyD0   D0
Alias      Myanti-D0   anti-D0
ChargeConj Myanti-D0   MyD0
#
Alias Mypi+ pi+
Alias Mypi- pi-
ChargeConj Mypi- Mypi+


Decay MyDstar
1.000   MyD0   Mypi+    VSS;
Enddecay
CDecay Myanti-Dstar

#
Decay MyD0
1.000   K- pi+  PHSP;
Enddecay
CDecay Myanti-D0
#
End
"""
),
                           list_forced_decays = cms.vstring('MyD0', 'Myanti-D0','MyDstar','Myanti-Dstar'),
                           convertPythiaCodes = cms.untracked.bool(False)
                         ),
                         operates_on_particles = cms.vint32(),
                         parameterSets = cms.vstring('EvtGen130')
                         ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
	    "SoftQCD:nonDiffractive = on",
            'PTFilter:filter = on', 
            'PTFilter:quarkToFilter = 4', 
            'PTFilter:scaleToFilter = 1.0'
	    ),
        parameterSets = cms.vstring(
	    'pythia8CommonSettings', 
            #'pythia8CUEP8M1Settings', 
            'pythia8CP5Settings',
            'processParameters')
    )
)

from GeneratorInterface.Core.ExternalGeneratorFilter import ExternalGeneratorFilter
generator = ExternalGeneratorFilter(_generator)

### Filters 


dfilter = cms.EDFilter(
    "MCSingleParticleFilter",
    MaxEta = cms.untracked.vdouble(3.0,3.0),
    MinEta = cms.untracked.vdouble(-3.0,-3.0),
    ParticleID = cms.untracked.vint32(413,-413)
)

d0filter = cms.EDFilter(
    "MCMultiParticleFilter",
    AcceptMore = cms.bool(True),
    EtaMax = cms.vdouble(2.5, 2.5),
    EtaMin = cms.vdouble(-2.5, -2.5),
    MotherID = cms.untracked.vint32(421),
    NumRequired = cms.int32(1),
    ParticleID = cms.vint32(-321, 211),
    PtMin = cms.vdouble(0.4, 0.4),
    Status = cms.vint32(0, 0)

)

decayfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1),
    NumberDaughters = cms.untracked.int32(2),
    ParticleID      = cms.untracked.int32(413),  ## DStar+ (already chage conjugate)
    DaughterIDs     = cms.untracked.vint32(421,211), ## D0 and pi+
    MinPt           = cms.untracked.vdouble( 0. ,  0.4), ## cuts based on data
    MinEta          = cms.untracked.vdouble(-2.8, -2.8), ## cuts based on data
    MaxEta          = cms.untracked.vdouble( 2.8,  2.8) ## cuts based on data
)


ProductionFilterSequence = cms.Sequence(generator*dfilter*decayfilter*d0filter)

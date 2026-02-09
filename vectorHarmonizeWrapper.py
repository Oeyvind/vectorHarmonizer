#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A wrapper for using vectorHarmonizer from Csound

Quick and dirty adaption from ImproSculpt4 eventCaller

@author: Øyvind Brandtsegg
@contact: obrandts@gmail.com
@license: GPL
"""

from pythresh import *
from vectorHarmonizer import *
import os

# Set up logging to file
log_file = os.path.join(os.path.dirname(__file__), 'vectorHarmonizer_debug.log')
log_handle = open(log_file, 'w')

def debug_log(msg):
    """Print to console and log to file"""
    print(msg)
    log_handle.write(msg + '\n')
    log_handle.flush()

class VectorHarmWrap:
    """Wrapper for using vectorHarmonizer from Csound.
    
    A minimized version of ImproSculpt4 EventCaller class, adapted for use with
    the Vector Harmonizer algorithm.
    """

    def __init__(self):
        """Initialize the VectorHarmWrap instance."""
        self.vHarmonize = VectorHarmonizer()
        """Instance of the VectorHarmonizer composition class."""
        self.pyThresh = PyThresh(0.3) # 300 millisecond time window for thresh
        """Instance of the thresh object, similar to a MAX/MSP thresh object."""
        self.vectorHarmonizeAutoVoiceRange = True
        """Auto update of vector harmonize voice range according to midi note number used as input to the harmonizer."""
        self.pendingOnEvents = {}
        """Queue of note events to be turned on, keyed by (note, channel) tuple."""
        self.pendingOffEvents = {}
        """Queue of note events to be turned off, keyed by (note, channel) tuple."""
        self.playChannels = [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
        self.recordChannels = [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0]

    def vectorHarmonizeMidiNote(self, note, channel, instr):
        """Process and return harmonized notes for a MIDI note on event.
        
        Harmonizes a MIDI note using the vectorHarmonizer to determine harmony notes.
        Returns one note from the harmonized chord on each call.
        
        Args:
            note: MIDI note number to be harmonized.
            channel: MIDI channel of the note, used to distinguish simultaneous notes.
            instr: Instrument number used for playback of harmonizing notes.
            
        Returns:
            Tuple of (pitch, instrument_number) as floats.
        """
        key = (note, channel)
        if key not in self.pendingOnEvents:
            self.pendingOnEvents[key] = []
        if self.pendingOnEvents[key] == []:
            self._generate_harmonized_chord(note, channel, instr)
        pitch, instr = self.pendingOnEvents[key].pop(0)
        print(f'[MIDI_NOTE] Returning note {pitch} (pending: {len(self.pendingOnEvents[key])} more)')
        return float(pitch), float(instr)

    def vectorHarmonizeMidiNoteOff(self, note, channel):
        """Process and return harmonized notes for a MIDI note off event.
        
        Returns harmony notes associated with a MIDI note off event,
        one note per call.
        
        Args:
            note: MIDI note number being turned off.
            channel: MIDI channel of the note.
            
        Returns:
            Tuple of (pitch, instrument_number) as floats.
        """
        key = (note, channel)
        if key not in self.pendingOffEvents:
            self.pendingOffEvents[key] = []
        if self.pendingOffEvents[key] == []:
            self._queue_chord_off(note, channel)
        pitch, instr = self.pendingOffEvents[key].pop(0)
        return float(pitch), float(instr)

    def _generate_harmonized_chord(self, note, channel, instr):
        """Generate and queue a harmonized chord for note on event.
        
        Args:
            note: MIDI note number to be harmonized.
            channel: MIDI channel of the note.
            instr: Instrument number used for playback.
        """
        if self.vectorHarmonizeAutoVoiceRange:
            self.vHarmonize.setVoiceRange([note-self.vHarmonize.autoVoiceRangeBorder, note+self.vHarmonize.autoVoiceRangeBorder])
        chord = self.vHarmonize.harmonize(note)
        print(f'[WRAPPER] Generated chord with {len(chord)} notes: {chord}')
        chord.append(-999) #end of list flag
        key = (note, channel)
        chordInstr = self.vHarmonize.setCurrentChordForNote(key, chord, instr)
        self.pendingOnEvents[key] = []
        for pitch, instr in chordInstr:
            self.pendingOnEvents[key].append([pitch, instr])
        print(f'[WRAPPER] Queued {len(chordInstr)} harmony notes for playback: {[p[0] for p in chordInstr]}')

    def _queue_chord_off(self, note, channel):
        """Queue a harmonized chord for note off event.
        
        Args:
            note: MIDI note number being turned off.
            channel: MIDI channel of the note.
        """
        key = (note, channel)
        chordInstr = self.vHarmonize.getCurrentChordForNote(key)
        if chordInstr == []: return
        self.pendingOffEvents[key] = []
        for pitch, instr in chordInstr:
            self.pendingOffEvents[key].append([pitch, instr])

    def recordIntervalVector(self, note):
        """Record an interval vector from realtime MIDI input.
        
        Packs incoming notes within the time window and converts them to an
        interval vector, which is then set for the harmonizer.
        
        Args:
            note: MIDI note number to be analyzed as part of an interval vector.
            
        Returns:
            The computed interval vector, or None if fewer than 2 notes collected.
        """
        notelist = self.pyThresh.thresh(note)
        print(f'[RECORD_VECTOR] Input note: {note}, collected notes: {notelist}')
        if len(notelist) < 2: 
            print(f'[RECORD_VECTOR] Only {len(notelist)} notes, returning None')
            return
        vector = self.vHarmonize.makeIntervalVector(notelist)
        print('recorded vector:', vector)
        vector = self.vHarmonize.setIntervalVector(vector)
        return vector

    def getIntervalVector(self, bogus=0):
        """Get the current interval vector.
        
        Returns:
            Tuple of 6 float values representing the interval vector.
        """
        v1,v2,v3,v4,v5,v6 = self.vHarmonize.intervalVector
        return float(v1),float(v2),float(v3),float(v4),float(v5),float(v6)

    def setIntervalVectorFromPclist(self, pclist):
        """Convert a pitch class list into an interval vector.
        
        Args:
            pclist: List of pitch classes to be analyzed and converted into
                    an interval vector.
        """
        vector = self.vHarmonize.makeIntervalVector(pclist)
        vector = self.vHarmonize.setIntervalVector(vector)

    def setAutoVoiceRangeFlag(self, state):
        """Set auto voice range on or off.
        
        When enabled, the voice range is updated by each harmonized MIDI note,
        using the MIDI note number as base and voiceRangeBorder as the relative
        +/- range from the base note.
        
        Args:
            state: Boolean indicating whether to enable (True) or disable (False)
                   automatic voice range adjustment.
        """
        self.vectorHarmonizeAutoVoiceRange = state

    def setPcsetRecordThreshTime(self, time):
        """Set the time window for realtime recording of pitches.
        
        Args:
            time: Size of the time window in milliseconds.
        """
        self.pyThresh.setThreshTime(time/1000.0)

    def setVectorHarmonizeVoiceRange(self, lowHighList):
        """Set the voice range for vector harmonizing.
        
        Args:
            lowHighList: List of [low, high] MIDI note numbers for the voice range.
        """
        self.vHarmonize.setVoiceRange(lowHighList)

    def getVectorHarmonizeVoiceRange(self, bogus=0):
        """Get the current voice range.
        
        Returns:
            Tuple of (low, high) MIDI note numbers.
        """
        low = float(self.vHarmonize.voiceRange[0])
        high = float(self.vHarmonize.voiceRange[1])
        return low, high


if __name__ == '__main__' :
    vh = VectorHarmWrap()
    note = 60
    channel = 1
    instr = 100
    noteH = 0
    while noteH > -999 :
        noteH,instrH = vh.vectorHarmonizeMidiNote(note, channel, instr)
        print('on', noteH,instrH)
    noteH = 0
    while noteH > -999 :
        noteH,instrH = vh.vectorHarmonizeMidiNoteOff(note, channel)
        print('off', noteH,instrH)
    for note in [65,66,70]:
        vh.recordIntervalVector(note)
    note = 60
    noteH = 0
    while noteH > -999 :
        noteH,instrH = vh.vectorHarmonizeMidiNote(note, channel, instr)
        print('on', noteH,instrH)
    print(vh.getVectorHarmonizeVoiceRange(0))

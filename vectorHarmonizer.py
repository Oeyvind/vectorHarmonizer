#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A simple harmonizer, choosing chord alternatives from an interval vector.

@author: Øyvind Brandtsegg
@contact: obrandts@gmail.com
@license: GPL
"""

import copy
import intervalVectorsAsPcsets
from listOperations import *
#import time # for profiling

class VectorHarmonizer:
    """
    Vector harmonizer

    A simple harmonizer, choosing chord alternatives from an interval vector.
    Voice rules control the selection of the next chord and it's voicing.
    The module takes (note number) and (chord structure) as input,

    Takes a note and an intervalVector, outputs the note and a voiced chord.
    Assumes knowledge of the previous chord (melody + harmonizing notes).
    The note is harmonized according to the following voice leading rules:
        1. Use shortest possible path for voice leading
        2. Use common tones if possible
        3. Avoid parallel motion simultaneously in all voices
        4. Choose chord spread (tightly spaced or spread out)
        5. Avoid repeating the exact same chord if possible
        6. Avoid going back to the second previous chord if possible
        7. If a note in the chord is outside the voice range, give it a penalty score
        8. If the previous chord contained out of range notes, and the next chord will move even further out of range, give it an extra penalty.

    A number of alternatives for "next chord" is created using the interval vector,
    each of these alternatives is given a score according to the rules stated above.
    The alternative with the *lowest* score is chosen as the harmonizing chord
    """

    def __init__(self):
        """
        Class constructor.

        @param self: The object pointer.
        """

        self.iVP = intervalVectorsAsPcsets.PcsetFromIntervalVector()
        """Instance of the pc set from interval vector utility class."""

        self.intervalVector = (0,0,1,1,1,0)
        """The default vector for harmonizing."""
        self.pcset = [0,1,5]
        """The default stored pcset, reflects interval vector."""
        self.fractionalInstrNum = 0.01
        """Fractional instrument number used to control turnoff of csound note events with indefinite duration."""
        # default values for giving a score to the different chord alternatives
        # Do Not adjust these values here, but send parameter updates to this class from the calling class
        self.previousMelodynote = [60]
        """Previous melody note, used for checking parallel motion."""
        self.previousChord = [59, 64]
        """Previous harmonizing notes, 2 notes for 3-voice harmony."""
        self.secondPreviousChord = [59, 64]
        """The second previous, for history control (to avoid toggling back and forth between two chords)."""
        self.semitoneScoreAdjust = 0.15
        """
        Arbitrary scaling factor for score values derived from counting semitones, in relation to other score values.
        Some rules output values typically in the range 0 - 2 (chord history, parallel motion etc.),
        while other rules count semitones and may return a value in the range 5 - 20.
        This scaling factor attempts to equalize the effect of different rule types,
        enabling a more intuitive use of the score values to adjust the relation between different rules.
        """
        self.distanceScore = 1
        """Scaling factor when counting the semitones distance from chord to chord."""
        self.commonToneScore = 1
        """Higher values give preference to using chords that has common tones with self.previousChord."""
        self.voiceSpreadScore = 1
        """Higher values give preference to using chord voicings with more distance internally between notes. (e.g. [60,74] instead of [60,62])"""
        self.parallelMotionScore = 1
        """Positive values helps avoid "all voice" parallel motion."""
        self.chordRepeatScore = 1
        """Positive values indicate preference for not repeating previous chord."""
        self.chordToggleScore = 1
        """Positive values indicate preference for not going back to second previous chord."""
        self.voiceRangeScore = 1
        """Positive values indicate better range control, interacts with self.voiceRangeBorder (effectively: rangeScore divided by rangeBorder)."""
        self.voiceRangeGravity = 1
        """Positive values indicate better range control, for voices outside of the allowed voice range, keeping them from moving further out of range."""
        self.voiceRange = [48,72]
        """Voice range [low, high], in midi note numbers. Not necessarily interpreted strictly."""
        self.autoVoiceRangeBorder = 7
        """Voice Range border size when auto setting voice range via midi note (semitones +/- from the input note)."""
        self.currentChordForNote = {}
        """
        For harmonizing of midi notes, the currently playing chord and the instrument number used to play the chord must be stored,
        so the harmony notes can be turned off when stopping the midi activated note.
        This dictionary stores this information in the format: {noteNumber: [instrumentNumber, n,n,n], noteNumber2 : [instrumentNumber, n,n,n]},
        where n is used to hold note numbers in the harmony chord and there may be any number of notes in a harmony chord.
        """

    def harmonize(self, note, intervalVector=None):
        """
        The actual harmonizer method.

        @param self: The object pointer.
        @param note: The base note to harmonize over.
        @param intervalVector: The interval vector to harmonize according to (if None, use self.intervalVector).
        @return: chord, The resulting chord.
        """
        #timeThen = time.time() # for profiling
        if not intervalVector:
            intervalVector = self.intervalVector
        print(f'[HARMONIZE] Starting with previousChord size: {len(self.previousChord)}, intervalVector: {intervalVector}')
        chordAlternatives = {}
        # find all chord alternatives, store in dictionary
        # using the transposed pcset as key, and a score as value
        for pcset in self.iVP.getPcsets(intervalVector):
            # get rid of the zero in the pcset,
            # as this equals the melody note and should not be treated as harmony
            print('pcset:', pcset)
            pcset = pcset[1:]
            # transpose the rest of the pcset so that the melody note is the "fundamental" of the set
            pcset = [n + (note % 12) for n in pcset]
            print('transposed pcset:', pcset)
            # expand this pitch set by finding all valid inversions and transpositions
            notes = self.findAllValidInversions(pcset)
            print('notes:', notes)
            chords = findAllCombinationsListOfLists(notes)
            print('chords:', chords)
            for chord in chords:
                # get a score by counting semitone distance as sum for all voices.
                semitoneScore = self.semitoneCount(chord)
                # check for common tones, and adjust score accordingly
                commonScore = self.commonNotesCheck(chord)
                # check for parallel motion
                parallelScore = self.parallelCheck(note, chord)
                # check chord spread
                spreadScore = self.spreadCheck(note, chord)
                # check for repeat of previous chord, and for toggle back to second previous chord
                historyScore = self.chordHistoryCheck(chord)
                # range checking for each voice
                voiceRangeScore = self.voiceRangeCheck(chord)
                # add up all intermediate scores
                score = semitoneScore + commonScore + spreadScore + parallelScore + historyScore + voiceRangeScore
                # put chord in dictionary with it's total score
                chordAlternatives[tuple(chord)] = score
        # To choose chord:
        scorelist = list(chordAlternatives.values())
        keylist = list(chordAlternatives)
        minScoreIndex = scorelist.index(min(scorelist))
        chord = list(keylist[minScoreIndex])
        print('chosen chord score:', scorelist[minScoreIndex])
        # Update previous and second previous chords, and previous melodynote
        self.previousMelodynote = note                  # previous melody note, used for checking parallel motion
        self.secondPreviousChord = self.previousChord   # store second previous, for history control (not toggle back and forth between two chords)
        self.previousChord = chord                      # update previous with currently chosen chord
        print(f'[HARMONIZE] Returning chord with {len(chord)} notes: {chord}')
        return chord

    def setCurrentChordForNote(self, note, chord, instr):
        """
        Generate fractional instrument number for each note in a chord to be played.

        Remember the currently played chord (note number and instrument number), as used for harmonizing a midi activated note.
        This is needed to control turnoff of notes with indefinite duration, when hamonizing midi input.

        @param self: The object pointer.
        @param note: The note to be harmonized
        @param instr: the instrument number used to play the chord.
        @param chord: The chord to be used for harmonizing.
        @return: chordInstr, The notes of the chord, each with a fractional instr number (as list [note, instrNum]).
        """
        chordInstr = []
        for n in chord:
            self.fractionalInstrNum %= 0.98
            self.fractionalInstrNum += 0.01
            chordInstr.append([n,instr+self.fractionalInstrNum])
        self.currentChordForNote[note] = chordInstr
        return chordInstr

    def getCurrentChordForNote(self, note):
        """
        Get the chord and (fractional( instrument number, as used for harmonizing a note.

        This method is called to turn off notes with indefinite duration, when hamonizing midi input.
        The internal memory of the chord will be deleted, so each chord can only be recalled once.

        @param self: The object pointer.
        @param note: The note to find the currently playing chord for.
        @return: chordInstr, the currently playing chord as used to harmonize note (a list of [note, instrument number] for each note in the chord).
        """
        chord = self.currentChordForNote[note]
        self.currentChordForNote[note] = []
        return chord

    def findAllValidInversions(self, pcset):
        """
        Finds inversions and transpositions of a pc set.

        Find all valid inversions and transpositions related to the previous chord,
        so that the maximum leap for any single voice is one octave.
        Returns a list of chords.

        @param self: The object pointer.
        @param pcset: The pc set to find valid inversions for.
        @return: notes, List of lists (of notes) with all valid chord inversions of the pc set.
        """
        # For each unique pitch class, find all valid octaviations
        print('pcset:', pcset)
        print('previousChord:', self.previousChord)
        notes = []
        # find all octaviations of pitches, within octave range from previous pitches
        for pc in pcset:
            tempNotes = []
            # transpose up by octaves until within one octave range below previous lowest chord note
            while pc < (min(self.previousChord) - 12):
                pc = pc + 12
            tempNotes.append(pc)
            print('tempNotes after transposing up:', tempNotes)
            # continue transposing, stop when exceeding one octave range above previous highest chord note
            while pc <= max(self.previousChord):
                pc = pc + 12
                tempNotes.append(pc)
                print('tempNotes during transposing up:', tempNotes)
            notes.append(tempNotes)
        return notes

    def semitoneCount(self, chord):
        """
        Returns the total distance in semitones from self.previousChord to chord.

        @param self: The object pointer.
        @param chord: The chord to analyze.
        @return: semitoneScore, the sum of distances, multiplied with user set score for distance.
        """
        distancelist = []
        for i in range(0, len(self.previousChord)):
            try:
                # count the number of semitones from previous note to this note
                distance = abs(chord[i] - self.previousChord[i])
            except:
                # in case size of chord has changed
                distance = 0
            distancelist.append(distance)
        semitoneScore = (sum(distancelist) * self.distanceScore) / float(len(self.previousChord)) * self.semitoneScoreAdjust
        return semitoneScore

    def commonNotesCheck(self, chord):
        """
        Checks for common notes between self.previousChord and chord.

        @param self: The object pointer.
        @param chord: The chord to analyze.
        @return: commonNoteScore, The number of common notes, multiplied with the user set score for common notes.
        """

        # added score (or penalty) for common tones
        commonNoteScore = 0
        for i in range(0, len(self.previousChord)):
            try:
                if chord[i] == self.previousChord[i]:
                    commonNoteScore += 1
            except:
                # in case size of chord has changed
                pass
        return commonNoteScore * (-self.commonToneScore)

    def spreadCheck(self, note, chord):
        """
        Checks the internal spread (distance between chord notes) of the chord, including the melody note to be harmonized.

        @param self: The object pointer.
        @param note: The melody note
        @param chord: The chord to analyze.
        @return: spreadScore, A score value representing the total internal distance in semitones between notes in the chord.
        """
        newchord = copy.copy(chord)
        newchord.append(note)
        semitones = 0
        numInterval = 1.0
        while len(newchord) > 1:
            for each in firstToAllSecond(newchord):
                semitones += abs(each[1]-each[0])
                numInterval += 1
            newchord.pop(0)
        return ((semitones*self.voiceSpreadScore)/numInterval)*self.semitoneScoreAdjust

    def parallelCheck(self, note, chord):
        """
        Checks for parallel motion in voice leading, including the melody note to be harmonized.

        @param self: The object pointer.
        @param note: The melody note
        @param chord: The chord to analyze.
        @return: parallelMotionScore, A score value representing the balance between parallel and contrary motion from the previous chord to this chord.
        """

        newchord = copy.copy(chord)
        newchord.append(note)
        oldchord = copy.copy(self.previousChord)
        oldchord.append(self.previousMelodynote)
        direction = 0
        for i in range(0, len(oldchord)):
            try:
                semitones = newchord[i] - oldchord[i]
                if semitones > 0:
                    direction = direction + 1
                elif semitones < 0 :
                    direction = direction - 1
            except:
                pass
        direction = abs(direction) # regardless of the direction of parallel motion
        if direction < 2: direction = 0 # we want a score if there is 2 or more voices moving in the same direction, and there is not at least one voice moving in the opposite direction.
        return direction*self.parallelMotionScore


    def chordHistoryCheck(self, chord):
        """
        Check for exact repeat of previous or second previous chord.

        @param self: The object pointer.
        @param chord: The chord to analyze.
        @return: historyScore, A single score value (sum of the two tests) if repeats found, zero if no repeats.
        """
        historyScore = 0
        if chord == self.previousChord:
            historyScore = self.chordRepeatScore
        if chord == self.secondPreviousChord:
            historyScore = historyScore + self.chordToggleScore
        return historyScore


    def voiceRangeCheck(self,chord):
        """
        Checks the voice range for each voice in chord.

        If a note is outside of the specified upper or lower border for normal range, it is considered to be in the "gravity field"..
        The algorithm gives a penalty to chord suggestions that make the voice go into the gravity field.
        The further into the gravity field, the higher the penalty, allowing for "slightly out of range" voices.
        The full suggested range for a voice could be considered to be "specified range + gravity field",
        but there's no guarantee that out of range notes will not occur. Under normal circumstances, one should not get many of them though.
        If it is already in the gravity field,
        chord suggestions that make the voice go even further out of range are given additional penalty.

        @param self: The object pointer.
        @param chord: The chord to analyze.
        @return: penalties, The voice range penalties.
        """

        penalties = 0
        for i in range(0, len(chord)):
            # reset penalties
            rangePenaltyLo = 0
            rangePenaltyHi = 0
            gravityPenaltyLo = 0
            gravityPenaltyHi = 0

            # test if the note is within any of the upper or lower gravity field,
            # essentially, if it is out of voice range
            fieldLo = chord[i] - self.voiceRange[0]
            fieldHi = self.voiceRange[1] - chord[i]
            # Calculate penalty based on how far into the field the note is
            if fieldLo < 0:
                rangePenaltyLo = abs(fieldLo)
            if fieldHi < 0:
                rangePenaltyHi = abs(fieldHi)
            # Additional penalty for moving further away from allowed range, further into the gravity field.
            # The previous chord note acts as a "zero gravity" threshold,
            # giving no gravity penalty if the new note moves inwards towards the allowed voice range
            if rangePenaltyLo > 0:
                if min(self.previousChord) > self.voiceRange[0]: #if the previous chord note was inside range
                    gravityPenaltyLo = 0
                else:
                    gravityPenaltyLo = min(self.previousChord) - chord[i]
                if gravityPenaltyLo < 0: gravityPenaltyLo = 0
            if rangePenaltyHi > 0:
                if max(self.previousChord) < self.voiceRange[1]: #if the previous chord note was inside range
                    gravityPenaltyHi = 0
                else:
                    gravityPenaltyHi = chord[i] - max(self.previousChord)
                if gravityPenaltyHi < 0: gravityPenaltyHi = 0
            penalties = penalties + \
                        ((rangePenaltyLo + rangePenaltyHi) * self.voiceRangeScore) + \
                        ((gravityPenaltyLo + gravityPenaltyHi) * self.voiceRangeGravity)
        return penalties*self.semitoneScoreAdjust

    def setVoiceRange(self, voiceRangeList):
        """
        Set the voice range.

        @param self: The object pointer.
        @param voiceRangeList: The list of [low,high] note numbers for the voice range.
        """
        self.voiceRange = voiceRangeList

    def makeIntervalVector(self, notelist):
        """
        Analyse a set of note numbers and make an interval vector.

        @param self: The object pointer.
        @param notelist: The list of note numbers to analyze
        @return: The interval vector as a list.
        """
        intervals = []
        notelist.sort()
        pcset = [(int(note) % 12) for note in notelist]
        # set pcset
        self.pcSet = pcset
        #pcsetCopy = copy.copy(pcset)
        length = len(pcset)
        basePc = pcset[0]
        #compare all to all and find intervals
        while len(pcset) > 1:
            for each in firstToAllSecond(pcset):
                interval = abs(each[1]-each[0])
                if interval != 0:
                    intervals.append(interval)
            pcset.pop(0)
        vector = [0,0,0,0,0,0]
        for interval in intervals:
            if interval > 6:
                # interval equivalence above tritone
                interval = 12 - interval
            i = interval-1 # the vector index for this interval
            vector[i] += 1
        return vector

    def setIntervalVector(self, vector):
        """
        Set the interval vector used as default for harmonizing.

        The harmonize() method may be called with a vector argument, in which case the default vector will not be used.
        Also initializes previousChord and secondPreviousChord to match the expected chord size.

        @param self: The object pointer.
        @param vector: The interval vector as a list of 6 values.
        @return: The currently set interval vector, use the previously stored vector if the input vector was not valid.
        """
        vector = tuple(vector)
        if vector not in self.iVP.getVectors():
            return self.intervalVector
        self.intervalVector = vector
        
        # Initialize previousChord to match the expected chord size
        # Get a sample pcset to determine the harmony size (pcset size - 1, since we remove the 0)
        pcsets = self.iVP.getPcsets(vector)
        if pcsets:
            harmony_size = len(pcsets[0]) - 1  # Size after removing the [0]
            # Initialize previousChord with neutral values based on the expected size
            # Use the middle of the voice range
            middle_note = (self.voiceRange[0] + self.voiceRange[1]) // 2
            self.previousChord = [middle_note + i for i in range(harmony_size)]
            self.secondPreviousChord = list(self.previousChord)
            print(f'Initialized previousChord for {harmony_size}-note harmony: {self.previousChord}')
        
        return self.intervalVector

def test():
    vh = VectorHarmonizer()
    vh.previousMelodynote = [60]
    vh.previousChord = [71, 55]#[44, 79]
    vh.secondPreviousChord = [71, 67]#[44, 79]
#    vh.voiceRange[0] = [60,77] # for voice 1
#    vh.voiceRange[1] = [60,77] # for voice 2
    vh.setIntervalVector((0,0,1,1,1,0))
    print('************')
    note = 60
    h = vh.harmonize(note)
    print(note, h)
    print('************')
    h = vh.harmonize(note)
    print(note, h)
    print('************')
    for note in range(50,71):
        h = vh.harmonize(note)
        print(note, h)
    print('************')

if __name__ == '__main__' :
    test()

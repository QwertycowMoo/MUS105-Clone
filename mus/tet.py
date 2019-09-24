###############################################################################
## @file
#  Twelve-tone Equal Temperament (TET).
#
#  The standard scale in western music divides the octave into twelve equal
#  divisions tuned to the frequency of A440 (440 Hertz). This module defines
#  an API that allows users to map between four common representations of
#  TET information:
#  1. Hertz frequency (cycles per second). A440 is 440.0 Hz and middle C
#     is 261.625 Hz.
#  2. MIDI key numbers (integers). MIDI key numbers range from 0 to 127.
#     A440 is the MIDI key number 69 and middle C is key number 60.
#  3. Pitch names (strings). A pitch name consists of a letter, an optional
#     accidental, and an octave number. The middle C octave is 4, so A440
#     is the pitch string 'A4' and middle C is 'C4'. The pitch strings 'B#3'
#     and 'Dbb4' are enharmonic spellings of 'C4', etc.
#  4. Pitch classes (integers). PCs range from 0 to 11 and represent the
#     ordinal positions of the chromatic scale without respect to octaves
#     or pitch spelling.  For example, the PC 0 represents any key number
#     or pitch that sounds like some octave multiple of 'C': e.g. 60,
#     72, 'C3', 'C5', 'B#4', 'Dbb8',  and so on.

import math


## Returns the midi key number for a given hertz frequency.
#  The formula for mapping frequency to midi key numbers is
#  69 + log2(hertz/440.0) * 12 rounded to the nearest integer.
#  @param hertz  The hertz frequency to convert.
#  @returns  An integer midi key number 0 - 127.
#
#  The function should raise a ValueError if the input
#  is not a positive number or does not produce a valid
#  midi key number.
def hertz_to_midi(hertz): #done

    hertzConv = round(69 + math.log((hertz/440), 2) * 12)
    if hertzConv < 128 and hertzConv >= 0:
        return hertzConv
    else:
        raise ValueError("The hertz value is outside of the valid MIDI range of 0-127. Your value was {}".format(hertzConv))

# Returns the hertz value for a given midi key number.
#  The formula for mapping midi key numbers into hertz is
#  440.0 * 2 ** ((midi-69)/12).
#  @param midi  The midi key number to convert.
#  @returns the hertz frequency of the midi key number.
#
#  The function should raise a ValueError if the input
#  is not a valid midi key number.
def midi_to_hertz(midi): #done
    if check_midi(midi) and isinstance(midi, int):
        return 440.0 * 2 ** ((round(midi) - 69) / 12)
    else:
        raise ValueError("The MIDI value is outside the valid MIDI range. Your input was {}".format(midi))


## Returns the pitch class integer for a given midi key number.
#  The formula for converting a midi key number into a pitch class
#  is: midi % 12.
#  @param midi  The midi key number to convert.
#  @returns An integer pitch class 0 - 11.
#
#  The function should raise a ValueError if the input is not valid
#  midi key number.
def midi_to_pc(midi):
    if check_midi(midi):
        #will have to round the midi
        return round(midi) % 12
    else:
        raise ValueError("The MIDI value is outside the valid MIDI range. Your input was {}".format(midi))

## Converts a pitch name into a midi key number. The BNF grammar of a
#  pitch string is:
# @code
#  <pitch> :=  <letter>, [<accidental>], <octave>
#  <letter> := 'C' | 'D' | 'E' | 'F' | 'G' | 'A' | 'B'
#  <accidental> := <2flat> | <flat> | <natural> | <sharp> | <2sharp>
#  <2flat> := 'bb' | 'ff'
#  <flat> := 'b' | 'f'
#  <natural> := ''
#  <sharp> := '#' | 's'
#  <2sharp> := '##' | 'ss'
#  <octave> := '00' | '0' | '1'  | '2'  | '3'  | '4'  | '5'  | '6'
#              '7'  | '8'  | '9'
# @endcode
#  The lowest possible pitch is 'C00' (key number 0) and then highest is
#  'Abb9' (key number 127 spelled with a double flat ). The pitch 'C4' is
#  midi key number 60 and 'A4' is midi key number 69. Examples of pitch
#  names: 'C4', 'F##2', 'Gs8', 'Bb3', 'Df00'.
#  @param pitch  The pitch name (string) to convert.
#  @returns An integer midi key number 0-127.
#
#  The function should signal a ValueError if the input is not a valid
#  pitch name or produces an invalid midi key number.
def pitch_to_midi(pitch):
    if isinstance(pitch, str):
        pitchList = list(pitch)
    else:
        raise ValueError("Your input pitch is not a valid pitch")
    #              0      2      4   5      7      9     11  Used to find the midi key for a pitch class
    # just use a dictionary dummy
    # dictionary.get('key','if not found')
    letterDict = {'C':0,
                  'D':2,
                  'E':4,
                  'F':5,
                  'G':7,
                  'A':9,
                  'B':11,}

    # .upper used if the user tries to use a lowercase letter
    midi = letterDict.get(pitchList[0],"Not Found")
    if midi != "Not Found":
    #checks for #, ##, b, bb, and natural and nothing else
        if pitchList[1] == '#' or pitchList[1] == 's':
            #if "##"
            if pitchList[2] == '#' or pitchList[2] == 's':
                midi += 2
                #checks for a valid octave number, makes sure there are no other characters other than digits
                if check_if_valid_octave(pitchList, 3):
                    #finds the midi number
                    return find_octave_in_pitch(pitchList, midi)
                    #checks the midi number to see if it is in the valid midi range and raises and error if not

                else:
                    raise ValueError("The input pitch is not a valid pitch")
            #if "#"
            else:
                midi += 1
                if check_if_valid_octave(pitchList, 2):
                    return find_octave_in_pitch(pitchList, midi)
                else:
                    raise ValueError("The input pitch is not a valid pitch")
        # if flats
        elif pitchList[1] == 'b' or pitchList[1] == 'f':
            #if 'bb'
            if pitchList[2] == 'b' or pitchList[2] == 'f':
                midi -= 2
                if check_if_valid_octave(pitchList, 3):
                    return find_octave_in_pitch(pitchList, midi)

                else:
                    raise ValueError("The input pitch is not a valid pitch")
            #if 'b'
            else:
                midi -= 1
                if check_if_valid_octave(pitchList, 2):
                    return find_octave_in_pitch(pitchList, midi)

                else:
                    raise ValueError("The input pitch is not a valid pitch")
        #needs to check if there are any other characters in the pitch other than numbers, uses check_if_valid_octave
        else:
            if check_if_valid_octave(pitchList, 1):
                return find_octave_in_pitch(pitchList, midi)
            else:
                raise ValueError("The input pitch is not a valid pitch")
    else:
        raise ValueError("The input pitch is not a valid pitch")

#checking for 00 vs 0
#creates a string with all numbers in the pitch
#then returns the total midi value with the appropriate amount of octaves
#throws Value Error if outside the valid midi range

def find_octave_in_pitch(pitchList, midi):

    octaves = [num for num in pitchList if num.isdigit()]
    octaves = ''.join(octaves)
    if octaves == '':
        raise ValueError("The input pitch is not a valid pitch")

    if octaves == '00':
        return midi
    elif len(octaves) < 2:
        midi += (int(octaves) + 1) * 12
        if check_midi(midi):
            return midi
        else:
            raise ValueError(
                "The input pitch is outside the valid MIDI range of 0-127. Your MIDI value was {}".format(midi))
    else:
        raise ValueError("The input pitch is not a valid pitch")

#Checks if the rest of the pitch is a valid pitch string, specifically the octave
def check_if_valid_octave(pitchList, preceedingChars):
    for num in range(preceedingChars, len(pitchList)):
        if not(str(pitchList[num]).isdigit()):
            return False
    return True
## Returns a pitch name for the given key number.
#  If no accidental is proved in the call, white key numbers produce
#  pitch names with no accidentals and black key numbers return C# Eb F# Ab Bb.
#  If an accidental is provided the pitch returned must use that accidental.
#  @param midi  the integer midi key number to convert.
#  @param accidental an optional argument that forces the returned pitch
#  to use the accidental provided
#  @returns A midi pitch name.
#
#  The function should raise a ValueError if the midi key number
#  is invalid or if the pitch requested does not support the specified
#  accidental.
def midi_to_pitch(midi, accidental=None):
    #can redo using a dictionary
    #or do a 3 lists, pitch class, accidental, and octave
    keyList = ['C','D','E','F','G','A','B']
    accidentalList = ['bb','ff','b','f','','#','s','##','ss']
    octaveList = ['00','0','1','2','3','4','5','6','7','8','9']
    #still need to check how the edge case of B# works
    if check_midi(midi):
        noteNumPitch = divmod(midi, 12)
        octave = noteNumPitch[0]
        if octave == 0:
            octave = '00'
        else:
            octave = str(noteNumPitch[0] - 1)
        if noteNumPitch[1] == 0:
            if accidental == 'bb' or accidental == 'ff':
                return 'Dbb'+ octave
            elif accidental == '#' or accidental == 's':
                return 'B#' + str((int(octave) - 1))
            elif accidental == None:
                return 'C' + octave
            else:
                raise ValueError("Pitch requested is not valid based on the midi number of {}".format(midi))
        if noteNumPitch[1] == 1:
            if accidental == 'b' or accidental == 'f':
                return 'Db' + octave
            elif accidental == '#' or accidental == 's' or accidental == None:
                return 'C#' + octave
            else:
                raise ValueError("Pitch requested is not valid based on the midi number of {}".format(midi))
        if noteNumPitch[1] == 2:
            if accidental == 'bb' or accidental == 'ff':
                return 'Ebb' + octave
            elif accidental == '##' or accidental == 'ss':
                return 'C##' + octave
            elif accidental == None:
                return 'D' + octave
            else:
                raise ValueError("Pitch requested is not valid based on the midi number of {}".format(midi))
        if noteNumPitch[1] == 3:
            if accidental == '#' or accidental == 's':
                return 'D#' + octave
            elif accidental == 'b' or accidental == 'f' or accidental == None:
                return 'Eb' + octave
            else:
                raise ValueError("Pitch requested is not valid based on the midi number of {}".format(midi))
        if noteNumPitch[1] == 4:
            if accidental == 'b' or accidental == 'f':
                return 'Fb' + octave
            elif accidental == '##' or accidental == 'ss':
                return 'D##' + octave
            elif accidental == None:
               return 'E' + octave
            else:
                raise ValueError("Pitch requested is not valid based on the midi number of {}".format(midi))
        if noteNumPitch[1] == 5:
            if accidental == 'bb' or accidental == 'ff':
                return 'Gbb' + octave
            elif accidental == '#' or accidental == 's':
                return 'E#' + octave
            elif accidental == None:
               return 'F' + octave
            else:
                raise ValueError("Pitch requested is not valid based on the midi number of {}".format(midi))

        if noteNumPitch[1] == 6:
            if accidental == 'b' or accidental == 'f':
                return 'Gb' + octave
            elif accidental == '#' or accidental == 's' or accidental == None:
                return 'F#' + octave
            else:
                raise ValueError("Pitch requested is not valid based on the midi number of {}".format(midi))
        if noteNumPitch[1] == 7:
            if accidental == 'bb' or accidental == 'ff':
                return 'Abb' + octave
            elif accidental == '##' or accidental == 'ss':
                return 'F##' + octave
            elif accidental == None:
                return 'G' + octave
            else:
                raise ValueError("Pitch requested is not valid based on the midi number of {}".format(midi))

        if noteNumPitch[1] == 8:
            if accidental == 'b' or accidental == 'f' or accidental == None:
                return 'Ab' + octave
            elif accidental == '#' or accidental == 's':
                return 'G#' + octave
            else:
                raise ValueError("Pitch requested is not valid based on the midi number of {}".format(midi))
        if noteNumPitch[1] == 9:
            if accidental == 'bb' or accidental == 'ff':
                return 'Bbb' + octave
            elif accidental == '##' or accidental == 'ss':
                return 'G##' + octave
            elif accidental == None:
                return 'A' + octave
            else:
                raise ValueError("Pitch requested is not valid based on the midi number of {}".format(midi))

        if noteNumPitch[1] == 10:
            if accidental == 'bb' or accidental == 'ff':
                return 'Cbb' + str(int(octave) + 1)
            if accidental == 'b' or accidental == 'f' or accidental == None:
                return 'Bb' + octave
            elif accidental == '#' or accidental == 's':
                return 'A#' + octave
            else:
                raise ValueError("Pitch requested is not valid based on the midi number of {}".format(midi))

        if noteNumPitch[1] == 11:
            if accidental == 'b' or accidental == 'f':
                return 'Cb' + octave
            elif accidental == '##' or accidental == 'ss':
                return 'A##' + octave
            elif accidental == None:
                return 'B' + octave
            else:
                raise ValueError("Pitch requested is not valid based on the midi number of {}".format(midi))
    else:
        raise ValueError("Midi value is not a valid number. Your midi value was {}".format(midi))

## Returns a pitch name for the given hertz value.
#  Hint: first convert the hertz value to midi.
#  @param hertz  The integer midi key number to convert.
#  @returns A floating point hertz value.
def hertz_to_pitch(hertz):
    #absolutely not done
    midi = hertz_to_midi(hertz)
    if(check_midi(midi)):
        return midi_to_pitch(midi)
    else:
        raise ValueError("The Hertz value is outside the valid Hertz range.")


## Returns a hertz value for the given pitch.
#  Hint: first convert the pitch to midi.
#  @param pitch  The pitch name to convert.
#  @returns A floating point hertz value.
def pitch_to_hertz(pitch):
    return midi_to_hertz(pitch_to_midi(pitch))


def check_midi(midi):
    if midi > 127 or midi < 0:
        return False
    return True

###############################################################################
# There are two methods you can use to test out code as you develop it.
#
# 1. Interactive testing: Start your Python interpreter, import the module 
#    (python file) that you are working on and then call your code:
#
#    >>> import tet
#    >>> pitch_to_hertz('A4')
#        440.0
#    >>> midi_to_pitch(72)
#        'C5'
#
# 2. Script testing: Start python in 'script' mode by giving it the file
#    you are working on. When Python loads the file it will evaluate all
#    definitions including a special 'if' block that you can put at the
#    end of the file. If this block exists then the code you put inside
#    the if statement (e.g. your testing code) will also be executed. To
#    define the block add this statement to the end of your file but with
#    the work 'pass' replaced by your testing code:
#
#    if __name__ == 'main':
#        pass
#
#    To run the file as python script use your IDE's 'Run' command. If
#    you are using the terminal, provide the file directly to the Python
#    command like this:
#
#    $ python3 /path/to/myfile.py 
#
#    See https://www.cs.bu.edu/courses/cs108/guides/runpython.html for more info.

if __name__ == '__main__':
    print("Testing...")
    print(pitch_to_midi("Cb0"))
    print(midi_to_pitch(pitch_to_midi("C4")))
    # add whatever test code you want here!

    print("Done!")


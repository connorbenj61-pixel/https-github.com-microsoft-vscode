from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

BPM = 124
tempo = bpm2tempo(BPM)

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(Message('program_change', program=0, time=0))
track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

ticks_per_beat = 480
beats = 64

for i in range(beats):
    track.append(Message('note_on', note=36, velocity=100, time=0))
    track.append(Message('note_off', note=36, velocity=0, time=ticks_per_beat))

mid.save('house_groove.mid')
print('Saved house_groove.mid – import into your DAW and add bass, hats, chords.')

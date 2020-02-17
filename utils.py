import ffmpy
import pydub
from pydub import AudioSegment, playback
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import subprocess


def play(x):
    if type(x) != pydub.audio_segment.AudioSegment:
        x = AudioSegment.from_wav("out.wav")
    playback.play(x)

def mkdir(fp):
    if not os.path.exists(fp):
        os.mkdir(fp)

def rm(fn):
    if os.path.exists(fn):
        os.remove(fn)

def compress_arguments(amount):
    '''
    e.g. amount=.5 => 2x as fast.
    https://trac.ffmpeg.org/wiki/How%20to%20speed%20up%20/%20slow%20down%20a%20video
    Atempo can't do more than 2x, so you need to string together multiple commands,
    e.g. "atempo=2.0,atempo=2.0" => "atempo=4.0"
    '''
    tempo = (1./amount)
    def f(t, string=''):
        if t <= 2:
            return string + ("atempo=%.64f" % t)
        else:
            return f(t/2., 'atempo=2,' + string)
    part2 = f(tempo)
    return ["-filter:a", part2]

def reverse_arguments():
    return '-map 0 -c:v copy -af "areverse"'

def compress(inp, out, amount):
    ff = ffmpy.FFmpeg(inputs =  {inp: None},
                      outputs = {out: compress_arguments(amount)})
    print(ff.cmd)
    ff.run()
#     print('Compress (%.2f): %s -> %s' % (amount, inp, out))

def reverse(inp, out):
    ff = ffmpy.FFmpeg(inputs =  {inp: None},
                      outputs = {out: reverse_arguments()})
    print(ff.cmd)
    ff.run()
#     print('Reverse %s -> %s' % (inp, out))

def find_wavs(path):
    file_names = os.listdir(path)
    file_names = [f for f in file_names if f.endswith('.wav')]
    return file_names

def read_audio_from_dir(path):
    file_names = find_wavs(path)
    labels = [w.replace('.wav', '') for w in file_names]
    file_paths = [os.path.join(path, fn) for fn in file_names]
    words = [AudioSegment.from_wav(fn) for fn in file_paths]
    result = dict(zip(labels, words))
    return result

def print_length(words):
    for k, a in words.items():
        print(k, len(a))

def get_audio_dur(fp):
    process = subprocess.Popen('soxi -D'.split() + [fp], stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()
    return float(output.strip('\n'))

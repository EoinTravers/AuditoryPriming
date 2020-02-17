# Subliminal Auditory Priming

This repo contains
code to generate auditory masked stimuli,
as used on BBC's Why are we conscious of so little?

For more details, see [eointravers.com/post/why-factor/](http://eointravers.com/post/why-factor/).

## Steps

To generate the stimuli, I

- Convinced friends and colleagues to lend me their voices:
  a woman to say "left" and "right" (targets),
  and a man to say those words plus some fillers (primes and masks).
- Manually edited the recordings in audacity so that all of the targets,
  and all of the primes and masks, were the same length.
  This can be done by slightly speeding up or slowing down segments,
  or by cutting out windows from the audio to shorten vowel sounds.
- Wrote a python script, using [Pydub](http://pydub.com/) and
  [FFmpeg](https://www.ffmpeg.org/)
  (called using the [ffmpy](https://pypi.org/project/ffmpy/) wrapper), to
    - Compress the primes and masks
    - Reverse the masks
    - Combine the primes, masks, and targets to produce the audio stimuli.


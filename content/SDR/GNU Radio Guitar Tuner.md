Title: Building a Guitar Tuner with GNU Radio
Date: 2017-01-07
Tags: GNU Radio, RTL-SDR
Summary: An aside on using GNU Radio to build a guitar tuner.
Status: draft

[...] you might have heard the phrase that our ears are logarithmic. What this means is that what we perceive as intervals between notes are actually ratios between those notes' frequencies.

Take a middle C (C_4) whose frequency is 261.63 Hz and go up an octave, what you get is C_5 at 523.25 Hz which is twice the frequency. Do the same for any other musical notes and you'll find that an octave "interval" gives you the same ratio of 2. So it's not frequency differences that we can identify, it's frequency ratios or if you prefer differences of the logarithms of the frequencies.
To know what the ratio corresponding to 1 semitone is, recall that an octave contains 12 semitones and as such, in order to evenly divide the 2 factor by 12 semitones we get 2^{1/12} (recall we're talking logarithmic scales here).

(missing fundamental)[https://en.wikipedia.org/wiki/Missing_fundamental]
(pitch detection)[https://en.wikipedia.org/wiki/Pitch_detection_algorithm]

The least obnoxious workaround I found to fix this in Windows systems was to set the environment variable GR_CONF_audio_audio_module in the batch file that launches the GNU Radio command line (C:\Program Files\GNURadio-3.7\bin\run_gr.bat for me) anywhere before the call to python.exe:

	:::
	REM --- Set PortAudio as default audio ---
	set GR_CONF_audio_audio_module=portaudio
	
This will make sure that whenever you launch the GNU Radio command prompt or the GNU Radio companion this environment variable will be set, telling GNU radio to use the portaudio library instead of the windows default for all it's audio needs.

MIC SETTINGS
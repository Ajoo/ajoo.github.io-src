Title: Intro to RTL-SDR
Date: 2016-12-18 13:00
Tags: RTL-SDR
Summary: A summary of what I've learned about RTL-SDR so far. From the working principles of the USB dongles to the software I intend to use to capture and process the data for future projects.
Status: published

Intro goes here

# Software Defined Radio

What is software defined radio

# A Cheap SDR

There are many commercially available SDRs, both receiver only (RX) and transceiver (RX/TX), but they're in general rather expensive (>$100 for RX and >$300 for RX/TX). This is where DVB-T TV tuner USB dongles based on the RTL2832U chipset come into play. As the name indicates, these cheap dongles (~$20) were meant for receiving DVB-T TV but hacked drivers from [Osmocom](http://sdr.osmocom.org/trac/wiki/rtl-sdr) are able to turn them into wideband receiver only SDRs. This cheap SDR is therefore tipically known as the RTL-SDR and in the next section we'll see what they're made of.

## The innards of RTL2832U based DVB-T TV USB dongles

The RTL-SDR blog's [about](http://www.rtl-sdr.com/about-rtl-sdr) page is a great source of further information about this awesome piece of hardware.

# The Software

To showcase all the tools I'm introducing and let the concepts sink in I'll walk you through demodulating an FM signal using all of them.

## SDR# #

The folks at the rtl-sdr blog have provided a [quickstart guide](http://www.rtl-sdr.com/qsg) to get you started with your RTL-SDR. If you follow the SDR# section you should be able to get your drivers installed and your dongle working with SDR#. This is a great program with a nice GUI interface to test your RTL-SDR on. It is able to demodulate many different kinds of signals and it gives you a nice visualization of the power spectral density and spectrogram of the output of your RTL SDR.

We won't play around with this program much so I won't elaborate more, but it's nice to have around. Make sure to tune to an FM radio station you like that has a strong enough signal and write down its frequency. The [FM broadcast band](https://en.wikipedia.org/wiki/FM_broadcast_band) varies according to your geographic location but a decent range to find stations would be 87.5~108 MHz. I will be using 97.4 MHz throughout this post, the frequency for Radio Comercial here in Lisbon, which has a particularly strong signal where I'm living.



## Amplitude and Frequency Modulation 101 - An Aside



## librtlsdr and the Command Line tools

Pretty much all software that interfaces with the RTL-SDR makes use of this library. If you followed the quickstart guide linked above and downloaded SDR#, one of the things that batch file you ran did was download this library and copy the 32 bit version of rtlsdr.dll to the sdrsharp folder. Sadly it threw the rest of it away so you'll have to go ahead to the [Osmocom rtl-sdr wiki](http://sdr.osmocom.org/trac/wiki/rtl-sdr) and download it again if you need the 64 bit version and the command line utilities that come packaged with it. You can either build it from [source](http://cgit.osmocom.org/rtl-sdr) or grab the [pre-built windows version](http://sdr.osmocom.org/trac/attachment/wiki/rtl-sdr/RelWithDebInfo.zip).

In it's 32 and 64 bits releases it contains a number of command line utilities and 3 dlls. Of the command line tools we'll be mostly interested in rtl_sdr and rtl_fm for now. You should make sure the dlls are in your path when using pyrtlsdr later, I usually just drop them in whatever folder I'm working on for convenience...

### rtl_sdr

	:::shell
	rtl_sdr -f 97400000 -g 20 -s 1020000 -n 10200000 COMERCIAL_s1m02_g20.bin
	
This utility stores the I and Q samples alternately as 8 bits unsigned integers. In order to load them in python we can therefore use something like:

	:::python
	def load_bin(filename):
		x = np.fromfile(filename, np.uint8) + np.int8(-127)
		return x.astype(np.int8).reshape((x.size//2, 2))
		
This will load the file and return an numpy.int8 numpy array with shape (nsamples, 2), the first column corresponding to I samples and the second to Q samples.

A more convenient format to process the data digitally is to load it as complex samples (I + j*Q). Unfortunately numpy doesn't have a complex integer type so we'll have to incur in a bit of memory overhead and spring for a numpy.complex64 array which makes it less useful when dealing with a large number of samples:

	:::python
	def load_bin_complex(filename):
		x = np.fromfile(filename, np.uint8)-np.float32(127.5)
		return 8e-3*x.view(np.complex64)


### rtl_fm

rtl_fm is a very resource efficient command line tool to demodulate FM, AM and SSB. For more information on this program make sure to check the [rtl_fm guide](http://kmkeen.com/rtl-demod-guide/).

The following command will demodulate and record a wideband FM channel at 97.4 MHz and record it in a file output.raw. You can press Ctrl+C to exit after capturing enough samples.

	:::shell
	rtl_fm -M wbfm -f 97.4M -g 20 output.raw
	
options:

* -M wbfm : Wideband FM Modulation
* -f 97.4M : Center frequency of 97.4 MHz
* -g 20 : Sets gain to 20 dB. Without this option present automatic gain is used

when using -M wbfm a few implicit options are assumed (which can be explicitely overriden):

* -s 170k : For wideband FM a sample rate of 170 kHz is chosen by default
* -A fast : fast polynomial approximation of arctangent used in demodulation
* -r 32k : output is decimated to 32 kHz
* -l 0 : disables squelch
* -E deemp : applies a deemphesis filter

The output I get running this command and stopping the execution is:

	:::shell
	Found 1 device(s):
	  0:  Realtek, RTL2838UHIDIR, SN: 00000001

	Using device 0: Generic RTL2832U OEM
	Found Rafael Micro R820T tuner
	Tuner gain set to 19.70 dB.
	Tuned to 97671000 Hz.
	Oversampling input by: 6x.
	Oversampling output by: 1x.
	Buffer size: 8.03ms
	Exact sample rate is: 1020000.026345 Hz
	Sampling at 1020000 S/s.
	Output at 170000 Hz.
	Signal caught, exiting!

You might notice that rtl_fm tuned to a different frequency (97.671 MHz) than that we specified (97.4 MHz). This is done to avoid a known imperfection in RTL-SDRs [...]. This way the dongle is tuned to a slightly different frequency and the software later corrects for this in the digital signal processing.

Another interesting thing is that the software chooses to ignore the sampling frequency we (implicitely) provide and instead oversamples by 6x at 1.02MHz. The input is then decimated to the right frequency (170 kHz) in software before being demodulated. I assume this serves two purposes:

* It avoids the illegal range [...]
* It provides greater control over the decimation process.

rtl_fm stores the raw audio in a file as signed 16 bits integers. To load it in python you can therefore do:

	:::python
	import numpy as np
	
	raw_audio = np.fromfile("output.raw", np.int16)
	
To listen to it you can always use scipy to store it as a .wav file and then play it in your favourite media player:

	:::python
	from scipy.io import wavfile
	
	wavfile.write("COMERCIAL.wav", rate=32000, raw_audio)
	
Recall that the default output rate of rtl_fm in wideband FM mode is 32 kHz but if you changed that with the -r option make sure to provide wavfile.write with the correct one (and that's within the range of your sound card...).

Alternativelly you could install and use [SoX](http://sox.sourceforge.net/) which is a great program to convert audio files between formats (including raw audio signals), as well as playing and recording them.

	:::shell
	sox -r 32k -t raw -e s -b 16 -c 1 -V1 COMERCIAL.RAW -t waveaudio

You can replace "-t waveaudio" with a .wav filename to store it in a wav file instead. Make sure to refer to [SoX's documentation](http://sox.sourceforge.net/sox.html) for a full description of the options available.

## pyrtlsdr

To collect 10 seconds of data with the same characteristics as that we collected with rtl_sdr we could do:

	:::python
	from rtlsdr import RtlSdr
	from contextlib import closing
	
	with closing(RtlSdr()) as sdr:
		sdr.sample_rate = 1020000
		sdr.center_freq = 97.4e6
		sdr.gain = 20
		#sdr.freq_correction = 
		#sdr.bandwidth = 
		x = sdr.read_samples(10*1020000)
		
TODO: allowable values for gain

# Demodulating FM

Basics of FM modulation

[DSP Tricks](http://www.embedded.com/design/configurable-systems/4212086/DSP-Tricks--Frequency-demodulation-algorithms-)

# Up Next

My next post will give a brief overview of the GPS system and sampling GPS L1 signals. Stay tuned!

# Useful Links:

* [rtl-sdr](http://www.rtl-sdr.com/)
* [Osmocom rtl-sdr wiki](http://sdr.osmocom.org/trac/wiki/rtl-sdr)
* [RTL-SDR subreddit](https://www.reddit.com/r/RTLSDR/) A subreddit dedicated to RTL-SDR. Make sure to check their wiki which is filled with useful information.
* [rtlsdr Community Wiki](http://rtlsdr.org/)

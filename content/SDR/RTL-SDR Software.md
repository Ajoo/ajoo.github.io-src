Title: Intro to RTL-SDR - Part II
Date: 2017-01-21 13:00
Category: SDR
Tags: RTL-SDR, Python, DSP
Summary: A summary of what I've learned about RTL-SDR so far. From the working principles of the USB dongles to the software I intend to use to capture and process the data for future projects.
Status: draft


In this second and final part of my introduction to RTL-SDR I'll go over the most popular software that is available for use with RTL-SDR dongles. I'll try to provide a big picture but I'll be focusing more on what I intend to use in future RTL-SDR projects.

As a software defined radio Hello World of sorts I'll go over how to demodulate FM signals using a variety of tools. First using specialized software that does the demodulation for us (SDR# and rtl_fm) and then doing the demodulation directly from captured samples of the complex-baseband representation (IQ) using the python scientific computing ecosystem. Finally we'll implement this demodulation in real time using GNURadio.

This post builds on the concepts presented in the [first part of this introduction]({filename}./RTL-SDR Hardware.md) helping frame them in the context of a real world application.


# SDR# #

The RTL-SDR blog has a great [quickstart guide](http://www.rtl-sdr.com/qsg) to get you started with your RTL-SDR USB dongle. If you're on Windows and follow the SDR# Setup Guide section you should be able to get your generic WinUSB drivers installed and your dongle working with SDR#. This program is a bit of a Jack of all trades when it comes to SDR. With a nice GUI interface it is able to demodulate many different kinds of signals providing you a nice visualization of the power spectral density (PSD) estimate and spectrogram (also known as waterfall) of the output of your RTL-SDR. Below is a screenshot of the program running when tuned for a section of the comercial FM band:

![SDR# screenshot]({filename}/images/SDR#.jpg)

We won't play around much with this program so I won't elaborate more, but it's always nice to have around. Make sure to tune to an FM radio station you like that has a strong enough signal and write down its frequency. I will be using 97.4 MHz throughout this post, the frequency for Radio Comercial here in Lisbon, which has a particularly strong signal where I'm living.


# librtlsdr and the rtl-sdr codebase

Most software that interfaces with the RTL-SDR makes use of this library. If you followed the quickstart guide linked above and downloaded SDR#, one of the things it has you do is run a batch file that downloads this library and copies the 32 bit version of rtlsdr.dll to the sdrsharp folder. Sadly it throws the rest of it away so you'll have to go ahead to the [Osmocom rtl-sdr website](http://sdr.osmocom.org/trac/wiki/rtl-sdr) and download it again if you need the 64 bit version and the command line utilities that come packaged with it. You can either grab the [pre-built windows version](http://sdr.osmocom.org/trac/attachment/wiki/rtl-sdr/RelWithDebInfo.zip) or [build it from source](http://sdr.osmocom.org/trac/wiki/rtl-sdr#Buildingthesoftware) if you're on Linux (or feeling adventurous).

The [rtl-sdr codebase](http://cgit.osmocom.org/rtl-sdr) (alternative [github mirror](https://github.com/steve-m/librtlsdr)), curated by Osmocom is the backbone of the rtl-sdr community. It contains the code for both the rtlsdr.dll drivers (librtlsdr) and a number of command line utilities that use this library to perform a number of functions. Out of these we'll be mostly interested in **rtl_test**, **rtl_sdr** and **rtl_fm** for now. The following sections will go into detail about each of these tools but for now let us focus on the main library.

The driver relies on libusb (which comes conveniently packed with the pre-built windows version but must be separately installed on Linux) to provide functions to interface with the RTL-SDR dongle. The functions it exports are what allow us to set the RTL-SDR dongle configuration parameters and read IQ samples. Some of these parameters are not exposed directly but are instead set through an internal algorithm. One possible reason for this is that the driver must support RTL dongles sporting a number of different tuner chips while providing a uniform tuner-agnostic interface. The list that follows reports the most relevant (for now) functions that the library exports and what their implementations mean for dongles with a R820T/T2 tuner:

* **rtlsdr_open/close**: opens the device and initializes it/closes the device;
* **rtlsdr_get_center_freq/set**: gets/sets the center frequency to tune to by configuring the tuner's PLL based frequency synthesizer to $f_c + f_IF$ (high-side injection);
* **rtlsdr_get_freq_correction/set**: gets/sets the frequency correction parameter in parts per million (ppm);
* **rtlsdr_get_tuner_type**: gets the tuner type;
* **rtlsdr_get_tuner_gains**: gets the list of supported gain values by the tuner. For the R820T this list is hardcoded and was determined experimentally. Its single parameter corresponds to all possible combinations of LNA and mixer gains as the VGA is always set to a fixed value;
* **rtlsdr_set_tuner_gain_mode**: sets the tuner gain mode to automatic (AGC is used for both LNA and mixer) or manual (gain value is provided manually through the next function);
* **rtlsdr_get_tuner_gain/set**: gets/sets the tuner gains. For R820T it selects the LNA and mixer gains in order to provide a gain value as close as possible to the provided gain. VGA gain (IF gain) is set to a constant;
* **rtlsdr_set_tuner_if_gain**: sets IF gain. Unsuported for R820T;
* **rtlsdr_set_tuner_bandwidth**: sets the tuner bandwidth through adjusting the IF filters. In practice, the list of supported values by the R820T tuner are 6, 7 and 8 MHz or a list of values ranging from 350 kHz to 2.43 MHz. The driver will always round upwards to the nearest supported value. The IF frequency used by the device is determined based on the bandwidth chosen with 4.57 MHz being used for 7 or 8 MHz bandwidth, 3.57 MHz for 6 MHz bandwidth and 2.3 MHz for any smaller bandwidth values;
* **rtlsdr_get_sample_rate/set**: gets/sets the sample rate of the rtl-sdr output to a value inside the allowed range of [225001; 300000] Hz ∪ [900001; 3200000] Hz. Also sets the bandwidth of the tuner to be the same as the sample rate if it wasn't set before.
* **rtlsdr_set_agc_mode**: sets the RTL2832U to use digital AGC (not the tuner's). This seems to amount only to simple fixed gain value being applied;
* **rtlsdr_read_sync**: reads a fixed number of interleaved 8-bit IQ samples from the device synchronously;
* **rtlsdr_read_async/cancel_async**: reads asynchronously from the device until cancel_async is called.

It should be mentioned that, as with a lot of useful open source software, there exist a number of forks that seek to tweak and extend the capabilities of the rtl-sdr beyond what the standard drivers allow. Most of these should however be considered experimental. Two examples of such forks are:

* [mutability's](https://github.com/mutability/rtl-sdr/): which extends the tuning range of the standard driver via a number of tricks involving manipulating the IF frequency and whether high or low-side injection is used;
* [keenerd's](https://github.com/keenerd/rtl-sdr): from the author of the rtl_fm and rtl_power command line tools which includes some modifications to the command line utilities;

#

## rtl_test

TODO: frequency error 
{For both kinds the tuner error is ~30 +-20 PPM}
{All of the dongles have significant frequency offsets from reality that can be measured and corrected at runtime. My ezcap with E4000 tuner has a frequency offset of about ~44 Khz or ~57 PPM from reality as determined by checking against a local 751 Mhz LTE cell using LTE Cell Scanner. Here's a plot of frequency offsets in PPM over a week. The major component of variation in time is ambient temperature. With the R820T tuner dongle after correctly for I have has a ~ -17 Khz offset at GSM frequencies or -35 ppm absolute after applying a 50 ppm initial error correction. When using kalibrate for this the initial frequency error is often too large and the FCCH peak might be outside the sampled 200 KHz bandwidth. This requires passing an initial ppm error parameter (from LTE scanner) -e . Another tool for checking frequency corrections is [keenerd's version](https://github.com/keenerd/rtl-sdr) of rtl_test which uses (I think) ntp and system clock to estimate it rather than cell phone basestation broadcasts.}


We'll start our exploration of the rtl-sdr command tools with rtl_test. This is an utility that allows you to perform different tests on your RTL-SDR dongle and figure out the allowable ranges for some of the control parameters when capturing samples with your dongle. The following command will capture samples at 2.4 MHz and report any samples lost. You can suspend the program with Ctrl+C and it will tell you how many samples per million were lost:

	:::
	> rtl_test -s 2400000
	Found 1 device(s):
	  0:  Realtek, RTL2838UHIDIR, SN: 00000001

	Using device 0: Generic RTL2832U OEM
	Found Rafael Micro R820T tuner
	Supported gain values (29): 0.0 0.9 1.4 2.7 3.7 7.7 8.7 12.5 14.4 15.7 16.6 19.7
	 20.7 22.9 25.4 28.0 29.7 32.8 33.8 36.4 37.2 38.6 40.2 42.1 43.4 43.9 44.5 48.0
	 49.6
	Sampling at 2400000 S/s.

	Info: This tool will continuously read from the device, and report if
	samples get lost. If you observe no further output, everything is fine.

	Reading samples in async mode...
	lost at least 64 bytes
	lost at least 144 bytes
	lost at least 100 bytes
	Signal caught, exiting!

	User cancel, exiting...
	Samples per million lost (minimum): 3
	
As you can see it will also report all the supported values for the gain setting of the tuner. 

As you can see my RTL-SDR blog dongle is dropping a few samples at 2.4 MHz. You can try different settings of the sample rate with the **-s** option in order to figure out a safe sample rate at which no samples are dropped. Keep in mind that this can vary according to temperature and also your computer and USB ports. 

The allowed range of sample rates for RTL SDR dongles is [225001; 300000] ∪ [900001; 3200000] Hz. If you try to use a sample rate outside of this range you will get an "Invalid sample rate" message and the default of 2.048 MHz will be used by rtl_test.

Using the **-p** option will also report the PPM error measurement as estimated (I think) from measuring GSM signals (since they're quite high frequency). Letting it run for a few minutes should give you a somewhat reliable estimate that you can then use as the frequency correction parameter for other programs such as SDR# or rtl_sdr. Unfortunately, I couldn't get this to work myself as I get no PPM reports from running the program and I'm not sure why...

## rtl_fm

rtl_fm is a very resource efficient command line tool to capture IQ samples from the RTL SDR and demodulate FM, AM and SSB signals. For more information on this program make sure to check the [rtl_fm guide](http://kmkeen.com/rtl-demod-guide/).

The following command will demodulate and record a wideband FM channel at 97.4 MHz and record it in a file output.raw. You can press Ctrl+C to exit after capturing enough samples.

	:::
	> rtl_fm -M wbfm -f 97.4M -g 20 output.raw
	
The meaning of the options is:

* **-M wbfm**: wideband FM modulation;
* **-f 97.4M**: center frequency of 97.4 MHz;
* **-g 20**: sets the tuner gain to the closest allowable value to 20 dB (19.7 dB). Without this option present automatic gain is used.

when using -M wbfm a few implicit options are assumed (which can be explicitely overriden):

* **-s 170k**: for wideband FM a sample rate of 170 kHz is chosen by default;
* **-A fast**: fast polynomial approximation of arctangent used in demodulation;
* **-r 32k**: output is decimated to 32 kHz;
* **-l 0**: disables squelch;
* **-E deemp**: applies a deemphesis filter.

The output I get running this command and then stopping the execution after a few seconds is:

	:::
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

You might notice that rtl_fm tuned to a different frequency (97.671 MHz) than that we specified (97.4 MHz). This is done to avoid a known imperfection in RTL-SDRs that causes a small DC bias to be present at the ADC output. This way the dongle is tuned to a slightly different frequency to avoid the DC spike and the software later corrects for this in the digital signal processing by shifting the captured signal in frequency to 0 Hz.

Notice also that the software oversamples by 6x at 1.02 MHz and then decimates the output to the (implicitely) specified frequency of 170 kHz before demodulating. This is because, first and foremost, 170 kHz is not a valid sampling frequency for the RTL-SDR (see the rtl_test section above for the valid range). 1.02 MHz is in fact the first integer multiple of 170 kHz that fits in the allowed range. But this is not the only reason; in fact if we specifically ask rtl_fm to sample the input at 240 kHZ with **-s 240k**, it will still oversample by 5x at 1.2 MHz despite the fact that 240 MHz is within the allowed range of sampling frequencies of the RTL SDR:

	:::
	Oversampling input by: 5x.
	Oversampling output by: 1x.
	Buffer size: 6.83ms
	Sampling at 1200000 S/s.
	Output at 240000 Hz.
	
My assumption is that this is done in order to mitigate the quantization noise. Recall that the output of the RTL SDR is 8 bits and therefore oversampling and decimating in software where we're not limited to 8 bits should provide a better noise figure than relying on doing the decimation in the chip. Furthermore, it provides greater control over the decimation process, letting the software choose the low-pass filter. From these considerations it would make sense to always use the highest possible sampling rate but rtl_fm is built with limited resources in mind so that might provide a reason for it compromising for sampling frequencies closer to 1 MHz.

rtl_fm stores the raw audio in a file as signed 16 bits integers. To load it in python with numpy you can therefore do:

	:::python
	import numpy as np
	
	raw_audio = np.fromfile("output.raw", np.int16)
	
To listen to it you can always use scipy to store it as a .wav file and then play it in your favourite media player:

	:::python
	from scipy.io import wavfile
	
	wavfile.write("COMERCIAL.wav", rate=32000, raw_audio)
	
Recall that the default output rate of rtl_fm in wideband FM mode is 32 kHz but if you changed that with the -r option make sure to provide wavfile.write with the correct one (and that it is within the range of your sound card...).

Alternativelly you could install and use [SoX](http://sox.sourceforge.net/) which is a great program to convert audio files between formats (including raw audio signals), as well as playing and recording them. The following command will play the raw audio file with sample rate 32 kHz, 16 bits signed int encoding and 1 channel:

	:::
	> sox -r 32k -t raw -e signed -b 16 -c 1 COMERCIAL.RAW -t waveaudio

You can replace "-t waveaudio" with a .wav filename to store it in a wav file instead. Make sure to refer to [SoX's documentation](http://sox.sourceforge.net/sox.html) for a full description of the options available.

## rtl_sdr

Finally, the most general use command line tool in the librtlsdr package is rtl_sdr. This program will let you capture IQ samples directly and store them in a file:

	:::
	> rtl_sdr -f 97400000 -g 20 -s 1020000 -n 10200000 COMERCIAL_s1m02_g20.bin
	
The options in this case mean:

* **-f 97400000**: sets the tuner frequency to 97.4 MHz;
* **-g 20**: sets the tuner gain to the closest allowable value to 20 dB (19.7 dB);
* **-s 1020000**: sets the sample rate to 1.02 MHz;
* **-n 10200000**: instructs rtl_sdr to capture 1.02e7 samples which should amount to a 10 seconds worth of samples at the given sample rate (10 s * 1.02e6 MHz).
	
This utility stores the I and Q samples alternately as 8 bits unsigned integers. In order to load them in python we can therefore use something like:

	:::python
	import numpy as np
	
	def load_iq(filename):
		x = np.fromfile(filename, np.uint8) + np.int8(-127) #adding a signed int8 to an unsigned one results in an int16 array
		return x.astype(np.int8).reshape((x.size//2, 2))	#we cast it back to an int8 array and reshape
		
This will load the file and return an numpy.int8 numpy array with shape (nsamples, 2), the first column corresponding to I samples and the second to Q samples.

A more convenient format to process the data digitally is to load it as complex samples (I + j*Q). Unfortunately numpy doesn't have a complex integer type so we'll have to incur in a bit of memory overhead and spring for a numpy.complex64 array which makes it less useful when dealing with a large number of samples:

	:::python
	def load_iq_complex(filename):
		x = np.fromfile(filename, np.uint8) - np.float32(127.5)	#by subtracting a float32 the resulting array will also be float32
		return 8e-3*x.view(np.complex64)						#viewing it as a complex64 array then yields the correct result

##

# pyrtlsdr

pyrtlsdr is a python library that wraps the librtlsdr rtlsdr.dll functions. It lets you read IQ samples from your RTL SDR directly in python and get them into a complex numpy array.

You should make sure that the librtlsdr dlls can be found by pyrtlsdr. Either add them to your python path or just drop a copy in your working directory...
To collect 10 seconds of data with the same characteristics as that we collected with rtl_sdr we would do:

	:::python
	from rtlsdr import RtlSdr
	from contextlib import closing
	
	#we use a context manager that automatically calls .close() on sdr
	#whether the code block finishes successfully or an error occurs
	with closing(RtlSdr()) as sdr:	
		sdr.sample_rate = 1020000
		sdr.center_freq = 97.4e6
		sdr.gain = 20
		#sdr.freq_correction = 
		#sdr.bandwidth = 
		x = sdr.read_samples(10*sdr.sample_rate)
		
Other properties of the RtlSdr class are:

* freq_correction
* bandwidth


# Demodulating FM

Now that we know how to capture IQ samples and load them in python, either through rtl_sdr or the pyrtlsdr python library, we can work on getting from these IQ samples to an actual audible signal.

Basics of FM modulation

[DSP Tricks](http://www.embedded.com/design/configurable-systems/4212086/DSP-Tricks--Frequency-demodulation-algorithms-)

# GNURadio

sds

# Up Next

My next posts will be an introduction to GNU radio where I'll demodulate FM signals in real time and another which will provide a brief overview to the GPS system and sampling of GPS L1 signals. Stay tuned!
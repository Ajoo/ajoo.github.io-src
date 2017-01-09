Title: Intro to RTL-SDR
Date: 2016-12-18 13:00
Category: SDR
Tags: RTL-SDR, Python, DSP
Summary: A summary of what I've learned about RTL-SDR so far. From the working principles of the USB dongles to the software I intend to use to capture and process the data for future projects.
Status: draft

TODO: 

* Intro
* Analog Communications 101/AM
* Analog Communications 101/FM
* Software Defined Radio
* A cheap SDR/innards
* The Software/librtlsdr/pyrtlsdr
* The Software/librtlsdr/demodulating FM

Intro goes here

# Analog Communications 101

Communication systems often involve transmiting a message $m(t)$ through a pass-band channel, i.e., a channel where only a limited range of frequencies can be used. A good example is comercial FM radio transmitions, usually restricted to a frequency band between 85 and 108 MHz which must accomodate multiple stations, each one being allocated a <200 kHZ band. Given that the message we're interested in transmiting often has support in a different range of frequencies, as is the case of raw audio signals in the human hearing range ([20 Hz; 20 kHz]), the signal must first be shifted in frequency in order to satisfy the requirements of the particular channel of comunication.

This is accomplished by modulation whereby one characteristic of a carrier wave (usually sinusoid like $A\cos(\omega_c t)$) will be made to vary according to the *modulating signal*: $m(t)$ (also called the message) producing a *modulated signal*: $s(t)=B(t)\cos[\omega_c t + \theta (t)]$. There are two main forms of analog modulation:

* **Amplitude Modulation (AM)**: where the characteristic that is made to vary is the amplitude $B(t)$ of the carrier;
* **Phase/Frequency Modulation (PM/FM)**: where the characteristic that varies is the phase $\theta (t)$ of the carrier.

TODO: [IMAGE MODULATION]

We'll discuss these in the following sections but before we move on here's a useful glossary of terms commonly used in telecommunications:

* **Baseband**: the frequency band of the modulating signal, also used to refer to the modulating signal as the baseband signal;
* **Center frequency**: the frequency around which the spectrum of the modulated signal is centered;
* **Bandwidth** (of a signal): some measure of the support of a signal in the frequency domain (has many different technical deffinitions).

#

## Amplitude Modulation

$$m(t)e^{i2\pi f_c t}\stackrel{\mathrm{\mathcal{F}}}{\longleftrightarrow}M(f)*\delta(f-f_c)=M(f-f_c)$$

$$m(t)\cos(2\pi f_c t)\stackrel{\mathrm{\mathcal{F}}}{\longleftrightarrow}\frac{1}{2}[M(f-f_c)+M(f+f_c)]$$

## Frequency Modulation



# Software Defined Radio

Many forms of radio communication systems were designed with analog technology in mind. Software Defined Radio (**SDR**) is a communication system where part of the traditionally analog signal processing, accomplished by means of analog electronic circuits is replaced by digital signal processing, accomplished my means of Analog to Digital Conversion/Digital to Analog Conversion (ADC/DCA) and general purpose computers running DSP software.

By replacing hardware components with software, through inserting an ADC/DCA as far upstream the signal flow as possible and processing the digital signal instead, very flexible and general purpose systems can be realized since software is much easier to change than hardware components. Ideally, one would place an ADC or DCA directly at the antenna for maximum flexibility  but this is not practical and SDR systems tipically include a flexible [RF front end](https://en.wikipedia.org/wiki/RF_front_end) before sampling as in the high level diagram below depicting the typical SDR system:

![Conceptual SDR system]({filename}/images/SDR_system.svg)

Note that the term Software Defined Radio denotes the whole communication system including the antenna, any specialized hardware and the computer/embedded system running the DSP. In the following however we'll (ab)use it by equating it with the hardware that is used to deliver the digital samples to a personal computer.

# A Cheap SDR

There are many general purpose commercially available SDRs, both receiver only and transceiver, but they're rather expensive in general (>€100 for RX and >€300 for RX/TX). This is where DVB-T TV tuner USB dongles based on the RTL2832U chipset come into play. As the name indicates, these cheap dongles (~€20) were meant for receiving DVB-T TV but hacked drivers from [Osmocom](http://sdr.osmocom.org/trac/wiki/rtl-sdr) are able to turn them into wideband receiver only SDRs. This cheap SDR is therefore tipically known as the **RTL-SDR**:

![RTL dongles]({filename}/images/RTL_dongles.jpg)

Here you can see the two dongles I own. The one on top is a pretty generic DVB-T USB dongle from NooElec. You can see in the picture the remote that comes with it for its intended use as a TV tuner. It has a standard MCX antenna connector and comes with a small whip antenna.

The dongle that you see at the bottom is the one sold by the [RTL-SDR blog](http://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/). It comes with several improvements over the generic dongles for use as a SDR. You can read all about these in the the webpage linked. For my intended use of capturing GPS signals I was mostly interested in the software enabled bias-T in order to power an active GPS antenna, the SMA antenna connector and of course the 1 PPM temperature controlled oscillator for more accurate tuning (the passive cooling is a nice plus too since these units tend to run hot when tuning to frequencies > 1500 MHz).

## The innards of RTL2832U based DVB-T TV USB dongles

A lot of the information in this section is collected from this [website](http://superkuh.com/rtlsdr.html) as well as 

Mainly used with three different kinds of tuners, the discontinued (and therefore very hard to find nowadays) Elonics E4000 and the Raphael Micro R820T and R820T2. The frequency 

# The Software

In this section I'll introduce the software I'm going to be using for RTL SDR projects. To showcase all the tools and make sure the concepts sink in I'll be using all of them to  demodulate an FM signal. I'll start with specialized tools that sample the RTL SDR and demodulate FM signals themselves (**SDR#** and **rtl_fm**) and then move on to those that simply capture the IQ samples from the RTL-SDR (**rtl_sdr** and **pyrtlsdr**). Since python will be my language of choice for anything RTL SDR related, I'll demodulate the FM signals directly from IQ samples using only numpy and scipy. I'm planing to, in a later post, use GNU radio to do the same in real time as a way to get aqquainted with the software.

## SDR# #

The RTL-SDR blog has a great [quickstart guide](http://www.rtl-sdr.com/qsg) to get you started with your RTL-SDR. If you follow the SDR# Setup Guide section you should be able to get your Osmocom drivers installed and your dongle working with SDR#. This is a great program with a nice GUI interface to test your RTL-SDR on. It is able to demodulate many different kinds of signals and it gives you a nice visualization of the power spectral density and spectrogram of the output of your RTL SDR.

We won't play around much with this program so I won't elaborate more, but it's always nice to have around. Make sure to tune to an FM radio station you like that has a strong enough signal and write down its frequency. I will be using 97.4 MHz throughout this post, the frequency for Radio Comercial here in Lisbon, which has a particularly strong signal where I'm living.


## librtlsdr and the Command Line tools

Pretty much all software that interfaces with the RTL-SDR makes use of this library. If you followed the quickstart guide linked above and downloaded SDR#, one of the things it has you do is run a batch file that downloads this library and copies the 32 bit version of rtlsdr.dll to the sdrsharp folder. Sadly it throws the rest of it away so you'll have to go ahead to the [Osmocom rtl-sdr wiki](http://sdr.osmocom.org/trac/wiki/rtl-sdr) and download it again if you need the 64 bit version and the command line utilities that come packaged with it. You can either build it from [source](http://cgit.osmocom.org/rtl-sdr) or grab the [pre-built windows version](http://sdr.osmocom.org/trac/attachment/wiki/rtl-sdr/RelWithDebInfo.zip).

In it's 32 and 64 bits releases librtlsdr contains a number of command line utilities and 3 dlls. Of the command line tools we'll be mostly interested in **rtl_test**, **rtl_sdr** and **rtl_fm** for now. The dynamic-link library rtlsdr.dll is what contains the functions to interface with RTL SDR that are used by all other tools.

### rtl_test

We'll start our exploration of librtlsdr with rtl_test. This is a command line utility that allows you to perform different tests on your RTL SDR dongle and figure out the allowable ranges for some of the control parameters when capturing samples with your dongle. The following command will capture samples at 2.4 MHz and report any samples lost. You can suspend the program with Ctrl+C and it will tell you how many samples per million were lost:

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
	
As you can see it will also report all the supported values for the gain setting of the tuner. When you specify a tuner gain in any other program it will usually use the nearest allowable value. Keep in mind that the default when no gain is specified is usually to use automatic gain control which uses a feedback of the signal itself to control the gain of the input LNA.

As you can see my RTL-SDR blog dongle is dropping a few samples at 2.4 MHz. You can try different settings of the sample rate with the **-s** option in order to figure out a safe sample rate at which no samples are dropped. Keep in mind that this can vary according to temperature and also your computer and USB ports. 

The allowed range of sample rates for RTL SDR dongles is [225001; 300000] ∪ [900001; 3200000] Hz. If you try to use a sample rate outside of this range you will get an "Invalid sample rate" message and the default of 2.048 MHz will be used by rtl_test.

Using the **-p** option will also report the PPM error measurement as estimated (I think) from measuring GSM signals (since they're quite high frequency). Letting it run for a few minutes should give you a somewhat reliable estimate that you can then use as the frequency correction parameter for other programs such as SDR# or rtl_sdr. Unfortunately, I couldn't get this to work myself as I get no PPM reports from running the program and I'm not sure why...

### rtl_fm

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

### rtl_sdr

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

## pyrtlsdr

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

# Up Next

My next posts will be an introduction to GNU radio where I'll demodulate FM signals in real time and another which will provide a brief overview to the GPS system and sampling of GPS L1 signals. Stay tuned!

# Useful Links:

* [rtl-sdr](http://www.rtl-sdr.com/)
* [Osmocom rtl-sdr wiki](http://sdr.osmocom.org/trac/wiki/rtl-sdr)
* [RTL-SDR subreddit](https://www.reddit.com/r/RTLSDR/) A subreddit dedicated to RTL-SDR. Make sure to check their wiki which is filled with useful information.
* [rtlsdr Community Wiki](http://rtlsdr.org/)
* [superkuh's website](http://superkuh.com/rtlsdr.html) An absolute bible when it comes to the internals of RTL-SDR USB dongles. Tons of useful information, links to datasheets, schematics, etc... 

# Educational Links:

* [University of Colorado's Communications Lab](http://www.eas.uccs.edu/~mwickert/ece4670/) Make sure to check out their lab assignments, particularly Lab 6 which this blog post draws inspiration from;
* [Stanford's Analog and Digital Communication Systems 2014 course](http://web.stanford.edu/class/ee179/) Again, make sure to check out the lab assignments with lots of RTL-SDR materials;


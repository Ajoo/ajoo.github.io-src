Title: Intro to RTL-SDR
Date: 2016-12-18 13:00
Tags: RTL-SDR
Summary: A summary of what I've learned about RTL-SDR so far. From the working principles of the USB dongles to the software I intend to use to capture and process the data for future projects.
Status: draft

Intro goes here

# Software Defined Radio

What is software defined radio

# A Cheap SDR

There are many commercially available SDRs, both receiver only (RX) and transceiver (RX/TX), but they're in general rather expensive (>$100 for RX and >$300 for RX/TX). This is where DVB-T TV tuner USB dongles based on the RTL2832U chipset come into play. As the name indicates, these cheap dongles (~$20) were meant for receiving DVB-T TV but hacked drivers from [Osmocom](http://sdr.osmocom.org/trac/wiki/rtl-sdr) are able to turn them into wideband receiver only SDRs. This cheap SDR is therefore tipically known as the RTL-SDR and in the next section we'll see what they're made of.

## The innards of RTL2832U based DVB-T TV USB dongles

The RTL-SDR blog's [about](http://www.rtl-sdr.com/about-rtl-sdr/) page is a great source of further information about this awesome piece of hardware.

# The Software

## SDR#

The folks at the rtl-sdr blog have provided a [quickstart guide](http://www.rtl-sdr.com/) to get your drivers installed and your dongle working with SDR#. This is a great program to test your RTL-SDR on. [...]

## librtlsdr and Command Line tools

Pretty much all software that interfaces with the RTL-SDR makes use of this library. If you followed the quickstart guide I linked earlier and downloaded SDR#, one of the things that batch-file you ran did was download this library and copy the 32 bit version of rtlsdr.dll to the sdrsharp folder. Sadly it threw the rest of it away so you'll have to go ahead to the [Osmocom rtl-sdr wiki](http://sdr.osmocom.org/trac/wiki/rtl-sdr) and download it again if you need the 64 bit version and the command line utilities that come packaged with it. You can either build it from source or grab the [pre-built windows version](http://sdr.osmocom.org/trac/attachment/wiki/rtl-sdr/RelWithDebInfo.zip).

## pyrtlsdr

## GNU Radio



# Up Next

My next post will give a brief overview of the GPS system and sampling GPS L1 signals. Stay tuned!

# Useful Links:

* [rtl-sdr](http://www.rtl-sdr.com/)
* [Osmocom rtl-sdr wiki](http://sdr.osmocom.org/trac/wiki/rtl-sdr)
* [RTL-SDR subreddit](https://www.reddit.com/r/RTLSDR/) A subreddit dedicated to RTL-SDR. Make sure to check their wiki which is filled with useful information.
* [rtlsdr Community Wiki](http://rtlsdr.org/)

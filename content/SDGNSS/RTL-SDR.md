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

# The Basic Software

command line tools
pyrtlsdr
GNU Radio

# Up Next

My next post will give a brief overview of the GPS system and sampling GPS L1 signals. Stay tuned!

# Useful Links:

* [rtl-sdr](http://www.rtl-sdr.com/)
* [Osmocom rtl-sdr wiki](http://sdr.osmocom.org/trac/wiki/rtl-sdr)
* [RTL-SDR subreddit](https://www.reddit.com/r/RTLSDR/)
* [rtlsdr Community Wiki](http://rtlsdr.org/)

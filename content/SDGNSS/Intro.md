Title: Software Defined GNSS
Date: 2016-12-18 12:00
Tags: GNSS, RTL-SDR
Summary: A short introduction to my Software Defined GNSS project
Status: published

When I first heard about Software Defined Radios (SDR) I was instantly interested. The ability to probe the electromagnetic spectrum around me and decode the ubiquitous signals being transmitted seemed to open a door to new and interesting experiments. I loved Digital Signal Processing (DSP) when I was in college (still do) and this was exactly what I was looking for to put it in practice. I started looking for a project to sink my teeth in that went besides using established software and a cheap SDR to decode well known AM, FM and ADS-B signals.

Since my main background is in Guidance, Navigation and Control (and I'm a person walking this Earth in 2016) I've made use of GPS before and I'm familiar to some extent with its inner workings from a course in Global Navigation Satellite Systems (GNSS) I attended in college. I've always felt however that my knowledge of this system is not as deep as I want it to be, particularly regarding the receiver side of things. I think it's therefore appropriate that my first foray into the exciting world of SDR be the implementation of a GPS/GNSS receiver in software. I intend to take this as far as I can, from measuring GPS L1 signals to computing a full navigation solution of position and velocity, learning as much as I can along the way and sharing it with any interested readers.

My particular goals for this project are therefore:

1. To put my knowledge of GNSS, telecommunications and DSP to work in a practical setting and keep me from getting rusty;
2. To fill in the blanks in my knowledge of GNSS receivers' inner workings;
3. To learn about new software libraries and tools, in particular those concerning real time digital signal processing;
4. To improve my communication and documentation skills.


# Materials

There are only two components (three if you're counting a decent computer/laptop) required for this project. One is an active GPS Antenna in order to be able to receive GPS signals in the L1 band (1575.42 MHz center frequency) and the other is a Software Defined Radio (SDR) which is responsible for delivering to your computer the digital samples of these signals shifted to baseband.

I will go into further detail into the hardware in my next blog post so don't worry if you don't understand what this is for just yet. This section is only meant to give you an idea of what you'll need and the costs associated. The particular choices I made are:

* [RTL-SDR Blog USB Dongle](https://www.amazon.com/RTL-SDR-Blog-RTL2832U-Software-Telescopic/dp/B011HVUEME/ref=lp_10230687011_1_1?srs=10230687011&ie=UTF8&qid=1482078660&sr=8-1) ($26) I chose this over other generic USB DVB-T TV dongles because it has a software enabled bias-T which allows me to power an active antenna without additional hardware or soldering mods. It also has other nice enhancements over regular dongles for use in Software Defined Radio. You could also get the version without the antennas which comes out cheaper ($20) since we're mostly interested in using a GPS antenna.
* [GPS Active Antenna](https://www.amazon.com/Waterproof-Active-Antenna-28dB-Gain/dp/B00LXRQY9A/ref=lp_10008493011_1_1?srs=10008493011&ie=UTF8&qid=1482079461&sr=8-1) ($15) Any active GPS antenna should do, there are plenty available at Amazon and other specialized sellers.

# Existing Software Libraries and Target Audience for These Blog Posts

Software based GPS/GNSS receivers are hardly uncharted waters. There are full fledged software libraries meant to accomplish what this little project of mine set out to do. Below is a list of those I'm aware of:


* [gnss-sdrlib](https://github.com/taroz/GNSS-SDRLIB) An open source GNSS Software Defined Radio Library with nice GUI elements written in C and C++
* [gnss-sdr](http://gnss-sdr.org) An open source library for implementing GNSS software defined receivers in C++
* [rtklib](http://www.rtklib.com/) An open source program package for GNSS positioning


I will not rely on these libraries except maybe for inspiration and test purposes as this project is meant mostly as an educational experience for myself and for any readers out there. I will attempt to make my posts as informative and as self-contained as possible so that I can refer back to them in the future and so that any reader might follow along and understand how to decode GNSS signals without having to refer to external materials. I will assume only basic knowledge of telecommunications, specially regarding the use of Fourier transforms and time <-> frequency representation of signals but no previous knowledge of GNSS.

# Up Next

My next post in this series will go into detail into what exactly is Software Defined Radio and the particular hardware and software that will be used in this project. Stay tuned!

# Useful Links:

* [sdrgps blog](http://sdrgps.blogspot.com) A blog by Philip Hahn on his experiments with software defined radio GPS and its use in high-power rockets


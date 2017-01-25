Title: Introduction to GNU Radio
Date: 2017-01-01
Tags: GNU Radio, RTL-SDR
Summary: An introduction to GNU Radio and real time Digital Signal Processing
Status: draft

Pros:

* Provides a powerful real-time capable DSP library for python

Cons:

* Python 2.7: This one's a bummer. I've made the switch to Python 3 for all my pythonic needs and I haven't found a library that I've wanted to use and didn't support it in a long time;
* The documentation is in the classical style of GNU projects, that is to say, very lacking. It is auto-generated with (Doxygen)[http://gnuradio.org/doc/doxygen/] for the C++ API, and (Sphinx)[http://gnuradio.org/doc/sphinx/] for the Python library. But as the tutorials tell you several times, you'll have to use the source to figure out how stuff works as often the block's description provides little help or doesn't exist at all;
* Extending functionality seems overly complicated: If you can build your desired application with the basic building blocks that GNU Radio provides "out of the box", all is fine and dandy. However, if you have to write a certain piece of DSP code yourself that you can integrate with GNU radio's flowcharts, you'll have to wrangle with building CMake Modules which under Windows sounds like a nightmare based on past experience... I think I'll have to switch over to a Linux environment for my future experiments with GNU Radio.

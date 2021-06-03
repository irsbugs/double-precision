# Double Precision

The Python/GTK program **double_precision.py** is designed to aid in understanding how the IEEE 754 Double Precision values
are created using 64 bits.

This program combines traditional creation of the GUI with creation using Gtk.Builder and an XML file that was created using *Glade*.

The header bar and the widgets on it were created using Glade. They have been left in this program as an example template and 
provide limited functionality to the main objective of demonstrating Double Precision.

An image has been embedded as base64 data. This is used as the Favicon, a Header-bar image, and the About Dialogs logo.

## Simh Alpha

The *simh* simulator for the *Alpha* computer will convert a quadword integer in one floating point register to an IEEE 754 double 
precision floating point value ("T-floating") in another register.

```
$ alpha

Alpha simulator V4.0-0 Current        git commit id: e7169d48

sim> ; Convert quadword to T_floating. CVTQT.
sim> ev -m 0x5BE017C1
0:	CVTQT R0,R1
4:	000000005BE017C1

sim> ; Universal NOP
sim> ev LDQ_U R31,0(R31)
0:	000000002FFF0000

sim> ev -m 2FFF0000
0:	LDQ_U R31,0
4:	000000002FFF0000

sim> ; Concatinate the two instructions and store at address 2000.
sim> d 2000 2FFF00005BE017C1
sim> e -m 2000:2004
2000:	CVTQT R0,R1
2004:	LDQ_U R31,0

sim> ; +1
sim> d f0 1
sim> d f1 0

sim> go 2000 until 2008

Breakpoint, PC: 2008 (0000000000000000)
sim> e f0:f1
F0:	0000000000000001
F1:	3FF0000000000000

sim> ; +2
sim> d f0 2
sim> go 2000 until 2008

Breakpoint, PC: 2008 (0000000000000000)
sim> e f0:f1
F0:	0000000000000002
F1:	4000000000000000

sim>; +3
sim> d f0 3
sim> go 2000 until 2008

Breakpoint, PC: 2008 (0000000000000000)
sim> e f0:f1
F0:	0000000000000003
F1:	4008000000000000

sim> ; -1
sim> d f0 FFFFFFFFFFFFFFFF
sim> go 1000 until 1008

Breakpoint, PC: 1008 (0000000000000000)
sim> e f0:f1
F0:	FFFFFFFFFFFFFFFF
F1:	BFF0000000000000

sim> ; -2
sim> d f0 FFFFFFFFFFFFFFFE
sim> go 1000 until 1008

Breakpoint, PC: 1008 (0000000000000000)
sim> e f0:f1
F0:	FFFFFFFFFFFFFFFE
F1:	C000000000000000
sim> 
```


Ian Stewart. May 2021.

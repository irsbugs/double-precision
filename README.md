# Double Precision

The Python/GTK program **double_precision.py** is designed to aid in understanding how the IEEE 754 Double Precision values
are created using 64 bits.

This program combines traditional creation of the GUI with creation using Gtk.Builder and an XML file that was created using *Glade*.

The header bar and the widgets on it were created using Glade. They have been left in this program as an example template and 
provide limited functionality to the main objective of demonstrating Double Precision.

An image has been embedded as base64 data. This is used as the Favicon, a Header-bar image, and the About Dialogs logo.

## Simh Alpha

The *simh* simulator for the *Alpha* computer will convert a quadword integer in one floating point register to an IEEE 754 double 
precision floating point value ("T-floating") in another register. The script file above, **double-precision** may be run with the 
simh / Alpha application. The output will be as follows:

```
$ alpha double-precision

Alpha simulator V4.0-0 Current        git commit id: e7169d48

Alpha double precision demonstration Using the instruction
CVTTQ Opcode: 16.0BE Description: Convert quadword to T_floating
Note that T_floating is IEEE 754 double precision floating point.

CVTQT R0,R1 = 5BE017C1
Universal NOP = LDQ_U R31,0(R31) = 2FFF0000

Deposit  1000 2FFF00005BE017C1
Deposit register F0 1

Breakpoint, PC: 1008 (0000000000000000)
Register F1 contains the Floating Point value of Register F0
F0:	0000000000000001
F1:	3FF0000000000000

Deposit register F0 2

Breakpoint, PC: 1008 (0000000000000000)
F0:	0000000000000002
F1:	4000000000000000

Deposit register F0 3

Breakpoint, PC: 1008 (0000000000000000)
F0:	0000000000000003
F1:	4008000000000000

Deposit register F0 -1 FFFFFFFFFFFFFFFF

Breakpoint, PC: 1008 (0000000000000000)
F0:	FFFFFFFFFFFFFFFF
F1:	BFF0000000000000

Deposit register F0 -2 FFFFFFFFFFFFFFFE

Breakpoint, PC: 1008 (0000000000000000)
F0:	FFFFFFFFFFFFFFFE
F1:	C000000000000000

Deposit register F0 -3 FFFFFFFFFFFFFFFD

Breakpoint, PC: 1008 (0000000000000000)
F0:	FFFFFFFFFFFFFFFD
F1:	C008000000000000

Deposit register F0 0

Breakpoint, PC: 1008 (0000000000000000)
F0:	0000000000000000
F1:	0000000000000000

Deposit register F0 7FFFFFFFFFFFFFFF - Max positive 64 bit integer 9.22 * 10^18

Breakpoint, PC: 1008 (0000000000000000)
F0:	7FFFFFFFFFFFFFFF
F1:	43E0000000000000

Deposit register F0 8000000000000000 - Max negative 64 bit integer -9.22 * 10^18

Breakpoint, PC: 1008 (0000000000000000)
F0:	8000000000000000
F1:	C3E0000000000000
Goodbye
```

Ian Stewart. May 2021.

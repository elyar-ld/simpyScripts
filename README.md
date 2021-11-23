# Simpy scripts

These are some examples of [SimPy](https://simpy.readthedocs.io/en/latest/index.html) scripts

## Currently

### Bicycle:
The very basic example of simulation.
A bicycle rolls 30 minutes, stops for rest for 10 minutes, and starts rolling again.


### TrafficLights:
Simulates two traffic lights.
Each traffic light utilizes a resource, the permission to use the road, during green and yellow light and turn light red when the resource is released.


### Documents:
Simulates the following scenario:

A small service company needs to elaborate documents certifying the service provided.
Each Poisson distributed with lam = 1800 secs time, a document request arrives.
Only one secretary elaborates documents.

The process comes with the following conditions depending on client context and requirements:

Conditions is a binary string from 00000 to 11111.
A 1 is a True in each condition.
The conditions and its probability are:

```
00001 : Previous document found (0.8)
00010 : Printing required (0.85)
00100 : PDF format required (0.3)
01000 : Send by mail (0.85)
10000 : Upload file to drive (0.25)
```

The process and each activity time (in seconds) are (times are normally distributed, with a SD = 0.1*time):
```
Seek the previous document of the same client (30)
if 00001:
	take previous (5)
else:
	Take last or similar document (60)
Edit with new data (60)
Generate QR code (20)
Copy QR metadata to DB file (30)
Paste QR image in document (60)
Copy document data to DB file (70)
Check QR code is working (90)
Save (5)
if 00010:
	Print (15)
if 00100:
	Save as PDF (20)
	if 01000:
		Compose email (90)
		Send (5)
	if 10000:
		Upload file to drive (60)
		Generate drive link (30)
		Compose email (180)
		Check drive link is working (60)
		Send (5)
```
The process diagram:

![Generate document process](https://lh3.googleusercontent.com/pw/AM-JKLUJ0KB9bT6LFR_v2tRHfsaxfNm2Z9U2caX9_ACNvgEk_GlSRoGdHjStS9WGKz4Dd7--6TtKy1M7ZM_oaIbe_IGZFmXf8dgL_QkhHLDCZ4El-N30Qfzr39PH-ERwhdstB7utGQOeO2p9d_K983Db8Sp0=w1060-h752-no?authuser=0)

The script also simulates the behavior if documents arrive at a higher pace, if there are many secretaries, and counts how many documents were not elaborated at the end of the day, and graphics the information generated.

<Cabbage>
form caption("Vector Harmonizer"), size(450, 440), pluginId("vha1"), gioRefresh(50), colour(20,30,40)

;csoundoutput bounds(15, 238, 618, 395), text("Csound Output")
label bounds(138, 190, 100, 11), text("Interval vector"),fontColour(255, 255, 255, 255), 
label bounds(138, 210, 100, 11), text("0"),fontColour(255, 255, 255, 255), identChannel("vect1")
label bounds(155, 210, 100, 11), text("0"),fontColour(255, 255, 255, 255), identChannel("vect2") 
label bounds(172, 210, 100, 11), text("0"),fontColour(255, 255, 255, 255), identChannel("vect3")
label bounds(189, 210, 100, 11), text("0"),fontColour(255, 255, 255, 255), identChannel("vect4")
label bounds(206, 210, 100, 11), text("0"),fontColour(255, 255, 255, 255), identChannel("vect5")
label bounds(223, 210, 100, 11), text("0"),fontColour(255, 255, 255, 255), identChannel("vect6")

label bounds(18, 10, 73, 15), text("Playback"),  colour(160, 160, 160, 255), fontColour(255, 255, 255, 255), 
checkbox bounds(18, 30, 64, 20), channel("play1"), text("ch 1"), shape("square"),  colour(0, 255, 0, 255), fontColour(160, 160, 160, 255), value(0), 
checkbox bounds(18, 50, 64, 20), channel("play2"), text("ch 2"), shape("square"),  colour(0, 255, 0, 255), fontColour(160, 160, 160, 255), value(0), 
checkbox bounds(18, 70, 64, 20), channel("play3"), text("ch 3"), shape("square"),  colour(0, 255, 0, 255), fontColour(160, 160, 160, 255), value(0), 
checkbox bounds(18, 90, 64, 20), channel("play4"), text("ch 4"), shape("square"),  colour(0, 255, 0, 255), fontColour(160, 160, 160, 255), value(0), 
checkbox bounds(18, 110, 64, 20), channel("play5"), text("ch 5"), shape("square"),  colour(0, 255, 0, 255), fontColour(160, 160, 160, 255), value(0), 

checkbox bounds(18, 140, 101, 20), channel("auto_vRange"), text("auto vRange"), value(1), shape("square"),  colour(0, 255, 0, 255), fontColour(160, 160, 160, 255), value(0), 
hslider bounds(18, 160, 50, 30), channel("vRangeBorder"), range(1, 12, 7, 1, 1),  colour(255, 255, 255, 255), trackerColour(0, 255, 0, 255), fontColour(160, 160, 160, 255), 
label bounds(70, 164, 50, 10), text("Border"),  colour(160, 160, 160, 255), fontColour(255, 255, 255, 255), 
hslider bounds(18, 180, 100, 30), channel("vRangeMin"), range(1, 127, 30, 1, 1),  colour(255, 255, 255, 255), trackerColour(0, 255, 0, 255), fontColour(160, 160, 160, 255), 
hslider bounds(18, 200, 100, 30), channel("vRangeMax"), range(1, 127, 90, 1, 1),  colour(255, 255, 255, 255), trackerColour(0, 255, 0, 255), fontColour(160, 160, 160, 255), 

label bounds(138, 10, 67, 15), text("Record"),  colour(160, 160, 160, 255), fontColour(255, 255, 255, 255), 
checkbox bounds(138, 30, 64, 20), channel("record1"), text("ch 1"), shape("square"),  colour(0, 255, 0, 255), fontColour(160, 160, 160, 255), value(0), 
checkbox bounds(138, 50, 64, 20), channel("record2"), text("ch 2"), shape("square"),  colour(0, 255, 0, 255), fontColour(160, 160, 160, 255), value(0), 
checkbox bounds(138, 70, 64, 20), channel("record3"), text("ch 3"), shape("square"),  colour(0, 255, 0, 255), fontColour(160, 160, 160, 255), value(0), 
checkbox bounds(138, 90, 64, 20), channel("record4"), text("ch 4"), shape("square"),  colour(0, 255, 0, 255), fontColour(160, 160, 160, 255), value(0), 
checkbox bounds(138, 110, 64, 20), channel("record5"), text("ch 5"), shape("square"),  colour(0, 255, 0, 255), fontColour(160, 160, 160, 255), value(0), 

label bounds(138, 146, 100, 11), text("thresh time"),  colour(160, 160, 160, 255), fontColour(255, 255, 255, 255), 
hslider bounds(138, 160, 100, 30), channel("rthresh"), range(1, 500, 30, 1, 1),  colour(255, 255, 255, 255), trackerColour(0, 255, 0, 255), fontColour(160, 160, 160, 255), 

checkbox bounds(366, 8, 64, 20), channel("panic"), text("panic"), shape("square"),  colour(0, 255, 0, 255), fontColour(160, 160, 160, 255), value(0)

label bounds(266, 8, 100, 15), text("Scores"),  colour(160, 160, 160, 255), fontColour(255, 255, 255, 255)
hslider bounds(260, 28, 100, 30), channel("vRangeScore"), range(0.0, 1.0, 1.0)
hslider bounds(260, 48, 100, 30), channel("gravityScore"), range(0.0, 1.0, 1.0)
hslider bounds(260, 68, 100, 30), channel("commonScore"), range(0.0, 1.0, 1.0)
hslider bounds(260, 88, 100, 30), channel("distanceScore"), range(0.0, 1.0, 1.0)
hslider bounds(260, 108, 100, 30), channel("parallelScore"), range(0.0, 1.0, 1.0)
hslider bounds(260, 128, 100, 30), channel("spreadScore"), range(0.0, 1.0, 1.0)
hslider bounds(260, 148, 100, 30), channel("toggleScore"), range(0.0, 1.0, 1.0)
hslider bounds(260, 168, 100, 30), channel("repeatScore"), range(0.0, 1.0, 1.0)

label bounds(366, 38, 65, 11), text("vRange"),  colour(160, 160, 160, 255), fontColour(255, 255, 255, 255), 
label bounds(366, 58, 65, 11), text("Gravity"),  colour(160, 160, 160, 255), fontColour(255, 255, 255, 255), 
label bounds(366, 78, 65, 11), text("Common"),  colour(160, 160, 160, 255), fontColour(255, 255, 255, 255), 
label bounds(366, 98, 65, 11), text("Distance"),  colour(160, 160, 160, 255), fontColour(255, 255, 255, 255), 
label bounds(366, 118, 65, 11), text("Parallel"),  colour(160, 160, 160, 255), fontColour(255, 255, 255, 255), 
label bounds(366, 138, 65, 11), text("Spread"),  colour(160, 160, 160, 255), fontColour(255, 255, 255, 255), 
label bounds(366, 158, 65, 11), text("Toggle"),  colour(160, 160, 160, 255), fontColour(255, 255, 255, 255), 
label bounds(366, 178, 65, 11), text("Repeat"),  colour(160, 160, 160, 255), fontColour(255, 255, 255, 255), 

csoundoutput bounds(5,230,400,200)

</Cabbage>
<CsoundSynthesizer>
<CsOptions>
;-odac -M2 -m0
-n -d -+rtmidi=NULL -M0 -Q0 -m0d 

</CsOptions>
<CsInstruments>

	sr = 44100  
	ksmps = 128
	nchnls = 2	
	0dbfs = 1

	massign 0,1
	pgmassign 0, 0

gihandle OSCinit 8912
gioutport = 8910


; tables
	giSine		ftgen	0, 0, 65536, 10, 1	; sine wave
	giNotesCh1	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1
	giNotesCh2	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1
	giNotesCh3	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1
	giNotesCh4	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1
	giNotesCh5	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1
	giNotesCh6	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1
	giNotesCh7	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1
	giNotesCh8	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1
	giNotesCh9	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1
	giNotesCh10	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1
	giNotesCh11	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1
	giNotesCh12	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1
	giNotesCh13	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1
	giNotesCh14	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1
	giNotesCh15	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1
	giNotesCh16	ftgen	0, 0, 128, -2, 0	; hold active notes on midi channel 1

	giNotesChans	ftgen	0, 0, 16, -2, giNotesCh1, giNotesCh2, giNotesCh3, giNotesCh4, \	; bookkeeping for tables holding active notes on different channels
					      giNotesCh5, giNotesCh6, giNotesCh7, giNotesCh8,\
					      giNotesCh9, giNotesCh10, giNotesCh11, giNotesCh12,\
					      giNotesCh13, giNotesCh14, giNotesCh15, giNotesCh16

; panic handler
instr 99
kpanic chnget "panic"
ktrig trigger kpanic, 0.5, 0 
Spanic = "Panic"
puts Spanic, ktrig+1
if ktrig > 0 then
  turnoff2, 2, 0, 0
  event "i", 2, 2, 86400
  turnoff2, 1, 0, 0
  event "i", 1, 2, 86400
  midiout 176, 1, 123, 0
  midiout 176, 2, 123, 0
  midiout 176, 3, 123, 0
  midiout 176, 4, 123, 0
endif
endin


; ***************
; send note
instr   1
	inote		notnum
	ivel 		veloc
	ichn		midichn
	itime		times
	iM_instr = 4
  ifracinstrt = inote*0.001

	;print inote, ivel, ichn
  OSCsend     1, "127.0.0.1",gioutport, "/vectorHarmonizerNote", "iii", inote, ivel, ichn
	;event_i "i", (iM_instr+ifracinstrt), 0, -1, inote, ivel, ichn
	;print itime
	xtratim 1/kr
	krelease	release
	if krelease > 0 then
  	OSCsend     1, "127.0.0.1",gioutport, "/vectorHarmonizerNote", "iii", inote, 0, ichn
		;event "i", -(iM_instr+ifracinstrt), 0, .1, inote, ivel, ichn
	endif
endin	

; ***************
; receive note
instr   2
	knote 		init 0
	kvel 		init 0
	kchn 		init 0
	kfracinstr	init 0
	kcount		init 0
	ktime		times
nxtmsg:
  kk  		OSClisten gihandle, "/vectorHarmonizerReturnNote", "ffff", knote, kvel, kchn, kfracinstr
if (kk == 0) goto ex
	kcount 		= kcount +1
	Stest		sprintfk "received notes %i %i %i", knote, kvel, kchn
  ;puts Stest, kcount
	;printk2 ktime
	event "i", 3+kfracinstr, 0, .1, knote, kvel, kchn
  kgoto nxtmsg
ex:
endin

; ***************
; receive note
instr   3

	inote	= p4
	ivel = p5
	ichn = p6
	ioff = (ivel == 0 ? 1 : 0)	; turnoff flagged by zero velocity
	iM_instr = 4
	ifracinstrt	= frac(p1)
	inotestab	table ichn-1, giNotesChans
	inuminst table inote, inotestab

;print inote, ioff, inuminst, ifracinstrt
	if ioff == 0 then
		tableiw inuminst+1, inote, inotestab
		itest		table inote, inotestab
		;print itest, inote
		event_i "i", iM_instr+ifracinstrt, 0, -1, inote, ivel, ichn
endif

if ioff == 1 then
	tableiw inuminst-1, inote, inotestab
	event_i "i", -(iM_instr+ifracinstrt), 0, .1, inote, ivel, ichn
 	itestoff	table inote, inotestab
	;print itestoff, inote
endif

endin

;***************************************************
; midi note out
;***************************************************
instr 4

;print p1,p2,p3,p4,p5
;print frac(p1)*10000
	inote 	= p4
	ivel	= p5
	ichn	= p6
	idur		= (p3 < 0 ? 9999 : p3)	; use very long duration for realtime events, noteondur will create note off when instrument stops
	noteondur ichn, inote, ivel, idur
endin

;***************************************************
; OSC listener
;***************************************************
instr 9
	print gihandle, gioutport
	kvRangeMin	init 0
	kvRangeMax	init 0
nxtrange:
	k1 OSClisten gihandle, "/vectorHarmonizerControlReturn/range", "ff", kvRangeMin, kvRangeMax
	;printk2 k1
if (k1 == 0) goto exrange
	chnset kvRangeMin, "vRangeMin"
	chnset kvRangeMax, "vRangeMax"
exrange:

	kv1	init 0
	kv2	init 0
	kv3	init 0
	kv4	init 0
	kv5	init 0
	kv6 init 0

nxtvect:
	kv OSClisten gihandle, "/vectorHarmonizerControlReturn/vector", "ffffff", kv1, kv2, kv3, kv4, kv5, kv6

if (kv == 0) goto exvect
	S1 sprintfk "text(%i)", kv1
	S2 sprintfk "text(%i)", kv2
	S3 sprintfk "text(%i)", kv3
	S4 sprintfk "text(%i)", kv4
	S5 sprintfk "text(%i)", kv5
	S6 sprintfk "text(%i)", kv6
	chnset S1, "vect1"
	chnset S2, "vect2"
	chnset S3, "vect3"
	chnset S4, "vect4"
	chnset S5, "vect5"
	chnset S6, "vect6"
exvect:
endin

;***************************************************
; test init control data (when not running under Cabbage)
	instr 11
		chnset 1, "play1"
		chnset 0, "play2"
		chnset 0, "play3"
		chnset 0, "play4"
		chnset 0, "play5"
		chnset 0, "record1"
		chnset 1, "record2"
		chnset 0, "record3"
		chnset 0, "record4"
		chnset 0, "record5"
		chnset 1, "auto_vRange"
		chnset 7, "vRangeBorder"
		chnset 40, "vRangeMin"
		chnset 80, "vRangeMax"
		chnset 30, "rthresh"
		chnset 1, "vRangeScore"
		chnset 1, "gravityScore"
		chnset 1, "commonScore"
		chnset 1, "distanceScore"
		chnset 1, "parallelScore"
		chnset 1, "spreadScore"
		chnset 1, "toggleScore"
		chnset 1, "repeatScore"
	endin


;***************************************************
; send control data
	instr 12

kplay1		chnget "play1"
kplay2		chnget "play2"
kplay3		chnget "play3"
kplay4		chnget "play4"
kplay5		chnget "play5"
krecord1	chnget "record1"
krecord2	chnget "record2"
krecord3	chnget "record3"
krecord4	chnget "record4"
krecord5	chnget "record5"
kauto_vRange	chnget "auto_vRange"
kvRangeBorder	chnget "vRangeBorder"
kvRangeMin	chnget "vRangeMin"
kvRangeMax	chnget "vRangeMax"
krthresh	chnget "rthresh"
kvRangeScore	chnget "vRangeScore"
kgravityScore	chnget "gravityScore"
kcommonScore	chnget "commonScore"
kdistanceScore	chnget "distanceScore"
kparallelScore	chnget "parallelScore"
kspreadScore	chnget "spreadScore"
ktoggleScore	chnget "toggleScore"
krepeatScore	chnget "repeatScore"

          		OSCsend     kplay1, "127.0.0.1",gioutport, "/vectorHarmonizerControl/play1", "f", kplay1
          		OSCsend     kplay2, "127.0.0.1",gioutport, "/vectorHarmonizerControl/play2", "f", kplay2
          		OSCsend     kplay3, "127.0.0.1",gioutport, "/vectorHarmonizerControl/play3", "f", kplay3
          		OSCsend     kplay4, "127.0.0.1",gioutport, "/vectorHarmonizerControl/play4", "f", kplay4
          		OSCsend     kplay5, "127.0.0.1",gioutport, "/vectorHarmonizerControl/play5", "f", kplay5
          		OSCsend     krecord1, "127.0.0.1",gioutport, "/vectorHarmonizerControl/record1", "f", krecord1
          		OSCsend     krecord2, "127.0.0.1",gioutport, "/vectorHarmonizerControl/record2", "f", krecord2
          		OSCsend     krecord3, "127.0.0.1",gioutport, "/vectorHarmonizerControl/record3", "f", krecord3
          		OSCsend     krecord4, "127.0.0.1",gioutport, "/vectorHarmonizerControl/record4", "f", krecord4
          		OSCsend     krecord5, "127.0.0.1",gioutport, "/vectorHarmonizerControl/record5", "f", krecord5
          		OSCsend     kauto_vRange, "127.0.0.1",gioutport, "/vectorHarmonizerControl/auto_vRange", "f", kauto_vRange
          		OSCsend     kvRangeBorder, "127.0.0.1",gioutport, "/vectorHarmonizerControl/kvRangeBorder", "f", kvRangeBorder 
          		OSCsend     kvRangeMin, "127.0.0.1",gioutport, "/vectorHarmonizerControl/kvRangeMin", "f", kvRangeMin	  
          		OSCsend     kvRangeMax, "127.0.0.1",gioutport, "/vectorHarmonizerControl/kvRangeMax", "f", kvRangeMax	  
          		OSCsend     krthresh, "127.0.0.1",gioutport, "/vectorHarmonizerControl/krthresh", "f", krthresh	  
          		OSCsend     kvRangeScore, "127.0.0.1",gioutport, "/vectorHarmonizerControl/kvRangeScore", "f", kvRangeScore  
          		OSCsend     kgravityScore, "127.0.0.1",gioutport, "/vectorHarmonizerControl/kgravityScore", "f", kgravityScore 
          		OSCsend     kcommonScore, "127.0.0.1",gioutport, "/vectorHarmonizerControl/kcommonScore", "f", kcommonScore  
          		OSCsend     kdistanceScore, "127.0.0.1",gioutport, "/vectorHarmonizerControl/kdistanceScore", "f", kdistanceScore
          		OSCsend     kparallelScore, "127.0.0.1",gioutport, "/vectorHarmonizerControl/kparallelScore", "f", kparallelScore
          		OSCsend     kspreadScore, "127.0.0.1",gioutport, "/vectorHarmonizerControl/kspreadScore", "f", kspreadScore  
          		OSCsend     ktoggleScore, "127.0.0.1",gioutport, "/vectorHarmonizerControl/ktoggleScore", "f", ktoggleScore  
          		OSCsend     krepeatScore, "127.0.0.1",gioutport, "/vectorHarmonizerControl/krepeatScore", "f", krepeatScore  
	endin


</CsInstruments>
<CsScore>
#define SCORELEN # 84600 #
i2  0 $SCORELEN		; listen to return notes
i9  0 $SCORELEN		; listen to return control data
;i11 .1 1		; test init control data
i12 0 $SCORELEN		; send control data
i99 0 $SCORELEN		; panic handler
e
</CsScore>
</CsoundSynthesizer>
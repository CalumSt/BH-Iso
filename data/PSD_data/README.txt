Original data files are from following sources and stored in original_data.

Virgo data:
From LIGO-T1300121 (used for the MDCs)
"Early" advanced Virgo design sensitivity: column 4 in adv_spectra_phase1.txt. 
Design sensitivity: column 2 in adv_spectra_phase2.txt.

From LIGO-P1200087, fig 1(b), numbers from fig1_adv_sensitivity.txt.
top of "early" blue curve seems to be the same as the "early" from T1300121.
I have used top of the mid and late curves from this document too.
Design curve agrees with T1300121.

LIGO Data:
From LIGO-T1200307,
Early: data50Mpc_step1.txt
Mid: data100Mpc_step2.txt
Late: data150Mpc_step3.txt
Final: dataNOMaLIGO.txt


I have extracted the columns needed for aligo and advirgo in the format the code needs.
Here are the details for later reference.

FILE                 SOURCE
====                 ======

aligo_early.txt    LIGO-T1200307
aligo_mid.txt      LIGO-T1200307
aligo_late.txt     LIGO-T1200307
aligo_design.txt   LIGO-T1200307

advirgo_early.txt  LIGO-T1300121 / LIGO-P1200087 (top of blue curve, column 2)
advirgo_mid.txt    LIGO-P1200087 (top of green curve, column 3)
advirgo_late.txt   LIGO-P1200087 (top of red curve, column 5)
advirgo_design.txt LIGO-T1300121 (agrees with design in LIGO-P1200087, black curve)



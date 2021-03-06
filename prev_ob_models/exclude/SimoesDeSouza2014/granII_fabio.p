// Type II granule cell
// Modified from Upinder S. Bhalla, Caltech, May 1991
// fields are ..
// name
// parent
// x,y,z  // coords of endpoint. 
// dia // needed for memb props. All lengths are in microns.
// ch name density 
// ch name density 
// .....
// Control lines start with '*'. Valid control options are 
// *relative 			- relative coords.
// *absolute			- absolute coords.
// *asymmetric			- use asymmetric compartments
// *symmetric			- use symmetric compartments

// #	name	parent		x	y	z	d	ch	dens	ch	dens	.	.	.

*asymmetric
*relative
*cartesian

*set_global	RM	12.0
*set_global	RA	0.5
*set_global	CM	0.01
*set_global	EREST_ACT	-0.065

*memb_factor 2.0

*start_cell /library/notfakespine1
notfakespine1	none		10	0	0	2
neck     	.      		1.9	0	0	0.23 
head	        .      		0.8	0	0	0.8   AMPA_NMDA -1000e-12 Ca_conc -26e10
*makeproto /library/notfakespine1

*start_cell /library/notfakespine2
notfakespine2	none		10	0	0	2
neck		.		-1.9	0	0	0.23 
head		.		-0.8	0	0	0.8   AMPA_NMDA -1000e-12 Ca_conc -26e10
*makeproto /library/notfakespine2

//*add_spines DENDR_DIAM SPINE_DENS SPINE_SUR   
//Adds membrane surface for collapsed spines to all compartments with
// dia <= DENDR_DIAM; units: DENDR_DIAM (um), SPINE_DENS (1/um), SPINE_SUR (um^2).

*add_spines 5 0.0139 3.37

*start_cell
*compt /library/notfakespine1
soma		none		0	0	8	6	Na2_rat_smsnn	1611	K_mit_usb	1313	KM_bsg_upi	1334	KA_bsg_yka	12.7	Rm	200e6

*polar

*compt /library/notfakespine2
trunk[0]	soma		40	0	0	2	Na2_rat_smsnn	1.7	K_mit_usb	71
*compt /library/notfakespine1
trunk[1]	.		40	-60	10	1.5	Na2_rat_smsnn	1.7	K_mit_usb	71
*compt /library/notfakespine2
trunk[2]	.		20	-30	10	1.4	Na2_rat_smsnn	1.7	K_mit_usb	71
*compt /library/notfakespine1
trunk[3]	.		20	0	0	1.3	Na2_rat_smsnn	1.7	K_mit_usb	71
*compt /library/notfakespine2
trunk[4]	.		20	40	10	1.3	Na2_rat_smsnn	1.7	K_mit_usb	71
*compt /library/notfakespine1
trunk[5]	.		20	60	20	1.3	Na2_rat_smsnn	1.7	K_mit_usb	71
*compt /library/notfakespine2
trunk[6]	.		20	40	10	1.3	Na2_rat_smsnn	1.7	K_mit_usb	71
*compt /library/notfakespine1
trunk[7]	.		20	0	0	1.3	Na2_rat_smsnn	1.7	K_mit_usb	71
*compt /library/notfakespine2
trunk[8]	.		20	20	10	1.3	Na2_rat_smsnn	1.7	K_mit_usb	71
*compt /library/notfakespine1
periph1[0]	trunk[8]	10	10	20	1.25	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph1[1]	.		10	10	30	1.25	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph1[2]	.		10	0	20	1.25	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph1[3]	.		10	-10	10	1.25	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph1[4]	.		10	0	20	1.25	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph11[0]	.		10	5	30	1.2	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph11[1]	.		10	10	20	1.2	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph11[2]	.		10	10	10	1.18	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph11[3]	.		10	20	10	1.17	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph11[4]	.		10	30	30	1.16	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph11[5]	.		10	20	40	1.15	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph11[6]	.		10	30	40	1.14	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph11[7]	.		10	40	10	1.13	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph11[8]	.		10	40	20	1.12	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph11[9]	.		10	50	30	1.11	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph11[10]	.		10	30	10	1.10	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph11[11]	.		10	20	50	1.09	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph11[12]	.		10	40	50	1.08	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph11[13]	.		10	40	20	1.07	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph11[14]	.		10	20	30	1.06	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph11[15]	.		10	20	10	1.05	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph11[16]	.		10	30	10	1.04	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph11[17]	.		10	40	10	1.03	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph11[18]	.		10	50	30	1.02	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph11[19]	.		10	50	40	1.01	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph11[20]	.		10	30	20	1.00	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph12[0]	periph1[4]	10	-20	30	1.2	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph12[1]	.		10	-20	50	1.2	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph12[2]	.		10	-30	50	1.18	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph12[3]	.		10	-30	10	1.16	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph12[4]	.		10	-50	20	1.15	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph12[5]	.		10	-50	10	1.14	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph12[6]	.		10	-40	40	1.13	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph12[7]	.		10	-40	30	1.12	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph121[0]	periph12[7]	10	-40	30	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph121[1]	.		10	-50	20	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph121[2]	.		10	-60	30	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph121[3]	.		10	-70	10	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph121[4]	.		10	-60	10	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph121[5]	.		10	-60	30	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph122[0]	periph12[7]	10	-80	10	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph122[1]	.		10	-90	30	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph122[2]	.		10	-100	20	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph122[3]	.		10	-100	30	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph122[4]	.		10	-100	30	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph122[5]	.		10	-90	30	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph122[6]	.		10	-80	50	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph122[7]	.		10	-80	40	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph122[8]	.		10	-80	40	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph122[9]	.		10	-70	40	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph122[10]	.		10	-90	30	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph122[11]	.		10	-90	10	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph2[0]	trunk[8]	10	120	20	1.2	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph2[1]	.		10	130	30	1.2	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph2[2]	.		10	130	30	1.19	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph2[3]	.		10	110	30	1.18	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph2[4]	.		10	110	40	1.17	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph2[5]	.		10	100	40	1.16	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph2[6]	.		10	120	40	1.15	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph2[7]	.		10	120	10	1.14	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph2[8]	.		10	140	10	1.13	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph2[9]	.		10	140	10	1.12	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph2[10]	.		10	120	20	1.11	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph2[11]	.		10	140	20	1.1	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph2[12]	.		10	150	20	1.1	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph21[0]	periph2[12]	10	170	20	1.03	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph21[1]	.		10	160	30	1.02	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph21[2]	.		10	150	30	1.01	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph21[3]	.		10	170	40	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph21[4]	.		10	150	20	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph21[5]	.		10	150	20	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph22[0]	periph2[12]	10	185	20	1.05	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph22[1]	.		10	190	20	1.03	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph22[2]	.		10	200	30	1.02	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph22[3]	.		10	220	30	1.01	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph22[4]	.		10	220	40	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph22[5]	.		10	200	20	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph22[6]	.		10	200	20	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
periph22[7]	.		10	220	30	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine2
periph22[8]	.		10	200	30	1.0	Na2_rat_smsnn	1355	K_mit_usb	243
*compt /library/notfakespine1
deep0[0]	soma		10	15	150	1.0
*compt /library/notfakespine2
deep0[1]	.		10	25	160	0.8
*compt /library/notfakespine1
deep0[2]	.		10	25	160	0.8
*compt /library/notfakespine2
deep0[3]	.		10	15	160	0.7
*compt /library/notfakespine1
deep0[4]	.		10	15	150	0.6
*compt /library/notfakespine2
deep0[5]	.		10	25	150	0.5
*compt /library/notfakespine1
deep0[6]	.		10	5	140	0.5
*compt /library/notfakespine2
deep0[7]	.		10	15	140	0.5
*compt /library/notfakespine1
deep1[0]	soma		10	125	140	1.0
*compt /library/notfakespine2
deep1[1]	.		10	125	140	0.8
*compt /library/notfakespine1
deep1[2]	.		10	135	130	0.8
*compt /library/notfakespine2
deep1[3]	.		10	145	130	0.7
*compt /library/notfakespine1
deep1[4]	.		10	135	150	0.6
*compt /library/notfakespine2
deep1[5]	.		10	135	150	0.5
*compt /library/notfakespine1
deep1[6]	.		10	145	140	0.5
*compt /library/notfakespine2
deep1[7]	.		10	155	140	0.5
*compt /library/notfakespine1
deep2[0]	soma		10	-105	140	1.0
*compt /library/notfakespine2
deep2[1]	.		10	-115	160	0.8
*compt /library/notfakespine1
deep2[2]	.		10	-105	160	0.7
*compt /library/notfakespine2
deep2[3]	.		10	-115	160	0.6
*compt /library/notfakespine1
deep2[4]	.		10	-125	150	0.5
*compt /library/notfakespine2
deep2[5]	.		10	-125	140	0.5
*compt /library/notfakespine1
deep2[6]	.		10	-115	130	0.5
*compt /library/notfakespine2
deep2[7]	.		10	-105	130	0.5






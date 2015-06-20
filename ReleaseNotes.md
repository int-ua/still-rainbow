# v0.96 #
Moved scenarios to private folder:<br>
<i>!:\private\e6c858ac\csv\</i><br>
And added functions for importing, exporting and deleting them.<br>

Added hotkeys map as png image, available in menu and located at<br>
<i>!:\private\e6c858ac\hotkeys.png</i><br>

Exit from help page on right button click.<br>
Minor help corrections.<br>
Showing an error if modules import fail.<br>
<h1>v0.95</h1>
Added pause to all loops. Translated help.<br>
Changed almost all hotkeys.<br>

From now on scenario format is uniform csv file with next fields:<br>
<i>velocity_red,velocity_green,velocity_blue,target_red,target_green,target_blue,wait_n_seconds</i><br>

All except wait interval are supposed to be nonnegative integers. However, there is much silent auto-correction of logic errors, so the only strict rule is that they can be read as integers. Seconds can be float values (rounded to nearest tenths during read) or integers.<br>

The most readable line(s) will be:<br>
00,15,22,000,090,255,1.5<br>
the most compact:<br>
0,15,22,0,90,255,1.5<br>
next line:<br>
-999,	0,	999,	-255,	285,	0,	3.1415<br>
will affect as:<br>
255,	0<sup>1</sup>,	255,	0,	255,	0,	3.1<br>

<sup>1</sup>If color not equals target, but velocity is 0 current velocity is used instead. And it's not a bug, it's a feature.<br>

Next line:<br>
0,0,0,255,255,255,0<br>
will result in using current velocity for all channels.<br>

To disable reading certain line, just comment it out with "#", leave blank or write less then 13 characters in it.
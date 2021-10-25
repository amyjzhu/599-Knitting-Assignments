;!knitout-2
;;Machine: SWG091N2
;;Gauge: 5
;;Width: 250
;;Carriers: 1 2 3 4 5 6 7 8 9 10
;;Position: Center
inhook  3 ;
tuck - f3 3 ; tuck loop -1, 
tuck - f1 3 ; tuck loop -1, 
tuck + f2 3 ; tuck loop -1, odd cast-on
tuck + f4 3 ; tuck loop -1, 
releasehook  3 ;
knit - f4 3 ; knit loop -1, stabilize cast-on
knit - f3 3 ; knit loop -1, 
knit - f2 3 ; knit loop -1, 
knit - f1 3 ; knit loop -1, 
knit + f1 3 ; knit loop 0, first row loops
knit + f2 3 ; knit loop 1, 
knit + f3 3 ; knit loop 2, 
knit + f4 3 ; knit loop 3, 
xfer f2 b2 ;send loops to decrease to back
xfer f3 b3 ;
rack -1 ;rack to xfer b3 to f2
xfer b3 f2 ;stack decreases with offset -1
rack 0 ;rack to xfer b2 to f2
xfer b2 f2 ;stack decreases with offset 0
knit - f4 3 ; knit loop 4, Knit course 1
knit - f3 3 ; knit loop 5, 
knit - f2 3 ; knit loop 6, 
knit - f1 3 ; knit loop 7, 
knit + f1 3 ; knit loop 8, Knit course 2
knit + f2 3 ; knit loop 9, 
knit + f3 3 ; knit loop 10, 
knit + f4 3 ; knit loop 11, 
xfer f2 b2 ;send loops to decrease to back
xfer f3 b3 ;
rack -1 ;rack to xfer b3 to f2
xfer b3 f2 ;stack decreases with offset -1
rack 0 ;rack to xfer b2 to f2
xfer b2 f2 ;stack decreases with offset 0
knit - f4 3 ; knit loop 12, Knit course 3
knit - f3 3 ; knit loop 13, 
knit - f2 3 ; knit loop 14, 
knit - f1 3 ; knit loop 15, 
outhook  3 ;
drop f1 ;Drop KnitGraph
drop f2 ;
drop f3 ;
drop f4 ;

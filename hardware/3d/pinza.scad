use <./catchnhole/catchnhole.scad>;
// Measurements are in MILIMETERS.
topleft=200;
topright=200;
base_len=45;
cwid = 10;
p = 5; // TODO: technically, we can use 0.6cm here. It **should** fit up to 0.75 but we want to add some margin.
// This would mean a stronger grip, lets try it this way...
leg_h = 9;

// Base cube's h is 5mm, wich leaves for leg_h - 5mm for the methacrylate piece's height.

internal_cube_w = (base_len / 1.5) - (p * 2);
internal_cube_h = 23;
internal_cube_l = cwid;
pieces_separation = 3;

separation = base_len + pieces_separation;
entry_len = 0.7;

module Grip(base_x, base_y){
    difference(){
        echo(base_x)
 
        union() {
             // Base
             translate([
                 base_x,
                 base_y,
                 -leg_h
             ]) 
                 cube([base_len, cwid, p]);

             // Legs
             translate([
                 base_x, 
                 base_y, 
                 -leg_h
             ]) 
                 cube([p, cwid, leg_h]);
                      
             translate([
                 base_x + base_len - p, 
                 base_y, 
                 -leg_h
             ]) 
                 cube([p, cwid, leg_h]);
             
             // Top piece
             translate([
                 base_x + (base_len / 2) - (internal_cube_w / 2), 
                 base_y + ((cwid - internal_cube_l) / 2), 
                 - leg_h - internal_cube_h
             ]) 
                 cube([internal_cube_w, internal_cube_l, internal_cube_h]);
        }
        
        // Main body leg bolts
        translate([
            base_x + (p/2) + 1,
            base_y + (cwid / 2),
            -leg_h
        ]) {
            bolt("M3", length = leg_h);
            nutcatch_parallel("M3");    
        }
        translate([
            base_x + base_len - (p/2) - 1, 
            base_y + (cwid / 2), 
            -leg_h
        ]){
            bolt("M3", length = leg_h);
            nutcatch_parallel("M3");    
        }
        // Top piece bolt
        translate([
            base_x  + (base_len / 2),
            base_y + p, 
            -( internal_cube_h + cwid)
        ]){
        
            bolt("M3", length = internal_cube_h - p);
            nutcatch_parallel("M3");    
        }
        
        // Top piece nut insertion
        translate([
            base_x  + (base_len / 2),
            base_y + p, 
            -( internal_cube_h + cwid - 10)
        ])
            nutcatch_sidecut("M3");    
    }

    difference() {
         // Base
         translate([base_x + base_len + pieces_separation, base_y, -p]) 
             cube([base_len, cwid, p]);
             
         translate([
            base_x + (p/2) + base_len + pieces_separation +2,
            base_y + (cwid / 2),
            -leg_h + p
        ]) {
            bolt("M3", length = leg_h + 10);
            nutcatch_parallel("M3");    
        }
        translate([
            base_x + base_len - (p/2) + base_len + pieces_separation -2, 
            base_y + (cwid / 2), 
            -leg_h + p 
        ]){
            bolt("M3", length = leg_h + 10);
            nutcatch_parallel("M3");    
        }
    }
}

cols = 7;
lines = 2;
rotate([180,0,0]){

for (col =[0:cols-1]) {
   for (lin =[0:lines-1]) 
       Grip(separation * 2 * lin, 20 * col);
}
}
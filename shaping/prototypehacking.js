let vertical_gauge = 15
let horizontal_gauge = 15

let pattern = "p, k, float {z}, k" // calculate pattern width
let num_repeats = 10 // tilings
// use these to calculate how long the variable parts of each pattern should be 

// we need to perform an operation that will shift all loops outwards by n.
// n should really only be 1 to begin with... but wouldn't the things at the outside shift a lot?
// I guess not a lot relative to the next stitches, but a lot relative to the old stitches 

// specify each size, in order from bottom to top, and when they occur
// say the tube is 30 centimetres long
tube_shape = [{ width: 5, at: 0 }, { width: 5.5, at: 5 }, { width: 10, at: 20 }, { width: 5, at: 30 }]

function get_pattern_signature(pattern) {
    // return a thing like 
}

function get_fixed_pattern_width(pattern) {


}

function get_size(pattern, num_repeats, width) {
    let fixed = get_fixed_pattern_width(pattern);
    let pattern_size = width / num_repeats;

    let variable = pattern_size - fixed
    // the length of each variable depends on the ratio of variable to known size and proportion of each variable 
}

function interpolate(width1, width2, distance) {
    // says when to do the shifts
    // say we have a basic interpolation strategy. We figure out how many shifts we need and then 
    // take the distance between two widths and two widths and return movement points (one transfer per point for now or could stack to do 2)
    let basic_strategy = () => {
        let num_points = Math.abs(width2 - width1) / distance
        let num_rows = distance * horizontal_gauge
        let dist = num_points / num_rows // how many rows between each point? 
        let points = Array.from({ length: num_points }, (_, i) => i * dist)
        return points // todo: check if this is correct 
        // how many rows is that though? 
    }

}


// what is the actual strategy for moving everything overr? hm
// for now, we just need to establish a number of stitches in each row.


//basically need to recreate knitout that looks like:
function do_a_tube() {
    // 15 rows of 20, 10 rows of 25, 5 rows of 35, 10 rows of 25, 15 rows of 20 = 55 rows
    // import the knitoutWriter code and instantiate it as an object
    var knitout = require('../../../knitting/knitout-frontend-js/knitout.js');
    k = new knitout.Writer({ carriers: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] });

    // add some headers relevant to this job
    k.addHeader('Machine', 'SWG091N2');
    k.addHeader('Gauge', '5');
    k.addHeader('Width', '250');
    k.addHeader('Position', 'Center');

    // swatch variables
    let height = 20; // 5-row repeats
    // var width = 40; 
    var width = 6; // 6 repeats
    var repeat_size = 4; // needles involved in repeat
    var carrier = "4";

    // bring in carrier using yarn inserting hook
    k.inhook(carrier);

    let sts = [30, 29, 28, 26, 25, 24, 22, 21, 20, 18, 17, 16, 14, 13, 12, 10, 9, 8, 6, 5, 4]
    sts.reverse();
    var front = (width * repeat_size) % 2

    // tuck on alternate needles to cast on
    for (var s of sts.reverse()) {
        if (s % 2 == front) {
            k.tuck("-", "f" + s, carrier);
        }
        else {
            //k.miss("-", "f"+s, carrier);
        }
    }
    for (var s of sts.reverse()) {
        if (s % 2 != front) {
            k.tuck("+", "f" + s, carrier);
        }
        else {
            //k.miss("+", "f"+s, carrier);
        }
    }

    // SOMETHING IS REALLY SILLY WITH POSITIONING 

    k.releasehook(carrier);

    // kpkf kpkf kpkf kpkf kpkf kpkf kpk
    // becomes kpkff kpkff kpkff kpkff kpkff kpkff kpk
    // each set before the midpoint moves over its distance from the midpoint

    k.xfer(`f${(width + 1) * repeat_size + 1}`, `b${(width + 1) * repeat_size + 1}`);

    for (var s = width; s > 0; s--) {
        k.xfer(`f${s * repeat_size + 1}`, `b${s * repeat_size + 1}`);
        // skip the next needle 
    }

    // initial knit
    for (var h = 0; h < height; h++) {
        // last three
        k.knit("-", `f${(width + 1) * repeat_size + 2}`, carrier);
        k.knit("-", `f${(width + 1) * repeat_size + 1}`, carrier);
        k.knit("-", `f${(width + 1) * repeat_size}`, carrier);

        for (var s = width; s > 0; s--) {
            k.knit("-", `f${s * repeat_size + 2}`, carrier);
            k.knit("-", `b${s * repeat_size + 1}`, carrier);
            k.knit("-", `f${s * repeat_size}`, carrier);
            // skip the next needle 
        }

        for (var s = 1; s <= width; s++) {
            k.knit("+", `f${s * repeat_size}`, carrier);
            k.knit("+", `b${s * repeat_size + 1}`, carrier);
            k.knit("+", `f${s * repeat_size + 2}`, carrier);
        }

        // last three
        k.knit("+", `f${(width + 1) * repeat_size}`, carrier);
        k.knit("+", `f${(width + 1) * repeat_size + 1}`, carrier);
        k.knit("+", `f${(width + 1) * repeat_size + 2}`, carrier);
    }

    // transfer outward
    // the first four transfer 3 out
    // the second four transfer 2 out 
    // the third transfer 1 out
    // etc

    // I forgot we need to transfer our purl stitches

    // first transfer the first half to the backside
    for (var s = 1; s <= width / 2; s++) {
        k.xfer(`f${s * repeat_size}`, `b${s * repeat_size}`)
        k.xfer(`f${s * repeat_size + 1}`, `b${s * repeat_size + 1}`)
        k.xfer(`f${s * repeat_size + 2}`, `b${s * repeat_size + 2}`)
    }

    // now we're going to rack and transfer
    for (racking = 1; racking <= 3; racking++) {
        // transfer the set that's closer
        to_xfer = (width / 2 + 1) - racking
        
        k.rack(racking * -1)

        needle_back = to_xfer * repeat_size
        needle_front = to_xfer * repeat_size - racking // new positions
        k.xfer("b" + needle_back, "f" + needle_front)
        k.xfer("b" + (needle_back + 1), "f" + (needle_front + 1))
        k.xfer("b" + (needle_back + 2), "f" + (needle_front + 2))
    }

    k.rack(0)

    // now the opposite direction...
    for (var s = (width / 2) + 2; s <= width + 1; s++) { // never 0 because that's fine 
        k.xfer(`f${s * repeat_size}`, `b${s * repeat_size}`)
        k.xfer(`f${s * repeat_size + 1}`, `b${s * repeat_size + 1}`)
        k.xfer(`f${s * repeat_size + 2}`, `b${s * repeat_size + 2}`)
    }

    // second rack and transfer
    for (racking = 1; racking <= 3; racking++) {
        // transfer the set that's closer
        to_xfer = (width / 2) + 1 + racking
        k.rack(racking)
        needle_back = to_xfer * repeat_size
        needle_front = to_xfer * repeat_size + racking // new positions
        k.xfer("b" + needle_back, "f" + needle_front)
        k.xfer("b" + (needle_back + 1), "f" + (needle_front + 1))
        k.xfer("b" + (needle_back + 2), "f" + (needle_front + 2))
    }

    k.rack(0)

    
    // go in new form
    // need to start at what needle?
    repeat_size = 5;
    shift_back = 4;

    // put purls back
    k.xfer(`f${(width + 1) * repeat_size + 1 - shift_back}`, `b${(width + 1) * repeat_size + 1 - shift_back}`);

    for (var s = width; s > 0; s--) {
        k.xfer(`f${s * repeat_size + 1 - shift_back}`, `b${s * repeat_size + 1 - shift_back}`);
        // skip the next needle 
    }

    for (var h = 0; h < height; h++) {
        // last three
        k.knit("-", `f${(width + 1) * repeat_size + 2 - shift_back}`, carrier);
        k.knit("-", `f${(width + 1) * repeat_size + 1 - shift_back}`, carrier);
        k.knit("-", `f${(width + 1) * repeat_size - shift_back}`, carrier);

        for (var s = width; s > 0; s--) {
            k.knit("-", `f${s * repeat_size + 2 - shift_back}`, carrier);
            k.knit("-", `b${s * repeat_size + 1 - shift_back}`, carrier);
            k.knit("-", `f${s * repeat_size - shift_back}`, carrier);
            // skip the next needle 
        }

        for (var s = 1; s <= width; s++) {
            k.knit("+", `f${s * repeat_size - shift_back}`, carrier);
            k.knit("+", `b${s * repeat_size + 1 - shift_back}`, carrier);
            k.knit("+", `f${s * repeat_size + 2 - shift_back}`, carrier);
        }

        // last three
        k.knit("+", `f${(width + 1) * repeat_size - shift_back}`, carrier);
        k.knit("+", `f${(width + 1) * repeat_size + 1 - shift_back}`, carrier);
        k.knit("+", `f${(width + 1) * repeat_size + 2 - shift_back}`, carrier);
    }

    k.outhook(carrier);

    k.write('shaping-floats.k');
}

do_a_tube()
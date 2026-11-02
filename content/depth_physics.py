"""Extended theory, context and viva material for the Physics practicals.

Each entry deepens what the simulation can show on its own: why the quantity
matters, what the working equation really says, how the measurement goes wrong
in a real lab, and the questions an examiner is likely to ask.
"""

PHYSICS_DEPTH = {
    "phy-vernier-ix": {
        "objectives": [
            "Read a vernier scale correctly and state the least count of the instrument.",
            "Correct a measured length for zero error before using it.",
            "Convert a diameter into a cross-sectional area with the right significant figures.",
        ],
        "theory": [
            "A vernier callipers works by comparing two scales of slightly different pitch. "
            "The main scale is marked in millimetres; the vernier scale carries ten divisions "
            "that together span nine main-scale divisions. One vernier division is therefore "
            "0.9 mm, and the difference between one main-scale and one vernier division is "
            "0.1 mm — that difference is the least count.",
            "To read the instrument you record where the vernier zero sits on the main scale, "
            "then find which vernier division lines up exactly with a main-scale mark. That "
            "coinciding division, multiplied by the least count, is the fraction of a "
            "millimetre to add. Because the jaws have thickness and the scale may not be "
            "printed exactly at zero, the closed-jaw reading (the zero error) must be "
            "subtracted from every measurement.",
        ],
        "formula": "least count = 1 main-scale division ÷ number of vernier divisions = 0.01 cm\n"
        "true length = observed reading − zero error\n"
        "A = πd² / 4",
        "context": "The same principle sits inside every caliper in a workshop, a machinist's "
        "micrometer and the digital vernier used to check brake discs. Reading an analogue "
        "scale is still the fallback when a battery dies, and the zero-error idea returns in "
        "every instrument that has a datum mark.",
        "precautions": [
            "Close the jaws gently and record the zero error before touching the object.",
            "Do not overtighten: soft metal and plastic compress and read small.",
            "Measure at three positions along and around the cylinder, then average.",
            "Keep the line of sight perpendicular to the scale to avoid parallax.",
        ],
        "errors": [
            "Parallax when the eye is not square to the scale.",
            "Zero error left uncorrected, which shifts every reading by the same amount.",
            "The cylinder is not perfectly circular, so one diameter does not describe it.",
        ],
        "exam": [
            "Always quote the least count with its unit and show the zero-error correction as a line of working.",
            "Give the area to the same number of significant figures as the diameter — no more.",
        ],
        "viva": [
            {"q": "Why does the vernier scale have ten divisions spanning nine main-scale divisions?",
             "a": "That mismatch creates a fixed 0.1 mm difference between adjacent divisions. Only one pair of marks can coincide at a time, so the position of that pair encodes the fraction of a division."},
            {"q": "What happens to your result if the zero error is positive and you forget to subtract it?",
             "a": "Every reading, and therefore the mean diameter, is too large by the zero error. The area, which depends on the square of the diameter, is then too large by roughly twice the fractional error."},
            {"q": "Why measure the diameter in two perpendicular directions?",
             "a": "A real cylinder is slightly elliptical. Two perpendicular diameters characterise the ellipse far better than a single measurement, and their mean is a good estimate of the effective diameter."},
        ],
    },
    "phy-screw-gauge-ix": {
        "objectives": [
            "Determine the pitch and least count of a screw gauge.",
            "Read main-scale and circular-scale values and combine them correctly.",
            "Explain why a ratchet is used instead of turning the thimble by hand.",
        ],
        "theory": [
            "A screw gauge converts a rotation into a very small linear movement. One full turn "
            "of the thimble advances the spindle by one pitch — commonly 0.5 mm. The circular "
            "scale is divided into 50 parts, so one division corresponds to 0.5 ÷ 50 = 0.01 mm. "
            "That is ten times finer than a vernier callipers.",
            "The reading is the main scale exposed beyond the sleeve plus the circular-scale "
            "division that lines up with the datum line, multiplied by the least count. If the "
            "circular scale reads past zero when the jaws are closed, the zero error is positive "
            "and is subtracted; if the datum sits below zero, the error is negative and is added.",
        ],
        "formula": "pitch = distance moved per complete turn\n"
        "least count = pitch ÷ circular-scale divisions\n"
        "diameter = main scale + (circular division × least count) − zero error",
        "context": "Screw gauges set the tolerance on fuel injectors, guitar strings and "
        "laboratory capillary tubing. The same screw-and-nut geometry drives a micrometer "
        "stage on a microscope and the fine-focus knob on the instrument you use in biology.",
        "precautions": [
            "Use the ratchet only — never force the thimble after the studs touch the wire.",
            "Check the zero error at the start and again at the end of the experiment.",
            "Measure the wire at three places and in two perpendicular directions.",
            "Straighten the wire without stretching it before measuring.",
        ],
        "errors": [
            "Over-tightening flattens a soft wire and gives a reading that is too small.",
            "Backlash in the screw thread if the thimble is reversed before reading.",
            "Dust or grease on the studs adds an unknown thickness.",
        ],
        "exam": [
            "State the pitch and least count before any reading — examiners award those marks separately.",
            "Keep the same number of decimal places throughout: 0.01 mm precision means two decimals in mm.",
        ],
        "viva": [
            {"q": "Why is the least count of a screw gauge smaller than that of vernier callipers?",
             "a": "The screw converts a large rotation into a small translation, so a single circular division represents only 0.01 mm, whereas the vernier's finest step is 0.1 mm."},
            {"q": "What is backlash and how is it avoided?",
             "a": "Backlash is lost motion when the direction of turning is reversed, caused by slack between screw and nut. Always approach the final position by turning in the same direction."},
            {"q": "Why is the wire's volume, not just its diameter, sometimes required?",
             "a": "Density and resistivity both depend on cross-sectional area, so the volume or area calculated from the diameter is needed for those follow-up calculations."},
        ],
    },
    "phy-moments-ix": {
        "objectives": [
            "State and apply the principle of moments to a balanced metre rod.",
            "Locate an unknown centre of gravity by balancing.",
            "Distinguish between mass and weight when setting up the equation.",
        ],
        "theory": [
            "A rigid body stays in rotational equilibrium when the total clockwise moment about "
            "any point equals the total anticlockwise moment. A moment is force × perpendicular "
            "distance from the pivot, so a small weight far from the pivot can balance a large "
            "weight close to it — the principle behind a see-saw and a wheelbarrow.",
            "Balancing the rod on a wedge first locates its centre of gravity. Once that point is "
            "known, suspending a known weight on one side and sliding it until balance is "
            "restored lets you calculate either an unknown weight or an unknown distance. Taking "
            "moments about the pivot removes the reaction force from the equation entirely.",
        ],
        "formula": "clockwise moments = anticlockwise moments\n"
        "W₁d₁ = W₂d₂ (about the pivot)",
        "context": "Moment balance decides the position of a crane's counterweight, the design of "
        "a door handle (far from the hinge for leverage) and the stability of a loaded truck. "
        "Physiotherapists use the same reasoning when judging load on a joint.",
        "precautions": [
            "Balance the rod first and mark the centre of gravity; do not assume it is the midpoint.",
            "Measure every distance from the pivot, not from the end of the rod.",
            "Use the perpendicular distance; keep the rod horizontal.",
            "Add the weight of the rod itself if the pivot is not at its centre of gravity.",
        ],
        "errors": [
            "Reading distances along the rod instead of perpendicular to the force.",
            "Ignoring the mass of the rod when it is not balanced at its centre.",
            "Friction at the pivot producing a small extra moment.",
        ],
        "exam": [
            "Name the pivot explicitly and state that you take moments about it.",
            "Show weights in newtons; a mass in grams must be multiplied by g.",
        ],
        "viva": [
            {"q": "Why does taking moments about the pivot simplify the calculation?",
             "a": "The reaction at the pivot acts through the pivot, so its perpendicular distance is zero and its moment vanishes from the equation."},
            {"q": "What is the difference between centre of mass and centre of gravity?",
             "a": "Centre of mass is the mass-weighted average position; centre of gravity is where the total weight acts. In a uniform gravitational field they coincide."},
            {"q": "How would a non-horizontal rod change the calculation?",
             "a": "The perpendicular distance becomes d cos θ, where θ is the angle to the horizontal, so every moment is reduced by the same factor and the balance condition is unchanged."},
        ],
    },
    "phy-hooke-ix": {
        "objectives": [
            "Plot a load–extension graph and identify the elastic region.",
            "Determine the spring constant from the gradient.",
            "Explain the limit of proportionality and elastic limit.",
        ],
        "theory": [
            "For a spring loaded within its elastic limit, the extension is directly proportional "
            "to the applied force. The constant of proportionality is the spring constant k, "
            "measured in newtons per metre; a stiff spring has a large k and extends little.",
            "The graph of force against extension is a straight line through the origin whose "
            "gradient is k. Beyond the limit of proportionality the line curves, and beyond the "
            "elastic limit the spring does not return to its original length. The area under the "
            "straight portion equals the elastic potential energy stored, ½Fx.",
        ],
        "formula": "F = kx\n"
        "Eₚ = ½kx²",
        "context": "Suspension springs, atomic-force microscope cantilevers, bathroom scales and "
        "the shock absorbers of a motorcycle are all designed around this linear region. "
        "Engineers choose k so that the expected load produces a usable, measurable deflection.",
        "precautions": [
            "Read the pointer after the spring has come to rest; do not let it oscillate.",
            "Use the extension, not the total length, in the calculation.",
            "Do not exceed the elastic limit — check that the spring returns to its start length.",
            "Keep the load hanging vertically and free of the scale.",
        ],
        "errors": [
            "Using total length instead of extension, which gives a line that misses the origin.",
            "Exceeding the elastic limit so the graph curves at high loads.",
            "Zero error in the ruler or a pointer that is not at the same height as the scale.",
        ],
        "exam": [
            "Always draw the line of best fit through the origin for the linear region and use its gradient.",
            "State the unit of k as N m⁻¹, not N/m written ambiguously.",
        ],
        "viva": [
            {"q": "Why must the line pass through the origin?",
             "a": "With no load there is no extension, so the relationship is proportional rather than merely linear. A line that misses the origin indicates a zero error or the weight of the spring itself."},
            {"q": "What does the area under the graph represent?",
             "a": "The work done in stretching the spring, which is stored as elastic potential energy: area = ½ × force × extension."},
            {"q": "How would two springs in series behave compared with one?",
             "a": "They extend twice as much for the same load, so the effective spring constant is halved; in parallel the constants add."},
        ],
    },
    "phy-pendulum-x": {
        "objectives": [
            "Measure the period of a simple pendulum accurately by timing many oscillations.",
            "Show that T² is proportional to L and determine g from the gradient.",
            "Explain why the small-angle approximation matters.",
        ],
        "theory": [
            "For small swings the restoring force on a pendulum is proportional to displacement, "
            "so the motion is simple harmonic. The period depends only on the length and the "
            "local gravitational field — not on the mass of the bob — which is why a pendulum "
            "makes a serviceable clock.",
            "Squaring the period gives T² = (4π²/g)L, a straight line through the origin when T² "
            "is plotted against L. The gradient is 4π²/g, so g follows from the slope. Timing "
            "twenty oscillations and dividing reduces the reaction-time error by a factor of "
            "twenty, which is the single biggest improvement you can make to the experiment.",
        ],
        "formula": "T = 2π√(L/g)\n"
        "T² = (4π²/g)L  →  g = 4π² / gradient",
        "context": "Pendulum clocks kept time for three centuries, and the same relation is used "
        "today to measure g in geophysical surveys and to calibrate accelerometers. Grandfather "
        "clocks are adjusted by raising or lowering the bob, changing L by a fraction of a "
        "millimetre per day of drift.",
        "precautions": [
            "Keep the amplitude below about 10°, otherwise the period lengthens.",
            "Time 20 oscillations and divide, rather than timing one swing.",
            "Measure L to the centre of the bob, not to its top.",
            "Start timing at the centre of the swing where the bob moves fastest and is easiest to judge.",
        ],
        "errors": [
            "Reaction time at start and stop, largely removed by timing many oscillations.",
            "Measuring length to the top of the bob instead of its centre.",
            "Large amplitude, which makes the motion non-simple-harmonic.",
        ],
        "exam": [
            "Plot T² against L, not T against L — the straight line makes the gradient meaningful.",
            "Quote g to the precision your timing supports, usually two or three significant figures.",
        ],
        "viva": [
            {"q": "Why is the mass of the bob irrelevant?",
             "a": "The restoring force and the inertia both scale with mass, so mass cancels in the equation of motion; only length and g remain."},
            {"q": "What happens to the period if the pendulum is taken to the Moon?",
             "a": "g is about one-sixth as large, so T increases by a factor of √6 — roughly 2.45 times longer."},
            {"q": "Why does a large amplitude increase the measured period?",
             "a": "The small-angle approximation sin θ ≈ θ fails, the restoring force is no longer proportional to displacement and the motion is not perfectly simple harmonic."},
        ],
    },
    "phy-resonance-x": {
        "objectives": [
            "Find the first and second resonance positions in a closed tube.",
            "Calculate wavelength from the separation of successive resonances.",
            "Use the end correction to explain why the tube is effectively longer than measured.",
        ],
        "theory": [
            "A tube closed at one end supports a stationary wave with a node at the closed end and "
            "an antinode at the open end. The shortest resonating length is a quarter wavelength; "
            "the next is three quarters. The difference between successive resonance lengths is "
            "therefore exactly half a wavelength, independent of any end correction.",
            "Because the antinode forms slightly outside the open end, the physical tube is "
            "shorter than the acoustic length by an end correction e, roughly 0.6 times the "
            "tube radius. Using the difference of two resonance lengths cancels e, which is why "
            "the two-position method is more reliable than a single reading.",
        ],
        "formula": "λ = 2(L₂ − L₁)\n"
        "v = fλ\n"
        "L + e = (2n − 1)λ/4",
        "context": "The same physics tunes a flute, a clarinet and an organ pipe, and explains why "
        "a bottle hums at a particular pitch as you fill it. Ultrasound scanners and mufflers "
        "are designed by controlling where nodes and antinodes fall.",
        "precautions": [
            "Hold the tuning fork close to the tube mouth but do not touch the tube.",
            "Raise and lower the water level slowly; the resonance is sharp.",
            "Measure from the water surface to the top of the tube.",
            "Keep the fork vibrating at the same frequency throughout — do not strike it harder to 'hear better'.",
        ],
        "errors": [
            "Judging the loudest point by ear, which is subjective and broad.",
            "Ignoring the end correction when using a single resonance length.",
            "Temperature drift changing the speed of sound during the experiment.",
        ],
        "exam": [
            "State clearly that the difference between the two resonance lengths equals λ/2.",
            "Use v = fλ with f in hertz and λ in metres to get m s⁻¹.",
        ],
        "viva": [
            {"q": "Why must the tube be closed at one end?",
             "a": "A closed end forces a displacement node, which fixes the allowed wavelengths at odd multiples of a quarter wavelength and makes the resonance positions sharp and predictable."},
            {"q": "What is the end correction and why does it cancel?",
             "a": "It is the small extra acoustic length beyond the open end. It is the same for both resonance positions, so it disappears when you subtract them."},
            {"q": "How does the speed of sound change on a hot day?",
             "a": "v increases roughly as the square root of absolute temperature, so about 0.6 m s⁻¹ per degree Celsius near room temperature."},
        ],
    },
    "phy-ohm-x": {
        "objectives": [
            "Verify that current is proportional to potential difference for a metallic conductor.",
            "Determine resistance from the gradient of a V–I graph.",
            "Explain why the graph must pass through the origin.",
        ],
        "theory": [
            "Ohm's law states that for a conductor at constant temperature the current is directly "
            "proportional to the potential difference across it. The constant of proportionality "
            "is the resistance, R = V/I, measured in ohms.",
            "A graph of V against I is a straight line through the origin with gradient R. Any "
            "curvature signals a change in resistance — usually heating, which increases the "
            "resistance of a metal. Plotting V against I rather than I against V is a convention "
            "that makes the gradient the resistance directly.",
        ],
        "formula": "V = IR\n"
        "R = V/I = gradient of V–I graph",
        "context": "Every resistor, heater element and extension lead is rated with this "
        "relationship in mind. It also explains why long, thin wires overheat: resistance rises "
        "with length and falls with cross-sectional area.",
        "precautions": [
            "Keep the current small so the wire does not heat and change resistance.",
            "Check the ammeter is in series and the voltmeter in parallel.",
            "Switch off between readings to let the wire cool.",
            "Use the correct polarity and range before closing the circuit.",
        ],
        "errors": [
            "Heating of the wire, which makes the graph bend at higher currents.",
            "Meter zero errors or a voltmeter of low resistance drawing current.",
            "Loose connections adding an unknown contact resistance.",
        ],
        "exam": [
            "State the gradient's unit and identify it explicitly as the resistance.",
            "Mention constant temperature as the condition for Ohm's law to hold.",
        ],
        "viva": [
            {"q": "Does a filament lamp obey Ohm's law?",
             "a": "Not over a wide range. As the filament heats, its resistance rises, so the V–I graph curves and the lamp is described as non-ohmic."},
            {"q": "Why is the voltmeter connected in parallel?",
             "a": "It must measure the potential difference across the component, so it is connected across it; a voltmeter has very high resistance so it draws almost no current."},
            {"q": "What is the effect of connecting the ammeter in parallel by mistake?",
             "a": "Its low resistance short-circuits the supply, a very large current flows and the meter or fuse may be damaged."},
        ],
    },
    "phy-series-x": {
        "objectives": [
            "Measure the equivalent resistance of two resistors in series and in parallel.",
            "Show that series resistances add and parallel conductances add.",
            "Explain the effect of each arrangement on current and voltage.",
        ],
        "theory": [
            "In series, the same current passes through both resistors and the potential "
            "differences add, so the equivalent resistance is the sum. In parallel, the same "
            "potential difference appears across both and the currents add, so the equivalent "
            "resistance is smaller than either resistor.",
            "The parallel result follows from adding conductances: 1/R = 1/R₁ + 1/R₂. A useful "
            "check is that the parallel equivalent must always be less than the smallest branch "
            "resistance, while the series equivalent must always exceed the largest.",
        ],
        "formula": "series: R = R₁ + R₂\n"
        "parallel: 1/R = 1/R₁ + 1/R₂",
        "context": "House wiring is parallel so that each appliance receives the full mains "
        "voltage and can be switched independently. Series connection is used where a voltage "
        "must be shared — for example in a string of small lamps or a potential divider.",
        "precautions": [
            "Switch off the supply before changing the circuit.",
            "Measure each resistor separately first to predict the expected result.",
            "Tighten connections so contact resistance does not add to the measured value.",
            "Keep the current low to avoid heating.",
        ],
        "errors": [
            "Contact resistance at the crocodile clips, which matters most for small resistances.",
            "Meter loading, especially a voltmeter comparable in resistance to the components.",
            "Using resistor colour codes instead of measuring the actual values.",
        ],
        "exam": [
            "Always state the rule you are using before substituting numbers.",
            "Check the parallel answer is smaller than both resistors — a quick way to catch a reciprocal slip.",
        ],
        "viva": [
            {"q": "Why is the parallel resistance smaller than either resistor?",
             "a": "Each branch provides an additional path for charge, so the total current for a given voltage is larger, which by R = V/I means a smaller equivalent resistance."},
            {"q": "What happens to the total resistance if one branch of a parallel circuit is removed?",
             "a": "It increases, because there is one fewer path; the remaining branch alone carries all the current."},
            {"q": "Why are domestic appliances connected in parallel?",
             "a": "So each receives the full supply voltage, can be switched independently, and a failure in one does not break the circuit for the others."},
        ],
    },
    "phy-spherometer-xi": {
        "objectives": [
            "Measure the sagitta of a spherical surface with a spherometer.",
            "Calculate the radius of curvature from the sagitta and the leg separation.",
            "Explain why a spherometer is used instead of a ruler for curved surfaces.",
        ],
        "theory": [
            "A spherometer rests on three legs that define a plane and a central screw that "
            "measures how far the surface rises or falls relative to that plane. The vertical "
            "distance from the plane of the legs to the surface is the sagitta h.",
            "For a spherical surface of radius R whose legs sit on a circle of radius a, geometry "
            "gives R = a²/(2h) + h/2. Because h is small compared with a, the second term is "
            "usually negligible, but keeping it makes the result exact for strongly curved "
            "surfaces.",
        ],
        "formula": "R = a²/(2h) + h/2\n"
        "a = mean distance between the legs ÷ √3",
        "context": "Opticians measure the curvature of spectacle lenses this way, and the same "
        "geometry is used to check the radius of a concave mirror before it is silvered. In "
        "industry, a spherometer-style probe checks the curvature of camera lenses and telescope "
        "mirrors.",
        "precautions": [
            "Press the legs gently onto the surface — do not let them slide.",
            "Measure the leg separation with vernier callipers, not a ruler.",
            "Take several readings at different positions to average out surface irregularities.",
            "Record the zero reading on a flat glass plate first.",
        ],
        "errors": [
            "The legs not sitting symmetrically on the curved surface.",
            "Sagitta measured at a point that is not the centre of curvature.",
            "Backlash in the screw if the direction of rotation is reversed.",
        ],
        "exam": [
            "Show the substitution for a explicitly: the three legs form an equilateral triangle.",
            "Quote R in the same unit as a and h, usually centimetres or millimetres.",
        ],
        "viva": [
            {"q": "Why are three legs used rather than four?",
             "a": "Three points always define a plane unambiguously; four points may rock if the surface is not perfectly flat, making the reference plane unreliable."},
            {"q": "What does a large sagitta tell you about the surface?",
             "a": "A larger h for the same leg separation means a more strongly curved surface and therefore a smaller radius of curvature."},
            {"q": "Why is the h/2 term often dropped?",
             "a": "For typical lenses h is a fraction of a millimetre while a is tens of millimetres, so h/2 is negligible compared with a²/2h — but it should still be mentioned."},
        ],
    },
    "phy-specific-heat-xi": {
        "objectives": [
            "Apply the method of mixtures to find a specific heat capacity.",
            "Account for heat lost to the calorimeter and surroundings.",
            "Explain why the measured value is usually lower than the accepted one.",
        ],
        "theory": [
            "When a hot solid is dropped into cooler water inside a calorimeter, heat leaves the "
            "solid until everything reaches a common temperature. If no heat escaped, the heat "
            "lost by the solid would equal the heat gained by the water and calorimeter.",
            "The calculation uses Q = mcΔθ and must include the water equivalent of the "
            "calorimeter, because the metal vessel also warms up. In practice some heat is lost "
            "to the air, so the measured specific heat capacity comes out slightly low; "
            "insulating the calorimeter and working quickly both reduce the discrepancy.",
        ],
        "formula": "m_s c_s (θ_hot − θ_mix) = (m_w c_w + W)(θ_mix − θ_cold)",
        "context": "Specific heat capacity decides why coastal cities have milder winters than "
        "inland deserts, why car radiators use water rather than oil, and how much energy a "
        "storage heater can hold overnight.",
        "precautions": [
            "Transfer the hot solid quickly to avoid cooling on the way.",
            "Stir gently and continuously so the final temperature is uniform.",
            "Record the maximum temperature reached, since the mixture starts cooling immediately.",
            "Include the calorimeter's water equivalent in the heat gained.",
        ],
        "errors": [
            "Heat lost to the surroundings during transfer and stirring.",
            "Water splashing out when the solid is dropped in.",
            "Thermometer lag, so the true maximum temperature is missed.",
        ],
        "exam": [
            "Write the heat-balance equation in symbols before substituting values.",
            "State one reason the answer differs from the accepted value; this is usually worth a mark.",
        ],
        "viva": [
            {"q": "Why is water a good coolant?",
             "a": "It has a high specific heat capacity, so it absorbs a large amount of energy for a modest temperature rise."},
            {"q": "What is the water equivalent of a calorimeter?",
             "a": "The mass of water that would absorb the same heat as the calorimeter for the same temperature rise, allowing the vessel to be treated as extra water in the equation."},
            {"q": "How would a lower room temperature affect the result?",
             "a": "Heat loss from the calorimeter would be greater, so the measured specific heat capacity would be lower than the true value."},
        ],
    },
    "phy-filament-xii": {
        "objectives": [
            "Plot the V–I characteristic of a tungsten filament lamp.",
            "Explain why the lamp is non-ohmic.",
            "Relate the changing gradient to the temperature coefficient of resistance.",
        ],
        "theory": [
            "A tungsten filament does not behave like a fixed resistor. As the current rises, the "
            "filament heats to around 2500 K, and the resistance of tungsten increases several "
            "times over its room-temperature value. The V–I graph therefore curves: each extra "
            "volt produces proportionally less extra current.",
            "The resistance at any point is still V/I, but the gradient of the V–I line is not "
            "constant. Only at very small currents, where the filament is still cool, does the "
            "characteristic approach a straight line through the origin.",
        ],
        "formula": "R = V/I (at each point)\n"
        "R = R₀[1 + α(θ − θ₀)]",
        "context": "Incandescent bulbs are a classic example of a self-heating resistor, and the "
        "same effect appears in fuses, which rely on the wire melting, and in the inrush current "
        "that makes a cold bulb draw a surge when first switched on.",
        "precautions": [
            "Increase the voltage in small steps and wait for the filament to stabilise.",
            "Do not exceed the rated voltage of the lamp.",
            "Switch off between readings to limit filament ageing.",
            "Use a power supply with current limiting rather than a bare battery.",
        ],
        "errors": [
            "Readings taken before the filament reaches thermal equilibrium.",
            "The lamp cooling between readings, giving inconsistent points.",
            "Meter loading at high current, which depresses the measured voltage.",
        ],
        "exam": [
            "Say explicitly that the gradient is not constant and therefore R is not constant.",
            "Quote the temperature coefficient of resistance as the physical reason.",
        ],
        "viva": [
            {"q": "Why does the resistance of the filament increase with current?",
             "a": "The current heats the tungsten, increasing lattice vibrations, which scatter conduction electrons more strongly and raise resistivity."},
            {"q": "Why does a bulb often fail at the moment it is switched on?",
             "a": "The cold filament has a much lower resistance, so the initial current is high and the thermal and mechanical stress is greatest at switch-on."},
            {"q": "Sketch the I–V graph for a filament lamp.",
             "a": "Current rises steeply at first, then flattens as the resistance grows, producing a curve that bends towards the voltage axis."},
        ],
    },
    "phy-rc-xii": {
        "objectives": [
            "Measure the time constant of an RC circuit from a discharge curve.",
            "Show that the time constant equals RC.",
            "Explain the meaning of one time constant in terms of charge remaining.",
        ],
        "theory": [
            "When a capacitor discharges through a resistor, the current and the potential "
            "difference fall exponentially. The rate of decay is set by the product RC, called "
            "the time constant: after one time constant the voltage has fallen to about 37 per "
            "cent of its initial value.",
            "Plotting the logarithm of voltage against time turns the exponential into a straight "
            "line whose gradient is −1/RC. This is more reliable than reading a single point off "
            "a curve, because it uses every measurement and makes departures from exponential "
            "behaviour obvious.",
        ],
        "formula": "V = V₀e^(−t/RC)\n"
        "ln V = ln V₀ − t/(RC)\n"
        "τ = RC",
        "context": "RC time constants set the flash rate of a camera, the sweep of windscreen "
        "wipers, the debounce delay in a keyboard and the timing of a 555 timer. Audio filters "
        "choose R and C so that the cut-off frequency, 1/(2πRC), falls where the designer wants it.",
        "precautions": [
            "Discharge the capacitor fully before each run.",
            "Start timing at the instant the circuit is broken, not when you look at the meter.",
            "Use a resistor large enough that the decay is slow compared with your reaction time.",
            "Check the capacitor's polarity if it is electrolytic.",
        ],
        "errors": [
            "Reaction-time delay at the start of timing.",
            "Voltmeter resistance discharging the capacitor in parallel with R.",
            "Leakage in the capacitor, which makes the decay non-exponential at long times.",
        ],
        "exam": [
            "Show that the gradient of ln V against t is −1/RC and rearrange for C or R.",
            "State that one time constant leaves about 37% of the initial voltage.",
        ],
        "viva": [
            {"q": "What is the significance of the time constant?",
             "a": "It is the time for the voltage to fall to 1/e of its initial value, about 37%, and it characterises how quickly the circuit responds."},
            {"q": "Why is ln V plotted rather than V?",
             "a": "The exponential becomes linear, so a straight line of gradient −1/RC can be fitted over the whole data set and checked for consistency."},
            {"q": "How would doubling R change the discharge?",
             "a": "The time constant doubles, so the capacitor takes twice as long to reach the same fraction of its initial voltage."},
        ],
    },
}

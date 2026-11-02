"""Extended theory, context and viva material for the Biology practicals."""

BIOLOGY_DEPTH = {
    "bio-sav-ix": {
        "objectives": [
            "Measure the surface area and volume of potato cubes of different sizes.",
            "Calculate the surface area to volume ratio for each cube.",
            "Relate the ratio to the efficiency of diffusion into a cell.",
        ],
        "theory": [
            "Every exchange of materials between a cell and its surroundings happens across the "
            "cell surface. The supply of oxygen and the removal of waste therefore depend on the "
            "area available, while the demand depends on the volume of living cytoplasm. As a cube "
            "grows, its surface area rises with the square of its side while its volume rises with "
            "the cube, so the ratio of surface area to volume falls steeply.",
            "This is why diffusion is fast enough in a bacterium but not in an elephant: a large "
            "organism cannot rely on its outer surface alone, so it needs lungs, gills, a gut and a "
            "circulatory system to create a large exchange area packed into a small volume. The "
            "potato cube is a simple physical model of that geometric constraint.",
        ],
        "formula": "surface area of a cube = 6s²\n"
        "volume of a cube = s³\n"
        "surface area : volume = 6s² / s³ = 6 / s",
        "context": "The same reasoning explains why cells divide rather than grow indefinitely, why "
        "leaves are thin and flat, why villi and alveoli are folded, and why a baked potato cooks "
        "faster when cut small. It also sets the limit on the size of a single-celled organism.",
        "precautions": [
            "Cut the cubes accurately with a sharp knife and measure each side with a ruler.",
            "Use the same potato and blot each cube dry so the masses are comparable.",
            "Keep the cubes in the dye or hydrogen peroxide for the same time.",
            "Handle the cubes with forceps to avoid squeezing water out of the tissue.",
        ],
        "errors": [
            "Cubes not truly cubical, so the measured side does not represent the whole block.",
            "Different immersion times, which changes how far the colour penetrates.",
            "Water on the surface adding mass that is not part of the tissue.",
        ],
        "exam": [
            "Show the calculation for one cube fully, then tabulate the rest.",
            "State the conclusion in terms of diffusion distance: the smaller cube has a larger "
            "ratio and its centre is reached sooner.",
        ],
        "viva": [
            {"q": "Why does the surface area to volume ratio fall as a cube grows?",
             "a": "Area scales as s² and volume as s³, so doubling the side multiplies the area by four "
                  "but the volume by eight; the ratio therefore halves."},
            {"q": "Why must cells remain small?",
             "a": "Diffusion alone must supply the whole cytoplasm. If the cell were too large the "
                  "centre would run short of oxygen and accumulate waste faster than diffusion could "
                  "replace or remove it."},
            {"q": "How do large organisms solve the same problem?",
             "a": "They evolve exchange surfaces with a large area folded into a small volume — "
                  "alveoli, villi, gill filaments — and a transport system to carry materials between "
                  "those surfaces and the body's cells."},
        ],
    },
    "bio-osmosis-ix": {
        "objectives": [
            "Measure the change in mass of potato tissue in solutions of different concentration.",
            "Plot percentage change in mass against concentration and find the isotonic point.",
            "Explain water movement in terms of water potential.",
        ],
        "theory": [
            "Osmosis is the net movement of water across a partially permeable membrane from a "
            "region of higher water potential to one of lower water potential. The potato cells "
            "contain vacuolar sap with dissolved sugars and salts, so the tissue has its own water "
            "potential. In pure water the outside has the higher water potential, water enters the "
            "cells, the vacuoles swell and the mass rises.",
            "In a concentrated sugar solution the outside has the lower water potential, water "
            "leaves the cells and the tissue loses mass and becomes floppy. At the isotonic point "
            "the two water potentials are equal, there is no net movement, and the mass does not "
            "change. Plotting percentage change in mass against concentration gives a line that "
            "crosses zero at that concentration.",
        ],
        "formula": "percentage change in mass = (final mass − initial mass) / initial mass × 100\n"
        "isotonic point = concentration where percentage change = 0",
        "context": "Osmosis governs water uptake by plant roots, the crispness of vegetables, the "
        "action of intravenous drips and the preservation of food in brine or syrup. It also "
        "explains why a slug shrivels in salt and why red blood cells burst in pure water.",
        "precautions": [
            "Use the same size and shape of potato tissue for every concentration.",
            "Blot the tissue gently before each weighing to remove surface solution.",
            "Leave each sample in its solution for the same length of time.",
            "Weigh on a balance reading to at least 0.01 g and record the initial mass before soaking.",
        ],
        "errors": [
            "Surface water left on the tissue, which inflates the final mass.",
            "Different soaking times, so the extent of osmosis is not comparable.",
            "Potato samples from different parts of the tuber with different sap concentrations.",
        ],
        "exam": [
            "Plot percentage change in mass, not the raw mass, so samples of different starting "
            "mass can be compared.",
            "Read the isotonic concentration from where the line crosses the axis and give it the "
            "unit of the independent variable.",
        ],
        "viva": [
            {"q": "Why does the potato gain mass in distilled water?",
             "a": "The water potential outside is higher than inside the cells, so water enters by "
                  "osmosis and the vacuoles swell."},
            {"q": "Why does the line not necessarily pass through the origin?",
             "a": "It does pass through zero percentage change at the isotonic concentration, but "
                  "that concentration is not zero — the potato sap already contains solutes."},
            {"q": "What would happen if the potato were boiled first?",
             "a": "Boiling disrupts the cell membranes, so they are no longer partially permeable and "
                  "osmosis cannot occur; the tissue would simply become waterlogged."},
        ],
    },
    "bio-amylase-temp-ix": {
        "objectives": [
            "Investigate the effect of temperature on the rate of starch digestion by amylase.",
            "Use iodine to detect the end point of the reaction.",
            "Explain the shape of the rate–temperature curve in terms of molecular motion and "
            "denaturation.",
        ],
        "theory": [
            "Amylase hydrolyses starch to maltose. The reaction happens when substrate molecules "
            "collide with the active site, so raising the temperature increases the kinetic energy "
            "of the molecules and the rate rises. At the optimum temperature the rate is highest.",
            "Above the optimum, the hydrogen bonds and ionic interactions holding the enzyme's "
            "tertiary structure begin to break. The active site loses its specific shape, the "
            "substrate no longer fits, and the enzyme is denatured. Denaturation is irreversible, "
            "which is why the rate falls sharply rather than levelling off.",
        ],
        "formula": "rate ∝ 1 / time to digest the starch\n"
        "optimum temperature = temperature of shortest digestion time",
        "context": "Industrial washing powders use amylase to remove starch stains at 30–40 °C, and "
        "the same enzyme begins digestion in the mouth. Fever above about 40 °C becomes dangerous "
        "precisely because human enzymes are being pushed past their optimum.",
        "precautions": [
            "Let the amylase and starch solutions reach the water-bath temperature before mixing.",
            "Use a fresh pipette for each sample to avoid carry-over of enzyme.",
            "Keep the iodine test volume and timing the same for every reading.",
            "Do not let the thermometer touch the bottom of the tube, where the glass is hotter.",
        ],
        "errors": [
            "Solutions not equilibrated, so the reaction does not run at the stated temperature.",
            "Judging the end point inconsistently; the blue-black colour fades gradually.",
            "Enzyme concentration changing between runs because of pipetting error.",
        ],
        "exam": [
            "Describe the curve in words: rises to an optimum, then falls sharply.",
            "Use the terms 'kinetic energy', 'collisions' and 'denaturation' — examiners look for all "
            "three.",
        ],
        "viva": [
            {"q": "Why does the rate increase before the optimum?",
             "a": "Higher temperature gives molecules more kinetic energy, so substrate and enzyme "
                  "collide more frequently and with more energy, producing more successful reactions "
                  "per second."},
            {"q": "Why is denaturation irreversible?",
             "a": "The bonds that maintain the tertiary structure are broken, and the polypeptide "
                  "cannot refold spontaneously into the precise active-site shape once that "
                  "organisation is lost."},
            {"q": "How would you find the optimum temperature more precisely?",
             "a": "Use narrower temperature intervals around the apparent optimum, repeat each "
                  "temperature, and plot rate against temperature to find the peak."},
        ],
    },
    "bio-amylase-ph-ix": {
        "objectives": [
            "Compare the activity of amylase and pepsin over a range of pH values.",
            "Explain the effect of pH on the charge and shape of the active site.",
            "Relate each enzyme's optimum to the environment in which it works.",
        ],
        "theory": [
            "Enzyme activity depends on the ionisation of the amino acids in and around the active "
            "site. Changing the pH changes which groups are protonated, altering the charge "
            "distribution and the hydrogen bonding that holds the tertiary structure. At the "
            "optimum pH the active site has exactly the right shape and charge to bind the "
            "substrate.",
            "Amylase works in the mouth and small intestine, near pH 7, so its optimum is close to "
            "neutral. Pepsin is secreted into the stomach, where hydrochloric acid keeps the pH "
            "near 2, and its optimum is strongly acidic. Away from the optimum the enzyme is "
            "progressively denatured, and the rate falls.",
        ],
        "formula": "rate ∝ 1 / time for the substrate to be digested\n"
        "optimum pH = pH giving the shortest digestion time",
        "context": "pH optima explain why antacid tablets affect digestion, why the small intestine "
        "neutralises stomach acid before pancreatic enzymes arrive, and why food-processing "
        "enzymes must be matched to the pH of the product.",
        "precautions": [
            "Use buffer solutions to hold the pH steady; without a buffer the reaction itself can "
            "shift the pH.",
            "Equilibrate enzyme and substrate at the required pH before mixing.",
            "Keep temperature constant, since it also affects rate.",
            "Rinse the pH electrode between samples and calibrate it first.",
        ],
        "errors": [
            "No buffer, so the nominal pH is not the pH during the reaction.",
            "Temperature varying between runs and confounding the pH effect.",
            "Enzyme denaturing during storage before the experiment begins.",
        ],
        "exam": [
            "Name the enzyme and its optimum pH together, with the location where it works.",
            "Explain the fall on either side in terms of active-site shape and denaturation.",
        ],
        "viva": [
            {"q": "Why does pepsin have a low optimum pH?",
             "a": "It evolved to work in the stomach, where parietal cells secrete hydrochloric acid; "
                  "its active site is stable and correctly charged only in that acidic environment."},
            {"q": "What happens to an enzyme far from its optimum pH?",
             "a": "Ionic bonds and hydrogen bonds holding the tertiary structure break, the active "
                  "site changes shape and the enzyme is denatured, so the rate falls."},
            {"q": "Why is a buffer necessary in this experiment?",
             "a": "It resists pH change during the reaction, so the independent variable stays at the "
                  "value you intend to test."},
        ],
    },
    "bio-photosynthesis-ix": {
        "objectives": [
            "Measure the rate of oxygen release from pondweed as light intensity changes.",
            "Explain the effect of light intensity, carbon dioxide and temperature on the rate.",
            "Identify the limiting factor from the shape of the graph.",
        ],
        "theory": [
            "Photosynthesis uses light energy to split water and reduce carbon dioxide to glucose, "
            "releasing oxygen as a by-product. The rate can be followed by counting the oxygen "
            "bubbles leaving a cut stem of pondweed, or by collecting the gas in a capillary tube.",
            "As light intensity rises the rate rises, because more light energy reaches the "
            "chloroplasts. At higher intensities another factor — usually carbon dioxide "
            "concentration or temperature — becomes limiting and the curve plateaus. Adding more "
            "light then has no effect until the limiting factor is relieved.",
        ],
        "formula": "rate = number of bubbles ÷ time (bubbles per minute)\n"
        "rate ∝ light intensity (at low intensity)",
        "context": "The same measurements underpin commercial glasshouse management, where growers "
        "supplement carbon dioxide and light to raise yield, and the study of ocean "
        "phytoplankton, which produces a large share of atmospheric oxygen.",
        "precautions": [
            "Use the same piece of pondweed and let it settle after each change.",
            "Keep the sodium hydrogencarbonate concentration constant while testing light intensity.",
            "Count bubbles over a full minute and repeat, because the stream is irregular.",
            "Keep the lamp at measured distances and shield the bench from other light sources.",
        ],
        "errors": [
            "Bubble size varying, so counting bubbles is only an approximate measure of gas volume.",
            "Heat from the lamp raising the temperature as well as the light intensity.",
            "Pondweed becoming exhausted or damaged during a long run.",
        ],
        "exam": [
            "State clearly which variable is being changed and which are controlled.",
            "Use the term 'limiting factor' when explaining the plateau.",
        ],
        "viva": [
            {"q": "Why does the rate stop increasing at high light intensity?",
             "a": "Light is no longer the limiting factor; carbon dioxide concentration or temperature "
                  "now limits the rate, so extra light cannot increase it."},
            {"q": "Why is sodium hydrogencarbonate added?",
             "a": "It supplies dissolved carbon dioxide so that carbon availability does not limit the "
                  "rate at low light intensities."},
            {"q": "Why is counting bubbles only an estimate?",
             "a": "Bubbles vary in size and some gas dissolves in the water, so the count does not "
                  "measure the true volume of oxygen released."},
        ],
    },
    "bio-transpiration-ix": {
        "objectives": [
            "Compare water loss from the upper and lower surfaces of a leaf.",
            "Relate the difference to stomatal distribution.",
            "Explain how temperature, humidity, light and wind affect transpiration.",
        ],
        "theory": [
            "Transpiration is the evaporation of water from the moist surfaces of mesophyll cells "
            "into the air spaces, followed by diffusion out through the stomata. Water lost this "
            "way is replaced by the transpiration stream moving up the xylem, driven by tension "
            "from the leaves.",
            "Most stomata are on the lower epidermis, which is shaded and cooler, so water loss is "
            "usually greater from the lower surface. Cobalt chloride paper is blue when dry and "
            "turns pink as it absorbs water, so the time taken for the colour change is a simple "
            "comparative measure of the rate of water loss.",
        ],
        "formula": "rate of water loss ∝ 1 / time for the paper to turn pink\n"
        "water loss ∝ stomatal density × water potential gradient",
        "context": "Transpiration pulls water and dissolved minerals from roots to leaves, cools "
        "the leaf, and drives the water cycle. Farmers manage irrigation and glasshouse humidity "
        "around it, and cut flowers last longer when humidity is high and the air is still.",
        "precautions": [
            "Handle the cobalt chloride paper with forceps; fingers carry moisture.",
            "Attach the paper to the leaf surface quickly and seal the edges.",
            "Compare leaves of the same species, age and size.",
            "Keep the leaf in the same light and temperature for each test.",
        ],
        "errors": [
            "Moisture from fingers or the air reaching the paper.",
            "Papers not in equally close contact with the leaf surface.",
            "Using different leaves or different times of day, so the comparison is unfair.",
        ],
        "exam": [
            "State that the lower surface loses water faster and link it to a higher stomatal "
            "density there.",
            "Name the environmental factors and explain each in terms of the water potential "
            "gradient.",
        ],
        "viva": [
            {"q": "Why are most stomata on the lower leaf surface?",
             "a": "That surface is shaded and cooler, so less water is lost, while the upper surface "
                  "can still capture light for photosynthesis."},
            {"q": "How does wind increase transpiration?",
             "a": "It removes the layer of humid air next to the leaf, maintaining a steep water "
                  "vapour gradient and so a faster rate of diffusion."},
            {"q": "Why is transpiration described as a necessary evil?",
             "a": "It is unavoidable while stomata are open for carbon dioxide uptake, and it risks "
                  "dehydration, but it also drives the transport of water and minerals and cools the "
                  "leaf."},
        ],
    },
    "bio-respiration-heat-ix": {
        "objectives": [
            "Measure the temperature rise produced by germinating seeds.",
            "Use boiled seeds as a control to show that the heat comes from living tissue.",
            "Explain why respiration releases heat.",
        ],
        "theory": [
            "Aerobic respiration oxidises glucose to carbon dioxide and water, releasing energy. "
            "Some of that energy is captured in ATP, but a substantial fraction appears as heat, "
            "because the reactions are not perfectly efficient. In a well-insulated flask the heat "
            "cannot escape quickly and the temperature rises.",
            "Germinating seeds respire rapidly because growth demands ATP, so they warm their "
            "surroundings — a fact gardeners use when germinating seeds in a cold frame. Boiled "
            "seeds have no living cells and no enzyme activity, so any temperature change they "
            "show reflects the surroundings rather than respiration. That comparison is what makes "
            "the experiment valid.",
        ],
        "formula": "heat released q = mcΔT\n"
        "rate of respiration ∝ temperature rise per unit time",
        "context": "The heat of respiration warms compost heaps, grain stores and damp hay, where it "
        "can become a fire risk. Warm-blooded animals rely on the same heat to maintain body "
        "temperature, and it explains why a thermos of germinating seeds feels warm.",
        "precautions": [
            "Use equal masses of seeds in identical, insulated flasks.",
            "Sterilise the seeds' surface to prevent microbial respiration confusing the result.",
            "Record the starting temperature after the apparatus has equilibrated.",
            "Keep both flasks in the same place so they experience the same room temperature.",
        ],
        "errors": [
            "Microbial growth on the seeds releasing additional heat.",
            "Flasks not insulated, so heat is lost as fast as it is produced.",
            "Unequal seed masses or different starting temperatures.",
        ],
        "exam": [
            "Identify the independent, dependent and control variables explicitly.",
            "Explain the role of the boiled seeds — they control for non-biological temperature "
            "change.",
        ],
        "viva": [
            {"q": "Why do germinating seeds release heat?",
             "a": "Respiration is exothermic; the energy released from glucose is partly transferred "
                  "to ATP and partly lost as heat to the surroundings."},
            {"q": "Why are boiled seeds included?",
             "a": "They are a control: they have no living cells, so any temperature change they show "
                  "is due to the environment, not respiration."},
            {"q": "How could you improve the reliability of the result?",
             "a": "Repeat with several batches, insulate the flasks better, and use a data logger to "
                  "record temperature continuously rather than reading a thermometer by eye."},
        ],
    },
    "bio-food-tests-xi": {
        "objectives": [
            "Carry out Benedict's, iodine, biuret and emulsion tests on food samples.",
            "Record the observation and the inference for each test separately.",
            "Explain why each reagent gives a characteristic colour change.",
        ],
        "theory": [
            "Food tests rely on specific chemical reactions. Benedict's solution contains copper(II) "
            "ions, which are reduced to copper(I) oxide by a reducing sugar on heating, giving a "
            "brick-red precipitate. Iodine molecules slot into the coiled amylose helix, producing "
            "an intense blue-black complex. Biuret reagent reacts with peptide bonds, forming a "
            "violet copper complex. The emulsion test dissolves lipid in ethanol and then pours it "
            "into water, where the lipid comes out of solution as a cloudy white emulsion.",
            "Each test answers a yes/no question about a particular class of molecule, and the "
            "strength of the colour gives a rough indication of quantity. A negative result is as "
            "informative as a positive one, provided the test has been carried out correctly and "
            "a known positive control has confirmed the reagent is working.",
        ],
        "formula": "reducing sugar + Cu²⁺ → Cu₂O (brick-red) on heating\n"
        "starch + I₂ → blue-black complex\n"
        "protein + Cu²⁺ in alkali → violet complex",
        "context": "These tests are used in food labelling, in testing for adulteration of honey or "
            "milk, and in clinical analysis of urine for glucose. Modern laboratories use "
            "spectrophotometers, but the underlying chemistry is the same.",
        "precautions": [
            "Heat Benedict's solution in a water bath, not directly over a flame.",
            "Add biuret reagent carefully; it is strongly alkaline and corrosive.",
            "Use a clean test tube for each sample to avoid contamination.",
            "Shake the emulsion test tube gently but thoroughly and let it stand.",
        ],
        "errors": [
            "Reusing tubes so a positive result carries over to the next sample.",
            "Overheating Benedict's test, which can give a misleading colour.",
            "Judging a weak colour change under poor lighting.",
        ],
        "exam": [
            "Present results as a table with sample, test, observation and inference columns.",
            "State the colour change, not just 'positive' or 'negative'.",
        ],
        "viva": [
            {"q": "Why is the biuret test carried out in alkaline conditions?",
             "a": "The violet copper–peptide complex forms only when the solution is alkaline, so "
                  "sodium hydroxide is added before or with the copper(II) sulfate."},
            {"q": "Why does iodine give a blue-black colour with starch?",
             "a": "Iodine molecules become trapped inside the coiled helix of amylose, and the "
                  "resulting charge-transfer complex absorbs light strongly, appearing blue-black."},
            {"q": "How would you test for a non-reducing sugar such as sucrose?",
             "a": "Boil with dilute hydrochloric acid to hydrolyse it to glucose and fructose, "
                  "neutralise with sodium hydrogencarbonate, then carry out Benedict's test."},
        ],
    },
    "bio-microscope-xi": {
        "objectives": [
            "Calculate the total magnification of a compound microscope.",
            "Measure the field of view and relate it to magnification.",
            "Prepare and focus a temporary mount using the correct sequence of objective lenses.",
        ],
        "theory": [
            "A compound microscope uses two lens systems. The objective forms a magnified real image "
            "inside the tube, and the eyepiece magnifies that image again. The total magnification "
            "is therefore the product of the two magnifications, not their sum: a 10× eyepiece with "
            "a 40× objective gives 400×.",
            "The field of view is the circular area visible through the eyepiece. It shrinks in "
            "proportion to the magnification, so an object that fills the field at 40× occupies only "
            "a quarter of the width at 100×. Knowing the field diameter lets you estimate the size "
            "of a specimen by judging what fraction of the field it spans.",
        ],
        "formula": "total magnification = eyepiece magnification × objective magnification\n"
        "field diameter at higher power = field diameter at lower power × "
        "(lower magnification ÷ higher magnification)",
        "context": "The same optics govern binoculars, cameras and telescopes. Microscopy is the "
            "foundation of cell biology, haematology and pathology, and the field-of-view "
            "calculation is used whenever a specimen is measured without a graticule.",
        "precautions": [
            "Start with the lowest-power objective and focus upwards, never downwards.",
            "Use the coarse focus only with the low-power objective.",
            "Keep both eyes open when viewing to reduce eye strain.",
            "Clean lenses with lens tissue, not a handkerchief.",
        ],
        "errors": [
            "Adding instead of multiplying the magnifications.",
            "Using the coarse focus with a high-power objective and cracking the slide.",
            "Measuring the field of view with a ruler held at the wrong distance.",
        ],
        "exam": [
            "Show the multiplication explicitly and give the answer with the × symbol.",
            "State that the field of view decreases as magnification increases.",
        ],
        "viva": [
            {"q": "Why is total magnification a product rather than a sum?",
             "a": "Each lens magnifies the image produced by the previous one, so the magnifications "
                  "multiply: the second lens enlarges an already enlarged image."},
            {"q": "Why must you start with the low-power objective?",
             "a": "It has a long working distance and a wide field, making it easy to find the "
                  "specimen; starting high-power risks driving the objective into the slide."},
            {"q": "How can you estimate the size of a cell without a graticule?",
             "a": "Measure the field diameter, estimate what fraction of the field the cell spans and "
                  "multiply the two."},
        ],
    },
    "bio-biostatistics-x": {
        "objectives": [
            "Calculate the mean, median and mode of a biological data set.",
            "Choose an appropriate measure of central tendency for the data.",
            "Plot a histogram and describe the shape of the distribution.",
        ],
        "theory": [
            "Biological measurements always vary, so a single value cannot describe a population. "
            "The mean uses every value and is the best estimate of the true value when the data "
            "are roughly symmetrical, but it is pulled by outliers. The median is the middle value "
            "and is more robust to skew, while the mode is the most frequent value and is the only "
            "measure that makes sense for categorical data.",
            "The spread matters as much as the centre. The range is simple but sensitive to extreme "
            "values; the standard deviation uses every point and describes how tightly the values "
            "cluster around the mean. A histogram shows the distribution, and its shape — "
            "symmetrical, skewed or bimodal — tells you which summary statistic is appropriate.",
        ],
        "formula": "mean x̄ = Σx / n\n"
        "median = middle value of the ordered data\n"
        "standard deviation s = √(Σ(x − x̄)² / (n − 1))",
        "context": "Biostatistics underpins clinical trials, public-health screening, ecological "
            "surveys and the interpretation of any biological measurement. The choice between mean "
            "and median determines how a drug's benefit or a population's income is reported.",
        "precautions": [
            "Order the data carefully before finding the median.",
            "Keep the same number of decimal places as the original measurements.",
            "Use class intervals of equal width for a histogram.",
            "Check for outliers and decide, with a reason, whether to include them.",
        ],
        "errors": [
            "Using the mean for strongly skewed data, which misrepresents the typical value.",
            "Forgetting to divide by n − 1 for a sample standard deviation.",
            "Drawing a bar chart when a histogram is required: histograms have continuous, "
            "touching bars.",
        ],
        "exam": [
            "State which average you chose and why, particularly for skewed data.",
            "Label both axes of the histogram, including units, and use equal class widths.",
        ],
        "viva": [
            {"q": "When is the median more useful than the mean?",
             "a": "When the data are skewed or contain outliers, because the median is not pulled "
                  "away from the centre by extreme values."},
            {"q": "What does the standard deviation tell you?",
             "a": "It measures the spread of the values around the mean; a small standard deviation "
                  "means the measurements are tightly clustered and the mean is more reliable."},
            {"q": "Why must histogram bars touch?",
             "a": "The variable is continuous, so the bars represent class intervals that run into "
                  "one another rather than separate categories."},
        ],
    },
    "bio-blood-pressure-xi": {
        "objectives": [
            "Measure systolic and diastolic blood pressure with a sphygmomanometer.",
            "Identify the Korotkoff sounds and explain what each marks.",
            "Interpret the reading against normal and elevated ranges.",
        ],
        "theory": [
            "The cuff is inflated above systolic pressure, compressing the brachial artery so that "
            "no blood flows and no sound is heard. As the pressure is released, the artery opens "
            "briefly at the peak of each heartbeat, producing the first Korotkoff sound; the "
            "pressure at that moment is the systolic pressure. As the cuff pressure falls further, "
            "the artery stays open throughout the cycle and the sound disappears; that pressure is "
            "the diastolic pressure.",
            "The reading is written as systolic over diastolic in millimetres of mercury. Systolic "
            "pressure reflects the force of ventricular contraction, while diastolic pressure "
            "reflects the resistance of the peripheral circulation. Both are influenced by "
            "cardiac output, blood volume, vessel elasticity and posture.",
        ],
        "formula": "blood pressure is written as systolic / diastolic (mmHg)\n"
        "pulse pressure = systolic − diastolic\n"
        "mean arterial pressure ≈ diastolic + (pulse pressure ÷ 3)",
        "context": "Blood pressure is one of the most useful vital signs: it screens for "
            "hypertension, guides emergency treatment and monitors the effect of drugs. The same "
            "principle of occluding a vessel and listening for the return of flow is used in "
            "Doppler studies and in the arm cuff of every GP surgery.",
        "precautions": [
            "Let the subject rest for five minutes and sit with the arm supported at heart level.",
            "Use a cuff of the correct size for the arm circumference.",
            "Release the pressure slowly, about 2–3 mmHg per second.",
            "Take at least two readings a minute apart and average them.",
        ],
        "errors": [
            "Cuff too small, which overestimates the pressure.",
            "Deflating too quickly, so the first and last sounds are missed.",
            "Arm above or below heart level, which shifts the reading by several mmHg.",
            "White-coat effect: anxiety in the clinic raising the pressure above its usual value.",
        ],
        "exam": [
            "State which sound marks which pressure — first sound systolic, disappearance "
            "diastolic.",
            "Quote the reading with units and note that a single reading is not a diagnosis.",
        ],
        "viva": [
            {"q": "What causes the Korotkoff sounds?",
             "a": "Turbulent flow through a partially compressed artery; as the artery opens and "
                  "closes with each pulse, the disturbed flow generates audible vibrations."},
            {"q": "Why is the cuff inflated above the expected systolic pressure?",
             "a": "To stop arterial flow completely, so that the first sound heard on release "
                  "unambiguously marks the return of flow at systolic pressure."},
            {"q": "Why is a single high reading not a diagnosis of hypertension?",
             "a": "Pressure varies with stress, exercise, caffeine and the time of day; diagnosis "
                  "requires repeated readings on separate occasions, often including home monitoring."},
        ],
    },
    "bio-genetics-dice-xii": {
        "objectives": [
            "Model a monohybrid cross using random dice throws.",
            "Compare observed phenotype ratios with the expected 3:1 ratio.",
            "Explain why small samples deviate from expected ratios.",
        ],
        "theory": [
            "In a monohybrid cross between two heterozygotes, Tt × Tt, each parent passes on either "
            "T or t with equal probability. The Punnett square gives genotypes 1 TT : 2 Tt : 1 tt, "
            "so three-quarters of the offspring show the dominant phenotype and one-quarter the "
            "recessive. That is the 3:1 ratio predicted by Mendel.",
            "A dice throw is a physical randomiser: 1–3 can represent T and 4–6 can represent t. "
            "Each throw is independent, so the model reproduces the segregation of alleles at "
            "meiosis. Observed ratios approach 3:1 only as the number of throws grows; with small "
            "samples, chance alone produces noticeable deviations, which is why a chi-squared test "
            "is used to decide whether a difference is significant.",
        ],
        "formula": "expected tall : short = 3 : 1\n"
        "percentage tall = (number tall ÷ total) × 100\n"
        "χ² = Σ (observed − expected)² / expected",
        "context": "The same logic predicts the inheritance of genetic disorders, the ratios in "
            "plant and animal breeding, and the outcome of crossing heterozygous crops for "
            "improved varieties. Randomisation is the basis of every genetic model and of "
            "statistical sampling.",
        "precautions": [
            "Use fair dice and throw them properly rather than placing them.",
            "Define the allele mapping before starting and keep it fixed.",
            "Record every throw, including inconvenient results — do not discard data.",
            "Use a large number of throws before comparing with the expected ratio.",
        ],
        "errors": [
            "Small sample size, so random fluctuation is mistaken for a real deviation.",
            "Recording only the phenotype and losing the genotype information.",
            "Changing the allele mapping partway through the experiment.",
        ],
        "exam": [
            "Show the Punnett square and derive the 3:1 ratio before presenting the dice results.",
            "Explain any deviation in terms of sample size and chance, not experimental error "
            "alone.",
        ],
        "viva": [
            {"q": "Why does the observed ratio differ from 3:1 in a small sample?",
             "a": "Each throw is independent and subject to chance; only as the number of trials "
                  "grows does the observed proportion converge on the expected probability."},
            {"q": "What does the chi-squared test tell you?",
             "a": "It compares observed and expected frequencies and estimates the probability that "
                  "the deviation arose by chance, allowing you to accept or reject the expected "
                  "ratio."},
            {"q": "Why is the dice model a good analogue of meiosis?",
             "a": "Alleles segregate randomly and independently into gametes, just as a fair die "
                  "produces each outcome with a fixed probability on every throw."},
        ],
    },
}

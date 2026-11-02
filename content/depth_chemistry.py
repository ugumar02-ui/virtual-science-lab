"""Extended theory, context and viva material for the Chemistry practicals."""

CHEMISTRY_DEPTH = {
    "chem-chromatography-ix": {
        "objectives": [
            "Separate the dyes in a mixture by partition between a mobile and a stationary phase.",
            "Measure Rf values and use them to identify a dye.",
            "Explain why the solvent front must not be allowed to reach the top of the paper.",
        ],
        "theory": [
            "Paper chromatography separates substances by their different affinities for two "
            "phases. The paper holds water in its fibres and acts as the stationary phase; the "
            "solvent creeping up the paper is the mobile phase. A dye that is more soluble in the "
            "solvent travels further, while one that binds more strongly to the paper stays near "
            "the origin.",
            "The ratio of the distance travelled by a spot to the distance travelled by the "
            "solvent front is the Rf value. Because Rf depends on the solvent, the paper and the "
            "temperature, it is only comparable between runs done under identical conditions. A "
            "single Rf is therefore evidence, not proof; comparing with a known standard run "
            "alongside is what makes the identification sound.",
        ],
        "formula": "Rf = distance moved by the spot ÷ distance moved by the solvent front",
        "context": "The same partition principle separates drugs in a forensic lab, detects "
        "pesticide residues in food and diagnoses metabolic disorders from a drop of blood. "
        "Thin-layer chromatography is the classroom-to-industry version of this practical.",
        "precautions": [
            "Use a pencil, not ink, for the baseline and the spot marks.",
            "Keep the spots small and let them dry between applications.",
            "Suspend the paper so the solvent touches it above the baseline.",
            "Stop the run before the solvent front reaches the top edge.",
        ],
        "errors": [
            "Spots too large, giving overlapping streaks instead of separate spots.",
            "The baseline dipping into the solvent, so dyes dissolve into the reservoir.",
            "Uneven solvent flow because the paper touches the beaker wall.",
        ],
        "exam": [
            "Measure both distances from the baseline, not from the bottom of the paper.",
            "Quote Rf without units and always to two decimal places.",
        ],
        "viva": [
            {"q": "Why must the baseline be drawn in pencil?",
             "a": "Ink is itself a mixture of dyes and would separate, adding extra spots and confusing the result."},
            {"q": "What does an Rf value greater than 1 mean?",
             "a": "It is impossible in a properly run chromatogram; it means the spot or the solvent front was measured incorrectly."},
            {"q": "How would changing the solvent affect the Rf values?",
             "a": "A more polar solvent carries polar dyes further, changing every Rf; values are only valid for the solvent system used."},
        ],
    },
    "chem-conductivity-ix": {
        "objectives": [
            "Distinguish electrolytes from non-electrolytes by testing conductivity.",
            "Relate conductivity to the presence of mobile ions.",
            "Explain why solid ionic compounds do not conduct.",
        ],
        "theory": [
            "A solution conducts electricity only if it contains mobile charge carriers. In an "
            "electrolyte these are ions; in metals they are electrons. A covalent compound such "
            "as sugar dissolves as neutral molecules, so its solution has no charge carriers and "
            "the lamp stays dark.",
            "The strength of conduction depends on both the number of ions and their mobility. "
            "Strong electrolytes dissociate almost completely, weak electrolytes only partially, "
            "so a weak acid lights the lamp dimly. Solid ionic salts do not conduct because the "
            "ions are locked in the lattice, even though the ions themselves are charged.",
        ],
        "formula": "electrolyte ⇌ ions in solution\n"
        "conductance ∝ number of mobile ions × ionic mobility",
        "context": "Electrolytes make batteries, electroplating, anodising and chlorine manufacture "
        "possible. The same test explains why you must never touch a mains switch with wet hands: "
        "tap water contains enough ions to carry a dangerous current.",
        "precautions": [
            "Use graphite or platinum electrodes; copper or iron would react and contaminate the solution.",
            "Clean and dry the electrodes between tests to avoid carry-over.",
            "Keep the electrode spacing and depth the same for every solution.",
            "Use low voltage and do not leave the circuit connected for long.",
        ],
        "errors": [
            "Residue from a previous solution making a non-electrolyte appear conductive.",
            "Different electrode areas or spacing changing the brightness independently of the solute.",
            "Judging weak conduction by eye when the lamp threshold hides small currents.",
        ],
        "exam": [
            "Say 'mobile ions', not just 'ions' — the mobility is the point of the liquid state.",
            "Classify each test substance as strong electrolyte, weak electrolyte or non-electrolyte with a reason.",
        ],
        "viva": [
            {"q": "Why does solid sodium chloride not conduct?",
             "a": "Its ions are held in fixed positions in the crystal lattice, so they cannot move to carry charge; melting or dissolving frees them."},
            {"q": "Why is acetic acid a weaker conductor than hydrochloric acid at the same concentration?",
             "a": "Acetic acid is only partially ionised, so it provides far fewer mobile ions for the same number of molecules."},
            {"q": "What would you observe if the electrodes were made of copper in silver nitrate solution?",
             "a": "The anode would dissolve and silver would plate onto the cathode; the solution changes composition, so the test would no longer measure the salt alone."},
        ],
    },
    "chem-solubility-ix": {
        "objectives": [
            "Measure how the solubility of a salt changes with temperature.",
            "Plot a solubility curve and interpret its shape.",
            "Distinguish solubility from rate of dissolving.",
        ],
        "theory": [
            "Solubility is the maximum mass of solute that dissolves in a fixed mass of solvent "
            "at a stated temperature. For most ionic solids, dissolving is endothermic and "
            "solubility rises with temperature; the curve is steep for potassium nitrate and "
            "almost flat for sodium chloride.",
            "A few salts, such as cerium(III) sulfate, become less soluble as the solution warms. "
            "The shape of the curve is used industrially in fractional crystallisation: cooling a "
            "hot saturated solution deposits the least soluble component first, which is how "
            "pure crystals are obtained from a mixture.",
        ],
        "formula": "solubility = mass of solute ÷ mass of solvent × 100 g per 100 g water",
        "context": "Solubility curves decide how much fertiliser can be dissolved in irrigation "
        "water, why salt crystallises from a drying lake, and how pharmaceutical chemists "
        "recrystallise a drug to purify it.",
        "precautions": [
            "Keep the water bath at a steady temperature while the solute dissolves.",
            "Stir until no more solid dissolves, then allow undissolved solid to settle.",
            "Weigh the dry solute and the solvent accurately.",
            "Filter or decant carefully so no solid is carried into the sample.",
        ],
        "errors": [
            "Assuming saturation before equilibrium is reached.",
            "Evaporation of solvent during heating, concentrating the solution.",
            "Temperature falling between saturation and sampling.",
        ],
        "exam": [
            "Read solubility at a stated temperature, and state the units as g per 100 g of water.",
            "Use the curve to explain crystallisation rather than quoting the definition alone.",
        ],
        "viva": [
            {"q": "What is the difference between solubility and rate of dissolving?",
             "a": "Solubility is how much can dissolve at equilibrium; rate is how quickly it dissolves. Grinding increases rate but not solubility."},
            {"q": "Why does potassium nitrate have a much steeper curve than sodium chloride?",
             "a": "Its dissolution is more strongly endothermic, so raising the temperature shifts the equilibrium towards the dissolved state far more."},
            {"q": "How would you obtain pure potassium nitrate from a mixture with sodium chloride?",
             "a": "Dissolve in hot water, cool, and filter the crystals that form first — potassium nitrate, with the steeper curve, crystallises preferentially."},
        ],
    },
    "chem-ph-x": {
        "objectives": [
            "Measure the pH of common solutions with indicator paper and a pH meter.",
            "Relate pH to hydrogen-ion concentration.",
            "Classify solutions as acidic, neutral or alkaline and compare their strength.",
        ],
        "theory": [
            "pH is the negative logarithm of the hydrogen-ion concentration. Because the scale is "
            "logarithmic, a change of one pH unit means a tenfold change in hydrogen-ion "
            "concentration, so pH 3 is a hundred times more acidic than pH 5, not twice.",
            "Universal indicator paper gives a rapid approximate reading, while a calibrated pH "
            "meter gives two decimal places. The meter must be calibrated with buffer solutions "
            "at two points, and the electrode rinsed between samples, otherwise the reading "
            "drifts — a point examiners like to test.",
        ],
        "formula": "pH = −log₁₀[H⁺]\n"
        "[H⁺] = 10^(−pH) mol dm⁻³",
        "context": "pH control governs blood chemistry (7.35–7.45), soil fertility, swimming-pool "
        "sanitation, food preservation and the formulation of every shampoo and skin cream. "
        "Enzymes and drug stability both depend on it.",
        "precautions": [
            "Rinse the electrode with distilled water and blot it dry between samples.",
            "Calibrate the meter with fresh buffers before measuring.",
            "Do not dip indicator paper into the stock bottle — use a clean rod.",
            "Measure at room temperature and note it, since pH depends on temperature.",
        ],
        "errors": [
            "Uncalibrated or drifting electrode.",
            "Carry-over between samples contaminating the next reading.",
            "Reading indicator colour under coloured lighting or after the paper has dried.",
        ],
        "exam": [
            "Remember pH is logarithmic — examiners test the tenfold step repeatedly.",
            "State that a lower pH means a higher hydrogen-ion concentration.",
        ],
        "viva": [
            {"q": "Why is pH 2 ten times more acidic than pH 3, not twice?",
             "a": "pH is a logarithmic scale: each unit is a factor of ten in hydrogen-ion concentration."},
            {"q": "Why must a pH meter be calibrated?",
             "a": "The electrode response drifts with age and use; two buffer points correct both the offset and the slope of the response."},
            {"q": "Why can universal indicator not give an exact pH?",
             "a": "It relies on comparing a continuous colour change by eye, so it resolves about one pH unit at best."},
        ],
    },
    "chem-standardise-naoh-x": {
        "objectives": [
            "Carry out a titration to a concordant end point.",
            "Calculate the concentration of sodium hydroxide from a standard acid.",
            "Explain the role of the indicator and the choice of phenolphthalein.",
        ],
        "theory": [
            "A titration finds the volume of one solution that exactly reacts with a known volume "
            "of another. At the equivalence point the moles of acid and base are in the ratio of "
            "their stoichiometric coefficients. For a monobasic acid and sodium hydroxide that "
            "ratio is 1:1.",
            "Phenolphthalein changes from colourless to pale pink in the alkaline region, which "
            "matches the sharp pH jump at the equivalence point of a strong acid–strong base "
            "titration. The first permanent pink tinge that survives swirling marks the end "
            "point; a deep pink means overshoot and a high result.",
        ],
        "formula": "cₐVₐ / a = c_bV_b / b\n"
        "for NaOH + HCl: c(acid) × V(acid) = c(base) × V(base)",
        "context": "Standardisation underpins every quantitative analysis: checking the strength "
        "of vinegar, measuring the active ingredient in a tablet, or monitoring the acidity of "
        "rain. Industrial laboratories standardise their base daily because carbonate uptake "
        "slowly changes its concentration.",
        "precautions": [
            "Rinse the burette with the base solution before filling it.",
            "Remove the air bubble below the tap.",
            "Read the meniscus at eye level with the bottom of the curve.",
            "Add dropwise near the end point and swirl continuously.",
        ],
        "errors": [
            "Parallax in reading the burette, giving a systematic offset.",
            "Overshooting the end point, which overestimates the base volume.",
            "Using wet glassware that dilutes the solution being titrated.",
        ],
        "exam": [
            "Show the mole ratio explicitly before substituting values.",
            "Take concordant titres within 0.10 cm³ and average them; do not average all runs blindly.",
        ],
        "viva": [
            {"q": "Why is phenolphthalein suitable here but not methyl orange?",
             "a": "Both work for a strong acid–strong base titration, but phenolphthalein gives a sharper, more visible change from colourless to pale pink near pH 8–9."},
            {"q": "What is a concordant titre?",
             "a": "Two or more titres agreeing to within 0.10 cm³, showing that the end point is reproducible."},
            {"q": "How would absorbed carbon dioxide affect the result?",
             "a": "It reacts with sodium hydroxide, lowering its effective concentration and making the calculated value too low."},
        ],
    },
    "chem-oxalic-x": {
        "objectives": [
            "Prepare and use a standard solution of oxalic acid.",
            "Determine the molarity of a sodium hydroxide solution by titration.",
            "Handle a diprotic acid correctly in the mole calculation.",
        ],
        "theory": [
            "Oxalic acid is a diprotic acid: one mole supplies two moles of hydrogen ions. That "
            "factor of two must appear in the mole ratio, or the calculated concentration is out "
            "by a factor of two — the most common error in this practical.",
            "Because oxalic acid is a stable solid that can be weighed accurately, it serves as a "
            "primary standard. A known mass dissolved in a known volume gives an exactly known "
            "concentration, which is then used to standardise the sodium hydroxide.",
        ],
        "formula": "n(acid) = mass ÷ molar mass\n"
        "c = n ÷ V(dm³)\n"
        "2 × c(acid) × V(acid) = c(base) × V(base)",
        "context": "Primary standards make chemical measurement traceable. The same approach "
        "standardises the EDTA used to test water hardness and the silver nitrate used in "
        "chloride analysis.",
        "precautions": [
            "Weigh the oxalic acid quickly — it is efflorescent and loses water of crystallisation.",
            "Dissolve completely before making up to the mark.",
            "Use a volumetric flask and read the bottom of the meniscus.",
            "Keep the phenolphthalein end point pale pink, not magenta.",
        ],
        "errors": [
            "Forgetting the 2:1 stoichiometry of the diprotic acid.",
            "Mass loss from the hydrated crystals before weighing.",
            "Filling the volumetric flask above the mark, diluting the standard.",
        ],
        "exam": [
            "Write the balanced equation and derive the mole ratio before any arithmetic.",
            "Give the final concentration to three significant figures with units of mol dm⁻³.",
        ],
        "viva": [
            {"q": "Why is oxalic acid used as a primary standard?",
             "a": "It is available pure and stable, can be weighed accurately, and has a high molar mass so weighing errors are proportionally small."},
            {"q": "How does the diprotic nature change the calculation?",
             "a": "One mole of acid neutralises two moles of hydroxide, so the acid contributes twice as many moles of H⁺ as a monobasic acid at the same concentration."},
            {"q": "What is the effect of using wet glassware?",
             "a": "Residual water dilutes the solution, so the actual concentration is lower than calculated and the titre is affected accordingly."},
        ],
    },
    "chem-flame-x": {
        "objectives": [
            "Identify metal ions from the colour they impart to a flame.",
            "Explain the origin of flame colour in terms of electron transitions.",
            "Recognise the limitations of flame tests as an identification method.",
        ],
        "theory": [
            "Heat excites electrons in metal ions to higher energy levels. As they fall back, they "
            "emit light of characteristic wavelengths, producing a colour that acts as a "
            "fingerprint: lithium crimson, sodium golden yellow, potassium lilac, calcium "
            "brick-red, copper blue-green, barium apple-green.",
            "The test is quick but not conclusive. Sodium contamination is ubiquitous and its "
            "yellow can mask other colours, so a cobalt-blue glass is used to filter it out. "
            "Mixtures produce blended colours, which is why a flame test is usually confirmed "
            "with a wet chemical test.",
        ],
        "formula": "ΔE = hf = hc/λ",
        "context": "Flame emission is the basis of atomic emission spectroscopy and the flame "
        "photometer used to measure sodium and potassium in blood and in drinking water. "
        "Fireworks colours are chosen by picking the right metal salt.",
        "precautions": [
            "Clean the nichrome wire in concentrated acid and heat it until the flame is colourless before each test.",
            "Use a small sample; too much salt gives a smoky, misleading flame.",
            "View potassium through cobalt-blue glass to filter sodium yellow.",
            "Work in a fume cupboard or well-ventilated area.",
        ],
        "errors": [
            "Contamination from a previous sample, especially sodium.",
            "Judging colour in poor lighting or against a coloured background.",
            "Confusing the outer oxidising flame colour with the sample's emission.",
        ],
        "exam": [
            "Give the colour and the ion together; a colour alone earns nothing.",
            "State one limitation, such as sodium masking or mixtures blending.",
        ],
        "viva": [
            {"q": "Why do different metal ions give different flame colours?",
             "a": "Each element has a unique set of energy levels, so the emitted photons have characteristic energies and therefore characteristic wavelengths."},
            {"q": "Why is a cobalt-blue glass used?",
             "a": "It absorbs the intense yellow sodium emission, allowing the lilac potassium colour to be seen."},
            {"q": "Why is a flame test not sufficient on its own?",
             "a": "Colours can be masked or blended in mixtures and depend on the observer, so a confirmatory chemical test is needed."},
        ],
    },
    "chem-halide-x": {
        "objectives": [
            "Identify chloride, bromide and iodide ions with silver nitrate.",
            "Interpret the colour and solubility of the silver halide precipitates.",
            "Explain why dilute nitric acid is added first.",
        ],
        "theory": [
            "Silver ions combine with halide ions to form insoluble silver halides: white silver "
            "chloride, cream silver bromide and pale yellow silver iodide. Adding dilute nitric "
            "acid first removes carbonate and hydroxide ions, which would otherwise precipitate "
            "white silver carbonate and be mistaken for chloride.",
            "The precipitates differ in their solubility in ammonia. Silver chloride dissolves "
            "readily in dilute ammonia, silver bromide only in concentrated ammonia, and silver "
            "iodide not at all. That solubility sequence is a second, independent piece of "
            "evidence and is what turns a colour match into an identification.",
        ],
        "formula": "Ag⁺(aq) + X⁻(aq) → AgX(s)\n"
        "AgCl + 2NH₃ → [Ag(NH₃)₂]⁺ + Cl⁻",
        "context": "This is the standard test for halides in water analysis and in the "
        "identification of unknown salts. The light sensitivity of silver halides was the basis "
        "of photographic film.",
        "precautions": [
            "Acidify with dilute nitric acid before adding silver nitrate.",
            "Add silver nitrate dropwise and observe the precipitate colour immediately.",
            "Test solubility in ammonia separately for each precipitate.",
            "Wash hands and avoid contact with silver nitrate, which stains skin.",
        ],
        "errors": [
            "Omitting the acid, so carbonate gives a false white precipitate.",
            "Judging cream and pale yellow under poor light — they are easy to confuse.",
            "Too much ammonia dissolving the precipitate before its behaviour is noted.",
        ],
        "exam": [
            "Give the precipitate colour and the ammonia solubility for full marks.",
            "Write the ionic equation, not just a word description.",
        ],
        "viva": [
            {"q": "Why add nitric acid before silver nitrate?",
             "a": "It removes carbonate and hydroxide ions that would otherwise form a white precipitate and be mistaken for a chloride."},
            {"q": "How would you distinguish bromide from iodide?",
             "a": "Silver bromide is cream and dissolves in concentrated ammonia; silver iodide is pale yellow and insoluble in ammonia."},
            {"q": "Why is the test done in the dark or quickly?",
             "a": "Silver halides decompose in light, darkening the precipitate and making the colour judgement unreliable."},
        ],
    },
    "chem-heat-neutralisation-xi": {
        "objectives": [
            "Measure the heat evolved when an acid neutralises a base.",
            "Calculate the enthalpy change per mole of water formed.",
            "Explain why the value is slightly smaller than the accepted −57.3 kJ mol⁻¹.",
        ],
        "theory": [
            "Neutralisation of a strong acid by a strong base is essentially the reaction of "
            "hydrogen ions with hydroxide ions to form water. Because the reacting ions are the "
            "same in every such pair, the enthalpy change is nearly constant at about "
            "−57.3 kJ mol⁻¹.",
            "The heat released warms the solution, and q = mcΔT gives the energy, with m the mass "
            "of the mixed solution and c its specific heat capacity, taken as that of water. "
            "Dividing by the number of moles of water formed gives the molar enthalpy change. "
            "Heat lost to the calorimeter and the surroundings makes the measured value "
            "numerically smaller than the true value.",
        ],
        "formula": "q = mcΔT\n"
        "ΔH = −q ÷ n(water formed)",
        "context": "Enthalpy of neutralisation underpins the design of hand warmers, the "
        "thermochemistry of antacid tablets and the safe handling of industrial acid spills, "
        "where the heat released can boil a solution.",
        "precautions": [
            "Use a polystyrene or insulated cup to reduce heat loss.",
            "Measure both solutions accurately and record their starting temperatures separately.",
            "Stir continuously and record the highest temperature reached.",
            "Work quickly so the mixture does not cool before the maximum is read.",
        ],
        "errors": [
            "Heat loss to the cup and surroundings, giving a low magnitude.",
            "Assuming the density and specific heat of the mixture equal those of pure water.",
            "Missing the true maximum temperature because of thermometer lag.",
        ],
        "exam": [
            "Remember the sign: heat released means ΔH is negative.",
            "Divide by the moles of water formed, not the moles of acid or base alone.",
        ],
        "viva": [
            {"q": "Why is the enthalpy of neutralisation nearly the same for all strong acid–strong base pairs?",
             "a": "The only reaction occurring is H⁺ + OH⁻ → H₂O; the spectator ions do not participate."},
            {"q": "Why is the measured value less exothermic than the accepted one?",
             "a": "Some heat is lost to the calorimeter and the air, so the observed temperature rise, and therefore q, is smaller."},
            {"q": "How would using a weak acid change the result?",
             "a": "The value would be smaller in magnitude because energy is needed to ionise the weak acid before neutralisation can occur."},
        ],
    },
    "chem-kmno4-xi": {
        "objectives": [
            "Carry out a redox titration using potassium manganate(VII).",
            "Use the self-indicating end point correctly.",
            "Calculate the mass of iron in a sample from the titre.",
        ],
        "theory": [
            "Acidified manganate(VII) is a strong oxidising agent. It oxidises iron(II) to "
            "iron(III) while being reduced from MnO₄⁻ to Mn²⁺, changing from deep purple to "
            "almost colourless. The first permanent pink tinge therefore signals that all the "
            "iron(II) has reacted — the solution indicates its own end point.",
            "The half-equations show a five-electron change for manganese and a one-electron "
            "change for iron, so one mole of manganate reacts with five moles of iron(II). "
            "Getting that 5:1 ratio right is the heart of the calculation.",
        ],
        "formula": "MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O\n"
        "Fe²⁺ → Fe³⁺ + e⁻\n"
        "n(Fe²⁺) = 5 × n(MnO₄⁻)",
        "context": "Redox titration is used to measure iron in ore, in drinking water and in "
        "pharmaceutical iron supplements. The same oxidising chemistry disinfects water and "
        "bleaches textiles.",
        "precautions": [
            "Acidify with dilute sulfuric acid, not hydrochloric acid, which manganate would oxidise.",
            "Read the burette at eye level against a white tile.",
            "Add the last drops slowly and swirl after each addition.",
            "Use freshly prepared iron(II) solution, since it oxidises in air.",
        ],
        "errors": [
            "Using hydrochloric acid, which consumes some oxidant.",
            "Iron(II) already partly oxidised before the titration begins.",
            "Reading the pale pink end point too late, overshooting the equivalence point.",
        ],
        "exam": [
            "Derive the 5:1 ratio from the half-equations rather than quoting it.",
            "Show the conversion from moles of iron to mass using the molar mass.",
        ],
        "viva": [
            {"q": "Why is no external indicator needed?",
             "a": "Manganate(VII) is intensely coloured and its reduced form Mn²⁺ is nearly colourless, so the first excess gives a visible pink."},
            {"q": "Why must sulfuric acid be used rather than hydrochloric acid?",
             "a": "Manganate(VII) would oxidise chloride ions to chlorine, consuming oxidant and giving a falsely high iron result."},
            {"q": "What is the oxidation state change of manganese?",
             "a": "It falls from +7 in manganate(VII) to +2 in Mn²⁺, a five-electron reduction."},
        ],
    },
    "chem-salt-analysis-xii": {
        "objectives": [
            "Identify the cation and anion in an unknown salt by systematic tests.",
            "Interpret solubility, gas evolution and precipitate behaviour.",
            "Distinguish confirmatory tests from preliminary observations.",
        ],
        "theory": [
            "Salt analysis proceeds in a fixed order: observe colour and solubility, test the "
            "solution's pH, then identify the anion and finally the cation. The order matters "
            "because some reagents used for cations would also precipitate anions, so the anion "
            "must be established first.",
            "Confirmatory tests distinguish between ions that give similar preliminary results. "
            "Ammonia added dropwise and then in excess separates cations by the differing "
            "solubility of their hydroxides in excess ligand; flame tests and specific "
            "precipitates then confirm the identification.",
        ],
        "formula": "cation + OH⁻ → hydroxide precipitate\n"
        "amphoteric hydroxides dissolve in excess NaOH",
        "context": "Qualitative analysis is the front line of forensic and environmental "
        "chemistry: identifying an unknown powder, checking for heavy-metal contamination, or "
        "confirming the composition of a mineral.",
        "precautions": [
            "Test the anion before the cation.",
            "Add reagents dropwise and record each observation before adding more.",
            "Use a fresh sample for each confirmatory test.",
            "Heat gently when testing for gases and hold the test paper in the vapour, not the liquid.",
        ],
        "errors": [
            "Adding excess reagent immediately, hiding the initial precipitate.",
            "Contaminated apparatus producing a false positive.",
            "Confusing a white precipitate with undissolved salt.",
        ],
        "exam": [
            "Record observations, then the inference — two separate columns.",
            "Give the ionic equation for each confirmatory test.",
        ],
        "viva": [
            {"q": "Why is the anion identified before the cation?",
             "a": "Some cation reagents form precipitates with anions, so the anion must be known to interpret later observations correctly."},
            {"q": "What does dissolving in excess sodium hydroxide tell you?",
             "a": "The hydroxide is amphoteric, which points to zinc, aluminium or lead rather than a simple basic cation."},
            {"q": "Why is a fresh sample used for each test?",
             "a": "Reagents added in one test would contaminate the sample and change the result of the next."},
        ],
    },
    "chem-carbonyl-xii": {
        "objectives": [
            "Distinguish aldehydes from ketones using oxidation tests.",
            "Interpret the silver mirror and the brick-red precipitate.",
            "Explain why ketones resist mild oxidation.",
        ],
        "theory": [
            "Aldehydes have a hydrogen attached to the carbonyl carbon; ketones do not. Mild "
            "oxidising agents can therefore convert an aldehyde to a carboxylic acid but leave a "
            "ketone unchanged. Tollens' reagent is reduced to metallic silver, forming a mirror, "
            "and Fehling's solution gives a brick-red precipitate of copper(I) oxide.",
            "The tests are specific to aldehydes under the stated conditions. Strong oxidising "
            "agents such as acidified dichromate will eventually attack ketones by breaking the "
            "carbon chain, so the choice of mild reagent is what makes the distinction meaningful.",
        ],
        "formula": "RCHO + 2[Ag(NH₃)₂]⁺ + 2OH⁻ → RCOO⁻ + 2Ag + 4NH₃ + H₂O\n"
        "RCHO + 2Cu²⁺ + 5OH⁻ → RCOO⁻ + Cu₂O + 3H₂O",
        "context": "These tests identify sugars and carbonyl compounds in food analysis and in "
        "clinical chemistry — glucose detection in urine historically used Fehling's solution. "
        "Tollens' reagent also silver mirrors glass.",
        "precautions": [
            "Prepare Tollens' reagent fresh and do not store it — it can form explosive silver fulminate.",
            "Warm gently in a water bath; boiling gives a black decomposition instead of a mirror.",
            "Clean the test tube for a good silver mirror.",
            "Use freshly prepared Fehling's solution and heat evenly.",
        ],
        "errors": [
            "Overheating, which destroys the reagent and gives a misleading black residue.",
            "Old or contaminated Tollens' reagent giving a false negative.",
            "Confusing the red precipitate with the blue solution colour.",
        ],
        "exam": [
            "Name the reagent, the observation and the inference for each test.",
            "State why the test distinguishes the two classes structurally.",
        ],
        "viva": [
            {"q": "Why do ketones not give a positive Tollens' test?",
             "a": "They lack the hydrogen on the carbonyl carbon that must be removed during oxidation, so they cannot be oxidised under these mild conditions."},
            {"q": "What is the silver mirror chemically?",
             "a": "Metallic silver deposited on the glass when silver ions in Tollens' reagent are reduced by the aldehyde."},
            {"q": "Why must Tollens' reagent be freshly prepared?",
             "a": "On standing it decomposes to explosive silver fulminate and loses its oxidising power."},
        ],
    },
}

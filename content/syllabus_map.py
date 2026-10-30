"""Official AKU-EB syllabus reference for every practical in the app.

Each entry records the exact topic and activity number from the 2025-26
syllabus PDFs, plus the activity wording. Nothing in this app is invented:
every practical below traces back to one of these lines. Where the app uses a
different method from the one named in the syllabus, the ``note`` field says so
and the note is shown to the student.

Source documents (Downloads/aku-syllabi):
  physics-ssc, physics-hssc, chemistry-ssc, chemistry-hssc,
  biology-ssc, biology-hssc  (AKU-EB 2025)
"""

# Number of practical activities listed in each official topic-wise table.
# Counted directly from the 2025 syllabus PDFs (Part I / Part II tables).
OFFICIAL_COUNTS: dict[str, dict[str, int]] = {
    "physics": {"IX": 12, "X": 12, "XI": 12, "XII": 12},
    "chemistry": {"IX": 12, "X": 12, "XI": 11, "XII": 11},
    "biology": {"IX": 19, "X": 36, "XI": 34, "XII": 22},
}

SYLLABUS: dict[str, dict[str, str]] = {
    # ------------------------------------------------------------- physics IX
    "phy-vernier-ix": {
        "ref": "Physics IX · Topic 1 Measurement · activity 2",
        "activity": "To calculate the area of the cross-section of a solid cylinder by measuring the diameter with Vernier callipers.",
    },
    "phy-screw-gauge-ix": {
        "ref": "Physics IX · Topic 1 Measurement · activity 3",
        "activity": "To measure the thickness of a metal strip or the diameter of a wire using a screw gauge.",
    },
    "phy-moments-ix": {
        "ref": "Physics IX · Topic 4 Turning Effect of Forces · activity 7",
        "activity": "To find the weight of an unknown object using the principle of moments.",
    },
    "phy-hooke-ix": {
        "ref": "Physics IX · Topic 5 Deformation of Solids · activity 9",
        "activity": "To study the relationship between load and extension of a helical spring with the help of a graph.",
    },
    # -------------------------------------------------------------- physics X
    "phy-pendulum-x": {
        "ref": "Physics X · Topic 11 Wave Motion · activity 2",
        "activity": "To study the effect of the change in the length of a simple pendulum on its time period and hence calculate the value of acceleration due to gravity 'g'.",
    },
    "phy-resonance-x": {
        "ref": "Physics X · Topic 12 Sound · activity 3",
        "activity": "To study the reflection of sound by determining the length of the air column at first loud sound using tuning forks of different frequencies and to determine the corresponding wavelength of sound.",
    },
    "phy-ohm-x": {
        "ref": "Physics X · Topic 15 Electric Current · activity 7",
        "activity": "To verify Ohm's law using a wire as a conductor.",
    },
    "phy-series-x": {
        "ref": "Physics X · Topic 16 D.C. Circuits · activities 9–10",
        "activity": "To study resistance in a series circuit and in a parallel circuit.",
    },
    # ------------------------------------------------------------- physics XI
    "phy-spherometer-xi": {
        "ref": "Physics XI · Topic 1 Physical Quantities and Measurement · activity 3",
        "activity": "Determine the radius of curvature of any spherical surface by using a spherometer.",
    },
    "phy-specific-heat-xi": {
        "ref": "Physics XI · Topic 10 Thermodynamics · activity 11",
        "activity": "Determine the specific heat capacity of solid using method of mixture (Regnault's Method).",
    },
    # ------------------------------------------------------------ physics XII
    "phy-filament-xii": {
        "ref": "Physics XII · Topic 13 Electric Current · activity 3",
        "activity": "Investigate the relationship between current passing through a tungsten filament lamp and the potential applied across it.",
    },
    "phy-rc-xii": {
        "ref": "Physics XII · Topic 12 Electrostatics · activity 2",
        "activity": "Determine time constant by charging and discharging a capacitor through a resistor.",
    },
    # ----------------------------------------------------------- chemistry IX
    "chem-chromatography-ix": {
        "ref": "Chemistry IX · Topic 7 Solutions · activity 10",
        "activity": "Perform paper chromatography to separate the components of the given ink mixture.",
    },
    "chem-conductivity-ix": {
        "ref": "Chemistry IX · Topic 8 Electrochemistry · activity 11",
        "activity": "Demonstrate the conductivity of different solutions.",
    },
    "chem-solubility-ix": {
        "ref": "Chemistry IX · Topic 7 Solutions · activity 8",
        "activity": "Demonstrate that temperature affects solubility.",
    },
    # ------------------------------------------------------------ chemistry X
    "chem-ph-x": {
        "ref": "Chemistry X · Topic 10 Acids, Bases and Salts · activity 2",
        "activity": "Measure the pH of different solutions using pH paper to detect their acidic, neutral, or basic nature.",
    },
    "chem-standardise-naoh-x": {
        "ref": "Chemistry X · Topic 10 Acids, Bases and Salts · activity 3",
        "activity": "Standardise the given solution of sodium hydroxide volumetrically.",
    },
    "chem-oxalic-x": {
        "ref": "Chemistry X · Topic 10 Acids, Bases and Salts · activity 4",
        "activity": "Measure the exact molarity of a solution of oxalic acid volumetrically.",
    },
    "chem-halide-x": {
        "ref": "Chemistry X · Topic 10 Acids, Bases and Salts · activity 5",
        "activity": "Perform the silver nitrate test to detect chloride, bromide and iodide ions.",
    },
    "chem-flame-x": {
        "ref": "Chemistry X · Topic 10 Acids, Bases and Salts · activity 6",
        "activity": "Perform a flame test to detect the presence of calcium, strontium, barium and copper ions by observing characteristic flame colours.",
    },
    # ----------------------------------------------------------- chemistry XI
    "chem-heat-neutralisation-xi": {
        "ref": "Chemistry XI · Topic 9 Chemical Energetics · activity 7",
        "activity": "Measure the heat of neutralisation of NaOH and HCl.",
    },
    "chem-kmno4-xi": {
        "ref": "Chemistry XI · Topic 10 Electrochemistry · activity 9",
        "activity": "Measure the amount of iron in the given sample volumetrically.",
    },
    # ---------------------------------------------------------- chemistry XII
    "chem-salt-analysis-xii": {
        "ref": "Chemistry XII · Topic 11 s- and p-Block Elements · activity 1",
        "activity": "Detect the given cations and anions.",
    },
    "chem-carbonyl-xii": {
        "ref": "Chemistry XII · Topic 17 Carbonyl Compounds: Aldehydes and Ketones · activity 7",
        "activity": "Detect the aldehyde and ketone functional group.",
    },
    # ------------------------------------------------------------- biology IX
    "bio-sav-ix": {
        "ref": "Biology IX · Topic 4 Cells and Tissues · activity 6",
        "activity": "Calculate surface area to volume ratio of cubes of different sizes.",
    },
    "bio-osmosis-ix": {
        "ref": "Biology IX · Topic 4 Cells and Tissues · activity 7",
        "activity": "Demonstrate the process of osmosis using a semi-permeable membrane.",
        "note": "The syllabus names cellophane and a thistle funnel. This version uses potato tissue instead, because it gives a measurable isotonic point; the principle is identical.",
    },
    "bio-amylase-temp-ix": {
        "ref": "Biology IX · Topic 6 Enzymes · activity 13",
        "activity": "Investigate the effect of temperature on enzyme action.",
    },
    "bio-amylase-ph-ix": {
        "ref": "Biology IX · Topic 6 Enzymes · activity 12",
        "activity": "Investigate the effect of pH on the action of amylase and pepsin.",
    },
    "bio-photosynthesis-ix": {
        "ref": "Biology IX · Topic 7 Bioenergetics · activity 14",
        "activity": "Perform an experiment to show the release of oxygen during photosynthesis.",
    },
    "bio-transpiration-ix": {
        "ref": "Biology IX · Topic 9 Transport · activity 19",
        "activity": "Conduct an experiment to investigate the rate of water loss at the two surfaces of leaves by using cobalt chloride paper.",
    },
    "bio-respiration-heat-ix": {
        "ref": "Biology IX · Topic 7 Bioenergetics · activity 16",
        "activity": "Set up an experiment to investigate the release of heat during aerobic respiration in germinating seeds.",
    },
    # ------------------------------------------------------------ biology X/XI
    "bio-biostatistics-x": {
        "ref": "Biology X · Topic 10 Biostatistics · activity 32",
        "activity": "Record the heights of class fellows to predict the type of variation and present the data in graphical form (histogram).",
    },
    "bio-microscope-xi": {
        "ref": "Biology XI · Topic 3 The Cell · activity 8",
        "activity": "Demonstrate microscope focusing techniques to identify the key cellular features of specimen.",
        "note": "This practical assesses the magnification and field-of-view calculations that go with focusing. A visual focusing simulation is planned for the next phase.",
    },
    "bio-food-tests-xi": {
        "ref": "Biology XI · Topic 1 Biological Molecules · activities 1–4",
        "activity": "Benedict's test for reducing sugar, iodine test for starch, emulsion test for lipids and Biuret test for proteins.",
    },
    "bio-blood-pressure-xi": {
        "ref": "Biology XI · Topic 13 Transport · activity 32",
        "activity": "Measure the blood pressure by using sphygmomanometer.",
    },
}

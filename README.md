# ECSS Verifier.

**ECSS Verifier** is an open source spacecraft systems engineering validation tool that performs automated compliance checks against ECSS (European Cooperation for Space Standardization) requirements across:
  1. Electrical
  2. Structural
  3. RF
  4. Avionics
  5. Material domains
using a **physics-aware rules engine**

It helps detect design violations, margin issues and cross domain incompatibilities early in the spacecraft development process.
___
## Features.
* ECSS rule based validation across multiple engineering domainds.
* Physics-aware unit handling using Pint.
* Structural, electrical, RF and radiation constraint checking.
* Material Property aware stress and thermal decrease analysis.
* Automated Detection of cross domain coupling issues.
* Outgassing and optical contamination risk detection.
* Clear engineering grade violation reports.
___
## Supported Domains as of v0.2
* Electrical Systems (ECSS-E-ST-20C)
* Structural Systems (ECSS-E-ST-32C)
* Avionics Systems (ECSS-E-ST-60C)
* RF Systems (ECSS-E-ST-50C)
* Material Properties and Thermal Behaviour
___
## How it works.
ECSS Verifier processes a system manifest describing spaceceaft components and evaluates them against the ECSS constraints.
Each component is:
  1. Normalized into standardizes engineering parameters.
  2. Checked against ECSS limits.
  3. Evaluated using physics-aware models.
  4. Reported with structural engineering findings.
___
## Project Structure:
engine.py: Core ECSS validation engine,
constants.py: ECSS rules, material database and mapping,
main.py: Entry point for validation,
manifest.py: System configuration input.
___
## Requirements.
  * Python 3.10+
  * Pint
___
# DISCLAIMER.
**THIS TOOL IS INTENDED FOR ENGINEERING ANALYSIS AND EDUCATIONAL PURPOSES. DO NOT REPLACE IT WITH FORMAL ECSS CERTIFICATION OR PROFESSIONAL SPACECRAFT QUALIFICATION PROCESSES.**

# ECSS Verifier Template

# This file defines a spacecraft system configuration.
# Each top level entry represents a hardware component.
#
# The ECSS Verifier reads this structure and applies:
# ECSS constraint checks
# Physics-based derating models
# Cross-domain system validation
#
# All values should use:
# Pint-compatible units (e.g. "45 volt", "350 kelvin")
# Or raw numbers where dimensionless

HARDWARE_MANIFEST = {

    # POWER / RF TRANSCEIVER UNIT

    # Represents a combined power + RF subsystem.
    # This type of component is typically sensitive to:
    # Thermal limits (ECSS-E-ST-20C)
    # Voltage derating under temperature stress
    # Current density in harness design
    "transceiver_v1": {

        # ECSS standard applied to this component
        "ecss_standard": "ECSS-E-ST-20C",

        # Material used in structural or electrical housing
        # Affects thermal degradation and mechanical retention
        "material": "Aluminum 6061-T6",

        # Maximum operating temperature
        "max_operational_temp": "350 kelvin",

        # Minimum operating temperature
        "min_operational_temp": "-10 degC",

        # Peak electrical bus voltage
        "operating_voltage_peak": "45 volt",

        # Peak current draw through harness
        "operating_current_peak": "12 ampere",

        # Wire diameter used in harness design
        # Used to compute current density and thermal overload risk
        "harness_wire_diameter": "1.2 millimeter",

        # Insulation thickness used in dielectric breakdown model
        "measured_dielectric_thickness": "0.5 millimeter"
    },


    # STRUCTURAL SUPPORT BRACKET

    # Mechanical load-bearing structure.
    # Checked for:
    # Axial stress limits
    # Shear stress limits
    # Resonance frequency constraints
    "payload_structural_bracket": {

        "ecss_standard": "ECSS-E-ST-32C",
        "material": "Titanium Grade 5",

        # Applied mechanical loads
        "applied_axial_load": "12000 newton",
        "applied_shear_stress": "180 megapascal",

        # Dynamic stability check (vibration or modal analysis)
        "resonance_frequency_measured": "28 hertz",

        # Outgassing risk flag (affects optical systems nearby)
        "max_outgassing_tml": "0.6 percent"
    },


    # HIGH POWER TELEMETRY TRANSMITTER

    # RF subsystem responsible for communication.
    # Critical checks:
    # RF output power limits
    # VSWR (antenna mismatch)
    # Thermal dissipation constraints
    "high_power_telemetry_transmitter": {

        "ecss_standard": "ECSS-E-ST-50C",

        # RF output power of transmitter
        "rf_power_output_measured": "65 watt",

        # Voltage Standing Wave Ratio (antenna mismatch indicator)
        "vswr_measured": "1.85"
    },


    # ONBOARD COMPUTER / DSP SYSTEM

    # Avionics subsystem exposed to radiation environment.
    # Checked for:
    # Total Ionizing Dose (TID)
    # Rad-hard compliance thresholds
    "onboard_computer_dsp": {

        "ecss_standard": "ECSS-E-ST-60C",

        # Radiation exposure estimate over mission lifetime
        "expected_tid_exposure": "75 kilorad",

        # Flag indicating exposure to radiation environment
        "radiation_exposed": True
    },


    # OPTICAL PAYLOAD (STAR TRACKER / CAMERA)

    # Sensitive optical subsystem.
    # Affected by:
    # Outgassing contamination
    # Line-of-sight placement from other components
    "star_tracker_lens_mount": {

        "ecss_standard": "ECSS-E-ST-32C",

        # Marks this as a sensitive optical system
        "sensitive_optical_payload": True
    }
}

# END OF MANIFEST

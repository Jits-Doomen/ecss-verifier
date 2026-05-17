import pint

ureg = pint.UnitRegistry()

try:
    ureg.define("decibelmilliwatt = 1 * milliwatt = dBm")
    ureg.define("decibelcarrier = 1 * dimensionless = dBc")
except pint.errors.RedefinedUnitError:
    pass

ECSS_REGISTRY = {
    "ECSS-E-ST-20C": {
        "revision": "C",
        "discipline": "Electrical",
        "max_operational_temp": ureg.Quantity(333.15, ureg.kelvin),
        "min_operational_temp": ureg.Quantity(253.15, ureg.kelvin),
        "max_bus_voltage": 50.0 * ureg.volt,
        "min_bus_voltage": 22.0 * ureg.volt,
        "isolation_resistance_minimum": 10.0 * ureg.megaohm,
        "max_parasitic_capacitance": 100.0 * ureg.nanofarad,
        "maximum_leakage_current": 5.0 * ureg.milliampere,
        "derating_factor_voltage": 0.75 * ureg.dimensionless,
        "derating_factor_current": 0.65 * ureg.dimensionless,
        "min_dielectric_breakdown": 500.0 * (ureg.volt / ureg.millimeter),
        "max_transient_spike_duration": 10.0 * ureg.microsecond,
        "harness_max_linear_current_density": 5.0 * (ureg.ampere / ureg.millimeter**2)
    },
    "ECSS-E-ST-32C": {
        "revision": "C",
        "discipline": "Structural",
        "max_outgassing_tml": 1.0 * ureg.percent,
        "max_outgassing_cvcm": 0.1 * ureg.percent,
        "max_outgassing_rmr": 0.1 * ureg.percent,
        "minimum_yield_margin": 1.25 * ureg.dimensionless,
        "ultimate_safety_factor": 1.5 * ureg.dimensionless,
        "maximum_shear_stress": 200.0 * ureg.megapascal,
        "maximum_axial_load": 15000.0 * ureg.newton,
        "minimum_resonance_frequency_hz": 35.0 * ureg.hertz,
        "max_thermal_expansion_coefficient": 25e-6 * (1 / ureg.kelvin),
        "fatigue_life_cycles_minimum": 100000 * ureg.dimensionless,
        "max_allowable_microstrain": 2000.0 * ureg.dimensionless
    },
    "ECSS-E-ST-60C": {
        "revision": "C",
        "discipline": "Avionics",
        "maximum_clock_frequency": 100.0 * ureg.megahertz,
        "minimum_radiation_hardness_tid": 50.0 * ureg.kilorad,
        "max_single_event_upset_rate": 1e-6 * (1 / ureg.day),
        "minimum_operating_voltage_core": 1.2 * ureg.volt,
        "maximum_power_dissipation": 15.0 * ureg.watt,
        "thermal_resistance_junction_case_max": 2.5 * (ureg.kelvin / ureg.watt),
        "latchup_immunity_let_threshold": 60.0 * ((ureg.megaelectronvolt * ureg.centimeter**2) / ureg.milligram),
        "gate_rupture_voltage_margin": 1.2 * ureg.dimensionless
    },
    "ECSS-E-ST-50C": {
        "revision": "C",
        "discipline": "RF",
        "max_rf_power_output": 50.0 * ureg.watt,
        "maximum_vswr": 1.5 * ureg.dimensionless,
        "minimum_receiver_sensitivity": ureg.Quantity(-110.0, ureg.dBm),
        "max_phase_noise_at_10kHz": ureg.Quantity(-90.0, ureg.dBc / ureg.hertz),
        "attenuation_harmonics_minimum": ureg.Quantity(40.0, ureg.dBc),
        "link_budget_margin_minimum": ureg.Quantity(3.0, ureg.decibel)
    }
}

MATERIAL_DB = {
    "Aluminum 6061-T6": {
        "density": 2.7 * (ureg.gram / ureg.centimeter**3),
        "thermal_conductivity": 167.0 * (ureg.watt / (ureg.meter * ureg.kelvin)),
        "yield_strength_baseline": 276.0 * ureg.megapascal,
        "ultimate_strength_baseline": 310.0 * ureg.megapascal,
        "shear_strength_baseline": 207.0 * ureg.megapascal,
        "elastic_modulus": 68.9 * ureg.gigapascal,
        "poissons_ratio": 0.33 * ureg.dimensionless,
        "cte": 23.0e-6 * (1 / ureg.kelvin),
        "thermal_degradation_start": ureg.Quantity(65.0, ureg.degC),
        "thermal_degradation_factor": 0.0025 * (1 / ureg.delta_degC),
        "vacuum_outgassing_susceptibility": True
    },
    "Titanium Grade 5": {
        "density": 4.43 * (ureg.gram / ureg.centimeter**3),
        "thermal_conductivity": 6.7 * (ureg.watt / (ureg.meter * ureg.kelvin)),
        "yield_strength_baseline": 880.0 * ureg.megapascal,
        "ultimate_strength_baseline": 950.0 * ureg.megapascal,
        "shear_strength_baseline": 550.0 * ureg.megapascal,
        "elastic_modulus": 113.8 * ureg.gigapascal,
        "poissons_ratio": 0.34 * ureg.dimensionless,
        "cte": 8.6e-6 * (1 / ureg.kelvin),
        "thermal_degradation_start": ureg.Quantity(150.0, ureg.degC),
        "thermal_degradation_factor": 0.0012 * (1 / ureg.delta_degC),
        "vacuum_outgassing_susceptibility": False
    },
    "CFRP_Composite": {
        "density": 1.6 * (ureg.gram / ureg.centimeter**3),
        "thermal_conductivity": 4.5 * (ureg.watt / (ureg.meter * ureg.kelvin)),
        "yield_strength_baseline": 600.0 * ureg.megapascal,
        "ultimate_strength_baseline": 900.0 * ureg.megapascal,
        "shear_strength_baseline": 90.0 * ureg.megapascal,
        "elastic_modulus": 135.0 * ureg.gigapascal,
        "poissons_ratio": 0.28 * ureg.dimensionless,
        "cte": 0.5e-6 * (1 / ureg.kelvin),
        "thermal_degradation_start": ureg.Quantity(80.0, ureg.degC),
        "thermal_degradation_factor": 0.004 * (1 / ureg.delta_degC),
        "vacuum_outgassing_susceptibility": True
    },
    "Invar 36": {
        "density": 8.1 * (ureg.gram / ureg.centimeter**3),
        "thermal_conductivity": 13.9 * (ureg.watt / (ureg.meter * ureg.kelvin)),
        "yield_strength_baseline": 240.0 * ureg.megapascal,
        "ultimate_strength_baseline": 490.0 * ureg.megapascal,
        "shear_strength_baseline": 150.0 * ureg.megapascal,
        "elastic_modulus": 144.0 * ureg.gigapascal,
        "poissons_ratio": 0.29 * ureg.dimensionless,
        "cte": 1.2e-6 * (1 / ureg.kelvin),
        "thermal_degradation_start": ureg.Quantity(200.0, ureg.degC),
        "thermal_degradation_factor": 0.0008 * (1 / ureg.delta_degC),
        "vacuum_outgassing_susceptibility": False
    }
}

FUZZY_MAP = {
    "temp": "max_operational_temp",
    "temperature": "max_operational_temp",
    "max_temp": "max_operational_temp",
    "operational_temperature": "max_operational_temp",
    "thermal_ceiling": "max_operational_temp",
    "voltage": "operating_voltage_peak",
    "max_voltage": "operating_voltage_peak",
    "voltage_peak": "operating_voltage_peak",
    "bus_voltage": "operating_voltage_peak",
    "tml": "max_outgassing_tml",
    "total_mass_loss": "max_outgassing_tml",
    "outgassing": "max_outgassing_tml",
    "cvcm": "max_outgassing_cvcm",
    "collected_volatile": "max_outgassing_cvcm",
    "axial": "applied_axial_load",
    "axial_load": "applied_axial_load",
    "load_force": "applied_axial_load",
    "shear": "applied_shear_stress",
    "shear_stress": "applied_shear_stress",
    "frequency": "resonance_frequency_measured",
    "freq": "resonance_frequency_measured",
    "structural_frequency": "resonance_frequency_measured",
    "tid": "expected_tid_exposure",
    "radiation": "expected_tid_exposure",
    "total_ionizing_dose": "expected_tid_exposure",
    "rf_power": "rf_power_output_measured",
    "transmit_power": "rf_power_output_measured",
    "vswr": "vswr_measured",
    "standing_wave_ratio": "vswr_measured",
    "current": "operating_current_peak",
    "max_current": "operating_current_peak",
    "current_peak": "operating_current_peak",
    "wire_diameter": "harness_wire_diameter",
    "cable_diameter": "harness_wire_diameter",
    "dielectric": "measured_dielectric_thickness",
    "insulation": "measured_dielectric_thickness"
}

VALID_PARAMETER_KEYS = {
    "ecss_standard", "material", "sensitive_optical_payload", "radiation_exposed", "external_facing_harness",
    "max_operational_temp", "min_operational_temp", "max_bus_voltage", "min_bus_voltage",
    "isolation_resistance_minimum", "max_parasitic_capacitance", "maximum_leakage_current",
    "derating_factor_voltage", "derating_factor_current", "max_outgassing_tml",
    "max_outgassing_cvcm", "max_outgassing_rmr", "minimum_yield_margin", "ultimate_safety_factor",
    "maximum_shear_stress", "maximum_axial_load", "minimum_resonance_frequency_hz",
    "maximum_clock_frequency", "minimum_radiation_hardness_tid", "max_single_event_upset_rate",
    "minimum_operating_voltage_core", "maximum_power_dissipation", "applied_axial_load",
    "applied_shear_stress", "operating_voltage_peak", "operating_current_peak",
    "expected_tid_exposure", "resonance_frequency_measured", "rf_power_output_measured",
    "vswr_measured", "harness_wire_diameter", "measured_dielectric_thickness",
    "thermal_resistance_junction_case_max", "latchup_immunity_let_threshold",
    "gate_rupture_voltage_margin", "max_phase_noise_at_10kHz",
    "attenuation_harmonics_minimum", "link_budget_margin_minimum"
}
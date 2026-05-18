import pint
import math
import re
from constants import ureg, ECSS_REGISTRY, MATERIAL_DB, FUZZY_MAP, VALID_PARAMETER_KEYS

class IntelligentECSSLinter:
    def __init__(self):
        self.registry = ECSS_REGISTRY
        self.materials = MATERIAL_DB
        self.fuzzy_resolver = FUZZY_MAP
        self.valid_keys = VALID_PARAMETER_KEYS

    def _normalize_quantity(self, raw_value) -> pint.Quantity:
        if isinstance(raw_value, pint.Quantity):
            return raw_value
        if isinstance(raw_value, (int, float)):
            return raw_value * ureg.dimensionless

        cleaned = str(raw_value).strip()
        match = re.match(r"^([+-]?\d*(?:\.\d+)?)(.*)$", cleaned)
        if match:
            num_part, unit_part = match.groups()
            unit_part = unit_part.strip()
            if num_part and unit_part:
                cleaned = f"{num_part} {unit_part}"

        try:
            return ureg(cleaned)
        except Exception:
            raise ValueError(f"Unit Parsing Framework Fault: Token sequence structural mapping failure: '{cleaned}'")

    def _resolve_key(self, user_key: str) -> str:
        normalized = user_key.strip().lower().replace(" ", "_").replace("-", "_")
        return self.fuzzy_resolver.get(normalized, normalized)

    def _get_floats(self, q1: pint.Quantity, q2: pint.Quantity):
        if q1.check('[temperature]'):
            return q1.to(ureg.kelvin).magnitude, q2.to(ureg.kelvin).magnitude
        return q1.to(q2.units).magnitude, q2.magnitude

    def _build_finding(self, component, parameter, standard, error, recommendation, severity="HIGH"):
        return {
            "component": component,
            "parameter": parameter,
            "severity": severity,
            "standard": standard,
            "error": error,
            "recommendation": recommendation
        }

    def _execute_structural_physics_checks(self, name: str, data: dict, retention: float, qt, anomalies: list):
        mat = data.get("material")
        raw_margin = data.get("minimum_yield_margin")
        raw_axial = data.get("applied_axial_load")
        raw_shear = data.get("applied_shear_stress")
        raw_freq = data.get("resonance_frequency_measured")

        severity_level = "WAIVED_STRUCTURAL" if "waiver" in data else "HIGH"

        if retention < 1.0 and mat in self.materials:
            m_props = self.materials[mat]
            if raw_margin:
                try:
                    qm = self._normalize_quantity(raw_margin).magnitude
                    baseline_req = self.registry["ECSS-E-ST-32C"]["minimum_yield_margin"].magnitude
                    dynamic_req = baseline_req / retention
                    if qm < dynamic_req:
                        anomalies.append(self._build_finding(name, "minimum_yield_margin [THERMAL-STRUCTURAL GRADIENT]", "ECSS-E-ST-32C", f"Mechanical reliability degradation under thermal loading. Required margin {dynamic_req:.4f}, measured {qm}.", f"Waiver active: {data.get('waiver')}" if "waiver" in data else "Increase structural safety factor or reduce thermal loading.", severity_level))
                except Exception:
                    pass

            if raw_axial:
                try:
                    qa = self._normalize_quantity(raw_axial)
                    base_axial_limit = self.registry["ECSS-E-ST-32C"]["maximum_axial_load"]
                    ax_limit = base_axial_limit * retention
                    au, al = self._get_floats(qa, ax_limit)
                    if au > al:
                        anomalies.append(self._build_finding(name, "applied_axial_load [THERMAL-STRUCTURAL OVERLOAD]", "ECSS-E-ST-32C", f"Structural load {qa} exceeds thermal derated limit {ax_limit}.", f"Waiver active: {data.get('waiver')}" if "waiver" in data else "Reduce axial load or increase material margin.", severity_level))
                except Exception:
                    pass

            if raw_shear:
                try:
                    qs = self._normalize_quantity(raw_shear)
                    mat_shear_baseline = m_props["shear_strength_baseline"]
                    ecss_shear_limit = self.registry["ECSS-E-ST-32C"]["maximum_shear_stress"]
                    resolved_limit = min(mat_shear_baseline.to(ecss_shear_limit.units).magnitude, ecss_shear_limit.magnitude) * ecss_shear_limit.units
                    dynamic_shear_limit = resolved_limit * retention
                    su, sl = self._get_floats(qs, dynamic_shear_limit)
                    if su > sl:
                        anomalies.append(self._build_finding(name, "applied_shear_stress [THERMAL-SHEAR INTEGRITY]", "ECSS-E-ST-32C", f"Shear stress {qs} exceeds thermal derated limit {dynamic_shear_limit}.", f"Waiver active: {data.get('waiver')}" if "waiver" in data else "Increase section thickness or reduce transverse load.", severity_level))
                except Exception:
                    pass

        if raw_freq:
            try:
                qf = self._normalize_quantity(raw_freq)
                f_limit = self.registry["ECSS-E-ST-32C"]["minimum_resonance_frequency_hz"]
                fu, fl = self._get_floats(qf, f_limit)
                if fu < fl:
                    anomalies.append(self._build_finding(name, "resonance_frequency_measured [HARMONIC MODAL ANALYSIS]", "ECSS-E-ST-32C", f"Measured resonance frequency {qf} below minimum {f_limit}.", f"Waiver active: {data.get('waiver')}" if "waiver" in data else "Increase structural stiffness or reduce distributed mass.", severity_level))
            except Exception:
                pass

    def _execute_electrical_physics_checks(self, name: str, data: dict, std: str, qt, anomalies: list):
        raw_voltage = data.get("operating_voltage_peak")
        raw_current = data.get("operating_current_peak")
        raw_harness_diam = data.get("harness_wire_diameter")
        raw_dielectric = data.get("measured_dielectric_thickness")

        severity_level = "WAIVED_ELECTRICAL" if "waiver" in data else "HIGH"

        if std == "ECSS-E-ST-20C":
            base_v_limit = self.registry["ECSS-E-ST-20C"]["max_bus_voltage"]
            factor = self.registry["ECSS-E-ST-20C"]["derating_factor_voltage"].magnitude

            if qt:
                try:
                    tu, tl = self._get_floats(qt, ureg.Quantity(313.15, ureg.kelvin))
                    if tu > tl:
                        factor *= 0.80
                except Exception:
                    pass

            if raw_voltage:
                try:
                    qv = self._normalize_quantity(raw_voltage)
                    vu, vl = self._get_floats(qv, base_v_limit * factor)
                    if vu > vl:
                        anomalies.append(self._build_finding(name, "operating_voltage_peak [THERMAL-ELECTRICAL DERATING]", "ECSS-E-ST-20C", f"Voltage {qv} exceeds derated limit {base_v_limit * factor}.", f"Waiver active: {data.get('waiver')}" if "waiver" in data else "Reduce bus voltage or redesign power stage.", severity_level))
                except Exception:
                    pass

            if raw_current and raw_harness_diam:
                try:
                    qi = self._normalize_quantity(raw_current)
                    qd = self._normalize_quantity(raw_harness_diam)
                    area = math.pi * (qd.to(ureg.millimeter).magnitude / 2.0)**2 * ureg.millimeter**2
                    current_density = qi.to(ureg.ampere) / area
                    density_limit = self.registry["ECSS-E-ST-20C"]["harness_max_linear_current_density"]
                    cu, cl = self._get_floats(current_density, density_limit)
                    if cu > cl:
                        anomalies.append(self._build_finding(name, "operating_current_peak [HARNESS THERMAL OVERLOAD]", "ECSS-E-ST-20C", f"Harness current density {current_density:.4f} exceeds allowable limit {density_limit}.", f"Waiver active: {data.get('waiver')}" if "waiver" in data else "Increase conductor diameter or reduce current.", severity_level))
                except Exception:
                    pass

            if raw_voltage and raw_dielectric:
                try:
                    qv = self._normalize_quantity(raw_voltage)
                    qthick = self._normalize_quantity(raw_dielectric)
                    dielectric_stress = qv.to(ureg.volt) / qthick.to(ureg.millimeter)
                    breakdown_limit = self.registry["ECSS-E-ST-20C"]["min_dielectric_breakdown"]
                    du, dl = self._get_floats(dielectric_stress, breakdown_limit)
                    if du > dl:
                        anomalies.append(self._build_finding(name, "measured_dielectric_thickness [INSULATION ARCDOWN]", "ECSS-E-ST-20C", f"Dielectric stress {dielectric_stress:.2f} exceeds limit {breakdown_limit}.", f"Waiver active: {data.get('waiver')}" if "waiver" in data else "Increase insulation thickness or reduce voltage.", severity_level))
                except Exception:
                    pass

    def _execute_rf_physics_checks(self, name: str, data: dict, std: str, anomalies: list):
        raw_rf_pow = data.get("rf_power_output_measured")
        raw_vswr = data.get("vswr_measured")

        severity_level = "WAIVED_RF" if "waiver" in data else "HIGH"

        if std == "ECSS-E-ST-50C":
            if raw_rf_pow:
                try:
                    qrf = self._normalize_quantity(raw_rf_pow)
                    rf_limit = self.registry["ECSS-E-ST-50C"]["max_rf_power_output"]
                    rfu, rfl = self._get_floats(qrf, rf_limit)
                    if rfu > rfl:
                        anomalies.append(self._build_finding(name, "rf_power_output_measured [RF AMPLIFIER BLOWOUT]", "ECSS-E-ST-50C", f"RF power {qrf} exceeds limit {rf_limit}.", f"Waiver active: {data.get('waiver')}" if "waiver" in data else "Reduce output power or improve thermal dissipation.", severity_level))
                except Exception:
                    pass

            if raw_vswr:
                try:
                    qvswr = self._normalize_quantity(raw_vswr).magnitude
                    vswr_limit = self.registry["ECSS-E-ST-50C"]["maximum_vswr"].magnitude
                    if qvswr > vswr_limit:
                        reflected_power_pct = (((qvswr - 1) / (qvswr + 1))**2) * 100.0
                        anomalies.append(self._build_finding(name, "vswr_measured [ANTENNA IMPEDANCE MISMATCH]", "ECSS-E-ST-50C", f"VSWR {qvswr} reflects {reflected_power_pct:.2f}% power back into transmitter.", f"Waiver active: {data.get('waiver')}" if "waiver" in data else "Retune antenna matching network.", severity_level))
                except Exception:
                    pass

    def analyze_system(self, system_manifest: dict) -> list:
        anomalies = []
        high_outgassers = []
        optical_nodes = []

        if not isinstance(system_manifest, dict):
            return [self._build_finding("GLOBAL_MANIFEST", "Schema Configuration Root", "SCHEMA", "System architecture root must be a dictionary.", "Correct manifest root object.")]

        normalized_components = {}
        for c_name, c_data in system_manifest.items():
            if not isinstance(c_data, dict):
                anomalies.append(self._build_finding(c_name, "Component Structural Layout", "SCHEMA", f"Hardware config block for '{c_name}' must be a dictionary.", "Correct component manifest schema."))
                continue

            normalized_components[c_name] = {self._resolve_key(k): v for k, v in c_data.items()}

        for name, data in normalized_components.items():
            for k in data.keys():
                if k not in self.valid_keys:
                    anomalies.append(self._build_finding(name, k, "SCHEMA", f"Field '{k}' is unrecognized by system schemas.", "Rename or remove unsupported field.", "MEDIUM"))

            std = data.get("ecss_standard")
            mat = data.get("material")
            severity_level = "WAIVED_STANDARD" if "waiver" in data else "HIGH"

            if not std or std not in self.registry:
                continue

            rules = self.registry[std]

            for key, raw_val in data.items():
                if key in ["ecss_standard", "material", "sensitive_optical_payload", "radiation_exposed", "external_facing_harness", "waiver"] or key not in rules:
                    continue

                try:
                    q_user = self._normalize_quantity(raw_val)
                    q_limit = rules[key]

                    if not isinstance(q_limit, pint.Quantity):
                        continue

                    if q_user.dimensionality != q_limit.dimensionality:
                        anomalies.append(self._build_finding(name, key, std, f"Dimensionality mismatch: {q_user.units} vs {q_limit.units}.", "Correct engineering units.", severity_level))
                        continue

                    val_u, val_l = self._get_floats(q_user, q_limit)

                    if "max_" in key or "maximum_" in key:
                        if val_u > val_l:
                            anomalies.append(self._build_finding(name, key, std, f"Measured value {q_user} exceeds limit {q_limit}.", f"Waiver active: {data.get('waiver')}" if "waiver" in data else "Reduce operational load.", severity_level))
                    elif "min_" in key or "minimum_" in key:
                        if val_u < val_l:
                            anomalies.append(self._build_finding(name, key, std, f"Measured value {q_user} below minimum {q_limit}.", f"Waiver active: {data.get('waiver')}" if "waiver" in data else "Increase engineering margin.", severity_level))
                except Exception as e:
                    anomalies.append(self._build_finding(name, key, std, f"Internal mapping failure: {str(e)}", "Inspect parameter formatting.", severity_level))

            raw_t = data.get("max_operational_temp")
            raw_tml = data.get("max_outgassing_tml")
            raw_tid = data.get("expected_tid_exposure")

            retention = 1.0
            qt = None
            if mat in self.materials and raw_t:
                try:
                    qt = self._normalize_quantity(raw_t)
                    m_props = self.materials[mat]
                    tu, tl = self._get_floats(qt, m_props["thermal_degradation_start"])
                    if tu > tl:
                        retention = 1.0 - ((tu - tl) * m_props["thermal_degradation_factor"].magnitude)
                        retention = max(0.01, min(1.0, retention))
                except Exception:
                    pass

            self._execute_structural_physics_checks(name, data, retention, qt, anomalies)
            self._execute_electrical_physics_checks(name, data, std, qt, anomalies)
            self._execute_rf_physics_checks(name, data, std, anomalies)

            if raw_tml:
                try:
                    qtml = self._normalize_quantity(raw_tml)
                    if qtml.to(ureg.percent).magnitude > 0.5:
                        high_outgassers.append(name)
                except Exception:
                    pass

            if data.get("sensitive_optical_payload"):
                optical_nodes.append(name)

            if data.get("radiation_exposed") and raw_tid:
                try:
                    qtid = self._normalize_quantity(raw_tid)
                    tid_limit = rules.get("minimum_radiation_hardness_tid", 50.0 * ureg.kilorad)
                    t_u, t_l = self._get_floats(qtid, tid_limit)
                    if t_u > t_l:
                        anomalies.append(self._build_finding(name, "expected_tid_exposure", "ECSS-E-ST-60C", f"Radiation exposure {qtid} exceeds silicon tolerance {tid_limit}.", f"Waiver active: {data.get('waiver')}" if "waiver" in data else "Increase shielding or use rad-hard components.", severity_level))
                except Exception:
                    pass

        if high_outgassers and optical_nodes:
            spatial_waiver = False
            for node in high_outgassers + optical_nodes:
                if "waiver" in normalized_components.get(node, {}):
                    spatial_waiver = True
            anomalies.append(self._build_finding("System Deployment Geometry Layout", "Outgassing Molecular Cross Contamination", "ECSS-E-ST-32C", f"Outgassing nodes {high_outgassers} have line of sight to optical payloads {optical_nodes}.", "Baffle mitigation documented via active system waiver status." if spatial_waiver else "Add baffling or relocate components.", "WAIVED_GEOMETRY" if spatial_waiver else "HIGH"))

        return anomalies

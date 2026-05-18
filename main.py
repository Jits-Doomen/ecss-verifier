import sys
from engine import IntelligentECSSLinter
from manifest import HARDWARE_MANIFEST

def run():
    engine = IntelligentECSSLinter()
    violations = engine.analyze_system(HARDWARE_MANIFEST)

    print("ECSS Verifier (v0.2)")

    blocking_violations = [v for v in violations if "WAIVED" not in v.get("severity", "")]

    if not violations:
        print("\nVerification passed. No engineering violations detected.\n")
        sys.exit(0)
    else:
        print(f"\n(Verification Report) System validation pipeline cataloged {len(violations)} total design manifestations:\n")
        for idx, error in enumerate(violations, start=1):
            print(f" Anomalous System Trace Node [{idx}]:")
            print(f" Target Component Subsystem: {error['component']}")
            print(f" Interface Metadata Channel: {error['parameter']}")
            print(f" Severity Level: {error.get('severity', 'HIGH')}")
            print(f" Standards Reference: {error.get('standard', 'ECSS')}")
            print(f" Engineering Finding: {error['error']}")
            print(f" Recommended Corrective Action: {error.get('recommendation', 'Engineering review required')}")

        if blocking_violations:
            print(f"\nVerification failed. Pipeline halted by {len(blocking_violations)} un-waived engineering violations.\n")
            sys.exit(2)
        else:
            print("\n(Verification Succeeded with Warnings) All detected anomalies contain valid engineering waivers. Context thread clear.\n")
            sys.exit(0)

if __name__ == "__main__":
    run()

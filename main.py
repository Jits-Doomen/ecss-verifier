import sys
from engine import IntelligentECSSLinter
from manifest import HARDWARE_MANIFEST

def run():
    engine = IntelligentECSSLinter()
    violations = engine.analyze_system(HARDWARE_MANIFEST)

    print("ESA / ECSS Ground Control Mission Systems Engineering Integrity Multi Physics Node Verification Platform")

    if not violations:
        print("\n(Verification Succeeded) Zero system configuration errors or derived stress anomalies were detected inside the execution context thread.\n")
        sys.exit(0)
    else:
        print(f"\n(Verification Failed) System validation pipeline caught {len(violations)} deep architectural anomalies or design cross coupling failures:\n")
        for idx, error in enumerate(violations, start=1):
            print(f" Anomalous System Trace Node [{idx}]:")
            print(f" Target Component Subsystem: {error['component']}")
            print(f" Interface Metadata Channel: {error['parameter']}")
            print(f" Severity Level: {error.get('severity', 'HIGH')}")
            print(f" Standards Reference: {error.get('standard', 'ECSS')}")
            print(f" Engineering Finding: {error['error']}")
            print(f" Recommended Corrective Action: {error.get('recommendation', 'Engineering review required')}")
        sys.exit(2)

if __name__ == "__main__":
    run()

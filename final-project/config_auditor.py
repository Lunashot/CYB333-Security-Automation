"""Check a fictional test rack configuration against a security baseline."""

import json
import sys
from datetime import datetime
from pathlib import Path


EXPECTED_TYPES = {
    "software_version": str,
    "logging_enabled": bool,
    "default_accounts_enabled": bool,
    "remote_access": str,
}


def load_json(file_name):
    """Open a JSON file and return its contents."""
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


def check_configuration(configuration, baseline):
    """Compare the configuration settings with the approved values."""
    results = []
    approved_settings = baseline["required_settings"]

    for setting, expected_value in approved_settings.items():
        if setting not in configuration:
            status = "FAIL"
            observed_value = None
            message = "The required setting is missing."
        elif type(configuration[setting]) is not EXPECTED_TYPES[setting]:
            status = "FAIL"
            observed_value = configuration[setting]
            message = "The setting has an invalid data type."
        elif configuration[setting] == expected_value:
            status = "PASS"
            observed_value = configuration[setting]
            message = "The setting matches the baseline."
        else:
            status = "FAIL"
            observed_value = configuration[setting]
            message = "The setting does not match the baseline."

        results.append(
            {
                "setting": setting,
                "status": status,
                "expected": expected_value,
                "observed": observed_value,
                "message": message,
            }
        )

    return results


def print_results(rack_name, results):
    """Display the audit results in the terminal."""
    print(f"\nConfiguration audit for {rack_name}")
    print("-" * 50)

    for result in results:
        print(f"{result['setting']}: {result['status']}")
        print(f"  Expected: {result['expected']}")
        print(f"  Observed: {result['observed']}")
        print(f"  {result['message']}")


def save_report(rack_name, results):
    """Save the audit results in the reports folder."""
    passed = sum(result["status"] == "PASS" for result in results)
    overall_status = "PASS" if passed == len(results) else "FAIL"

    report = {
        "rack_name": rack_name,
        "audit_time": datetime.now().isoformat(timespec="seconds"),
        "overall_status": overall_status,
        "passed_checks": passed,
        "failed_checks": len(results) - passed,
        "results": results,
    }

    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)
    report_path = reports_folder / "audit_report.json"

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print("-" * 50)
    print(f"Overall status: {overall_status}")
    print(f"Report saved to {report_path}")


def main():
    """Load the files, run the checks, and create the report."""
    if len(sys.argv) != 2:
        print("Usage: python3 config_auditor.py <configuration_file>")
        return 1

    try:
        configuration = load_json(sys.argv[1])
        baseline = load_json("baseline.json")
        results = check_configuration(configuration, baseline)
        rack_name = configuration.get("rack_name", "Unknown rack")
        print_results(rack_name, results)
        save_report(rack_name, results)
    except FileNotFoundError as error:
        print(f"File error: {error}")
        return 1
    except json.JSONDecodeError as error:
        print(f"JSON error: {error}")
        return 1
    except (KeyError, TypeError) as error:
        print(f"Configuration error: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

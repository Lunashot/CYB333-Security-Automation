# Simulated Test Rack Configuration Auditor

## Project Description

This project is a small Python program that checks a fictional test rack configuration against an approved security baseline. It was inspired by equipment support work, but it does not connect to any real company systems or use confidential information. The program only reads the configuration and reports its findings.

The program checks whether:

- The software version is approved
- Logging is enabled
- Default accounts are disabled
- Remote access is restricted

For each setting, the program shows a pass or fail result and explains what it found. It also saves the results in a JSON report.

## Project Files

- `config_auditor.py` - the main Python program
- `baseline.json` - the approved settings
- `samples/` - fictional configurations used to test the program
- `reports/` - the location where the audit report is saved

## Requirements

- Python 3.10 or newer
- No extra packages are required
- No API keys are used

## How to Run the Program

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run one of the following commands:

```bash
python3 config_auditor.py samples/compliant_rack.json
```

```bash
python3 config_auditor.py samples/noncompliant_rack.json
```

The program displays the result in the terminal and saves the latest result as `reports/audit_report.json`.

## Sample Configurations

Four fictional samples are included:

- `compliant_rack.json` passes all checks
- `noncompliant_rack.json` contains settings that do not match the baseline
- `missing_setting_rack.json` is missing a required setting
- `invalid_type_rack.json` uses the wrong data type for a setting

You can test any sample by replacing the file name in the run command.

## Security and Privacy

All names, settings, and values in this repository are fictional. The project does not include passwords, API keys, company code, or real equipment data.

## Limitations

This is a classroom demonstration. It checks four predefined settings in local JSON files and does not make changes to a system.

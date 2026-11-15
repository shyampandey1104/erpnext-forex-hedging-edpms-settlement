# ERPNext RBI EDPMS/IDPMS Settlement & Forex Hedging Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![RBI](https://img.shields.io/badge/RBI-EDPMS%20%2F%20IDPMS%20Compliant-darkblue.svg)](https://rbi.org.in)

Cross-border trade finance engine addressing Reserve Bank of India (RBI) Export Data Processing and Monitoring System (EDPMS) statutory 9-month realization mandates and Ind AS 21 Foreign Exchange Realization Ledgers.

## Features
- **EDPMS Realization Timers:** 270-day statutory tracking preventing RBI caution-listing penalties.
- **SWIFT FIRC Multi-Bill Allocation:** Matches international inwards remittances against partial container shipments.
- **Ind AS 21 Forex Accounting:** Computes realized foreign exchange gain/loss against booking date reference rates.

## Tests
```bash
python3 -m unittest discover tests
```

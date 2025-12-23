# Wireless Sensor Network

Designed by:
- Amalia Magana (IR-SC)
- Anya Meetoo (IR-SI)
- Célian Hilal Hamdan (IR-SC)
- Jean-Philippe Loubejac--Combalbert (IR-SI)
- Julie Revelli (AE-SE)
- Marie-Line Da Costa Bento (IR-SC)

This repository contains the PHY and MAC components used to prototype a simple wireless sensor network, including GNU Radio Companion flowgraphs for simulation and USRP-based tests, plus embedded-python MAC blocks for framing and decoding.

## Repository Structure

- `mac/`
  - `random_mac_generator.py`: GNU Radio embedded Python block that generates valid MAC frames with randomized payload (address, cow id, lat/lon/alt) and CRC32.
  - `mac_decoder.py`: GNU Radio embedded Python block that decodes frames, verifies CRC32, and prints parsed fields.
- `phy/`
  - `simu_modulation_and_demodulation.grc`: End-to-end simulation flowgraph (modulation + demodulation) in GNU Radio Companion.
  - `ursp_modulation.grc`: USRP sender flowgraph for on-air transmission.
  - `usrp_demodulation.grc`: USRP receiver flowgraph for on-air demodulation.
## Prerequisites

- GNU Radio 3.10+ with Qt GUI support
- UHD drivers (for USRP hardware)
- Python 3.8+
- PyQt5 (when running the Python flowgraph)

Example install (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install gnuradio uhd-host
python3 -m pip install --user PyQt5 packaging
```


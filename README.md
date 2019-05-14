
# Wifi Deauth Tester

## The Warning

**If you don't want to experience a long stretch in a jail cell, DO NOT use this on any network without permission**. This utility is built for testing and educational purposes and is not meant to be used on any network you do not own or have permission to deauth. Don't be stupid and if you are stupid, don't say I didn't warn you.

## Requirements

- Python 2.7
- Wifi card **in monitor mode** that supports packet injection
- Linux(tested on Ubuntu 19.04 and Kali)

## Usage
- \--bssid - BSSID of the Access Point you want to target
- \--channel - Channel the Access Point is running on
- \--interface - Network Interface you want to use
- \--target - (Optional)Specify single target to attack

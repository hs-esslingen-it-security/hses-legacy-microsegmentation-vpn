## Test Data

The test data used in this project is sourced from the SWaT trace **SWaT.A6_Dec 2019** (`Dec2019_00000_20191206100500.pcap`).

### Pre-processing

The pre-processing steps are executed using the `preprocess.sh` script. The key steps are as follows:

- **Traffic Filtering**: Filter traffic related to PLCs and SCADA, extract the first 50,000 packets (file size limitations) and save them to `dump.pcap` (used in Docker network).

- **Flow Analysis**: The result of the flow analysis is saved in to `filtered_flows.csv`.
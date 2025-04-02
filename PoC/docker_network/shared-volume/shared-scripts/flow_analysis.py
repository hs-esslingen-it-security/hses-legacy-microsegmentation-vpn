import pandas as pd
from nfstream import NFStreamer, NFPlugin

########################
# aggregate flows
########################

# NFPlugins for Industrial Communication
class EthernetIP(NFPlugin):
    def on_init(self, packet, flow):
        # Check if the packet is UDP and the port is 2222
        return packet.protocol == 17 and packet.dst_port == 2222 #  I/O over EtherNet/IP
    def on_expire(self, flow):
        if EthernetIP:
            flow.application_name = "EthernetIP"  # Override app name
            flow.application_category_name = "Network"  # Override app category

# my_dataframe = my_streamer.to_pandas(columns_to_anonymize=[])
def parse_dump(input_pcap, output_csv):
    """
    Parses a network dump file and extracts communication flows (store as csv)
    """
    
    my_streamer = NFStreamer(source=input_pcap,  # or live network interface
                             udps=EthernetIP(volatile=True))
    total_flows = my_streamer.to_csv(path=output_csv)
    df_flows = my_streamer.to_pandas(columns_to_anonymize=[])

    return df_flows

if __name__ == "__main__":
    df_flows = parse_dump(input_pcap="../shared-pcaps/dump.pcap", output_csv="../shared-pcaps/flows.csv")
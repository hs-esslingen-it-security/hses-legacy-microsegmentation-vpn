import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

########################
# derive segments
########################

# definition for host_level / segmentation_level segmentation
def host_level_segmentation(ip, df_flows):
    df_ip = df_flows[(df_flows['src_ip'] == ip) | (df_flows['dst_ip'] == ip)]
    df_host_level = pd.concat([df_ip['src_ip'], df_ip['dst_ip']]).drop_duplicates().reset_index(drop=True) # filter unique hosts
    df_host_level = df_host_level[df_host_level != ip].to_frame(name="ip") # filter out self

    # sort and print
    df_host_level = df_host_level.sort_values(by=["ip"], key=lambda x: x.str.split(".").apply(lambda y: [int(z) for z in y]))

    logging.info(f"Unique Host-level Communication Flows for {ip}:\n{df_host_level.to_string(index=False)}\n")
    return df_host_level


def application_level_segmentation(ip, df_flows):
    df_ip = df_flows[(df_flows['src_ip'] == ip) | (df_flows['dst_ip'] == ip)]

    df_selected = df_ip[["src_ip", "dst_ip", "src_port", "dst_port", "protocol", "src2dst_packets", "dst2src_packets", "application_name"]].drop_duplicates() 
    df_grouped = df_selected.groupby(["src_ip", "dst_ip", "src_port", "dst_port", "protocol", "application_name"]).agg({
        "src2dst_packets": "sum",   # Summing packets from src to dst
        "dst2src_packets": "sum"    # Summing packets from dst to src
    }).reset_index()
    df_grouped["bi-directional"] = df_grouped["dst2src_packets"] > 0
    df_grouped["src_port"] = df_grouped["src_port"].apply(lambda x: None if x > 49152 else x)
    df_grouped["dst_port"] = df_grouped["dst_port"].apply(lambda x: None if x > 49152 else x)
    df_grouped = df_grouped.astype({"src_port": "Int64", "dst_port": "Int64"})


    df_app_level = df_grouped[['src_ip', 'dst_ip', 'src_port', 'dst_port', 'protocol', 'application_name', 'bi-directional']].drop_duplicates() 
    df_app_level = df_app_level.sort_values(by=["src_ip"], key=lambda x: x.str.split(".").apply(lambda y: [int(z) for z in y]))

    logging.info(f"Unique Application-level Communication Flows for {ip}:\n{df_app_level.to_string(index=False)}\n")
    return df_app_level
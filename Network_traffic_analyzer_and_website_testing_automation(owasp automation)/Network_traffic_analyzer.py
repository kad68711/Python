import sys
import logging
from scapy.all import *
import pandas as pd
from tabulate import tabulate
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)



def plot_all_graphs(protocol_counts, ip_communication_protocols):
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))  # Create a figure with 2 subplots

      # Integrate protocol distribution bar plot
    bars=axes[0].bar(protocol_counts["Protocol"], protocol_counts["Percentage"], color='skyblue')
    axes[0].set_title('Protocol Distribution')
    axes[0].set_xlabel('Protocol')
    axes[0].set_ylabel('Percentage')
    axes[0].tick_params(axis='x', rotation=45)

     # Annotate each bar with its percentage value
    for bar, percentage in zip(bars, protocol_counts["Percentage"]):
        axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f'{percentage:.2f}%', ha='center', va='bottom')

     # Set xticks and xticklabels
    protocol_names = protocol_counts["Protocol"]
    axes[0].set_xticks(range(len(protocol_names)))
    axes[0].set_xticklabels(protocol_names)



    # Plot share of protocols between IPs
    colors = plt.cm.tab20.colors  # Color palette
    for i, (protocol, group) in enumerate(ip_communication_protocols.groupby('Protocol')):
        axes[1].scatter(group['Source IP'], group['Destination IP'], s=group['Percentage']*2, label=protocol, color=colors[i], alpha=0.8)  # Adjust alpha value here
    axes[1].set_title('Share of Each Protocol Between IPs')
    axes[1].set_xlabel('Source IP')
    axes[1].set_ylabel('Destination IP')
    axes[1].legend(title='Protocol', bbox_to_anchor=(1.05, 1), loc='upper left')
    axes[1].tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)  # Hide both axes

    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show(block=False)


def read_pcap(pcap_file):
    try:
        packets = rdpcap(pcap_file)
    except FileNotFoundError:
        logger.error(f"PCAP file not found: {pcap_file}")
        sys.exit(1)
    except Scapy_Exception as e:
        logger.error(f"Error reading PCAP file: {e}")
        sys.exit(1)
    return packets

def extract_packet_data(packets):
    packet_data = []

    for packet in tqdm(packets, desc="Processing packets", unit="packet"):
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet[IP].proto
            size = len(packet)
            packet_data.append({"src_ip": src_ip, "dst_ip": dst_ip, "protocol": protocol, "size": size})

    return pd.DataFrame(packet_data)

def protocol_name(number):
    protocol_dict = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
    return protocol_dict.get(number, f"Unknown({number})")





def analyze_packet_data(df):
    total_bandwidth = df["size"].sum()
    protocol_counts = df["protocol"].value_counts(normalize=True) * 100
    protocol_counts.index = protocol_counts.index.map(protocol_name)

    ip_communication = df.groupby(["src_ip", "dst_ip"]).size().sort_values(ascending=False)
    ip_communication_percentage = ip_communication / ip_communication.sum() * 100
    ip_communication_table = pd.concat([ip_communication, ip_communication_percentage], axis=1).reset_index()

    protocol_frequency = df["protocol"].value_counts()
    protocol_frequency.index = protocol_frequency.index.map(protocol_name)

    protocol_counts_df = pd.concat([protocol_frequency, protocol_counts], axis=1).reset_index()
    protocol_counts_df.columns = ["Protocol", "Count", "Percentage"]

    ip_communication_protocols = df.groupby(["src_ip", "dst_ip", "protocol"]).size().reset_index()
    ip_communication_protocols.columns = ["Source IP", "Destination IP", "Protocol", "Count"]
    ip_communication_protocols["Protocol"] = ip_communication_protocols["Protocol"].apply(protocol_name)

    # Calculate percentage for each protocol for each source-destination pair
    ip_communication_protocols["Percentage"] = ip_communication_protocols.groupby(["Source IP", "Destination IP"])["Count"].transform(lambda x: (x / x.sum()) * 100)

    return total_bandwidth, protocol_counts_df, ip_communication_table, protocol_frequency, ip_communication_protocols

def extract_packet_data_security(packets):
    packet_data = []

    for packet in tqdm(packets, desc="Processing packets for port scanning activity", unit="packet"):
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet[IP].proto
            size = len(packet)

            if TCP in packet:
                dst_port = packet[TCP].dport
            else:
                dst_port = 0

            packet_data.append({"src_ip": src_ip, "dst_ip": dst_ip, "protocol": protocol, "size": size, "dst_port": dst_port})

    return pd.DataFrame(packet_data)

def detect_port_scanning(df,port_scan_threshold):
    # Group packets by source IP and destination port
    port_scan_df = df.groupby(['src_ip', 'dst_port']).size().reset_index(name='count')
    
    # Count the unique ports for each source IP
    unique_ports_per_ip = port_scan_df.groupby('src_ip').size().reset_index(name='unique_ports')
    
    # Check for a large number of packets to different ports on a single IP address
    potential_port_scanners = unique_ports_per_ip[unique_ports_per_ip['unique_ports'] >= port_scan_threshold]
    ip_addresses = potential_port_scanners['src_ip'].unique()
    
    if len(ip_addresses) > 0:
        logger.warning(f"Potential port scanning detected from IP addresses: {', '.join(ip_addresses)}")
        
        # again you are returning the below code for tkinter use
        return f"Potential port scanning detected from IP addresses:\n {',\n '.join(ip_addresses)}"


def print_results(total_bandwidth, protocol_counts_df, ip_communication_table, protocol_frequency, ip_communication_protocols):
    # Convert bandwidth to Mbps or Gbps
    if total_bandwidth < 10**9:
        bandwidth_unit = "Mbps"
        total_bandwidth /= 10**6
    else:
        bandwidth_unit = "Gbps"
        total_bandwidth /= 10**9

    logger.info(f"Total bandwidth used: {total_bandwidth:.2f} {bandwidth_unit}")
    logger.info("\nProtocol Distribution:\n")
    logger.info(tabulate(protocol_counts_df, headers=["Protocol", "Count", "Percentage"], tablefmt="grid"))
    logger.info("\nTop IP Address Communications:\n")
    logger.info(tabulate(ip_communication_table, headers=["Source IP", "Destination IP", "Count", "Percentage"], tablefmt="grid", floatfmt=".2f"))

    logger.info("\nShare of each protocol between IPs:\n")
    logger.info(tabulate(ip_communication_protocols, headers=["Source IP", "Destination IP", "Protocol", "Count", "Percentage"], tablefmt="grid", floatfmt=".2f"))

    # you are adding all the msgs to up so that they can be sent to tkinter to be displayed.
    log_messages = []
    log_messages.append(f"Total bandwidth used: {total_bandwidth:.2f} {bandwidth_unit}\n")
    log_messages.append("\nProtocol Distribution:\n")
    log_messages.append(tabulate(protocol_counts_df, headers=["Protocol", "Count", "Percentage"], tablefmt="grid"))
    log_messages.append("\nTop IP Address Communications:\n")
    log_messages.append(tabulate(ip_communication_table, headers=["Source IP", "Destination IP", "Count", "Percentage"], tablefmt="grid", floatfmt=".2f"))
    log_messages.append("\nShare of each protocol between IPs:\n")
    log_messages.append(tabulate(ip_communication_protocols, headers=["Source IP", "Destination IP", "Protocol", "Count", "Percentage"], tablefmt="grid", floatfmt=".2f"))

    return ''.join(log_messages)




def main(pcap_file,port_scan_threshold):
    packets = read_pcap(pcap_file)
    df = extract_packet_data(packets)
    total_bandwidth, protocol_counts, ip_communication_table, protocol_frequency, ip_communication_protocols = analyze_packet_data(df)
    #latency_df = calculate_latency(packets)
    # Plot graphs
    plot_all_graphs(protocol_counts, ip_communication_protocols)

    general_results =print_results(total_bandwidth, protocol_counts, ip_communication_table, protocol_frequency, ip_communication_protocols)
    
    

    df = extract_packet_data_security(packets)
    
    port_scanning_results=detect_port_scanning(df,port_scan_threshold)
     
 
     
    return [general_results,port_scanning_results]


    



    
# Set a default port_scan_threshold value
default_port_scan_threshold = 10
file_path="./smallFlows.pcap"

# main(file_path, default_port_scan_threshold)


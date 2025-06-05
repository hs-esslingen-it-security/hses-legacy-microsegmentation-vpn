import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import kaleido

########################
# visualize flows
########################

def bezier_curve(start, end, control, num_points=20):
    """
    Computes a quadratic Bezier curve with control point
    """
    t_values = np.linspace(0, 1, num_points)
    bezier_points = [( 
        (1 - t)**2 * start[0] + 2 * (1 - t) * t * control[0] + t**2 * end[0],
        (1 - t)**2 * start[1] + 2 * (1 - t) * t * control[1] + t**2 * end[1]
    ) for t in t_values]
    
    return zip(*bezier_points)  # Separate x and y lists

def compute_perpendicular_point(mid, start, end, offset):
    """
    Computes a control point for the Bezier curve that is perpendicular to the line segment.
    """
    direction = np.array([end[1] - start[1], start[0] - end[0]])  # Perpendicular vector
    norm = np.linalg.norm(direction)
    if norm == 0:
        return mid
    direction = (direction / norm) *     offset
    return mid + direction


def visualize_flows_df(df_flows, output_file, pos=None):
    """
    visualize recorded communication flows dataframe as graph
    """
    graph = nx.MultiDiGraph()
    bezier_factor = 0.75
    # Calculate total packets across all communications for scaling
    total_packets = df_flows["src2dst_packets"].sum() + df_flows["dst2src_packets"].sum()

    for index, flow in df_flows.iterrows():
        graph.add_nodes_from([flow["src_ip"], flow["dst_ip"]])  # Add nodes if not already in graph

        service_name = flow["application_name"]
        protocol_map = {6: "TCP", 17: "UDP"}
        protocol = protocol_map.get(flow['protocol'], "Unknown")  
        # edge color depending on one-sided or bi-directional communication, TCP or UDP
        # edge_color = "blue" if flow["dst2src_packets"] == 0 else "orange"
        # Mapping for colors based on protocol and direction
        color_map = {
            (6, True): "orange",   # TCP + Bidirectional
            (6, False): "skyblue",   # TCP + One-way
            (17, True): "orangered", # UDP + Bidirectional
            (17, False): "blue"  # UDP + One-way
        }
        is_bidirectional = flow["dst2src_packets"] > 0
        edge_color = color_map.get((flow["protocol"], is_bidirectional), "gray")  # Default to gray if unknown

        # Determine label format
        if flow["dst2src_packets"] > 0:
            label = f"{flow['src_ip']} <-> {flow['dst_ip']} {protocol} {service_name}"
        else:
            label = f"{flow['src_ip']} -> {flow['dst_ip']} {protocol} {service_name}"

        # Create a single edge between client_1 and client_2
        graph.add_edge(
            flow["src_ip"], flow["dst_ip"],
            weight=flow["src2dst_packets"] + flow["dst2src_packets"],
            bezier=bezier_factor,
            label=label,
            service=service_name,
            length=2,
            color=edge_color
        )

    pos = pos or nx.circular_layout(graph)
    fig = go.Figure()
    annotations = []

    for start, end, data in graph.edges(data=True):
        x1, y1 = pos[start]
        x2, y2 = pos[end]
        control_point = compute_perpendicular_point(np.array([(x1 + x2) / 2, (y1 + y2) / 2]), np.array([x1, y1]), np.array([x2, y2]), data['bezier'] * 0.1 * np.linalg.norm([x2 - x1, y2 - y1])) 
        bezier_x, bezier_y = bezier_curve((x1, y1), (x2, y2), control_point, num_points=50)
        
        # Plot the curve
        min_width = 5  # Mindestdicke der Linie
        max_width = 12  # Maximale Dicke der Linie für sehr große Werte
        scaled_width = min(max(min_width, (data['weight'] / (total_packets / 96))), max_width)
        fig.add_trace(go.Scatter(
            x=bezier_x, 
            y=bezier_y, 
            line=dict(width=scaled_width, color=data['color']), 
            mode='lines', 
            name=data['label']))
        
         # Calculate the midpoint of the Bezier curve for the label
        mid_t = 0.5  # Midpoint of the Bezier curve (t=0.5)
        mid_x = (1 - mid_t)**2 * x1 + 2 * (1 - mid_t) * mid_t * control_point[0] + mid_t**2 * x2
        mid_y = (1 - mid_t)**2 * y1 + 2 * (1 - mid_t) * mid_t * control_point[1] + mid_t**2 * y2
        
        # Add label for protocol at the midpoint of the Bezier curve
        annotations.append(go.layout.Annotation(
            x=mid_x, 
            y=mid_y, 
            text=data['service'], 
            showarrow=False, 
            bgcolor='#FFFFFF', 
            font=dict(size=7)))

    # plot nodes
    # adjust node colors to match figure in paper
    node_color_map = {
        "192.168.1.10": "#C0E78C",
        "192.168.1.20": "#F5CE67",
        "192.168.1.30": "#F19CF9",
        "192.168.1.40": "#ED7092",
        "192.168.1.50": "#F1A466",
        "192.168.1.60": "#62D1EE",
        "192.168.1.100": "#666DF2",
    }
    node_label_map = {
        "192.168.1.10": "PLC1",
        "192.168.1.20": "PLC2",
        "192.168.1.30": "PLC3",
        "192.168.1.40": "PLC4",
        "192.168.1.50": "PLC5",
        "192.168.1.60": "PLC6",
        "192.168.1.100": "SCADA",
    }
    for node in graph.nodes():
        fig.add_trace(go.Scatter(
            x=[pos[node][0]], 
            y=[pos[node][1]], 
            text=node_label_map[node], # SWaT use case; else: use node IP (node_label = node)
            mode='markers+text', 
            marker=dict(size=60, color=node_color_map[node]), # , color=node_color_map[node]
            textposition='middle center', 
            name=node, 
            showlegend=False,
            textfont=dict(size=16)))
    
    # overall layout
    fig.update_layout(
        showlegend=True, 
        legend=dict(
            font=dict(size=16),  # Adjust text size
            orientation="h",  # Horizontal legend
            yanchor="top",  # Align from the top
            y=-0.2,  # Move legend below the figure
            xanchor="center",  
            x=0.5  # Center the legend
        ),
        hovermode='closest', 
        margin=dict(b=0, l=0, r=0, t=0), 
        plot_bgcolor='#FFFFFF', 
        # annotations=annotations, 
        xaxis=dict(showticklabels=False, zeroline=False), 
        yaxis=dict(showticklabels=False, zeroline=False))

    fig.write_image(output_file)
    fig.show()


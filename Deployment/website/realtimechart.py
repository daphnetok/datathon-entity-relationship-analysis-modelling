import re
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# The raw text containing both Entities and Relationships sections.
def create_graph(data):

    # Extract Entities

    # Isolate the entities section: everything between "**Entities:**" and "**Relationships:**"
    entities_block_match = re.search(r'\*\*Entities:\*\*(.*?)\*\*Relationships:\*\*', data, re.DOTALL)
    entities_text = entities_block_match.group(1) if entities_block_match else ""

    # Define a regex pattern to capture the entity name (before the hyphen) and its description (after the hyphen)
    entity_pattern = r'\d+\.\s*([^-]+?)\s*-\s*(.+)'
    entities_found = re.findall(entity_pattern, entities_text)

    # Create a list of entity names
    entity_names = [name.strip() for name, desc in entities_found]

    print("Entities:")
    print(entity_names)

    # Extract Relationships

    # Isolate the relationships section (everything after "**Relationships:**")
    relationships_block_match = re.search(r'\*\*Relationships:\*\*(.*)', data, re.DOTALL)
    relationships_text = relationships_block_match.group(1) if relationships_block_match else ""

    # Define a regex pattern to capture each relationship block:
    # It captures the subject entity (before "has relationships with:")
    # and then captures all lines starting with an asterisk (*) that list the target entities.
    subject_pattern = r'\d+\.\s*(.+?)\s+has relationships with:\s*((?:\*.*(?:\n|$))+)' 
    subject_matches = re.findall(subject_pattern, relationships_text, re.DOTALL)

    # Initialize a list to hold edges (subject, target)
    edges = []

    # For each relationship block, extract the target entity from each asterisk (*) line.
    for subject, rel_block in subject_matches:
        subject = subject.strip()
        # Each line in rel_block should match the pattern: "* TargetEntity - description..."
        relationship_lines = re.findall(r'\*\s*(.+?)\s*-\s*(.+)', rel_block)
        for target, desc in relationship_lines:
            target = target.strip()
            edges.append((subject, target))

    print("\nEdges (relationships):")
    for edge in edges:
        print(edge)

    # Create the Graph

    # Create a graph
    G = nx.Graph()

    # Add all nodes (entities)
    G.add_nodes_from(entity_names)

    # Add all edges (relationships)
    G.add_edges_from(edges)

    # Define a layout for the graph
    pos = nx.spring_layout(G, seed=42)

    # Draw the graph
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=1500)
    nx.draw_networkx_edges(G, pos, width=2)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
    plt.axis('off')
    plt.title("Entities and Relationships Network Graph")

    # Save and Return the Graph as a Base64 String

    # Save the plot to a BytesIO buffer in PNG format
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    # Encode the image to Base64
    img_bytes = buffer.getvalue()
    graph_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    # Clean up plt to avoid overlapping figures
    plt.close()

    return graph_base64


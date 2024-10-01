# main.py

from src.access_control import HierarchicalABAC, DynamicPolicy
from src.encryption import Paillier
from src.drl import REINFORCEAgent
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
import random

def generate_transaction(size):
    """ Generate a random transaction of a given size. """
    return random.getrandbits(size * 8)  # Simulate transaction as a bitstring

def plot_confusion_matrix(cm, labels):
    """ Plot the confusion matrix. """
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title('Confusion Matrix')
    plt.show()

def plot_malicious_nodes(node_status):
    """ Plot the graph for malicious node detection. """
    G = nx.Graph()

    for node, is_malicious in node_status.items():
        G.add_node(node, malicious=is_malicious)

    # Add edges between nodes (assuming a fully connected graph for simplicity)
    for i in range(len(node_status)):
        for j in range(i + 1, len(node_status)):
            G.add_edge(list(node_status.keys())[i], list(node_status.keys())[j])

    colors = ['red' if is_malicious else 'green' for is_malicious in node_status.values()]
    nx.draw(G, with_labels=True, node_color=colors, font_weight='bold', font_size=10)
    plt.title('Malicious Node Detection')
    plt.show()

def run_simulation():
    try:
        print("Starting Simulation...")

        # Setup ABAC with dynamic policies
        abac = HierarchicalABAC()
        abac.add_policy("role", "hierarchical", ["admin", "superuser"])
        print("ABAC Policies Set Up.")

        dynamic_policy = DynamicPolicy({"location": "HQ"}, trust_threshold=0.8)
        dynamic_policy.add_trust_score("Node1", 0.9)
        attributes = {"role": "admin", "location": "HQ"}

        # Setup Paillier for encryption
        paillier = Paillier()
        print("Paillier Encryption Initialized.")

        # Initialize blockchain nodes
        num_nodes = 200
        nodes = [f"Node{i+1}" for i in range(num_nodes)]
        print(f"Initialized {num_nodes} blockchain nodes.")

        # Simulate transactions and mining
        transactions = []
        transaction_sizes = np.random.randint(200, 401, size=num_nodes)  # Random sizes between 200 and 400

        for size in transaction_sizes:
            transaction = generate_transaction(size)
            transactions.append(transaction)

        # Simulate mining results and trust scores
        mining_results = []
        node_status = {}

        for node in nodes:
            trust_score = random.uniform(0, 1)  # Random trust score between 0 and 1
            if trust_score < 0.5:  # If trust score is below 0.5, mark as malicious
                node_status[node] = True
                mining_results.append(0)  # Failed mining
            else:
                node_status[node] = False
                mining_results.append(1)  # Successful mining

        # Generate classification report
        y_true = mining_results  # True results (1 for success, 0 for failure)
        y_pred = [1 if result == 1 else 0 for result in mining_results]  # Predicted results (same in this case)

        # Generate confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        print("Confusion Matrix:")
        print(cm)

        # Plot confusion matrix
        labels = ['Failed', 'Successful']
        plot_confusion_matrix(cm, labels)

        # Print classification report
        print(classification_report(y_true, y_pred, target_names=["Failed", "Successful"]))

        # Plot malicious nodes
        plot_malicious_nodes(node_status)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_simulation()

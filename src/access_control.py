# src/advanced_access_control.py

import time

class DynamicPolicy:
    def __init__(self, base_attributes, trust_threshold):
        # Base attributes and dynamic factors like time or load
        self.base_attributes = base_attributes
        self.trust_threshold = trust_threshold
        self.trust_scores = {}

    def add_trust_score(self, node_id, score):
        self.trust_scores[node_id] = score

    def evaluate_policy(self, node_id, attributes):
        if node_id in self.trust_scores and self.trust_scores[node_id] >= self.trust_threshold:
            for key, value in self.base_attributes.items():
                if key in attributes and attributes[key] == value:
                    return True
        return False


class HierarchicalABAC:
    def __init__(self):
        self.policies = {}

    def add_policy(self, attribute, policy_type, roles):
        self.policies[attribute] = {'type': policy_type, 'roles': roles}

    def is_authorized(self, node_id, attributes):
        for attribute, policy_info in self.policies.items():
            if attribute in attributes:
                if policy_info['type'] == "hierarchical":
                    if any(role in policy_info['roles'] for role in attributes['role']):
                        return True
        return False

    def apply_dynamic_policy(self, node_id, attributes, dynamic_policy: DynamicPolicy):
        return dynamic_policy.evaluate_policy(node_id, attributes)

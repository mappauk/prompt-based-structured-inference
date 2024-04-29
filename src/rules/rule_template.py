import pandas as pd

class RuleTemplate:
    def __init__(self,
                 name: str,
                 features: list, 
                 labels: list, 
                 head_predicate_format: str,
                 rule_variable_format: str,
                 rule_type: str):
        self.name = name
        self.features = features
        self.labels = labels
        self.head_variable_format = head_predicate_format
        self.rule_variable_format = rule_variable_format
        self.rule_type = rule_type
    
    def get_rule_groundings(self, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError()
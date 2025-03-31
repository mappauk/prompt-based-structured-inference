import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from typing import List, Dict, Callable
from src.rules.rule_template import RuleTemplate
from src.rules.rule_type import RuleType
from parse import parse

class GurobiInferenceModel:
    def __init__(self, rules: 
                 Dict[str, RuleTemplate], 
                 rule_groundings: Dict[str, pd.DataFrame], 
                 constraints: List[Callable[[Dict[str, pd.DataFrame], Dict[str, gp.Var], gp.Model], None]],
                 num_solutions: int = 1):
        self.rules = rules
        self.rule_groundings = rule_groundings
        self.constraints = constraints
        self.num_solutions = num_solutions
    
    def get_solution(self, m):
        results = {}
        for var in m.getVars():
            results[var.VarName] = var.X
        return results

    def inference(self) -> Dict[str, int]:
        # get groundings
        rule_dict = {}
        head_dict = {}
        head_to_rule = {}
        head_format_added = set()
        with gp.Env() as env:
            with gp.Model(env=env) as model:
                # Create a new model
                m = gp.Model("mip1")
                # comment following line to see output
                m.setParam('OutputFlag', 0)
                if self.num_solutions > 1:
                    m.setParam(GRB.Param.PoolSearchMode, 2)
                    m.setParam(GRB.Param.PoolSolutions, 10)
                objective = 0
                for rule_name, rule_grounding in self.rule_groundings.items():
                    rule = self.rules[rule_name]
                    for item, row in rule_grounding.iterrows():
                        # add variable for each rule grounding
                        rule_variable_name = row['RuleVariable']
                        head_variable_name = row['HeadVariable']
                        head_negation_variable_name = row['HeadVariable'] + '_n'
                        temp_rule = m.addVar(vtype=GRB.BINARY, name=rule_variable_name)
                        rule_dict[rule_variable_name] = temp_rule
                        # build objective function which is the sum over all rule variables and their scores
                        objective = objective + temp_rule*row['Score']
                        if rule.rule_type == RuleType.BINARY:
                            temp_rule_n = m.addVar(vtype=GRB.BINARY, name=rule_variable_name + '_n')
                            objective = objective + temp_rule_n*(1 - row['Score'])
                            rule_dict[rule_variable_name + '_n'] = temp_rule_n
                        if not head_variable_name in head_dict:
                            # add variable for head predicate of rule as well as it's negation
                            temp_head = m.addVar(vtype=GRB.BINARY, name=head_variable_name)
                            temp_head_negate = m.addVar(vtype=GRB.BINARY, name=head_negation_variable_name)
                            head_dict[head_variable_name] = temp_head
                            head_dict[head_negation_variable_name] = temp_head_negate
                            # add constraint that only one of the head variable and it's negation can be active at the same time
                            m.addConstr(temp_head_negate + temp_head == 1)
                            # add constraint that rule variable can only be activated if head predicate is activated
                            m.addConstr(temp_rule <= temp_head)
                            head_to_rule[head_variable_name] = [rule_variable_name]
                            if rule.rule_type == RuleType.BINARY:
                                m.addConstr(temp_rule_n <= temp_head_negate)
                                head_to_rule[head_negation_variable_name] = [rule_variable_name + '_n']
                        else:
                            # add constraint that rule variable can only be activated if head predicate is activated
                            temp_head = head_dict[head_variable_name]
                            m.addConstr(temp_rule <= temp_head)
                            head_to_rule[head_variable_name].append(rule_variable_name)
                            if rule.rule_type == RuleType.BINARY:
                                m.addConstr(temp_rule_n <= head_dict[head_variable_name + "_n"])
                                head_to_rule[head_negation_variable_name].append(rule_variable_name + '_n')
                    # constraint for multiclass variables to force only one label to be activated
                    if rule.rule_type == RuleType.MULTI_CLASS and rule.head_variable_format not in head_format_added:
                        head_format_added.add(rule.head_variable_format)
                        label_groupings = rule_grounding.groupby(rule_grounding.columns.difference(['label', 'RuleVariable', 'HeadVariable', 'Score']).to_list())
                        for group_name, group in label_groupings:
                            temp_const = 0
                            for index, row in group.iterrows():
                                temp_const += head_dict[row['HeadVariable']]
                            m.addConstr(temp_const == 1)

                m.setObjective(objective, GRB.MAXIMIZE)                
                # constraint to enforce activation of at least one rule predicate given the activation of a corresponding head predicate 
                for key, value in head_to_rule.items():
                    temp_const = 0
                    for prem in value:
                        temp_const += rule_dict[prem]
                    m.addConstr(temp_const >= head_dict[key])    
                # custom rule constraints
                for constr_func in self.constraints:
                   constr_func(self.rule_groundings, head_dict, m)
                # optimize
                m.optimize()
                all_results = []
                if self.num_solutions > 1:
                    for i in range(0, m.getAttr('SolCount')):
                        m.setParam('SolutionNumber', i)
                        all_results.append(self.get_solution(m))
                else:
                    all_results.append(self.get_solution(m))                 
                return all_results


                
                


from utils.DSL.conditions import BaseCondition, ConditionNode, InCondition, SimpleCondition
from lark import Transformer
from utils.DSL.conditions import ComparisonOperator

class ConditionTransformer(Transformer):
    def __init__(self):
        super().__init__()
            
    def STRING(self, value):
        return value.strip('"').strip("'")
    
    def NUMBER(self, value):
        if '.' in value:
            return float(value)
        else:
            return int(value)

    def value_list(self, args):
        return args

    def simple_condition(self, args):
        field_name_token = args[0]
        op_token = args[1]
        val = args[2]

        field_name = field_name_token.value
        op = op_token.value
        cond = SimpleCondition(field=field_name, operator=ComparisonOperator(op), value=val)
        return ConditionNode(condition=cond)

    def in_condition(self, args):
        field_name_token = args[0]
        values = args[1]

        field_name = field_name_token.value
        cond = InCondition(field=field_name, values=values)
        return ConditionNode(condition=cond)

    def condition_group(self, args):
        node = args[0]
        if isinstance(node, BaseCondition):
            return ConditionNode(condition=node)
        return node

    def and_operation(self, args):
        return ConditionNode(and_nodes=[args[0], args[1]])

    def or_operation(self, args):
        return ConditionNode(or_nodes=[args[0], args[1]])

    def start(self, args):
        node = args[0]
        if isinstance(node, BaseCondition):
            return ConditionNode(condition=node)
        elif isinstance(node, ConditionNode):
            return node
        else:
            return ConditionNode(condition=node)
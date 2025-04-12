from enum import Enum

from pydantic import BaseModel, SerializeAsAny

class ComparisonOperator(str, Enum):
    EQ = "="
    GT = ">"
    LT = "<"
    GTE = ">="
    LTE = "<="

class BaseCondition(BaseModel):
    pass

class SimpleCondition(BaseCondition):
    field: str
    operator: ComparisonOperator
    value: str | int | float

class InCondition(BaseCondition):
    field: str
    values: list[str | int | float]

class ConditionNode(BaseModel):
    and_nodes: list["ConditionNode"] | None = None
    or_nodes: list["ConditionNode"] | None = None
    condition: SimpleCondition | InCondition | None = None

    def is_leaf(self):
        return self.condition is not None and not self.and_nodes and not self.or_nodes

ConditionNode.model_rebuild()
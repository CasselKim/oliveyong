from lark import Lark
from utils.DSL.transformer import ConditionTransformer
from utils.DSL.evaluate import evaluate_condition

with open('grammer.lark', 'r', encoding='utf-8') as f:
    condition_grammar = f.read()

parser = Lark(condition_grammar, start='start', parser='lalr', transformer=ConditionTransformer())

dsl = 'customer_segment = "VIP" AND brand_id IN [5,7] AND (product_id IN [101,102] OR mov > 50000)'

condition_tree = parser.parse(dsl)

context = {
  "customer_segment": "VIP",
  "brand_id": 5,
  "product_id": 101,
  "mov": 40000
}

result = evaluate_condition(condition_tree, context)
print(result)
from utils.DSL.conditions import ComparisonOperator, ConditionNode, InCondition, SimpleCondition

SEGMENT_RANK = {
    'NO OLIVE': 0,
    'BABY OLIVE': 1,
    'PINK OLIVE': 2,
    'GREEN OLIVE': 3,
    'BLACK OLIVE': 4,
    'GOLD OLIVE': 5
}

def compare_values(op, left, right):
    # left, right에 customer_segment 비교가 필요하면 등급 비교 수행
    # 우선 customer_segment 비교인지 판별 필요
    # 가정: DSL에서 customer_segment를 문자열로, right도 문자열로 표시
    # 예: customer_segment > BABY OLIVE

    # 먼저 두 값 모두 세그먼트 테이블에 있는지 확인
    # 아닐 경우 일반 비교로 처리
    if isinstance(left, str) and isinstance(right, str):
        if left in SEGMENT_RANK and right in SEGMENT_RANK:
            left_rank = SEGMENT_RANK[left]
            right_rank = SEGMENT_RANK[right]
            if op == '=':
                return left_rank == right_rank
            elif op == '>':
                return left_rank > right_rank
            elif op == '<':
                return left_rank < right_rank
            elif op == '>=':
                return left_rank >= right_rank
            elif op == '<=':
                return left_rank <= right_rank
            # 그 외 연산자가 없으면 False 반환
            return False

    # 세그먼트가 아니거나 등급 비교 불가능하면 일반 비교 로직
    if op == '=':
        return left == right
    elif op == '>':
        return left > right
    elif op == '<':
        return left < right
    elif op == '>=':
        return left >= right
    elif op == '<=':
        return left <= right
    elif op == 'IN':
        return left in right
    return False

def evaluate_condition(node, context):
    # node는 parse된 DSL 트리 (ConditionNode 형태), context는 {brand_id, product_id, customer_segment, mov ...} 딕셔너리
    # 가정: evaluate_condition은 하위 노드(and_nodes, or_nodes, condition)를 재귀적으로 평가

    if node.condition:
        # 단일 조건일 경우
        # condition 필드는 SimpleCondition, InCondition 등
        field = node.condition.field
        if isinstance(node.condition, SimpleCondition):
            op = node.condition.operator
            val = node.condition.value
        elif isinstance(node.condition, InCondition):
            op = "IN"
            val = node.condition.values

        # context에서 필드값 가져오기
        left_value = context.get(field)

        # 세그먼트 비교 시 DSL에서 "BABY OLIVE" 등 문자열이 val에 들어있다고 가정
        # compare_values로 비교
        return compare_values(op, left_value, val)
    elif node.and_nodes:
        # AND 조건일 경우
        return all(evaluate_condition(n, context) for n in node.and_nodes)
    elif node.or_nodes:
        # OR 조건일 경우
        return any(evaluate_condition(n, context) for n in node.or_nodes)
    # 빈 노드일 경우 True 반환 또는 False 반환(설계에 따라 다름)
    return True
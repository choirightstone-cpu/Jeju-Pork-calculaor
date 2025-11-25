import math

def calculate_table_count(total_people, people_per_table):
    return math.ceil(total_people / people_per_table)

def calculate_total_cost(
    total_people,
    people_per_table,
    menu_config
):
    """
    Calculates the total cost based on the menu configuration per table.
    
    menu_config: dict containing price and quantity for each item type per table.
    Example:
    {
        "special_platter": {"price": 48000, "qty": 2},
        "extra_meat": {"price": 14000, "qty": 2},
        ...
    }
    """
    num_tables = calculate_table_count(total_people, people_per_table)
    
    table_cost = 0
    breakdown = {}
    
    for item, details in menu_config.items():
        item_cost = details['price'] * details['qty']
        table_cost += item_cost
        breakdown[item] = item_cost
        
    total_cost = table_cost * num_tables
    per_person_cost = total_cost / total_people if total_people > 0 else 0
    
    return {
        "total_cost": total_cost,
        "per_person_cost": per_person_cost,
        "num_tables": num_tables,
        "table_cost": table_cost,
        "breakdown": breakdown
    }

def optimize_menu(target_budget_per_person, total_people, people_per_table, current_config):
    """
    Optimization logic to adjust quantities to fit the budget.
    Returns: (optimized_config, reasoning_list)
    """
    num_tables = calculate_table_count(total_people, people_per_table)
    total_budget = target_budget_per_person * total_people
    budget_per_table = total_budget / num_tables
    
    optimized_config = {k: v.copy() for k, v in current_config.items()}
    reasoning = []
    
    # Calculate current table cost
    current_table_cost = sum(item['price'] * item['qty'] for item in optimized_config.values())
    
    if current_table_cost > budget_per_table:
        reasoning.append("현재 예산을 초과하여 비용 절감을 시도합니다.")
        # Strategy: Reduce Extra Meat first, then Drinks, then Alcohol
        
        # 1. Reduce Extra Meat
        while optimized_config['extra_meat']['qty'] > 0 and current_table_cost > budget_per_table:
            optimized_config['extra_meat']['qty'] -= 1
            current_table_cost -= optimized_config['extra_meat']['price']
            reasoning.append(f"비용 절감을 위해 '{optimized_config['extra_meat']['name']}' 1개를 줄였습니다.")
            
        # 2. Reduce Drinks (if still over)
        while optimized_config['drinks']['qty'] > 0 and current_table_cost > budget_per_table:
            optimized_config['drinks']['qty'] -= 1
            current_table_cost -= optimized_config['drinks']['price']
            reasoning.append(f"비용 절감을 위해 '{optimized_config['drinks']['name']}' 1개를 줄였습니다.")

        # 3. Reduce Beer (if still over)
        while optimized_config['beer']['qty'] > 0 and current_table_cost > budget_per_table:
            optimized_config['beer']['qty'] -= 1
            current_table_cost -= optimized_config['beer']['price']
            reasoning.append(f"비용 절감을 위해 '{optimized_config['beer']['name']}' 1개를 줄였습니다.")
            
        # 4. Reduce Soju (if still over)
        while optimized_config['soju']['qty'] > 0 and current_table_cost > budget_per_table:
            optimized_config['soju']['qty'] -= 1
            current_table_cost -= optimized_config['soju']['price']
            reasoning.append(f"비용 절감을 위해 '{optimized_config['soju']['name']}' 1개를 줄였습니다.")
            
        if current_table_cost > budget_per_table:
            reasoning.append("⚠️ 최소한의 메뉴로도 예산을 맞추기 어렵습니다. 예산을 늘리거나 인원 조정을 고려해보세요.")
            
    elif current_table_cost < budget_per_table:
        reasoning.append("현재 예산에 여유가 있어 메뉴를 업그레이드합니다.")
        # Strategy: Add Special Platter if possible, then Extra Meat, then Drinks
        
        # 1. Try to add Special Platter (Priority)
        while (current_table_cost + optimized_config['special_platter']['price']) <= budget_per_table:
             optimized_config['special_platter']['qty'] += 1
             current_table_cost += optimized_config['special_platter']['price']
             reasoning.append(f"예산 여유분을 활용해 '{optimized_config['special_platter']['name']}' 1개를 추가했습니다! 🍖")

        # 2. Try to add Extra Meat
        while (current_table_cost + optimized_config['extra_meat']['price']) <= budget_per_table:
             optimized_config['extra_meat']['qty'] += 1
             current_table_cost += optimized_config['extra_meat']['price']
             reasoning.append(f"예산 여유분을 활용해 '{optimized_config['extra_meat']['name']}' 1개를 추가했습니다.")
             
    else:
        reasoning.append("현재 구성이 예산에 딱 맞습니다! 완벽한 계획입니다. 👍")
            
    return optimized_config, reasoning

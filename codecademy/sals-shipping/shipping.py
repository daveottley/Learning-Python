#!/usr/bin/env python3

from typing import Tuple, Callable, Dict

def main():
    print("Welcome to Sal's Shipping!")

    while True:
        weight_str = input("What is the weight of your package in pounds? (a number) ")
        
        try:
            # Attempt to parse as a float (handles decimals, negatives, etc.)
            weight = float(weight_str)
            if weight <= 0:
                print("Weight must be a positive number.")
                continue
            break;
        except ValueError:
            print("Please enter a valid number.")
    
    method, cost = calculate_cheapest(weight)

    print(f"Your most affordable option is {method} and your cost to ship will be US ${cost:.2f}.")

def calculate_cheapest(weight: float) -> Tuple[str, float]:
    """
    Determines the cheapest shipping method based on the packages weight.

    Args:
        weight (float): The weight of the package in pounds.

    Returns:
        Tuple[str, float]:  A tuple containing the name of the cheapest shipping method
                            and the corresponding cost. 
    """
    
    # Define cost calculation functions for each shipping method
    def ground_cost(w: float) -> float:
        """
        Calculates cost for Ground shipping. Uses a flat charge of $20
        plus a per-pound charge based on the weight of the package.
        """
        if w < 0:
            raise ValueError("Weight cannot be negative")

        # Define weight thresholds and corresponding price per pound
        # Each tuple contains (upper_bound, price_per_pound)
        # The last tuple has upper_bound set to float('inf') to handle weights >10 lb
        pricing_structure: List[Tuple[float, float]] = [
            (2, 1.50),      # <= 2 lb
            (6, 3.00),      # >2 lb <= 6 lb
            (10, 4.00),     # >6 lb <= 10 lb
            (float('inf'), 4.75)  # >10 lb
        ]
        flat_charge = 20

        # Determine the price per pound based on weight
        for upper_bound, price_per_pound in pricing_structure:
            if w <= upper_bound:
                cost = flat_charge + (w * price_per_pound)
                break

        return cost

    def ground_premium_cost(w: float) -> float:
        """Calculates cost for Ground Premium shipping. Always $125.00"""
        return 125

    def drone_cost(w: float) -> float:
        """Calculates cost for Drone shipping. 3x Ground rate w/ no flat fee"""
        # Define weight thresholds and corresponding price per pound
        # Each tuple contains (upper_bound, price_per_pound)
        # The last tuple has upper_bound set to float('inf') to handle weights >10 lb
        pricing_structure: List[Tuple[float, float]] = [
            (2, 4.50),      # <= 2 lb
            (6, 9.00),      # >2 lb <= 6 lb
            (10, 12.00),     # >6 lb <= 10 lb
            (float('inf'), 4.75)  # >10 lb
        ]
        
        # Determine the price per pound based on weight
        for upper_bound, price_per_pound in pricing_structure:
            if w <= upper_bound:
                cost = w * price_per_pound
                break
        
        return cost
    
    # Dictionary storing method->cost_function mappings
    shipping_methods: Dict[str, Callable[[float], float]] = {
        "Ground": ground_cost,
        "Ground Premium": ground_premium_cost,
        "Drone": drone_cost
    }
   
    best_method = None
    lowest_cost = float('inf') # Initialize with infinity to ensure any cost will be lower

    # Iterate over shipping methods and determine the one with the lowest cost
    for method, cost_func in shipping_methods.items():
        cost = cost_func(weight)
        #print(f"Calculating cost for {method}: ${cost:.2f}") # Debug statement
        if cost < lowest_cost:
            lowest_cost = cost
            best_method = method

    return best_method, lowest_cost
    

if __name__ == "__main__":
    main()

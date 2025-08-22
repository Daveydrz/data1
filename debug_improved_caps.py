#!/usr/bin/env python3
"""
Debug script to understand why frequency capping is not working in the improved manager.
"""

import data
from datetime import datetime

def debug_frequency_capping():
    """Debug the frequency capping logic step by step."""
    print("🔧 DEBUGGING FREQUENCY CAPPING LOGIC")
    print("=" * 50)
    
    # Create improved manager
    first_person_templates = [
        data.FirstPersonExpandedTravelTemplate,
        data.FirstPersonHealthGoalTemplate,
        data.FirstPersonWorkRoleTemplate
    ]
    
    third_person_templates = [
        data.ThirdPersonPetTemplate,
        data.ThirdPersonAdvancedCognitiveTemplate
    ]
    
    manager = data.ImprovedBalancedTemplateManager(first_person_templates, third_person_templates)
    manager.set_generation_parameters(50, "balanced")
    
    # Simulate some usage to create imbalance
    manager.entity_type_usage['PERSON'] = 5  # minimum
    manager.entity_type_usage['CONCEPT'] = 10  # 2x
    manager.entity_type_usage['ACTIVITY'] = 20  # 4x (should be capped)
    
    print("Current entity usage:")
    for entity_type in ['PERSON', 'CONCEPT', 'ACTIVITY']:
        usage = manager.entity_type_usage[entity_type]
        cap = manager.get_frequency_cap(entity_type, is_entity=True)
        is_capped = manager.is_frequency_capped(entity_type, is_entity=True)
        print(f"  {entity_type}: usage={usage}, cap={cap}, is_capped={is_capped}")
    
    # Test template viability
    print(f"\nTesting template viability:")
    for template_class in first_person_templates:
        try:
            is_viable, reason = manager.is_template_viable(template_class, "first_person")
            print(f"  {template_class.__name__}: viable={is_viable}, reason={reason}")
            
            if is_viable:
                # Show what this template would generate
                template = template_class(0, datetime.now(), "first_person")
                _, entities_meta, relations_meta = template.generate()
                
                print(f"    Would generate entities: {[entity_type for _, (entity_type, _) in entities_meta.items()]}")
                print(f"    Would generate relations: {[rel_type for rel_type, _, _ in relations_meta]}")
                
        except Exception as e:
            print(f"  {template_class.__name__}: ERROR - {e}")
    
    # Test template selection
    print(f"\nTesting template selection:")
    for i in range(5):
        template = manager.select_next_template("first_person")
        print(f"  Selection {i+1}: {template.__name__}")

def debug_balance_calculation():
    """Debug the balance calculation logic."""
    print("\n🔧 DEBUGGING BALANCE CALCULATION")
    print("=" * 50)
    
    # Test balance calculation with known values
    manager = data.ImprovedBalancedTemplateManager([], [])
    
    # Set up test data
    manager.entity_type_usage = {
        'PERSON': 10,     # minimum
        'CONCEPT': 20,    # 2x
        'ACTIVITY': 30,   # 3x (at limit)
        'LOCATION': 40    # 4x (violates 3x rule)
    }
    
    manager.relation_type_usage = {
        'USES': 5,        # minimum
        'AT_LOCATION': 10, # 2x
        'DOES_ACTIVITY': 15 # 3x (at limit)
    }
    
    print("Test data:")
    print(f"  Entity usage: {manager.entity_type_usage}")
    print(f"  Relation usage: {manager.relation_type_usage}")
    
    # Calculate balances
    entity_balance = manager._calculate_type_balance(is_entity=True)
    relation_balance = manager._calculate_type_balance(is_entity=False)
    overall_balance = manager.calculate_proper_balance_score()
    
    print(f"\nBalance calculations:")
    print(f"  Entity balance: {entity_balance:.1f}%")
    print(f"  Relation balance: {relation_balance:.1f}%") 
    print(f"  Overall balance: {overall_balance:.1f}%")
    
    # Expected: 
    # Entity: min=10, max=40, ratio=10/40=0.25 (25%)
    # Since max > min*3 (40 > 30), this violates 3x rule
    # Should be in 0-33.3% range (violates 3x rule)
    
    # Relation: min=5, max=15, ratio=5/15=0.33 (33%)
    # Since max = min*3 (15 = 15), this is at 3x limit
    # Should be 33.3% (exactly at 3x rule limit)

if __name__ == "__main__":
    debug_frequency_capping()
    debug_balance_calculation()
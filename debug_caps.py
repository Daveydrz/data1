#!/usr/bin/env python3
"""
Debug script to understand frequency capping behavior.
"""

import data

def debug_frequency_capping():
    print("🔧 Debugging Frequency Capping")
    print("=" * 40)
    
    # Create a manager and simulate the process
    first_person_templates = [
        data.FirstPersonExpandedTravelTemplate,
        data.FirstPersonObjectOwnershipTemplate,
        data.FirstPersonHealthGoalTemplate,
        data.FirstPersonWorkRoleTemplate,
        data.FirstPersonWeatherMoodTemplate,
    ]
    
    third_person_templates = [
        data.ThirdPersonPetTemplate,
        data.ThirdPersonComprehensiveMemoryTemplate,
        data.ThirdPersonPetCareTemplate,
        data.ThirdPersonAdvancedCognitiveTemplate,
        data.ThirdPersonTemporalExpertiseTemplate,
    ]
    
    manager = data.BalancedTemplateManager(first_person_templates, third_person_templates)
    manager.set_generation_parameters(200, "balanced")
    
    # Simulate some usage
    manager.entity_type_usage["PERSON"] = 50
    manager.entity_type_usage["CONCEPT"] = 1
    manager.entity_type_usage["ACTIVITY"] = 25
    
    manager.relation_type_usage["DOES_ACTIVITY"] = 30
    manager.relation_type_usage["FEELS"] = 1
    manager.relation_type_usage["USES"] = 15
    
    print("Current usage simulation:")
    print(f"PERSON: {manager.entity_type_usage['PERSON']}")
    print(f"CONCEPT: {manager.entity_type_usage['CONCEPT']}")
    print(f"ACTIVITY: {manager.entity_type_usage['ACTIVITY']}")
    
    print(f"DOES_ACTIVITY: {manager.relation_type_usage['DOES_ACTIVITY']}")
    print(f"FEELS: {manager.relation_type_usage['FEELS']}")
    print(f"USES: {manager.relation_type_usage['USES']}")
    
    # Check frequency caps
    entity_cap_person = manager.get_frequency_cap("PERSON", True)
    entity_cap_concept = manager.get_frequency_cap("CONCEPT", True)
    relation_cap_activity = manager.get_frequency_cap("DOES_ACTIVITY", False)
    relation_cap_feels = manager.get_frequency_cap("FEELS", False)
    
    print(f"\nFrequency caps:")
    print(f"PERSON cap: {entity_cap_person}, is_capped: {manager.is_frequency_capped('PERSON', True)}")
    print(f"CONCEPT cap: {entity_cap_concept}, is_capped: {manager.is_frequency_capped('CONCEPT', True)}")
    print(f"DOES_ACTIVITY cap: {relation_cap_activity}, is_capped: {manager.is_frequency_capped('DOES_ACTIVITY', False)}")
    print(f"FEELS cap: {relation_cap_feels}, is_capped: {manager.is_frequency_capped('FEELS', False)}")
    
    # Check 3x compliant caps
    entity_3x_cap = manager.get_3x_compliant_cap(True)
    relation_3x_cap = manager.get_3x_compliant_cap(False)
    print(f"\n3x compliant caps:")
    print(f"Entity types: {entity_3x_cap}")
    print(f"Relation types: {relation_3x_cap}")
    
    # Test gap scores
    gap_person = manager.get_distribution_gap_score("PERSON", True)
    gap_concept = manager.get_distribution_gap_score("CONCEPT", True)
    gap_activity = manager.get_distribution_gap_score("DOES_ACTIVITY", False)
    gap_feels = manager.get_distribution_gap_score("FEELS", False)
    
    print(f"\nGap scores:")
    print(f"PERSON: {gap_person}")
    print(f"CONCEPT: {gap_concept}")
    print(f"DOES_ACTIVITY: {gap_activity}")
    print(f"FEELS: {gap_feels}")

if __name__ == "__main__":
    debug_frequency_capping()
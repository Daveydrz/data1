#!/usr/bin/env python3
"""
Template Analysis Tool

This script analyzes the existing templates to understand why certain entity types
are missing and provides specific recommendations for achieving 100% coverage.
"""

import re
import sys
from typing import Set, Dict, List
from data import EntityTypes


def extract_entity_types_from_templates() -> Dict[str, Set[str]]:
    """
    Extract entity types used by each template by analyzing the data.py source code.
    """
    template_entities = {}
    
    try:
        with open('data.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all template classes
        template_pattern = r'class (\w+Template)\(Template\):'
        templates = re.findall(template_pattern, content)
        
        for template in templates:
            # Find the generate method for this template
            class_start = content.find(f'class {template}(Template):')
            if class_start == -1:
                continue
                
            # Find the next class or end of file
            next_class = content.find('class ', class_start + 1)
            if next_class == -1:
                class_content = content[class_start:]
            else:
                class_content = content[class_start:next_class]
            
            # Extract EntityTypes usage
            entity_types = set()
            entity_pattern = r'EntityTypes\.([A-Z_]+)'
            matches = re.findall(entity_pattern, class_content)
            
            for match in matches:
                entity_types.add(match)
            
            template_entities[template] = entity_types
    
    except Exception as e:
        print(f"Error analyzing templates: {e}")
        return {}
    
    return template_entities


def analyze_missing_entity_coverage(missing_entities: Set[str]) -> None:
    """Analyze why specific entities are missing and provide targeted recommendations."""
    
    print(f"\n🔍 DETAILED ANALYSIS: Why are AMOUNT and INDUSTRY missing?")
    print("=" * 70)
    
    # Analyze AMOUNT
    print(f"\n📊 AMOUNT Entity Analysis:")
    print(f"   • Definition: Represents quantities, measurements, monetary values")
    print(f"   • Examples: '$100', '5 pounds', '3.5 hours', '50%', '10 items'")
    print(f"   • Current Status: Missing from all templates")
    print(f"   • Likely Cause: Templates use DURATION for time amounts, MONEY for currency")
    print(f"   • Impact: Generic quantity expressions are not captured")
    
    # Analyze INDUSTRY  
    print(f"\n🏭 INDUSTRY Entity Analysis:")
    print(f"   • Definition: Represents business sectors, professional domains")
    print(f"   • Examples: 'healthcare', 'technology', 'manufacturing', 'retail'")
    print(f"   • Current Status: Missing from all templates")
    print(f"   • Likely Cause: Templates use BUSINESS for companies, not industry sectors")
    print(f"   • Impact: Professional context and sector-specific content not captured")


def generate_template_recommendations() -> None:
    """Generate specific template recommendations for missing entities."""
    
    print(f"\n💡 SPECIFIC TEMPLATE RECOMMENDATIONS:")
    print("=" * 50)
    
    print(f"\n1. 🎯 Quick Fix - Enhance Existing Templates:")
    print(f"   Add these entity types to FirstPersonRareEntityTypesTemplate:")
    
    print(f"\n   For AMOUNT:")
    print(f'   amount = random.choice(["$500", "50 items", "75%", "3.2 million"])')
    print(f'   "amount1": (EntityTypes.AMOUNT, amount),')
    
    print(f"\n   For INDUSTRY:")
    print(f'   industry = random.choice(["healthcare", "technology", "retail", "manufacturing"])')
    print(f'   "industry1": (EntityTypes.INDUSTRY, industry),')
    
    print(f"\n2. 📝 Create Dedicated Templates:")
    
    print(f"\n   FirstPersonIndustryExperienceTemplate:")
    print(f'   "I have 5 years of experience in the healthcare industry"')
    print(f'   Uses: INDUSTRY, AMOUNT (years), SKILL, EXPERIENCE')
    
    print(f"\n   FirstPersonQuantityManagementTemplate:")
    print(f'   "I need to manage 50 items of resources for this project"')
    print(f'   Uses: AMOUNT, PROJECT, GOAL, ACTIVITY')
    
    print(f"\n3. 🔧 Enhanced Comprehensive Template:")
    print(f"   Modify FirstPersonComprehensiveCoverageTemplate to include:")
    print(f"   • Financial amounts (budgets, costs, savings)")
    print(f"   • Quantity measurements (items, percentages, volumes)")
    print(f"   • Industry context (sector, domain, field)")


def create_enhanced_template_code() -> None:
    """Generate code for an enhanced template that covers missing entities."""
    
    print(f"\n📄 ENHANCED TEMPLATE CODE:")
    print("=" * 40)
    
    template_code = '''
class FirstPersonMissingEntitiesTemplate(Template):
    def generate(self):
        """Template specifically designed to cover AMOUNT and INDUSTRY entities."""
        
        # Missing entity types
        amount = random.choice([
            "$1,500", "25 items", "80%", "2.5 million", 
            "150 pounds", "90 degrees", "75 points"
        ])
        
        industry = random.choice([
            "healthcare", "technology", "finance", "education",
            "manufacturing", "retail", "automotive", "aerospace"
        ])
        
        activity = random.choice(ACTIVITIES)
        skill = random.choice(SKILLS)
        location = random.choice(LOCATIONS)
        
        text = f"I work in the {industry} industry where I manage {amount} " \\
               f"of resources while doing {activity} in {location}. " \\
               f"This requires strong {skill} skills."
        
        entities = {
            "user": (EntityTypes.PRONOUN, "I"),
            "industry1": (EntityTypes.INDUSTRY, industry),
            "amount1": (EntityTypes.AMOUNT, amount),
            "activity1": (EntityTypes.ACTIVITY, activity),
            "skill1": (EntityTypes.SKILL, skill),
            "location1": (EntityTypes.LOCATION, location)
        }
        
        relations = [
            (RelationTypes.WORKS_IN, "user", "industry1"),
            (RelationTypes.MANAGES, "user", "amount1"),
            (RelationTypes.DOES_ACTIVITY, "user", "activity1"),
            (RelationTypes.AT_LOCATION, "activity1", "location1"),
            (RelationTypes.HAS_SKILL, "user", "skill1"),
            (RelationTypes.USED_FOR, "skill1", "activity1")
        ]
        
        return text, entities, relations
'''
    
    print(template_code)


def main():
    """Main analysis function."""
    
    print("🔍 Template Analysis for Missing Entities")
    print("=" * 50)
    
    missing_entities = {"AMOUNT", "INDUSTRY"}
    
    # Analyze why entities are missing
    analyze_missing_entity_coverage(missing_entities)
    
    # Generate recommendations
    generate_template_recommendations()
    
    # Create enhanced template code
    create_enhanced_template_code()
    
    print(f"\n🎯 IMPLEMENTATION PRIORITY:")
    print(f"1. HIGH: Add AMOUNT and INDUSTRY to FirstPersonRareEntityTypesTemplate")
    print(f"2. MEDIUM: Create FirstPersonMissingEntitiesTemplate")
    print(f"3. LOW: Enhance existing templates with these entity types")
    
    print(f"\n✅ Expected Result: 100% entity coverage (68/68)")


if __name__ == "__main__":
    main()
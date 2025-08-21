#!/usr/bin/env python3
"""
Comprehensive Entity Coverage Report

This script provides a complete analysis of entity coverage in the generated dataset,
identifies missing entities, and provides actionable recommendations for achieving 100% coverage.
"""

import json
import sys
from collections import defaultdict
from typing import Dict, Set, List, Tuple
from data import EntityTypes


def run_comprehensive_analysis():
    """Run complete entity coverage analysis and generate report."""
    
    print("🔍 COMPREHENSIVE ENTITY COVERAGE ANALYSIS")
    print("="*80)
    
    # Step 1: Extract all entity types
    all_entity_types = {attr for attr in dir(EntityTypes) if not attr.startswith('_')}
    print(f"\n📋 STEP 1: Entity Types Inventory")
    print(f"   • Total entity types defined in EntityTypes class: {len(all_entity_types)}")
    
    # Step 2: Analyze dataset
    dataset_path = "DeBERTa_finetuning_dataset_expanded_relations.json"
    entity_usage, used_entity_types = analyze_dataset(dataset_path)
    
    # Step 3: Identify missing entities
    missing_entity_types = all_entity_types - used_entity_types
    coverage_percentage = len(used_entity_types) / len(all_entity_types) * 100
    
    print(f"\n📊 STEP 2: Dataset Analysis Results")
    print(f"   • Entity types actually used: {len(used_entity_types)}")
    print(f"   • Entity types missing: {len(missing_entity_types)}")
    print(f"   • Coverage percentage: {coverage_percentage:.1f}%")
    
    # Step 4: Detailed analysis of missing entities
    print(f"\n❌ STEP 3: Missing Entity Types ({len(missing_entity_types)})")
    if missing_entity_types:
        for i, entity_type in enumerate(sorted(missing_entity_types), 1):
            print(f"   {i}. {entity_type}")
        
        print(f"\n🔍 DETAILED ANALYSIS OF MISSING ENTITIES:")
        analyze_missing_entities(missing_entity_types)
    else:
        print("   ✅ No missing entities - perfect coverage!")
    
    # Step 5: Recommendations
    print(f"\n💡 STEP 4: Recommendations for 100% Coverage")
    provide_actionable_recommendations(missing_entity_types)
    
    # Step 6: Implementation plan
    print(f"\n🚀 STEP 5: Implementation Plan")
    create_implementation_plan(missing_entity_types)
    
    # Step 7: Summary
    print(f"\n🎯 SUMMARY")
    print("="*40)
    print(f"Current Status: {len(used_entity_types)}/{len(all_entity_types)} entity types covered ({coverage_percentage:.1f}%)")
    if missing_entity_types:
        print(f"Missing: {', '.join(sorted(missing_entity_types))}")
        print(f"Action Required: Implement recommendations to achieve 100% coverage")
    else:
        print(f"Status: ✅ PERFECT COVERAGE ACHIEVED!")
    
    return missing_entity_types


def analyze_dataset(dataset_path: str) -> Tuple[Dict[str, int], Set[str]]:
    """Analyze dataset to extract entity usage statistics."""
    
    entity_usage = defaultdict(int)
    used_entity_types = set()
    
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        
        print(f"   • Dataset records analyzed: {len(dataset):,}")
        
        for record in dataset:
            entities = record.get('entities', [])
            for entity_info in entities:
                entity_type = entity_info.get('type')
                if entity_type:
                    entity_usage[entity_type] += 1
                    used_entity_types.add(entity_type)
        
        total_instances = sum(entity_usage.values())
        print(f"   • Total entity instances: {total_instances:,}")
        
        return dict(entity_usage), used_entity_types
        
    except Exception as e:
        print(f"❌ Error analyzing dataset: {e}")
        sys.exit(1)


def analyze_missing_entities(missing_entities: Set[str]) -> None:
    """Provide detailed analysis of why specific entities are missing."""
    
    entity_analysis = {
        "AMOUNT": {
            "definition": "Represents quantities, measurements, monetary values",
            "examples": ["$500", "50 items", "75%", "3.2 million", "150 pounds"],
            "cause": "Templates use DURATION for time, MONEY for currency - missing general quantities",
            "impact": "Generic quantity expressions not captured",
            "difficulty": "Easy - add to existing templates"
        },
        "INDUSTRY": {
            "definition": "Represents business sectors, professional domains", 
            "examples": ["healthcare", "technology", "manufacturing", "retail", "finance"],
            "cause": "Templates use BUSINESS for companies - missing industry sectors",
            "impact": "Professional context and sector-specific content not captured",
            "difficulty": "Easy - add to work-related templates"
        }
    }
    
    for entity_type in sorted(missing_entities):
        analysis = entity_analysis.get(entity_type, {
            "definition": "Entity type definition not analyzed",
            "examples": ["Examples not provided"],
            "cause": "Cause not analyzed",
            "impact": "Impact not analyzed", 
            "difficulty": "Unknown"
        })
        
        print(f"\n   📋 {entity_type}:")
        print(f"      • Definition: {analysis['definition']}")
        print(f"      • Examples: {', '.join(analysis['examples'])}")
        print(f"      • Why missing: {analysis['cause']}")
        print(f"      • Impact: {analysis['impact']}")
        print(f"      • Fix difficulty: {analysis['difficulty']}")


def provide_actionable_recommendations(missing_entities: Set[str]) -> None:
    """Provide specific, actionable recommendations."""
    
    if not missing_entities:
        print("   ✅ No recommendations needed - perfect coverage achieved!")
        return
    
    print(f"\n   🎯 IMMEDIATE ACTIONS (High Priority):")
    print(f"   1. Enhance FirstPersonRareEntityTypesTemplate:")
    
    if "AMOUNT" in missing_entities:
        print(f"      • Add AMOUNT entity type:")
        print(f'        amount = random.choice(["$500", "50 items", "75%", "3.2 million"])')
        print(f'        "amount1": (EntityTypes.AMOUNT, amount)')
    
    if "INDUSTRY" in missing_entities:
        print(f"      • Add INDUSTRY entity type:")
        print(f'        industry = random.choice(["healthcare", "technology", "retail"])')
        print(f'        "industry1": (EntityTypes.INDUSTRY, industry)')
    
    print(f"\n   📝 TEMPLATE ENHANCEMENTS (Medium Priority):")
    print(f"   2. Create dedicated templates for missing entities")
    print(f"   3. Enhance FirstPersonComprehensiveCoverageTemplate")
    print(f"   4. Add missing entities to work-related templates")
    
    print(f"\n   🔧 VALIDATION IMPROVEMENTS (Low Priority):")
    print(f"   5. Add pre-generation coverage validation")
    print(f"   6. Implement real-time coverage tracking")
    print(f"   7. Set 100% coverage requirement")


def create_implementation_plan(missing_entities: Set[str]) -> None:
    """Create a detailed implementation plan."""
    
    if not missing_entities:
        print("   ✅ No implementation needed - perfect coverage achieved!")
        return
    
    print(f"\n   Phase 1: Quick Fixes (Est. 30 minutes)")
    print(f"   ├── Locate FirstPersonRareEntityTypesTemplate in data.py")
    print(f"   ├── Add missing entity type variables and entity definitions")
    print(f"   ├── Update text template to include new entities")
    print(f"   └── Test generation with small dataset")
    
    print(f"\n   Phase 2: Validation (Est. 15 minutes)")
    print(f"   ├── Run entity_analysis.py to verify coverage")
    print(f"   ├── Generate test dataset (1000 records)")
    print(f"   ├── Confirm 100% entity coverage achieved")
    print(f"   └── Document the fix")
    
    print(f"\n   Phase 3: Full Dataset (Est. 60 minutes)")
    print(f"   ├── Generate full dataset with enhanced templates")
    print(f"   ├── Run comprehensive analysis")
    print(f"   ├── Verify 100% coverage maintained")
    print(f"   └── Update documentation")
    
    print(f"\n   📅 Total Estimated Time: 1.75 hours")
    print(f"   🎯 Expected Outcome: 100% entity coverage (68/68)")


def main():
    """Main function to run the comprehensive analysis."""
    missing_entities = run_comprehensive_analysis()
    
    print(f"\n" + "="*80)
    if missing_entities:
        print(f"🔧 NEXT STEPS: Implement the recommendations above to achieve 100% coverage")
    else:
        print(f"🎉 PERFECT COVERAGE: No action required!")
    print(f"="*80)


if __name__ == "__main__":
    main()
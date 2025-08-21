#!/usr/bin/env python3
"""
Entity Coverage Analysis Tool

This script analyzes the generated dataset to identify which entity types
are missing from the 68 total entity types defined in the EntityTypes class.
It provides comprehensive analysis including usage statistics and recommendations.
"""

import json
import sys
from collections import defaultdict, Counter
from typing import Dict, Set, List, Tuple
from data import EntityTypes


def extract_all_entity_types() -> Set[str]:
    """Extract all 68 entity types from the EntityTypes class."""
    return {attr for attr in dir(EntityTypes) if not attr.startswith('_')}


def analyze_dataset_entity_usage(dataset_path: str) -> Tuple[Dict[str, int], Set[str]]:
    """
    Analyze the dataset to count entity type usage.
    
    Returns:
        - Dictionary mapping entity types to their usage counts
        - Set of entity types actually used in the dataset
    """
    entity_usage = defaultdict(int)
    used_entity_types = set()
    
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        
        print(f"📊 Analyzing {len(dataset)} records from dataset...")
        
        for record in dataset:
            entities = record.get('entities', [])
            # Handle both list and dict formats for entities
            if isinstance(entities, list):
                for entity_info in entities:
                    entity_type = entity_info.get('type')
                    if entity_type:
                        entity_usage[entity_type] += 1
                        used_entity_types.add(entity_type)
            elif isinstance(entities, dict):
                for entity_id, entity_info in entities.items():
                    entity_type = entity_info.get('type')
                    if entity_type:
                        entity_usage[entity_type] += 1
                        used_entity_types.add(entity_type)
        
        return dict(entity_usage), used_entity_types
        
    except FileNotFoundError:
        print(f"❌ Error: Dataset file '{dataset_path}' not found!")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in dataset file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading dataset: {e}")
        sys.exit(1)


def generate_coverage_report(all_entity_types: Set[str], 
                           used_entity_types: Set[str],
                           entity_usage: Dict[str, int]) -> None:
    """Generate comprehensive entity coverage report."""
    
    missing_entity_types = all_entity_types - used_entity_types
    
    print("\n" + "="*80)
    print("🔍 ENTITY COVERAGE ANALYSIS REPORT")
    print("="*80)
    
    print(f"\n📈 COVERAGE SUMMARY:")
    print(f"   • Total entity types defined: {len(all_entity_types)}")
    print(f"   • Entity types actually used: {len(used_entity_types)}")
    print(f"   • Entity types missing: {len(missing_entity_types)}")
    print(f"   • Coverage percentage: {len(used_entity_types)/len(all_entity_types)*100:.1f}%")
    
    if missing_entity_types:
        print(f"\n❌ MISSING ENTITY TYPES ({len(missing_entity_types)}):")
        for i, entity_type in enumerate(sorted(missing_entity_types), 1):
            print(f"   {i}. {entity_type}")
    else:
        print(f"\n✅ ALL ENTITY TYPES ARE COVERED!")
    
    print(f"\n✅ USED ENTITY TYPES ({len(used_entity_types)}):")
    # Sort by usage count (descending), then alphabetically
    sorted_used = sorted(used_entity_types, 
                        key=lambda x: (-entity_usage.get(x, 0), x))
    
    for i, entity_type in enumerate(sorted_used, 1):
        count = entity_usage.get(entity_type, 0)
        print(f"   {i:2}. {entity_type:<25} (used {count:,} times)")
    
    print(f"\n📊 USAGE STATISTICS:")
    total_entity_instances = sum(entity_usage.values())
    print(f"   • Total entity instances: {total_entity_instances:,}")
    print(f"   • Average instances per type: {total_entity_instances/len(used_entity_types):.1f}")
    
    # Show distribution
    usage_counts = list(entity_usage.values())
    usage_counts.sort(reverse=True)
    
    print(f"   • Most used entity type: {usage_counts[0]:,} instances")
    print(f"   • Least used entity type: {usage_counts[-1]:,} instances")
    print(f"   • Median usage: {usage_counts[len(usage_counts)//2]:,} instances")


def analyze_why_entities_missing(missing_entity_types: Set[str]) -> None:
    """Analyze why certain entity types might be missing."""
    
    if not missing_entity_types:
        print("\n🎉 NO MISSING ENTITIES - PERFECT COVERAGE!")
        return
    
    print(f"\n🔍 ANALYSIS: Why are {len(missing_entity_types)} entity types missing?")
    print("-" * 60)
    
    # Categorize missing entities by likely cause
    rare_entities = set()
    template_gaps = set()
    
    for entity_type in missing_entity_types:
        # These are likely candidates for rare/specialized entities
        if entity_type in ['MEMORY_TYPE', 'LIFE_STAGE', 'CULTURAL_ELEMENT', 
                          'LEARNING_METHOD', 'PERSONAL_GROWTH', 'COMMUNITY_ROLE',
                          'GEOPOLITICAL_ENTITY', 'RECURRING_SCHEDULE', 'START_TIME', 
                          'END_TIME', 'NICKNAME', 'RELATIONSHIP_TYPE']:
            rare_entities.add(entity_type)
        else:
            template_gaps.add(entity_type)
    
    if rare_entities:
        print(f"\n🔸 RARE/SPECIALIZED ENTITIES ({len(rare_entities)}):")
        print("   These entities may need dedicated templates:")
        for entity in sorted(rare_entities):
            print(f"     • {entity}")
    
    if template_gaps:
        print(f"\n🔸 TEMPLATE GAPS ({len(template_gaps)}):")
        print("   These entities may need more template coverage:")
        for entity in sorted(template_gaps):
            print(f"     • {entity}")


def provide_recommendations(missing_entity_types: Set[str]) -> None:
    """Provide actionable recommendations for improving coverage."""
    
    print(f"\n💡 RECOMMENDATIONS FOR 100% COVERAGE:")
    print("-" * 50)
    
    if not missing_entity_types:
        print("✅ Perfect coverage achieved! No recommendations needed.")
        return
    
    print("1. 📝 CREATE DEDICATED TEMPLATES:")
    print("   Consider creating templates specifically for missing entity types:")
    for entity_type in sorted(missing_entity_types):
        print(f"     • Add template using {entity_type}")
    
    print("\n2. 🔧 ENHANCE EXISTING TEMPLATES:")
    print("   • Review FirstPersonRareEntityTypesTemplate")
    print("   • Review FirstPersonComprehensiveCoverageTemplate")
    print("   • Add missing entity types to these comprehensive templates")
    
    print("\n3. 📊 BALANCE GENERATION PROBABILITY:")
    print("   • Use BalancedTemplateManager to prioritize missing entity types")
    print("   • Add scoring bonus for uncovered entity types")
    
    print("\n4. 🧪 VALIDATION IMPROVEMENTS:")
    print("   • Run validate_comprehensive_coverage() before generation")
    print("   • Add entity coverage tracking during generation")
    print("   • Set minimum coverage threshold (e.g., 100%)")


def main():
    """Main analysis function."""
    
    print("🚀 Entity Coverage Analysis Tool")
    print("=" * 50)
    
    # Step 1: Extract all entity types
    print("📋 Step 1: Extracting all entity types from EntityTypes class...")
    all_entity_types = extract_all_entity_types()
    print(f"   Found {len(all_entity_types)} total entity types")
    
    # Step 2: Analyze dataset
    dataset_path = "DeBERTa_finetuning_dataset_expanded_relations.json"
    print(f"📊 Step 2: Analyzing dataset '{dataset_path}'...")
    entity_usage, used_entity_types = analyze_dataset_entity_usage(dataset_path)
    
    # Step 3: Generate comprehensive report
    print("📈 Step 3: Generating coverage report...")
    generate_coverage_report(all_entity_types, used_entity_types, entity_usage)
    
    # Step 4: Analyze why entities are missing
    missing_entity_types = all_entity_types - used_entity_types
    analyze_why_entities_missing(missing_entity_types)
    
    # Step 5: Provide recommendations
    provide_recommendations(missing_entity_types)
    
    print(f"\n🎯 SUMMARY: {len(missing_entity_types)} out of {len(all_entity_types)} entity types are missing")
    if missing_entity_types:
        print(f"Missing entities: {', '.join(sorted(missing_entity_types))}")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
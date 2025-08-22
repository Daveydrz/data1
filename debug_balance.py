#!/usr/bin/env python3
"""
Debug script to analyze balance distribution in detail.
"""

import data
import collections

def analyze_balance():
    print("🔍 Analyzing Balance Distribution")
    print("=" * 50)
    
    # Generate a dataset and analyze distribution using improved manager
    result = data.generate_improved_balanced_dataset(num_records=200)
    dataset = result["dataset"]
    manager = result["metadata"]["balance_manager"]
    
    print(f"\n📊 Distribution Analysis:")
    
    # Analyze entity distribution
    entity_usage = manager["entity_usage"]
    entity_counts = [count for count in entity_usage.values() if count > 0]
    
    print(f"\nEntity Type Distribution:")
    print(f"  Total entity types: {len(entity_usage)}")
    print(f"  Used entity types: {len(entity_counts)}")
    print(f"  Min usage: {min(entity_counts) if entity_counts else 0}")
    print(f"  Max usage: {max(entity_counts) if entity_counts else 0}")
    print(f"  Average usage: {sum(entity_counts) / len(entity_counts) if entity_counts else 0:.1f}")
    
    if entity_counts:
        entity_ratio = min(entity_counts) / max(entity_counts)
        print(f"  Balance ratio: {entity_ratio:.3f} ({entity_ratio * 100:.1f}%)")
    
    # Analyze relation distribution  
    relation_usage = manager["relation_usage"]
    relation_counts = [count for count in relation_usage.values() if count > 0]
    
    print(f"\nRelation Type Distribution:")
    print(f"  Total relation types: {len(relation_usage)}")
    print(f"  Used relation types: {len(relation_counts)}")
    print(f"  Min usage: {min(relation_counts) if relation_counts else 0}")
    print(f"  Max usage: {max(relation_counts) if relation_counts else 0}")
    print(f"  Average usage: {sum(relation_counts) / len(relation_counts) if relation_counts else 0:.1f}")
    
    if relation_counts:
        relation_ratio = min(relation_counts) / max(relation_counts)
        print(f"  Balance ratio: {relation_ratio:.3f} ({relation_ratio * 100:.1f}%)")
    
    # Show most and least used types
    entity_sorted = sorted(entity_usage.items(), key=lambda x: x[1], reverse=True)
    relation_sorted = sorted(relation_usage.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\nMost Used Entity Types:")
    for entity_type, count in entity_sorted[:10]:
        print(f"  {entity_type}: {count}")
    
    print(f"\nLeast Used Entity Types:")
    for entity_type, count in entity_sorted[-10:]:
        if count > 0:
            print(f"  {entity_type}: {count}")
    
    print(f"\nMost Used Relation Types:")
    for relation_type, count in relation_sorted[:10]:
        print(f"  {relation_type}: {count}")
    
    print(f"\nLeast Used Relation Types:")
    for relation_type, count in relation_sorted[-10:]:
        if count > 0:
            print(f"  {relation_type}: {count}")
    
    # Calculate the 3x rule compliance
    if entity_counts and relation_counts:
        entity_max = max(entity_counts)
        entity_min = min(entity_counts)
        relation_max = max(relation_counts)
        relation_min = min(relation_counts)
        
        entity_3x_compliant = entity_max <= entity_min * 3
        relation_3x_compliant = relation_max <= relation_min * 3
        
        print(f"\n3x Rule Compliance:")
        print(f"  Entity types: {'✅ PASS' if entity_3x_compliant else '❌ FAIL'} (max={entity_max}, min={entity_min}, ratio={entity_max/entity_min:.1f}x)")
        print(f"  Relation types: {'✅ PASS' if relation_3x_compliant else '❌ FAIL'} (max={relation_max}, min={relation_min}, ratio={relation_max/relation_min:.1f}x)")
        
        overall_compliant = entity_3x_compliant and relation_3x_compliant
        print(f"  Overall: {'✅ COMPLIANT' if overall_compliant else '❌ NOT COMPLIANT'}")

if __name__ == "__main__":
    analyze_balance()
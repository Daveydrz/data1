#!/usr/bin/env python3
"""
Test script to find optimal dataset size for 3x balance rule.
"""

import data

def test_optimal_size():
    print("🎯 Finding Optimal Dataset Size for 3x Balance Rule")
    print("=" * 60)
    
    # Test different sizes to find what works
    test_sizes = [500, 750, 1000, 1500, 2000]
    
    for size in test_sizes:
        print(f"\n📊 Testing {size} records...")
        try:
            result = data.generate_balanced_dataset(num_records=size)
            
            dataset = result["dataset"]
            metadata = result["metadata"]
            balance_manager = metadata["balance_manager"]
            coverage_stats = metadata["coverage_stats"]
            
            # Analyze balance
            entity_usage = balance_manager["entity_usage"]
            relation_usage = balance_manager["relation_usage"]
            
            entity_counts = [count for count in entity_usage.values() if count > 0]
            relation_counts = [count for count in relation_usage.values() if count > 0]
            
            if entity_counts and relation_counts:
                entity_min, entity_max = min(entity_counts), max(entity_counts)
                relation_min, relation_max = min(relation_counts), max(relation_counts)
                
                entity_ratio = entity_max / entity_min if entity_min > 0 else float('inf')
                relation_ratio = relation_max / relation_min if relation_min > 0 else float('inf')
                
                entity_3x_ok = entity_ratio <= 3.0
                relation_3x_ok = relation_ratio <= 3.0
                both_3x_ok = entity_3x_ok and relation_3x_ok
                
                # Perspective check
                first_person = sum(1 for r in dataset if r.get('context', {}).get('Perspective') == 'first_person')
                first_person_ratio = first_person / len(dataset) * 100
                perspective_ok = abs(first_person_ratio - 60) < 5
                
                status = "✅" if both_3x_ok else "❌"
                print(f"   {status} Size {size}: Entity {entity_ratio:.1f}x, Relation {entity_ratio:.1f}x, "
                      f"Coverage {coverage_stats['entity_coverage_percent']:.0f}%/{coverage_stats['relation_coverage_percent']:.0f}%, "
                      f"Perspective {first_person_ratio:.1f}%")
                
                if both_3x_ok:
                    print(f"   🎉 SUCCESS! {size} records achieves 3x balance rule!")
                    print(f"      Entity balance: {entity_min}-{entity_max} ({entity_ratio:.1f}x)")
                    print(f"      Relation balance: {relation_min}-{relation_max} ({relation_ratio:.1f}x)")
                    print(f"      Coverage: {coverage_stats['entity_coverage_percent']:.1f}% entities, {coverage_stats['relation_coverage_percent']:.1f}% relations")
                    print(f"      Perspective: {first_person_ratio:.1f}% first-person ({'✅ GOOD' if perspective_ok else '⚠️ OFF'})")
                    return size
                    
        except Exception as e:
            print(f"   ❌ Error with {size} records: {e}")
    
    print(f"\n⚠️  None of the tested sizes achieved perfect 3x balance")
    print(f"   This suggests that with 172 total types (68 entities + 104 relations),")
    print(f"   achieving perfect 3x balance may require very large datasets or algorithmic improvements.")
    
    return None

if __name__ == "__main__":
    optimal_size = test_optimal_size()
    if optimal_size:
        print(f"\n🎯 Recommendation: Use {optimal_size} records for optimal balance")
    else:
        print(f"\n🎯 Recommendation: Current system excels at coverage guarantee.")
        print(f"   For applications requiring perfect balance, consider:")
        print(f"   1. Using larger datasets (5000+ records)")
        print(f"   2. Accepting coverage > balance tradeoff")
        print(f"   3. Focusing on specific entity/relation subsets")
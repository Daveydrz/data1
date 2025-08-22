#!/usr/bin/env python3
"""
Test script with larger dataset to validate balance.
"""

import data

def test_larger_dataset():
    print("🧪 Testing with Larger Dataset for Better Balance")
    print("=" * 60)
    
    # Test with 1000 records for better balance potential
    try:
        result = data.generate_balanced_dataset(num_records=1000)
        
        dataset = result["dataset"]
        stats = result["statistics"]
        metadata = result["metadata"]
        balance_manager = metadata["balance_manager"]
        
        print(f"\n📊 FINAL RESULTS:")
        print(f"✅ Generated {len(dataset)} records")
        
        # Check coverage
        coverage_stats = metadata["coverage_stats"]
        print(f"🎯 Entity coverage: {coverage_stats['entity_coverage_percent']:.1f}%")
        print(f"🎯 Relation coverage: {coverage_stats['relation_coverage_percent']:.1f}%")
        print(f"⚖️ Overall balance: {coverage_stats['balance_score']:.1f}%")
        
        # Detailed balance analysis
        entity_usage = balance_manager["entity_usage"]
        relation_usage = balance_manager["relation_usage"]
        
        entity_counts = [count for count in entity_usage.values() if count > 0]
        relation_counts = [count for count in relation_usage.values() if count > 0]
        
        if entity_counts and relation_counts:
            entity_min, entity_max = min(entity_counts), max(entity_counts)
            relation_min, relation_max = min(relation_counts), max(relation_counts)
            
            entity_ratio = entity_max / entity_min if entity_min > 0 else float('inf')
            relation_ratio = relation_max / relation_min if relation_min > 0 else float('inf')
            
            print(f"\n📈 Balance Analysis:")
            print(f"Entity types: min={entity_min}, max={entity_max}, ratio={entity_ratio:.1f}x")
            print(f"Relation types: min={relation_min}, max={relation_max}, ratio={relation_ratio:.1f}x")
            
            # Check 3x rule compliance
            entity_3x_ok = entity_ratio <= 3.0
            relation_3x_ok = relation_ratio <= 3.0
            
            print(f"\n🎯 3x Rule Compliance:")
            print(f"Entity types: {'✅ PASS' if entity_3x_ok else '❌ FAIL'} ({entity_ratio:.1f}x)")
            print(f"Relation types: {'✅ PASS' if relation_3x_ok else '❌ FAIL'} ({relation_ratio:.1f}x)")
            print(f"Overall: {'✅ COMPLIANT' if entity_3x_ok and relation_3x_ok else '❌ NOT COMPLIANT'}")
            
            # Show distribution stats
            entity_avg = sum(entity_counts) / len(entity_counts)
            relation_avg = sum(relation_counts) / len(relation_counts)
            
            print(f"\n📊 Distribution Statistics:")
            print(f"Entity types: avg={entity_avg:.1f}, coverage={len(entity_counts)}/68")
            print(f"Relation types: avg={relation_avg:.1f}, coverage={len(relation_counts)}/104")
        
        # Check perspective distribution
        first_person = sum(1 for r in dataset if r.get('context', {}).get('Perspective') == 'first_person')
        third_person = len(dataset) - first_person
        first_person_ratio = first_person / len(dataset) * 100
        
        print(f"\n👤 Perspective Distribution:")
        print(f"First-person: {first_person} ({first_person_ratio:.1f}%)")
        print(f"Third-person: {third_person} ({100-first_person_ratio:.1f}%)")
        print(f"Target ratio: {'✅ GOOD' if abs(first_person_ratio - 60) < 5 else '⚠️ OFF TARGET'}")
        
        # Final assessment
        success_criteria = [
            ("100% Entity Coverage", coverage_stats['entity_coverage_percent'] >= 100),
            ("100% Relation Coverage", coverage_stats['relation_coverage_percent'] >= 100),
            ("Entity 3x Rule", entity_3x_ok if entity_counts else False),
            ("Relation 3x Rule", relation_3x_ok if relation_counts else False),
            ("Perspective Ratio", abs(first_person_ratio - 60) < 5)
        ]
        
        print(f"\n🎉 SUCCESS CRITERIA:")
        all_passed = True
        for criterion, passed in success_criteria:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{criterion}: {status}")
            if not passed:
                all_passed = False
        
        print(f"\nOVERALL: {'🎉 ALL CRITERIA MET!' if all_passed else '⚠️ SOME CRITERIA NOT MET'}")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_larger_dataset()
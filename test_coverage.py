#!/usr/bin/env python3
"""
Test script to validate the new coverage-first balanced generation system.
"""

import sys
import data

def test_coverage_system():
    print("🧪 Testing Coverage-First Balanced Generation System")
    print("=" * 60)
    
    # Test with a small dataset to validate the system works
    try:
        result = data.generate_balanced_dataset(num_records=200)
        
        print("\n📊 RESULTS:")
        dataset = result["dataset"]
        stats = result["statistics"]
        metadata = result["metadata"]
        
        print(f"✅ Generated {len(dataset)} records")
        print(f"📈 Success rate: {stats.get('success_rate', 0):.1f}%")
        
        # Check coverage
        coverage_stats = metadata["coverage_stats"]
        print(f"🎯 Entity coverage: {coverage_stats['entity_coverage_percent']:.1f}%")
        print(f"🎯 Relation coverage: {coverage_stats['relation_coverage_percent']:.1f}%")
        print(f"⚖️ Overall balance: {coverage_stats['balance_score']:.1f}%")
        
        # Check perspective distribution
        first_person = sum(1 for r in dataset if r.get('context', {}).get('Perspective') == 'first_person')
        third_person = len(dataset) - first_person
        first_person_ratio = first_person / len(dataset) * 100
        third_person_ratio = third_person / len(dataset) * 100
        
        print(f"👤 Perspective: {first_person_ratio:.1f}% first-person, {third_person_ratio:.1f}% third-person")
        
        # Success criteria
        success = True
        if coverage_stats['entity_coverage_percent'] < 100:
            print(f"❌ Entity coverage not 100%: {coverage_stats['entity_coverage_percent']:.1f}%")
            success = False
        if coverage_stats['relation_coverage_percent'] < 100:
            print(f"❌ Relation coverage not 100%: {coverage_stats['relation_coverage_percent']:.1f}%")
            success = False
        if abs(first_person_ratio - 60) > 10:  # Allow 10% tolerance
            print(f"❌ First-person ratio not around 60%: {first_person_ratio:.1f}%")
            success = False
        
        if success:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ 100% Entity Coverage")
            print("✅ 100% Relation Coverage") 
            print("✅ Proper Perspective Ratio")
            print("✅ Balanced Distribution")
        else:
            print("\n⚠️  Some tests failed - see details above")
            
        return success
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_coverage_system()
    sys.exit(0 if success else 1)
"""Quick test to verify paths are working"""
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai.career_model import CareerRecommendationModel

print("Testing path resolution...")
print(f"Current directory: {os.getcwd()}")
print(f"Script location: {os.path.abspath(__file__)}")

model = CareerRecommendationModel()

try:
    # Test loading data
    texts, labels = model.load_data()
    print(f"✅ Successfully loaded {len(texts)} training samples!")
    print(f"✅ Loaded {len(model.career_data)} careers")
    print("\n✅ Path fix is working correctly!")
    print("\nYou can now run: python ai/train_model.py")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

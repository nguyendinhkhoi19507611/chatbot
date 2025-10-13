"""
Main training script for the career recommendation model
Run this script to train the AI model
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.career_model import train_and_evaluate

if __name__ == '__main__':
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   CAREER CHATBOT - AI MODEL TRAINING SCRIPT             ║")
    print("║   Ứng dụng AI trong Chatbot tư vấn hướng nghiệp         ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print("\n")
    
    try:
        model, metrics = train_and_evaluate()
        
        print("\n✅ Training completed successfully!")
        print("\nYou can now run the backend server to use the trained model.")
        
    except Exception as e:
        print(f"\n❌ Error during training: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

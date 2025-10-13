"""
Career Recommendation Model using Machine Learning
Trains a model to recommend careers based on user interests
"""

import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from datetime import datetime

class CareerRecommendationModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        self.label_encoder = LabelEncoder()
        self.career_data = None
        self.model_metrics = {}
        
    def load_data(self, career_data_path=None, training_data_path=None):
        """Load career and training data"""
        print("Loading data...")
        
        # Get absolute paths relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(current_dir)
        
        if career_data_path is None:
            career_data_path = os.path.join(backend_dir, 'data', 'career_data.json')
        if training_data_path is None:
            training_data_path = os.path.join(backend_dir, 'data', 'training_data.json')
        
        # Load career information
        with open(career_data_path, 'r', encoding='utf-8') as f:
            career_json = json.load(f)
            self.career_data = career_json['careers']
        
        # Load training samples
        with open(training_data_path, 'r', encoding='utf-8') as f:
            training_json = json.load(f)
            training_samples = training_json['training_samples']
        
        # Prepare training data
        texts = []
        labels = []
        
        for sample in training_samples:
            # Combine user input and interests into text
            text = sample['user_input'] + ' ' + ' '.join(sample['interests'])
            texts.append(text)
            labels.append(sample['recommended_career_id'])
        
        # Augment data with career descriptions and synthetic patterns
        for career in self.career_data:
            base_text = career['description'] + ' ' + ' '.join(career['interests'])
            texts.append(base_text)
            labels.append(career['id'])

            # Simple synthetic augmentation (synonyms / prompts)
            prompts = [
                f"Tôi thích {', '.join(career['interests'][:2])} và quan tâm nghề {career['name']}",
                f"Công việc phù hợp với sở thích {', '.join(career['interests'][:3])}",
                f"Tôi muốn trở thành {career['name_en']}"
            ]
            for p in prompts:
                texts.append(p)
                labels.append(career['id'])
        
        print(f"Loaded {len(texts)} training samples")
        return texts, labels
    
    def train(self, texts, labels):
        """Train the career recommendation model"""
        print("\n" + "="*60)
        print("TRAINING CAREER RECOMMENDATION MODEL")
        print("="*60)
        
        # Encode labels BEFORE splitting to include all classes
        print("\nEncoding labels...")
        labels_enc = self.label_encoder.fit_transform(labels)
        
        # Split data (no stratify due to small dataset)
        X_train, X_test, y_train_enc, y_test_enc = train_test_split(
            texts, labels_enc, test_size=0.15, random_state=42
        )
        
        print(f"\nTraining set size: {len(X_train)}")
        print(f"Test set size: {len(X_test)}")
        
        # Vectorize text
        print("\nVectorizing text data...")
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        # Train model
        print("\nTraining Random Forest model...")
        self.model.fit(X_train_vec, y_train_enc)
        
        # Evaluate on training set
        y_train_pred = self.model.predict(X_train_vec)
        train_accuracy = accuracy_score(y_train_enc, y_train_pred)
        
        # Evaluate on test set
        print("\nEvaluating model...")
        y_pred = self.model.predict(X_test_vec)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test_enc, y_pred)
        precision = precision_score(y_test_enc, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test_enc, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test_enc, y_pred, average='weighted', zero_division=0)
        
        # Store metrics
        self.model_metrics = {
            'train_accuracy': train_accuracy,
            'test_accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'training_samples': len(texts)
        }
        
        # Print results
        print("\n" + "="*60)
        print("MODEL EVALUATION RESULTS")
        print("="*60)
        print(f"Training Accuracy:   {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
        print(f"Test Accuracy:       {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"Precision (weighted): {precision:.4f} ({precision*100:.2f}%)")
        print(f"Recall (weighted):    {recall:.4f} ({recall*100:.2f}%)")
        print(f"F1 Score (weighted):  {f1:.4f} ({f1*100:.2f}%)")
        
        print("\n" + "-"*60)
        print("CLASSIFICATION REPORT")
        print("-"*60)
        
        # Get unique classes in test set
        unique_test_classes = np.unique(y_test_enc)
        target_names = [self.get_career_name(self.label_encoder.classes_[i]) for i in unique_test_classes]
        print(classification_report(y_test_enc, y_pred, labels=unique_test_classes, target_names=target_names, zero_division=0))
        
        print("\n" + "-"*60)
        print("CONFUSION MATRIX")
        print("-"*60)
        cm = confusion_matrix(y_test_enc, y_pred)
        print(cm)
        
        return self.model_metrics
    
    def get_career_name(self, career_id):
        """Get career name by ID"""
        for career in self.career_data:
            if career['id'] == career_id:
                return career['name'][:20]  # Truncate for display
        return f"Career_{career_id}"
    
    def predict(self, user_text, top_n=3):
        """Predict top N career recommendations"""
        # Vectorize input
        X = self.vectorizer.transform([user_text])
        
        # Get prediction probabilities
        probas = self.model.predict_proba(X)[0]
        
        # Get top N predictions
        top_indices = np.argsort(probas)[-top_n:][::-1]
        
        recommendations = []
        for idx in top_indices:
            career_id = self.label_encoder.classes_[idx]
            confidence = probas[idx]
            
            # Find career details
            career_info = next((c for c in self.career_data if c['id'] == career_id), None)
            
            if career_info:
                recommendations.append({
                    'career_id': career_id,
                    'career_name': career_info['name'],
                    'description': career_info['description'],
                    'confidence': float(confidence),
                    'interests': career_info['interests'],
                    'skills': career_info['skills'],
                    'salary_range': career_info['salary_range'],
                    'education': career_info['education']
                })
        
        return recommendations
    
    def save_model(self, model_dir=None):
        """Save trained model and artifacts"""
        if model_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_dir = os.path.join(current_dir, 'models')
        
        os.makedirs(model_dir, exist_ok=True)
        
        print(f"\nSaving model to {model_dir}...")
        
        # Save model
        joblib.dump(self.model, os.path.join(model_dir, 'career_model.pkl'))
        joblib.dump(self.vectorizer, os.path.join(model_dir, 'vectorizer.pkl'))
        joblib.dump(self.label_encoder, os.path.join(model_dir, 'label_encoder.pkl'))
        
        # Save career data
        with open(os.path.join(model_dir, 'career_data.json'), 'w', encoding='utf-8') as f:
            json.dump(self.career_data, f, ensure_ascii=False, indent=2)
        
        # Save metrics
        with open(os.path.join(model_dir, 'model_metrics.json'), 'w', encoding='utf-8') as f:
            json.dump(self.model_metrics, f, ensure_ascii=False, indent=2)
        
        print("Model saved successfully!")
    
    def load_model(self, model_dir=None):
        """Load trained model and artifacts"""
        if model_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_dir = os.path.join(current_dir, 'models')
        
        print(f"Loading model from {model_dir}...")
        
        self.model = joblib.load(os.path.join(model_dir, 'career_model.pkl'))
        self.vectorizer = joblib.load(os.path.join(model_dir, 'vectorizer.pkl'))
        self.label_encoder = joblib.load(os.path.join(model_dir, 'label_encoder.pkl'))
        
        # Load career data
        with open(os.path.join(model_dir, 'career_data.json'), 'r', encoding='utf-8') as f:
            self.career_data = json.load(f)
        
        # Load metrics
        try:
            with open(os.path.join(model_dir, 'model_metrics.json'), 'r', encoding='utf-8') as f:
                self.model_metrics = json.load(f)
        except:
            self.model_metrics = {}
        
        print("Model loaded successfully!")


def train_and_evaluate():
    """Main function to train and evaluate the model"""
    print("\n" + "="*60)
    print("CAREER RECOMMENDATION AI MODEL TRAINING")
    print("="*60)
    
    # Create model
    model = CareerRecommendationModel()
    
    # Load data
    texts, labels = model.load_data()
    
    # Train model
    metrics = model.train(texts, labels)
    
    # Save model
    model.save_model()
    
    # Test predictions
    print("\n" + "="*60)
    print("TESTING PREDICTIONS")
    print("="*60)
    
    test_cases = [
        "Tôi thích lập trình và xây dựng phần mềm",
        "Tôi yêu thích nghệ thuật và thiết kế",
        "Tôi muốn giúp đỡ người khác và chăm sóc sức khỏe",
        "Tôi thích phân tích dữ liệu và machine learning",
        "Tôi đam mê nấu ăn và sáng tạo món ăn mới"
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\nTest case {i}: \"{test_text}\"")
        recommendations = model.predict(test_text, top_n=3)
        print("Top 3 recommendations:")
        for j, rec in enumerate(recommendations, 1):
            print(f"  {j}. {rec['career_name']} (Confidence: {rec['confidence']*100:.2f}%)")
    
    print("\n" + "="*60)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"\nFinal Model Metrics:")
    print(f"  - Test Accuracy: {metrics['test_accuracy']*100:.2f}%")
    print(f"  - F1 Score: {metrics['f1_score']*100:.2f}%")
    print(f"  - Training Samples: {metrics['training_samples']}")
    print(f"  - Training Date: {metrics['training_date']}")
    
    return model, metrics


if __name__ == '__main__':
    model, metrics = train_and_evaluate()

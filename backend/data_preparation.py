import pandas as pd
import spacy
import os
import re
import numpy as np

def preprocess_text(text, nlp):
    """Tokenize, lemmatize, and remove punctuation."""
    if pd.isna(text) or not isinstance(text, str):
        return ""
    
    # Clean text
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Process with spaCy (limit text length for speed)
    if len(text) > 1000000:  # If text is very long, truncate
        text = text[:1000000]
    
    try:
        doc = nlp(text)
        tokens = [token.lemma_ for token in doc 
                  if not token.is_punct and not token.is_space 
                  and len(token.text) > 1 and not token.is_stop]
        return " ".join(tokens[:500])  # Limit tokens to prevent memory issues
    except:
        # Fallback to simple processing if spaCy fails
        words = text.split()
        return " ".join(words[:500])

def main():
    print("="*50)
    print("🚀 Data Preparation for CareerBuddy AI")
    print("="*50)
    
    # File paths
    dataset_path = "dataset.csv"
    output_path = "dataset_clean.csv"
    
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at {dataset_path}")
        return
    
    print(f"\n📊 Loading dataset: {dataset_path}")
    print(f"📏 File size: {os.path.getsize(dataset_path) / (1024*1024):.2f} MB")
    
    # Load the dataset
    print("\n🔄 Reading CSV file...")
    df = pd.read_csv(dataset_path, encoding='utf-8')
    print(f"✅ Dataset loaded with {len(df):,} rows and {len(df.columns)} columns")
    
    # Display column info
    print(f"\n📋 Columns in dataset:")
    for col in df.columns:
        print(f"  - {col}")
    
    # Check for missing values
    print(f"\n🔍 Missing values before cleaning:")
    missing_before = df.isnull().sum()
    for col in df.columns:
        if missing_before[col] > 0:
            print(f"  {col}: {missing_before[col]:,} missing ({missing_before[col]/len(df)*100:.1f}%)")
    
    # Drop rows with missing critical data
    critical_columns = ['job title', 'skills']
    existing_critical = [col for col in critical_columns if col in df.columns]
    
    if existing_critical:
        print(f"\n🧹 Dropping rows with missing values in: {existing_critical}")
        initial_rows = len(df)
        df.dropna(subset=existing_critical, inplace=True)
        print(f"✅ Removed {initial_rows - len(df):,} rows")
        print(f"📊 Rows after cleaning: {len(df):,}")
    
    # Remove duplicates
    print(f"\n🧹 Removing duplicates...")
    initial_rows = len(df)
    df.drop_duplicates(subset=['job title', 'skills'], inplace=True)
    print(f"✅ Removed {initial_rows - len(df):,} duplicate rows")
    print(f"📊 Rows after deduplication: {len(df):,}")
    
    # Sample if dataset is too large (for faster processing)
    if len(df) > 50000:
        print(f"\n📊 Dataset is large ({len(df):,} rows). Sampling 50,000 rows for faster processing...")
        df = df.sample(n=50000, random_state=42)
        print(f"✅ Sampled to {len(df):,} rows")
    
    # Convert text columns to lowercase
    print(f"\n🔧 Converting text to lowercase...")
    text_columns = ['job title', 'role', 'skills', 'company', 'qualifications']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower()
    
    # Create role column if missing
    if 'role' not in df.columns:
        print("📝 Creating 'role' column from 'job title'...")
        df['role'] = df['job title']
    
    # Create text features combining role and skills
    print(f"\n🔧 Creating text features...")
    df['text_features'] = df['role'].fillna('') + " " + df['skills'].fillna('')
    
    # Load spaCy (with error handling)
    print(f"\n🔧 Loading spaCy model...")
    try:
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy loaded successfully")
        
        # Process in smaller chunks to avoid memory issues
        print(f"\n🔄 Preprocessing text (this may take a few minutes)...")
        chunk_size = 1000
        processed_chunks = []
        
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i+chunk_size]
            print(f"  Processing chunk {i//chunk_size + 1}/{(len(df)-1)//chunk_size + 1}")
            
            # Apply preprocessing with progress tracking
            processed_texts = []
            for idx, text in enumerate(chunk['text_features']):
                if idx % 100 == 0 and idx > 0:
                    print(f"    Processed {idx}/{len(chunk)} in current chunk")
                processed_texts.append(preprocess_text(text, nlp))
            
            chunk = chunk.copy()
            chunk['processed_text'] = processed_texts
            processed_chunks.append(chunk)
        
        df = pd.concat(processed_chunks, ignore_index=True)
        
    except Exception as e:
        print(f"⚠️ spaCy preprocessing failed: {e}")
        print("Using simple preprocessing instead...")
        df['processed_text'] = df['text_features'].str.lower().str.replace(r'[^\w\s]', ' ', regex=True)
    
    # Save cleaned dataset
    print(f"\n💾 Saving cleaned dataset...")
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    # Show final stats
    print(f"\n✅ Data preparation complete!")
    print(f"📁 Cleaned dataset saved to: {output_path}")
    print(f"📊 Final dataset shape: {df.shape}")
    
    # Show sample
    print(f"\n📝 Sample of processed data:")
    sample_cols = ['job title', 'skills']
    existing_sample = [col for col in sample_cols if col in df.columns]
    if existing_sample:
        print(df[existing_sample + ['processed_text']].head(3))
    
    # Show class distribution
    print(f"\n📊 Job title distribution (top 10):")
    if 'job title' in df.columns:
        title_dist = df['job title'].value_counts().head(10)
        for title, count in title_dist.items():
            print(f"  {title}: {count:,} ({count/len(df)*100:.1f}%)")

if __name__ == "__main__":
    main()
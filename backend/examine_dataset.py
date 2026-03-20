import pandas as pd
import os

def examine_dataset():
    """Examine the structure of your dataset"""
    
    dataset_path = "dataset.csv"
    
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at {dataset_path}")
        return
    
    print(f"📊 Dataset found: {dataset_path}")
    print(f"📏 File size: {os.path.getsize(dataset_path) / (1024*1024):.2f} MB")
    
    # Try to read the dataset with different encodings
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            print(f"\n🔍 Trying encoding: {encoding}")
            
            # Read just the first few rows to check structure
            df = pd.read_csv(dataset_path, encoding=encoding, nrows=5)
            
            print(f"✅ Successfully read with {encoding} encoding")
            print(f"\n📋 Columns found: {list(df.columns)}")
            print(f"\n📝 First few rows:")
            print(df.head())
            print(f"\n📊 Data types:")
            print(df.dtypes)
            
            # Check for null values
            print(f"\n🔍 Null values in first 5 rows:")
            print(df.isnull().sum())
            
            # Save the encoding that works
            return encoding
            
        except Exception as e:
            print(f"❌ Failed with {encoding}: {str(e)[:100]}")
    
    print("\n❌ Could not read the dataset with any common encoding")
    return None

if __name__ == "__main__":
    encoding = examine_dataset()
    if encoding:
        print(f"\n✅ Use encoding: {encoding} for this dataset")
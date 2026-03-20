import pandas as pd
import random

def augment_dataset():
    """Create synthetic variations of the dataset for better training"""
    
    print("🚀 Augmenting dataset...")
    
    # Load cleaned dataset
    if not os.path.exists("dataset_clean.csv"):
        print("❌ dataset_clean.csv not found")
        return
    
    df = pd.read_csv("dataset_clean.csv")
    print(f"📊 Original dataset: {len(df)} rows")
    
    # Skill variations
    skill_variations = {
        "python": ["Python", "Python3", "Python Programming", "Python Development"],
        "javascript": ["JavaScript", "JS", "ECMAScript", "Javascript"],
        "java": ["Java", "Java 8", "Java 11", "Core Java"],
        "sql": ["SQL", "MySQL", "PostgreSQL", "Database"],
        "react": ["React", "ReactJS", "React.js"],
        "machine learning": ["Machine Learning", "ML", "Deep Learning"],
        "data science": ["Data Science", "Data Analysis", "Analytics"],
        "aws": ["AWS", "Amazon Web Services", "Cloud Computing"],
        "docker": ["Docker", "Containerization"],
        "kubernetes": ["Kubernetes", "K8s"]
    }
    
    # Create variations
    augmented_rows = []
    
    for idx, row in df.iterrows():
        # Add original
        augmented_rows.append(row.to_dict())
        
        # Create 2 variations of each row
        for var_num in range(2):
            new_row = row.to_dict().copy()
            
            # Vary skills
            if pd.notna(row.get('skills', '')):
                skills = str(row['skills']).lower()
                for orig, alts in skill_variations.items():
                    if orig in skills and random.random() > 0.5:
                        skills = skills.replace(orig, random.choice(alts).lower())
                new_row['skills'] = skills
            
            # Update text features
            if 'text_features' in new_row:
                new_row['text_features'] = str(new_row.get('role', '')) + " " + str(new_row.get('skills', ''))
            
            if 'processed_text' in new_row:
                new_row['processed_text'] = new_row['text_features']
            
            augmented_rows.append(new_row)
    
    # Create augmented dataframe
    augmented_df = pd.DataFrame(augmented_rows)
    print(f"✅ Augmented dataset: {len(augmented_df)} rows")
    
    # Save augmented dataset
    output_file = "dataset_augmented.csv"
    augmented_df.to_csv(output_file, index=False)
    print(f"💾 Saved to {output_file}")
    
    return augmented_df

if __name__ == "__main__":
    import os
    augment_dataset()
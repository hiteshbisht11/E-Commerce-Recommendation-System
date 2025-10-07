import pandas as pd
import os


def load_data(
    filepath="C:/Users/hp/Desktop/E-Commerce-Recommendation-System/data/raw/amazon_reviews.csv",
    sample_size=None,
):
    """
    Load Amazon reviews dataset with basic preprocessing

    Parameters:
    -----------
    file_path : str
        Path to the CSV file (default: 'data/raw/amazon_review.csv')
    sample_size : int, optional
        If specified, returns random sample of this size (useful for testing)

    Returns:
    --------
    pd.DataFrame
        Cleaned DataFrame with reviews data
    """

    print(filepath)
    print("inside load data")

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}")

    print("loading data from {file_path}....")

    df = pd.read_csv(filepath)

    print(f"initial shape : {df.shape}")
    print(f"columns : {df.columns.to_list()}")

    # Basic info before cleaning
    print("\n=== Data Overview ===")
    print(f"Total reviews: {len(df):,}")
    print(f"Missing values:\n{df.isnull().sum()}")

    # Basic cleaning
    # 1. Drop rows where essential columns are missing

    essential_cols = ["reviewerName", "overall", "reviewText"]
    df = df.dropna(subset=essential_cols)

    # 2. Ensure rating is numeric
    df["overall"] = pd.to_numeric(df["overall"], errors="coerce")
    df = df.dropna(subset="overall")

    try:
        df["reviewTime"] = pd.to_datetime(df["reviewTime"])
        print("review time converted to datetime")
    except:
        print("could not convert reviewtime to datetime")

    numerical_cols = [
        "helpful_yes",
        "helpful_no",
        "total_vote",
        "score_pos_neg_diff",
        "score_average_rating",
        "wilson_lower_bound",
        "day_diff",
    ]

    for col in numerical_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    print(f"after cleaning : {df.shape}")
    print(f"Reviews remaining : {len(df):,}")

    if sample_size and sample_size < len(df):
        df = df.sample(n=sample_size, random_state=42)
        print(f"sampled {sample_size:,} reviews")

    return df


def get_dataset_stats(file_path="data/raw/amazon_review.csv"):
    """
    Get comprehensive statistics about the dataset

    Parameters:
    -----------
    file_path : str
        Path to the CSV file

    Returns:
    --------
    dict
        Dictionary with dataset statistics
    """

    df = load_data(file_path)

    stats = {
        "total_reviews": len(df),
        "unique_reviewers": df["reviewerName"].nunique(),
        "avg_rating": df["overall"].mean(),
        "rating_distribution": df["overall"].value_counts().to_dict(),
        "reviews_with_text": df["reviewText"].notna().sum(),
        "date_range": (
            (df["reviewTime"].min(), df["reviewTime"].max())
            if "reviewTime" in df.columns
            else None
        ),
        "avg_helpful_votes": (
            df["helpful_yes"].mean() if "helpful_yes" in df.columns else None
        ),
    }

    print("\n=== Dataset Statistics ===")
    print(f"Total Reviews: {stats['total_reviews']:,}")
    print(f"Unique Reviewers: {stats['unique_reviewers']:,}")
    print(f"Average Rating: {stats['avg_rating']:.2f}")
    print(f"\nRating Distribution:")
    for rating, count in sorted(stats["rating_distribution"].items()):
        print(f"  {rating} stars: {count:,} ({count/stats['total_reviews']*100:.1f}%)")

    return stats


# def load_for_recommendations(file_path='data/raw/amazon_review.csv',
#                             min_reviews_per_user=3,
#                             min_reviews_per_product=5):
#     """
#     Load data specifically formatted for recommendation system

#     Parameters:
#     -----------
#     file_path : str
#         Path to the CSV file
#     min_reviews_per_user : int
#         Filter users with less than this many reviews
#     min_reviews_per_product : int
#         Filter products with less than this many reviews

#     Returns:
#     --------
#     pd.DataFrame
#         DataFrame with user_id, product_id, rating columns
#     """

#     print("Loading data for recommendation system...")

#     # Load base data
#     df = load_data(file_path)

#     # Create user_id and product_id from reviewerName and implicit product info
#     # Since we don't have explicit product IDs, we'll create them from review context
#     print("\n=== Preparing for Recommendations ===")

#     # For now, we'll use reviewerName as user_id
#     # Note: In real scenario, you'd need actual product IDs
#     df['user_id'] = df['reviewerName'].astype('category').cat.codes
#     df['rating'] = df['overall']

#     # We need product IDs - if not present, we'll need to extract/generate them
#     # This is a limitation of your dataset
#     print("⚠ WARNING: Dataset doesn't have explicit product_id column")
#     print("  You may need to add product information to build proper recommendations")

#     # Count reviews per user
#     user_counts = df['user_id'].value_counts()
#     valid_users = user_counts[user_counts >= min_reviews_per_user].index

#     df = df[df['user_id'].isin(valid_users)]

#     print(f"✓ Users with >= {min_reviews_per_user} reviews: {len(valid_users):,}")
#     print(f"✓ Final dataset size: {len(df):,}")

#     # Select relevant columns
#     rec_df = df[['user_id', 'rating', 'reviewText', 'reviewTime']].copy()

#     return rec_df


# def create_user_item_matrix(file_path='data/raw/amazon_review.csv'):
#     """
#     Create user-item interaction matrix (placeholder function)

#     Note: This function is incomplete because your dataset lacks product_id
#     You'll need to either:
#     1. Get a dataset with product IDs, OR
#     2. Extract product info from review text, OR
#     3. Use a different dataset

#     Returns:
#     --------
#     None (placeholder)
#     """
#     print("⚠ Cannot create user-item matrix without product_id column")
#     print("  Please use a dataset that includes product identifiers")
#     print("  Or we can help you extract product info from text")
#     return None


if __name__ == "__main__":
    print("Testing data loader...\n")
    df = load_data(sample_size=1000)
    print("\n" + "=" * 50)
    print("First few rows:")
    print(df.head())

    print("\n" + "=" * 50)
    print("Data types:")
    print(df.dtypes)

    print("\n" + "=" * 50)
    get_dataset_stats()

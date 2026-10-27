import pandas as pd


DATA_PATH = "data/raw/Music Info.csv"

def clean_data(data):
    """
    Cleans the input DataFrame by performing the following operations:
    1. Removes duplicate rows based on the 'spotify_id' column.
    2. Drops the 'genre' and 'spotify_id' columns.
    3. Fills missing values in the 'tags' column with the string 'no_tags'.
    4. Converts the 'name', 'artist', and 'tags' columns to lowercase.

    Parameters:
    data (pd.DataFrame): The input DataFrame containing the data to be cleaned.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """
    return (
        data
        .drop_duplicates(subset="track_id")
        .drop(columns=["genre","spotify_id"])
        .fillna({"tags":"no_tags"})
        .assign(
            name=lambda x: x["name"].str.lower(),
            artist=lambda x: x["artist"].str.lower(),
            tags=lambda x: x["tags"].str.lower()
        )
        .reset_index(drop=True)
    )
    
    
def data_for_content_filtering(data):
    """
    Cleans the input DataFrame by dropping specific columns.

    This function takes a DataFrame and removes the columns "track_id", "name",
    and "spotify_preview_url". It is intended to prepare the data for content based
    filtering by removing unnecessary features.

    Parameters:
    data (pandas.DataFrame): The input DataFrame containing songs information.

    Returns:
    pandas.DataFrame: A DataFrame with the specified columns removed.
    """
    return (
        data
        .drop(columns=["track_id","name","spotify_preview_url"])
    )
    
    
def main(data_path):
    """
    Load, clean, transform, and save the data.
    """
    from pathlib import Path

    # Create processed folder
    Path("data/processed").mkdir(parents=True, exist_ok=True)

    # Load raw data
    data = pd.read_csv(data_path)

    # Clean data
    cleaned_data = clean_data(data)

    # Save cleaned data
    cleaned_data.to_csv(
        "data/processed/cleaned_data.csv",
        index=False
    )

    # Prepare data for content-based filtering
    transformed_data = data_for_content_filtering(cleaned_data)

    # Save transformed data
    transformed_data.to_csv(
        "data/processed/content_filtering_data.csv",
        index=False
    )

    print("Cleaned data saved successfully!")
    print("Content filtering data saved successfully!")
    print("Cleaned data shape:", cleaned_data.shape)
    print("Transformed data shape:", transformed_data.shape)

    

if __name__ == "__main__":
    main(DATA_PATH)
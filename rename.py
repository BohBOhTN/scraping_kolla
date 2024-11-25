import pandas as pd

def rename_columns(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Display the current column names
    print("\nCurrent column names:")
    print(df.columns.tolist())

    # Create a list to store new column names
    new_column_names = []

    # Loop through the existing columns and ask the user for new names
    for col in df.columns:
        new_name = input(f"Enter a new name for column '{col}' (leave empty to keep the current name): ")
        if new_name.strip():
            new_column_names.append(new_name.strip())
        else:
            new_column_names.append(col)

    # Rename the columns in the DataFrame
    df.columns = new_column_names

    # Save the DataFrame with the new column names back to CSV
    new_csv_file = input("Enter the name for the new CSV file (e.g., 'new_file.csv'): ")
    df.to_csv(new_csv_file, index=False)
    print(f"\nThe new CSV file with renamed columns has been saved as '{new_csv_file}'.")

if __name__ == "__main__":
    # Get the input CSV file name
    csv_file = input("Enter the path to the CSV file: ")
    rename_columns(csv_file)

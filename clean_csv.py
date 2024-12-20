import os
import pandas as pd
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define the mappings for file names to sub-categories and categories
sub_category_mapping = {
    "Thé": "Drinks", "Smoothies": "Drinks", "Jwajem": "Drinks", "Milkshake": "Drinks", 
    "Mojito": "Drinks", "Cafés": "Drinks", "Boissons": "Drinks", "Frappucino": "Drinks", 
    "Jus": "Drinks", "Café Dalgona": "Drinks", "Latté": "Drinks", "Café Glacé": "Drinks", 
    "Aromatisé": "Drinks", "Chocolat": "Drinks", "Drinks": "Drinks",
    
    "Les Entrées": "Cuisine", "Nos Spécialités": "Cuisine", "Traditionnel": "Cuisine", 
    "Poisson Chrafi": "Cuisine", "Nos Pates": "Cuisine", "Viandes Et Volailles": "Cuisine",
    
    "Petit-déjeuner": "Petit-Déjeuner",
    
    "Omelette": "Salé", "Crêpe": "Salé",
    
    "Crêpe": "Sucré", "Gaufre": "Sucré", "Desserts": "Sucré", "Pancake": "Sucré",
    
    "Chicha": "Chicha", "Pack Client": "Chicha"
}

def normalize_name(filename):
    """
    Normalize the file name to match the mapping keys:
    - Replace underscores with spaces
    - Remove file extensions
    - Normalize special characters
    """
    name = os.path.splitext(filename)[0]  # Remove file extension
    name = name.replace("_", " ")         # Replace underscores with spaces
    return name.strip()                   # Trim whitespace

def generate_reference(product_name, index, used_references):
    """
    Generate a unique 5-character reference for each product based on its name and index.
    Ensures uniqueness by checking if the reference is already used.
    """
    # Use the product name and index to create a potential reference
    reference = (product_name[:3] + str(index)[:2]).upper()[:5]
    
    # Ensure uniqueness by checking against used references
    original_reference = reference
    count = 1
    while reference in used_references:
        # Modify the reference by appending a number to ensure it's unique
        reference = f"{original_reference}{count}"[:5]
        count += 1
    
    # Add the reference to the set of used references
    used_references.add(reference)
    
    return reference

def process_csv_files(folder_path):
    all_dataframes = []  # List to hold all processed DataFrames
    used_references = set()  # Set to track used references

    # Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        # Check if it's a CSV file
        if filename.endswith(".csv"):
            # Normalize the file name
            normalized_name = normalize_name(filename)
            
            # Check for the corresponding sub-category and category based on the normalized name
            sub_category = normalized_name
            category = sub_category_mapping.get(normalized_name)
            
            if category:
                # Read the CSV into a DataFrame
                file_path = os.path.join(folder_path, filename)
                df = pd.read_csv(file_path)
                
                # Add the new columns
                df['sub-category'] = sub_category
                df['category'] = category
                
                # Generate and add the 'reference' column
                df['reference'] = df.apply(
                    lambda row: generate_reference(row['Title'], row.name, used_references), axis=1
                )
                
                # Add the DataFrame to the list
                all_dataframes.append(df)
                
                # Define the output file path (new cleaned file)
                output_path = os.path.join(folder_path, f"cleaned_{filename}")
                
                # Save the modified DataFrame to a new CSV file
                df.to_csv(output_path, index=False)
                
                # Log success message
                print(f"{Fore.GREEN}Processed and saved: {output_path}{Style.RESET_ALL}")
            else:
                # Log skipped files with explanation
                print(f"{Fore.YELLOW}No category mapping found for {filename} "
                      f"(normalized as '{normalized_name}'), skipping.{Style.RESET_ALL}")

    # Merge all processed DataFrames and save as all_products.csv
    if all_dataframes:
        merged_df = pd.concat(all_dataframes, ignore_index=True)
        merged_output_path = os.path.join(folder_path, "all_products.csv")
        merged_df.to_csv(merged_output_path, index=False)
        print(f"{Fore.CYAN}All processed CSVs merged and saved as: {merged_output_path}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}No CSVs were processed, skipping merging.{Style.RESET_ALL}")

if __name__ == "__main__":
    print(f"{Fore.CYAN}Welcome to the CSV Cleaner Script!{Style.RESET_ALL}")
    folder_path = input(f"{Fore.BLUE}Enter the folder path containing the CSV files: {Style.RESET_ALL}")
    process_csv_files(folder_path)
    print(f"{Fore.CYAN}Processing completed!{Style.RESET_ALL}")

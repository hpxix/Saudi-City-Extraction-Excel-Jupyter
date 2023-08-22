import json
import re
import pandas as pd 

# Read the Excel file
df = pd.read_excel("chats(20230807-024404).xlsx")

# Load target IDs from JSON file
# The with statement ensures that the file will be automatically closed when the code
# The "city.json" file in read mode ("r") and specifies the encoding as UTF-8 ("utf-8").
with open("city.json", "r", encoding="utf-8") as json_file:
    target_ids = json.load(json_file)


# Compile regular expressions for city names
# .join() is used for  say give me the iterable Json and convert it to string.
# '|' at the begging of a compiler means i want the keys set show value next to them as the or opperator works as a matching point ex; z|wood matches zoo or wood here we are saying label|join matching in this case wea are using 2 langues so we said english | arabic both of them shall be .joined.

city_names_ar = [city["label"] for city in target_ids]
city_names_en = [city["value"] for city in target_ids]
city_patterns_ar = re.compile(
    '|'.join(map(re.escape, city_names_ar)), re.IGNORECASE)
city_patterns_en = re.compile(
    '|'.join(map(re.escape, city_names_en)), re.IGNORECASE)

# Function to extract cities from chat content using regular expressions
# it doesn't refer to the df file thus it's a helper function that findsall chat content
# The parameter serves as a way to pass the content of a chat to the function, allowing the function to operate on that specific content.


def extract_cities(chat_content):
    matched_cities_ar = city_patterns_ar.findall(chat_content)
    matched_cities_en = city_patterns_en.findall(chat_content)
    chat_cities = matched_cities_ar + matched_cities_en
    return chat_cities


# Create an empty list to store extracted cities for each chat
extracted_cities_list = []

# For loop created assigning 'content' column
# if instance() <= means check if parameter is string.
# now assign an extracted_cities var for the parameter chat content
# then return empty string if extracte_cities is is not true or found,
# then return an empty string if chat content isn't a string as well.

for chat_content in df['content']:
    if isinstance(chat_content, str):
        extracted_cities = extract_cities(chat_content)
        # print(extracted_cities)  # Add this line to check the extracted cities
        if extracted_cities:
            extracted_cities_list.append(extracted_cities)
        else:
            extracted_cities_list.append("")
    else:
        extracted_cities_list.append("")


# Calculate the maximum number of extracted cities in any chat
# we take the max len of cities and make it a boolean using isinstance and give it a type of list if not give me 0,

max_extracted_cities = max(len(cities) if isinstance(
    cities, list) else 0 for cities in extracted_cities_list)


# Broadcast extracted cities across multiple columns if necessary
# col_name = formated string of extractedcity_ an intrement that increases according to the code bellow
# df[colname] will assign a loop variable with an increment that could be increased by i and as we said above if the increment increases python gets ready to add a column by 1 else add an empty string for cities in extracted_cities_list,

if max_extracted_cities > 1:
    for i in range(max_extracted_cities):
        col_name = f'ExtractedCity_{i+1}'
        df[col_name] = [cities[i] if i < len(
            cities) else '' for cities in extracted_cities_list]

# Save the modified DataFrame
df.to_excel("chats_with_cities.xlsx", index=False)

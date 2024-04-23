# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 11:17:10 2024

@author: Pratiksha G
"""
    
import pdfplumber
from itertools import groupby
import math
import pandas as pd
import regex as re
from googletrans import Translator
from unidecode import unidecode



def extract_text_with_font(pdf_path):
    def key_function(char):
        return char['fontname'], char['size']

    with pdfplumber.open(pdf_path) as pdf:
        text_with_font = []
        
        for page in pdf.pages:
            characters = page.chars
            for (fontname, size), group in groupby(characters, key=key_function):
                text = ''.join(char['text'] for char in group)
                text_with_font.append((text, fontname, size))
        
        return text_with_font
    
def is_recipe(text):
    # Define recipe keywords
    recipe_keywords = ["skære", "prøve", "hurtigt", "velbekomme", "lav"]

    # Tokenize the text into words
    words = re.findall(r'\b\w+\b', text)

    # Check if any word in the text exactly matches a recipe keyword
    return any(word.lower() in recipe_keywords for word in words)

def filter_out_recipes(string_list):
    # Use a list comprehension to filter out strings that are identified as recipes
    filtered_list = [string for string in string_list if not is_recipe(string)]
    return filtered_list

def split_string(s):
    if 'dybfrost.' in s:
        if s.startswith('dybfrost.'):
            return s
        else:
            return s.split('dybfrost.')[0].strip(), 'dybfrost.' + s.split('dybfrost.')[1].strip()
    else:
        return s

def process_strings(string_list):
    result_list = []
    current_string = ""

    for string in string_list:
        if re.search(r'pris\s+\d+\.|frit\s+valg\.|maks\.\s+\d+\.|kunde\.$', string):

            # Condition met, append the current string
            current_string += " " + string
            result_list.append(current_string)
            current_string = ""  # Reset current_string for the next group
        else:
            # Condition not met, store the first string
            if not current_string:
                current_string = string
            else:
                current_string += " " + string

    # Append the last group of strings if any
    if current_string:
        result_list.append(current_string)
        
    result_list = [string.strip() for string in result_list]
    
    result_list = [item for item in result_list if not re.search(r'^\d+\s*x\s+\d+\s+cl', item)]
    result_list = [ item for item in result_list if not (item.startswith("frit valg."))]
    
    # Apply the function to each string in the list
    result_list = [split_string(s) for s in result_list]

    
    processed_strings = []
    for item in result_list:
        if isinstance(item, tuple):
            # If the current item is a tuple, insert its elements at the position where the tuple is found
            index = result_list.index(item)
            processed_strings.extend(item)
        else:
            # If the current item is not a tuple, just append it to the output list
            processed_strings.append(item)
    
    return processed_strings

def final_clean(product_names_list,processed_strings):
    final_name = []; final_desc =[]
    
    for index, (name, description) in enumerate(zip(product_names_list, processed_strings)):
        
        if len(description)>104:
            final_name.append(None)
            final_desc.append(None)
            # break
            
            
        else: 
            final_name.append(name)
            final_desc.append(description)
            # index_name = index
            # print(index)
    # return index,index_name,final_name,final_desc
    return final_name,final_desc
            
        
def data_cleaning(text_with_font):
    
    product_name1 = [text for text, fontname, size in text_with_font if math.isclose(size, 9.5)]
    product_name1 = [' '.join(s.split()) for s in product_name1]
    
    # Remove strings starting with a number using list comprehension
    product_name1 = [s for s in product_name1 if not s[0].isdigit()]
    
    product_name = []
    for s in product_name1:
        if s.startswith("eller"):
            if product_name:  # Check if there's a previous string to merge with
                product_name[-1] += " " + s  # Merge with the previous string
            else:
                product_name.append(s)  # If there's no previous string, add the current one
        else:
            product_name.append(s)  # If the current string doesn't start with "eller," add it as is

    # Iterate through the original strings
    product_names = []
    i = 0
    while i < len(product_name):
        current_string = product_name[i]

        # Check if the current string ends with "eller"
        if current_string.strip().endswith("eller"):
            # Merge the current string with the next string
            next_string = product_name[i + 1]
            merged_string = current_string +" "+ next_string
            product_names.append(merged_string)
            i += 2  # Skip the next string as it's already merged
        else:
            # Add the current string as is
            product_names.append(current_string)
            i += 1
            
    product_names_list =  filter_out_recipes(product_names)
    product_names_list = [ item for item in product_names_list if not (item.startswith("med"))]
    try:
        removed_element = product_names_list.pop(33)
    except IndexError:
        print(f"Position 33 is out of range for the given list.")
    product_names_list = [item.lower() for item in product_names_list]

    product_names_list = [ item for item in product_names_list if not (item.startswith("pasta") or item.startswith("pastasalat"))]

    
    # Product description logic
    product_desc = [text for text, fontname, size in text_with_font if math.isclose(size, 7.5)]
    product_desc = [' '.join(s.split()) for s in product_desc]
    product_desc = [item.lower() for item in product_desc]
    product_desc = [item for item in product_desc if not re.search(r'\d+\s+point', item)]
    product_desc = [ item for item in product_desc if not (item.startswith("før-pris") or item.startswith("begrænset parti.") or item.startswith("sælges"))]
    product_desc = [item for item in product_desc if item != '']
    
        
    # Remove commas from digits in the list
    product_desc = [item.replace(',', '') if any(c.isdigit() for c in item) else item for item in product_desc]

    product_des = []
    for s in product_desc:
        if s.startswith("maks"):
            if product_des:  # Check if there's a previous string to merge with
                product_des[-1] += " " + s  # Merge with the previous string
            else:
                product_des.append(s)  # If there's no previous string, add the current one
        else:
            product_des.append(s)  # If the current string doesn't start with "eller," add it as is

    processed_strings = process_strings(product_des)
    
    final_name1 =[];final_desc1=[]
    
    final_name1.extend(product_names_list[-4:])
    final_desc1.extend(processed_strings[-4:])
    
    product_names_list = product_names_list[:-4]
    processed_strings = processed_strings[:-4]
    
   
    # while len(processed_strings) > 0:
    final_name,final_desc = final_clean(product_names_list,processed_strings)
        # product_names_list = product_names_list[index_name:]
        # processed_strings = processed_strings[index+1:]
    final_name.extend(final_name1)
    final_desc.extend(final_desc1)
    quantity = []; price= []
    # q = "dybfrost. 555-570 g. kg-pris maks. 5225. frit valg. maks. 6 stk. pr. kunde."
    
    for q in final_desc:
        try:
            q1 = re.findall(r"\d+\s*x\s*\d+\s*\w+|\b\d+-\d+\s*g\b|\d+\s+g|\d+\s+ml|\d+\s+stk|\d+\s+liter|\d+\s+cl", q)
            if len(q1)!= 0:
                if len(q1) == 1:
                    q2=q1[0]
                else:
                    q2 = q1[0]+"/"+q1[1]
            else:
                q2 = 1
        except:
            q2 = 1
            pass
        quantity.append(q2)
        
    for q in final_desc:
        try:
            q1 = re.findall(r"\d+\.|(?<=pris)\s+\d+|(?<=maks.)\s+\d+", q)[0]
            # q2 = re.findall(r"\d+\s+stk",q)
        except: 
            q1 = 1
        price.append(q1)
    price = [str(s).strip() for s in price]
    price  = [p[:len(p)-2]+'.'+p[len(p)-2:] for p in price]
    quantity = [str(s).strip() for s in quantity]

    
    
    return final_name,final_desc,quantity,price

# Function to translate a single string
def translate_to_english(text):
    translator = Translator()
    translation = translator.translate(text, src='da', dest='en')
    return translation.text

def convert_uni_normal(city):
    # Convert Unicode text into Normal text
    
    converted_text = unidecode(city)
    return converted_text



path = "coop.pdf"
# read_extract_from_pdf(path)                                        
text_with_font = extract_text_with_font(path) 
final_name,final_desc,quantity,price = data_cleaning(text_with_font)

data = {'Product_Name': final_name,
        'Product_Description': final_desc,
        'Quantity':quantity,
        'Price':price}
df = pd.DataFrame(data)
df = df.dropna()

df['Product_Name'] = df['Product_Name'].str.strip()
for index, row in df.iterrows():
    city_value = row['Product_Name']
    city_value = convert_uni_normal(city_value)
    df.at[index, 'Product_Name'] = city_value

# Apply translation to the column
df['Product_Name'] = df['Product_Name'].apply(translate_to_english)
df['Product_Description'] = df['Product_Description'].apply(translate_to_english)
df['Quantity'] = df['Quantity'].apply(translate_to_english)


for i, q in df['Product_Description'].items():
    match = re.findall(r"\d+\.|(?<=pris)\s+\d+|(?<=maks\.)\s+\d+", q)
    if match:
        # Extracted number
        number = match[0]
        number = number.replace('.','')

        # Add a period before the last two digits
        modified_number = number[:-2] + '.' + number[-2:]

        # Replace the original number with the modified one in the string
        q1 = re.sub(r"\d+\.|(?<=pris)\s+\d+|(?<=maks\.)\s+\d+", modified_number, q)
        df.at[i, 'Product_Description'] = q1
        
df.to_csv("COOP_Data.csv", index=False)     






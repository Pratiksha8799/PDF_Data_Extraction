
# Data Extraction from PDFs
![App Screenshot](https://github.com/Pratiksha8799/PDF_Data_Extraction/blob/main/AI.png)

This is an overview and in-depth description of the COOP Data Extraction project. The goal of this project is to extract important data from a PDF file containing product information, clean it, translate it to English, and store it as a CSV file for further analysis.


## Features

- PDF Extraction Module: The project starts with extracting text from the input PDF file using the pdfplumber library. This module extracts text along with font information from each page of the PDF.

- Data Cleaning Module: The extracted text is processed to separate product names and descriptions based on font size and other criteria. Various cleaning operations are performed on the extracted data to remove irrelevant information and noise.
- Translation Module: The cleaned data, specifically product names and descriptions, are translated from Danish to English using the googletrans library.
- Data Conversion and Saving: The translated data is formatted and saved into a CSV file named "COOP_Data.csv" for further analysis.

## Dependencies

To run this project, you will need to install following libraries.

* pdfplumber: Used for extracting text and font information from PDF files.
* pandas: Utilized for data manipulation and creating DataFrames for storing extracted data.
* regex (re): Employed for pattern matching and text processing operations.
* googletrans: Used for translating text from one language to another.
* unidecode: Utilized for converting Unicode text into normal text.
* itertools: Used for various iteration-related tasks, particularly in conjunction with groupby.
* math: Used for mathematical operations, particularly for comparing floating-point numbers.*

## Deployment

To deploy this project run
* Clone the repository.
* Navigate to the project directory.
* Install required dependencies.
* Run the app. 
```bash
  python Offer_extraction.py
```






## Usage
* Installation of Required Libraries: Before using the script, make sure you have installed the required Python libraries.
* Downloading the Script:  Download the provided Python script and save it in your working directory.
* Preparing the PDF File: Place the PDF file containing the product information in the same directory as the script. Ensure that the PDF file follows the format expected by the script for accurate extraction.
* Executing the Script: Open a terminal or command prompt, navigate to the directory containing the script and the PDF file, and run the script using Python
* Analysis and Further Processing: After the script has executed successfully, you can open the generated CSV file. The CSV file contains the cleaned and translated product information, which you can analyze further or integrate into other applications as needed




## Used By

The project can be utilized by individuals or organizations who are:

* Retailers: Retail companies may use this project to extract product information from supplier catalogs or pricing lists in PDF format. They can then analyze the extracted data to update their own product databases or pricing information.

* Data Analysts: Professionals working in data analysis roles may find this project useful for extracting structured data from PDF files for market research, competitor analysis, or trend analysis purposes.

* Language Professionals: Individuals or companies specializing in language translation services may use this project to automate the translation of text from one language to another, particularly for tasks involving large volumes of text.

* Automation Enthusiasts: Programmers interested in automating repetitive data extraction and processing tasks may use this project as a template or starting point for developing similar automation scripts tailored to their specific requirements.

* Educational Institutions: Academic institutions or researchers conducting studies on product data, language translation, or document processing techniques may utilize this project for experimentation or as a reference for developing their own tools.
## 🚀 Conclusion

In conclusion, overall the project provides a robust and adaptable solution for automating the extraction and processing of product information from PDF files, catering to a diverse range of users and use cases.


## Support

For support, email pratikshagarkar871999@gmail.com


## About me

[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://medium.com/@pratiksha.garkar)


## Links
[pdfplumber](https://pypi.org/project/pdfplumber/)

[googletrans](https://pypi.org/project/googletrans/)

[regex](https://pypi.org/project/regex/)

[regex](https://pypi.org/project/unidecode/)



## Future Scope

* Improved Description Generation: Enhance the functionality of the OpenAi_Api_Fun function to generate more informative and accurate descriptions for products. This could involve training the model on a larger dataset or fine-tuning the model's parameters to improve the quality of generated descriptions.

"""
This file contains code for the application "Gemini Pro Class Generator".
Author: GlobalCreativeApkDev
"""


# Importing necessary libraries
import google.generativeai as gemini
import sys
import os
from dotenv import load_dotenv
from mpmath import mp, mpf

mp.pretty = True


# Creating static functions to be used in this application.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating main function used to run the application.


def main() -> int:
    """
    This main function is used to run the application.
    :return: an integer
    """

    load_dotenv()
    gemini.configure(api_key=os.environ['GEMINI_API_KEY'])

    # Asking user input values for generation config
    temperature: str = input("Please enter temperature (0 - 1): ")
    while not is_number(temperature) or float(temperature) < 0 or float(temperature) > 1:
        temperature = input("Sorry, invalid input! Please re-enter temperature (0 - 1): ")

    float_temperature: float = float(temperature)

    top_p: str = input("Please enter Top P (0 - 1): ")
    while not is_number(top_p) or float(top_p) < 0 or float(top_p) > 1:
        top_p = input("Sorry, invalid input! Please re-enter Top P (0 - 1): ")

    float_top_p: float = float(top_p)

    top_k: str = input("Please enter Top K (at least 1): ")
    while not is_number(top_k) or int(top_k) < 1:
        top_k = input("Sorry, invalid input! Please re-enter Top K (at least 1): ")

    float_top_k: int = int(top_k)

    max_output_tokens: str = input("Please enter maximum input tokens (at least 1): ")
    while not is_number(max_output_tokens) or int(max_output_tokens) < 1:
        max_output_tokens = input("Sorry, invalid input! Please re-enter maximum input tokens (at least 1): ")

    int_max_output_tokens: int = int(max_output_tokens)

    # Set up the model
    generation_config = {
        "temperature": float_temperature,
        "top_p": float_top_p,
        "top_k": float_top_k,
        "max_output_tokens": int_max_output_tokens,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = gemini.GenerativeModel(model_name="gemini-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    convo = model.start_chat(history=[
    ])

    while True:
        clear()
        language: str = input("What programming language do you want to create a class in? ")
        convo.send_message("Is " + str(language) + " a programming language (one word response only)?")
        language_check_answer: str = str(convo.last.text).upper()
        while language_check_answer != "YES":
            language = input("Sorry, invalid input! What programming language do you want to create a class in? ")
            convo.send_message("Is " + str(language) + " a programming language (one word response only)?")
            language_check_answer = str(convo.last.text).upper()

        class_name: str = input("Please enter the name of the class you want to create (no extension please): ")
        prompt = """
Create a """ + str(language) + """ class """ + str(class_name) + """ with the following specifications.

Attributes:
"""

        attribute_pairs: dict = {}  # attribute names and descriptions
        num_attributes: str = input("How many attributes do you want to include in the class " + str(class_name) + "? ")
        while not is_number(num_attributes) or int(num_attributes) < 1:
            num_attributes = input(
                "Sorry, invalid input! How many attributes do you want to include in the class " + str(class_name)
                + "? ")

        for i in range(int(num_attributes)):
            attribute_name: str = input("Enter the name of the attribute: ")
            description: str = input("Description of the attribute " + str(attribute_name) + ": ")
            attribute_pairs[attribute_name] = description

        attribute_count: int = 1  # initial value
        for attribute in attribute_pairs:
            prompt += """
""" + str(attribute_count) + """. """ + str(attribute) + """ -> """ + str(attribute_pairs[attribute]) + """
"""
            attribute_count += 1

        prompt += """

Methods:
"""

        method_pairs: dict = {}  # method names and descriptions
        num_methods: str = input("How many methods do you want to include in the class " + str(class_name) + "? ")
        while not is_number(num_methods) or int(num_methods) < 1:
            num_methods = input("Sorry, invalid input! How many methods do you want to include in the class "
                                + str(class_name) + "? ")

        for i in range(int(num_methods)):
            method_name: str = input("Enter the name of the method: ")
            description: str = input("Description of the method " + str(method_name) + ": ")
            method_pairs[method_name] = description

        method_count: int = 1
        for method in method_pairs:
            prompt += """
""" + str(method_count) + """. """ + str(method) + """ -> """ + str(method_pairs[method]) + """
"""
            method_count += 1

        prompt += """
Additional Instructions: Only include the code in your response.        
"""

        convo = model.start_chat(history=[
        ])
        convo.send_message(prompt)
        code: str = '\n'.join(str(convo.last.text).split('\n')[1:-1])

        # Writing the code to a file
        convo = model.start_chat(history=[
        ])
        convo.send_message("What is the extension of a " + str(language).lower().capitalize()
                           + " file (please include the dot, one word response only)?")
        code_file_extension: str = str(convo.last.text)
        file_name: str = str(class_name) + str(code_file_extension)
        class_file = open(os.path.join("classes", str(file_name)), "w")
        class_file.write(code)
        class_file.close()

        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_generating: str = input("Do you want to continue generating a class? ")
        if continue_generating != "Y":
            return 0


if __name__ == '__main__':
    main()

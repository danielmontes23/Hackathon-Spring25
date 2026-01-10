from pylatex import Document, Command, NoEscape, Section, UnsafeCommand, Package
from pylatex.utils import bold
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

class document_creation():
    def __init__(self):
        '''
        Initializes the document with the moderncv class and some default packages.'''
        self.doc = Document(
            documentclass='moderncv',
            document_options=['11pt', 'a4paper', 'sans']
        )

        self.doc.packages.append(Package('inputenc', options='utf8'))
        self.doc.packages.append(Package('geometry', options=['scale=0.85']))

    def set_style(self, style: str) -> dict:
        '''
        Sets the style for the document.
        
        :param style: The style to set. Valid options are 'casual', 'classic', 'oldstyle', 'banking', 'fancy'.

        :return: A dictionary indicating whether the style was set successfully.'''
        # Define valid style options
        valid_styles = ['casual', 'classic', 'oldstyle', 'banking', 'fancy']
        if style in valid_styles:
            self.doc.preamble.append(Command('moderncvstyle', style))
            return {'isvalid': True}
        return {'isvalid': False}
    
    def set_color(self, color: str) -> dict:
        '''
        Sets the color theme for the document.
        
        :param color: The color theme to set. Valid options are 'blue', 'orange', 'green', 'red', 'purple', 'grey', 'black'.

        :return: A dictionary indicating whether the color was set successfully.'''
        # Define valid color options
        valid_colors = ['blue', 'orange', 'green', 'red', 'purple', 'grey', 'black']
        if color in valid_colors:
            self.doc.preamble.append(Command('moderncvcolor', color))
            return {'isvalid': True}
        return {'isvalid': False}

    def personal_info(self, fname: str, lname: str, title: str, faddress: str | None = None, laddress: str | None = None,
                     email: dict | None = None, phone: dict | None = None,
                     social: dict | None = None, homepage: str | None = None) -> dict:
        '''
        Adds personal information to the document.
        
        :param fname: First name.
        
        :param lname: Last name.
        
        :param title: Title or position.
        
        :param faddress: First line of address.
        
        :param laddress: Second line of address.
        
        :param email: Dictionary of email addresses with keys as labels.
        
        :param phone: Dictionary of phone numbers with keys as labels.
        
        :param social: Dictionary of social media links with keys as labels.
        
        :param homepage: Personal homepage URL.
        
        :return: A dictionary indicating whether the information was added successfully.'''
        counter = 3

        self.doc.preamble.append(Command('name', [fname, lname]))
        self.doc.preamble.append(Command('title', title))
        if faddress and laddress:
            self.doc.preamble.append(Command('address', [faddress, laddress]))
        if phone:
            for key, value in phone.items():
                self.doc.preamble.append(Command('phone', arguments=value, options=key))
                counter += 1
        if email:
            for key, value in email.items():
                self.doc.preamble.append(Command('email', value))
                counter += 1
        if homepage:
            self.doc.preamble.append(Command('homepage', homepage))
            counter += 1
        if social:
            for key, value in social.items():
                self.doc.preamble.append(Command('social', arguments=value, options=key))
                counter += 1

        self.doc.append(Command('makecvtitle'))
        return {'added': counter}

    
    def add_summary(self, section:str, section_data: str):
        '''
        Adds a summary section to the document.
        
        :param section: The name of the section.
        
        :param section_data: The content of the section.

        :return: A dictionary indicating whether the section was added successfully.'''
        if isinstance(section, str) and isinstance(section_data, dict):
            with self.doc.create(Section(section)):
                    self.doc.append(Command('cvitem', arguments=['', NoEscape(section_data)]))
                    return {'isvalid': True}
        return {'isvalid': False}
    

    def add_section_2(self, section: str, section_data: dict):
        '''
        Adds a section with key-value pairs to the document.

        :param section: The name of the section.
        
        :param section_data: A dictionary containing key-value pairs. key is the dates, and value is the data.

        
        :return: A dictionary indicating whether the section was added successfully.'''
        
        if isinstance(section, str) and isinstance(section_data, dict):
            with self.doc.create(Section(section)):
                for key in section_data.keys():
                    self.doc.append(Command('cvitem', arguments=[key, NoEscape(section_data[key])]))

                return {'isvalid': True}
        return {'isvalid': False}
            

    def add_section_6(self, section: str, data: dict):
        '''
        Adds a section with six key-value pairs to the document.
        
        :param section: The name of the section.
        
        :param data: A dictionary containing six key-value pairs. The keys are 'dates', 'title', 'company', 'city', 'country', and 'data'.

        :return: A dictionary indicating whether the section was added successfully.
        '''
        with self.doc.create(Section(section)):
            for entry in data.values():
                self.doc.append(Command('cventry', arguments=[
                    entry['dates'],
                    NoEscape(entry['title']),
                    NoEscape(entry['company']),
                    NoEscape(entry['city']),
                    NoEscape(entry['country']),
                    NoEscape(entry['data'])
                ]))
            return {'isvalid': True}
        return {'isvalid': False}
        
    def generate(self, name: str):
        '''
        Generates the PDF document and saves it to the specified name.
        
        :param name: The name of the output file (without extension).'''
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        try:
            self.doc.generate_pdf(os.path.join(OUTPUT_DIR, name), clean_tex=False, compiler='pdflatex')
            return {'isvalid': True}
        except subprocess.CalledProcessError as e:
            print(f"LaTeX compilation failed with exit code {e.returncode}")
            print(f"Output: {e.output.decode()}")
            log_file_path = f'./src/python/output/{name}.log'
            if os.path.exists(log_file_path):
                with open(log_file_path, 'r') as log_file:
                    print("Log file contents:")
                    print(log_file.read())
            raise
        

# # Experience
# self.doc.append(Section('Experience'))



# self.doc.append(NoEscape(r'''
# \cventry{2018--2021}{Software Developer}{CodeWorks Ltd.}{New York, NY}{}{
# \begin{itemize}
#   \item Designed and implemented RESTful APIs used by over 500,000 users.
#   \item Integrated third-party services (Stripe, Auth0) reducing onboarding time by 40\%.
# \end{itemize}
# }
# '''))

# # Education
# self.doc.append(Section('Education'))
# self.doc.append(NoEscape(r'''
# \cventry{2014--2018}{B.S. in Computer Science}{University of Example}{Example City}{}{
# GPA: 3.8/4.0 \\
# Dean’s List (2015–2018)
# }
# '''))

# Skills
# self.doc.append(Section('Skills'))
# self.doc.append(NoEscape(r'''
# \cvitem{Languages}{Python, JavaScript, Go, C++}
# \cvitem{Frameworks}{React, Node.js, Django, Flask}
# \cvitem{Tools}{Docker, Kubernetes, Git, CI/CD, AWS}
# '''))

# Projects
# self.doc.append(Section('Projects'))
# self.doc.append(NoEscape(r'''
# \cvitem{OpenTasker}{
# Open-source task manager built with React and Django. Supports user auth, due-date reminders, and multi-device sync.
# \newline \textbf{GitHub:} \texttt{github.com/janedoe/opentasker}
# }
# \cvitem{CLI Budget Tracker}{
# Lightweight command-line tool for tracking daily expenses in CSV format.
# \newline \textbf{GitHub:} \texttt{github.com/janedoe/budget-cli}
# }
# '''))

# Languages
# self.doc.append(Section('Languages'))
# self.doc.append(NoEscape(r'''
# \cvitemwithcomment{English}{Native}{}
# \cvitemwithcomment{Spanish}{Professional working proficiency}{}
# '''))



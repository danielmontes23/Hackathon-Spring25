from pylatex import Document, Command, NoEscape, Section, UnsafeCommand, Package
from pylatex.utils import bold
import os
import subprocess

class document_creation():
    def __init__(self):
        self.doc = Document(
            documentclass='moderncv',
            document_options=['11pt', 'a4paper', 'sans']
        )

        self.doc.packages.append(Package('inputenc', options='utf8'))
        self.doc.packages.append(Package('geometry', options=['scale=0.85']))

    def set_style(self, style: str) -> dict:
        valid_styles = ['casual', 'classic', 'oldstyle', 'banking', 'fancy']
        if style in valid_styles:
            self.doc.preamble.append(Command('moderncvstyle', style))
            return {'isvalid': True}
        return {'isvalid': False}
    
    def set_color(self, color: str) -> dict:
        valid_colors = ['blue', 'orange', 'green', 'red', 'purple', 'grey', 'black']
        if color in valid_colors:
            self.doc.preamble.append(Command('moderncvcolor', color))
            return {'isvalid': True}
        return {'isvalid': False}

    def personal_info(self, fname: str, lname: str, title: str, faddress: str, laddress: str,
                     email: dict | None = None, phone: dict | None = None,
                     social: dict | None = None, homepage: str | None = None) -> dict:
        counter = 3

        self.doc.preamble.append(Command('name', [fname, lname]))
        self.doc.preamble.append(Command('title', title))
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


    def add_section_2(self, section: str, section_data: str):
        if isinstance(section, str) and isinstance(section_data, str):
            with self.doc.create(Section(section)):
                self.doc.append(Command('cvitem', arguments=['', NoEscape(section_data)]))

    def add_section_6(self, section: str, dates: str, title: str, company: str, city: str, country: str, data: str):
        with self.doc.create(Section(section)):
            self.doc.append(Command('cventry', arguments=[
                dates, title, company, city, country, NoEscape(data)
            ]))

    def generate(self, name: str):
        # Ensure output directory exists
        os.makedirs('output', exist_ok=True)
        try:
            # Generate PDF using latexmk
            self.doc.generate_pdf(f'output/{name}', clean_tex=False, compiler='pdflatex')
        except subprocess.CalledProcessError as e:
            print(f"LaTeX compilation failed with exit code {e.returncode}")
            print(f"Output: {e.output.decode()}")
            log_file_path = f'output/{name}.log'
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



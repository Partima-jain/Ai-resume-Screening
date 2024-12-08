import fitz  # PyMuPDF
import joblib
import re
import tkinter as tk
from tkinter import Tk, Label, Button, Text, Scrollbar, filedialog, Frame, END , font

# Load the model and vectorizer
model = joblib.load('model.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Define a list of skills and their corresponding roles
SKILLS_ROLES = [
    # Technical Skills
    ('Python', 'Software Engineer'),
    ('JavaScript', 'Frontend Developer'),
    ('DSA', 'Backend Developer'),
    ('Java', 'Backend Developer'),
    ('C#', 'Software Engineer'),
    ('C++', 'Software Engineer'),
    ('HTML', 'Frontend Developer'),
    ('CSS', 'Frontend Developer'),
    ('SQL', 'Database Administrator'),
    ('React', 'Frontend Developer'),
    ('Node.js', 'Backend Developer'),
    ('Machine Learning', 'Data Scientist'),
    ('Data Analysis', 'Data Analyst'),
    ('Django', 'Backend Developer'),
    ('Flask', 'Backend Developer'),
    ('AWS', 'Cloud Engineer'),
    ('Docker', 'DevOps Engineer'),
    ('Kubernetes', 'DevOps Engineer'),
    ('Git', 'Version Control'),
    ('Pandas', 'Data Analyst'),
    ('NumPy', 'Data Analyst'),
    ('Ruby', 'Backend Developer'),
    ('Swift', 'Mobile Developer'),
    ('PHP', 'Backend Developer'),
    ('TypeScript', 'Frontend Developer'),
    ('HTML5', 'Frontend Developer'),
    ('CSS3', 'Frontend Developer'),
    ('Rest API', 'API Developer'),
    ('GraphQL', 'API Developer'),
    ('Redis', 'Database Administrator'),
    ('MongoDB', 'Database Administrator'),
    ('PostgreSQL', 'Database Administrator'),
    ('NoSQL', 'Database Administrator'),
    ('Terraform', 'Cloud Engineer'),
    ('Azure', 'Cloud Engineer'),
    ('Jenkins', 'DevOps Engineer'),
    ('Ansible', 'DevOps Engineer'),
    ('Tableau', 'Data Analyst'),
    ('SAS', 'Data Analyst'),
    ('Hadoop', 'Data Engineer'),
    ('Spark', 'Data Engineer'),
    ('Power BI', 'Data Analyst'),
    ('Artificial Intelligence', 'AI Engineer'),
    ('Cybersecurity', 'Security Analyst'),
    ('Networking', 'Network Engineer'),
    ('Virtualization', 'Cloud Engineer'),
    
    # Non-Technical Skills
    ('Project Management', 'Project Manager'),
    ('Agile', 'Project Manager'),
    ('Scrum', 'Project Manager'),
    ('Time Management', 'All Roles'),
    ('Critical Thinking', 'All Roles'),
    ('Problem Solving', 'All Roles'),
    ('Data Visualization', 'Data Analyst'),
    ('User Experience Design', 'UX Designer'),
    ('SEO', 'Digital Marketer'),
    ('Content Writing', 'Content Writer'),
    ('Digital Marketing', 'Digital Marketer'),
    
    # Personal Skills
    ('Communication', 'All Roles'),
    ('Teamwork', 'All Roles'),
    ('Leadership', 'All Roles'),
    ('Adaptability', 'All Roles'),
    ('Creativity', 'All Roles'),
    ('Interpersonal Skills', 'All Roles'),
    ('Conflict Resolution', 'All Roles'),
    ('Networking', 'All Roles'),
    ('Emotional Intelligence', 'All Roles'),
    ('Attention to Detail', 'All Roles'),
]


def extract_skills(resume_text):
    skills_found = []
    for skill, _ in SKILLS_ROLES:  # No need for the role in this case
        is_found = skill.lower() in resume_text.lower()
        skills_found.append({
            'skill': skill,
            'found': is_found
        })
    return skills_found

def extract_name(resume_text):
    # Regular expression to capture names
    # This pattern captures lines that typically start with capitalized words, like "John Doe"
    name_pattern = r'([A-Z][a-zA-Z]+\s[A-Z][a-zA-Z]+)'  
    names = re.findall(name_pattern, resume_text)
    # Return the first found name or None
    return names[0] if names else None

def predict_category(resume_text):
    resume_tfidf = tfidf_vectorizer.transform([resume_text])
    predicted_category = model.predict(resume_tfidf)[0]
    skills_found = extract_skills(resume_text)
    return predicted_category, skills_found

def upload_pdfs():
    filepaths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    if filepaths:
        result_text.delete(1.0, END)  # Clear existing text
        result_text.pack()

        # Define the bold font style
        bold_font = font.Font(weight='bold',size=19)
        result_text.tag_configure('bold', font=bold_font)
        
        for filepath in filepaths:
            doc = fitz.open(filepath)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            
            # Extract name from resume text
            name = extract_name(text)
            predicted_category, skills_found = predict_category(text)

            # Show the name if found
            if name:
                result_text.insert('end', "Name: ", 'bold')  # Insert label in bold font
                result_text.insert('end', f"{name}\n")  # Insert name in normal font
            else:
                result_text.insert('end', "Name: ", 'bold')  # Insert label in bold font
                result_text.insert('end', "Not Found")  # Insert name in normal font

            # Show predicted category
            result_text.insert(END, "Predicted Category: ", 'bold')  # Insert label for predicted category in bold
            result_text.insert(END, f"{predicted_category}\n")  # Insert category in normal font

            # Prepare to display skills only if found
            filtered_skills = [skill_info for skill_info in skills_found if skill_info['found']]

            if filtered_skills:
                result_text.insert(END, "Skills:\n", 'bold')  # Insert label for skills in bold
                for skill_info in filtered_skills:
                    result_text.insert(END, f" • {skill_info['skill']}\n")  # Bullet points for skills
            else:
                result_text.insert(END, "No skills found.\n")
            
            result_text.insert(END, "\n" + "=" * 40 + "\n\n")  # Separator between resumes

# GUI Setup
root = Tk()
root.title("Resume Screening")
root.geometry("800x600")  # Set the window size

root.configure(bg='grey90')

# Add a frame for better layout
frame = Frame(root, padx=20, pady=20,bg='grey84')
frame.pack(padx=10, pady=10, fill='both', expand=True)

Label(frame, text="Resume Screening:", font=('bold', 30), bg='grey84').pack(pady=(0, 10))

Button(frame, text="Upload PDF", command=upload_pdfs, font=('Arial', 12), bg='grey84').pack(pady=(0, 20))

# Create a Text widget with a scrollbar to display results
result_frame = Text(frame, wrap='word', height=20, width=60, font=('Arial', 16))
result_frame.pack(pady=10, fill='both', expand=True, padx=(20, 10))
# Initial message

# Adding scrollbar
scrollbar = Scrollbar(frame, command=result_frame.yview)
scrollbar.pack(side='right', fill='y')

result_frame.config(yscrollcommand=scrollbar.set)

# Create a Text widget to display results
result_text = result_frame

# Add a footer at the bottom of the application
footer = tk.Label(root, text="Made with ❤️ by Devinsh Upadhaya And Team", font=("Arial", 10) ,bg='grey90')
footer.pack(side='bottom', pady=10)

# Run the main loop
root.mainloop()

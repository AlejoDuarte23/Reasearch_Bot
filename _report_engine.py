import os
import requests
import subprocess
from bs4 import BeautifulSoup
import re
from pathlib import Path

from _search_engine import fetch_elsevier_content, fetch_hindawi_content,fetch_mdpi_content,fetch_springeropen_content,fetch_arxiv_content

pdflatex_path = 'C:/Users/aleja/AppData/Local/Programs/MiKTeX/miktex/bin/x64'
os.environ["PATH"] += os.pathsep + pdflatex_path


def compile_tex_to_pdf(tex_file):
    directory = os.getcwd()
    base_name = os.path.splitext(os.path.basename(tex_file))[0]
    latex_command = ['pdflatex', '-interaction=nonstopmode', base_name + '.tex']
    try:
        subprocess.run(latex_command, cwd=directory)
    except subprocess.CalledProcessError as e:
        print("pdflatex command failed with return code", e.returncode)

def write_latex_file(records, query):
    with open(f'{query}.tex', 'w', encoding='utf-8') as f:
        f.write("\\documentclass[8pt]{extarticle}\n")
        f.write("\\usepackage{graphicx}\n")
        f.write("\\usepackage{hyperref}\n")
        f.write("\\begin{document}\n")
        
        for record in records:
            f.write(f"\\section{{\\href{{{record['href']}}}{{ {record['title']} }}}}\n")
            
            if record['abstract'] != 'N/A':
                f.write(f"\\subsection{{Abstract}}\n")
                f.write(f"{record['abstract']}\n")
                
            if record['conclusion'] != 'N/A':
                f.write(f"\\subsection{{Conclusion}}\n")
                f.write(f"{record['conclusion']}\n")
        
        f.write("\\end{document}")
        
def compile_tex_to_pdf(tex_file):
    """Compile the LaTeX report into a PDF"""
    directory, base_name_with_extension = os.path.split(tex_file)
    base_name = os.path.splitext(base_name_with_extension)[0]
    latex_command = ['pdflatex', '-interaction=nonstopmode', f'{base_name}.tex']
    
    print("Latex command: ", latex_command)  # Debug line
    print("Working directory: ", directory)  # Debug line
    
    try:
        output = subprocess.check_output(latex_command, cwd=directory)
        print(output.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print("pdflatex command failed with return code", e.returncode)
        print(e.output.decode('utf-8'))

def sanitize_filename(filename):
    return filename.replace(" ", "_").replace("  ", "_")

if __name__ == '__main__':
    query = "FE model updating"
    sanitized_query = sanitize_filename(query)
    
    # Fetch records
    records_hind = fetch_hindawi_content(query)
    records_mdpi = fetch_mdpi_content(query)
    # records_spring = fetch_springeropen_content(query)
    records_arvix = fetch_arxiv_content(query)
    records_elsevier = fetch_elsevier_content(query)
    # Join records
    join_records =  records_mdpi + records_elsevier #+records_hind #+records_spring
    
    # Write LaTeX file
    write_latex_file(join_records, sanitized_query)
    
    # Compile the LaTeX file into a PDF
    tex_file_path = os.path.join('C:\\Users\\aleja\\Documents\\Researchbot', f'{sanitized_query}.tex')
    compile_tex_to_pdf(tex_file_path)
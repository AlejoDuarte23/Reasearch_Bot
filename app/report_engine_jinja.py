from jinja2 import Environment, FileSystemLoader

def sanitize_filename(filename):
    return filename.replace(" ", "_").replace("  ", "_")

def write_html_file(records, query , path = 'results'):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template.html')
    rendered_html = template.render(records=records, query=query)
    
    html_file_path = f'{path}/{sanitize_filename(query)}.html'
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
    
    return html_file_path


def main(records, query):
    html_file = write_html_file(records, query)
    return html_file
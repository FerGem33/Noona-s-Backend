from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

env = Environment(loader=FileSystemLoader("app/templates/reportes"))

def generate_pdf(template_name: str, context: dict) -> bytes:
    template = env.get_template(template_name)
    html = template.render(context)
    return HTML(string=html).write_pdf()

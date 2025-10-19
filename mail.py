from email.message import EmailMessage
from jinja2 import Environment, PackageLoader, select_autoescape


_report_env = Environment(
    loader=PackageLoader("email_template"), autoescape=select_autoescape()
)


def _render(email_template, email_data={}):
    template = _report_env.get_template(email_template)
    return template.render(**email_data)


def send_mail(email_template, email_data):
    return _render(email_template, email_data)

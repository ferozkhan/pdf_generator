"""Modules and packages related to invoice generation goes here."""

import os

from weasyprint import HTML


def get_invoice_template():
    """
    Returns invoice template.

    :return: str
    """
    return "Date: {invoice_date}," \
           "Number: {invoice_number}"


def get_invoice_data(invoice):
    """
    Returns data for invoice.

    :param invoice: object
    :return: dict
    """
    return {
        "invoice_number": invoice.number,
        "invoice_date": str(invoice.date)
    }


def prepare_invoice(invoice):
    """
    Returns invoice template with data.

    :param invoice: object
    :return: str
    """
    tmpl = get_invoice_template()
    invoice_data = get_invoice_data(invoice)
    return tmpl.format(**invoice_data)


def generate_invoice(content, invoice_path, invoice_name):
    """
    Function returns nothing but generate and save invoice's pdf.

    :param content: str
    :param invoice_path: posix_path
    :param invoice_name: str
    :return: none
    """
    html = HTML(string=content)
    html.write_pdf(os.path.join(invoice_path, invoice_name))

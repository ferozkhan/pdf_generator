from weasyprint import HTML

# html = HTML('./invoice_templates/invoice_v1.html')
# html.write_pdf('../invoices/invoice.pdf')


def get_invoice_template():
    return "Date: {invoice_date}," \
           "Number: {invoice_number}"


def get_invoice_data(invoice):
    return {
        "invoice_number": invoice.number,
        "invoice_date": str(invoice.date)
    }


def generate_invoice(invoice):
    tmpl = get_invoice_template()
    invoice_data = get_invoice_data(invoice)
    return tmpl.format(**invoice_data)

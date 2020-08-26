from weasyprint import HTML

# html = HTML('./invoice_templates/invoice_v1.html')
# html.write_pdf('../invoices/invoice.pdf')


def get_invoice_template():
    return "invoice number: {}"

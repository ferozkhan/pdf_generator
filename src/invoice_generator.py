from weasyprint import HTML

html = HTML('./invoice_templates/invoice_v1.html')
html.write_pdf('../invoices/invoice.pdf')

import sys
import pandas as pd
from bs4 import BeautifulSoup
from fpdf import FPDF

def read_file(file_path, file_type):
    if file_type == "csv":
        return pd.read_csv(file_path)
    elif file_type == "excel":
        return pd.read_excel(file_path)
    elif file_type == "html":
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        soup = BeautifulSoup(content, 'lxml')
        tables = soup.find_all('table')
        return pd.read_html(str(tables[0]))[0]
    else:
        print("Unsupported file type")
        return None

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Data Output', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_table(self, df):
        self.set_font('Arial', '', 10)
        col_widths = [self.get_string_width(str(col)) + 10 for col in df.columns]
        for i, row in df.iterrows():
            for j, col in enumerate(row):
                col_widths[j] = max(col_widths[j], self.get_string_width(str(col)) + 10)

        row_height = self.font_size * 1.5
        spacing = 1.5

        # Header
        for i, col in enumerate(df.columns):
            self.cell(col_widths[i], row_height * spacing, col, border=1, align='C')
        self.ln(row_height * spacing)

        # Data
        for i, row in df.iterrows():
            for j, col in enumerate(row):
                self.cell(col_widths[j], row_height * spacing, str(col), border=1)
            self.ln(row_height * spacing)

def save_to_pdf(data, filename):
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title("Data Output")
    pdf.add_table(data)
    pdf.output(filename)
    print(f"Data saved to '{filename}'.")

def main(file_path, file_type):
    data = read_file(file_path, file_type)
    if data is not None:
        save_to_pdf(data, "output.pdf")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 Scraper.py <file_path> <file_type>")
        sys.exit(1)

    file_path = sys.argv[1]
    file_type = sys.argv[2]
    main(file_path, file_type)






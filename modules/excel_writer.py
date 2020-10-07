import pandas as pd

class Writer():
    def __init__(self, df: pd.DataFrame, filename: str):
        self.df = df
        self.writer = pd.ExcelWriter("results.xlsx", engine='xlsxwriter')

    def format_and_save_to_xlsx(self):
        """
        Method used to write pandas dataframe into excel file and format the columns
        :return None:
        """
        self.df.to_excel(self.writer, sheet_name='Products', index=False)
        workbook = self.writer.book
        format = workbook.add_format()
        format.set_align('center')
        format.set_align('vcenter')
        worksheet = self.writer.sheets['Products']
        worksheet.set_column('A:A', 40)
        worksheet.set_column('B:B', 62)
        worksheet.set_column('C:C', 62)
        worksheet.set_column('D:D', 36, format)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 40, format)
        worksheet.set_column('G:G', 30)
        self.writer.save()
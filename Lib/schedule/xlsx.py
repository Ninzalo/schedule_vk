import time
import win32com.client as win32

def xls_to_xlsx(src, dst):
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    try:
        excel.Application.Quit()
    except:
        pass
    time.sleep(2)
    wb = excel.Workbooks.Open(src)
    time.sleep(1)

    wb.SaveAs(dst, FileFormat=51)  # FileFormat = 51 is for .xlsx extension
    wb.Close()  # FileFormat = 56 is for .xls extension
    excel.Application.Quit()
    del wb, excel

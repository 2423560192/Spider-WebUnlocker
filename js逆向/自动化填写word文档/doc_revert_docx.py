#首先得安装pywin32库，此处省略
import os
from win32com.client import Dispatch,DispatchEx,constants



def doc_to_docx(f_path):
    w=Dispatch('Word.Application')
    doc=w.Documents.Open(f_path)
    new_path=os.path.splitext(f_path)[0]+'.docx'
    doc.SaveAs(new_path,12,False,'',True,'',False,False,False,False)
    doc.Close()
    w.Quit()
    return new_path

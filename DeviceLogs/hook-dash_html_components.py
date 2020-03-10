# When you're encountering following error.
# > IOError: [Errno 2] No such file or directory: 'C:\\Users\\username\\AppData\\Local\\Temp\\_MEI502322\\openpyxl\\.constants.json'
# 
# This solution tested under Python 2.7.10 and Pyinstaller 3.0.
# 
# Put this file to your script folder. 
# Add this hook to your distribution by
# > pyinstaller --onefile --additional-hooks-dir=. yourscript.py
#
from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('dash_html_components')

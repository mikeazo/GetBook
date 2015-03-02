GetBook is a Python script to create epub ebooks or .book files and folders (see http://bencrowder.net/blog/2010/06/md2epub/) from the online texts made available by the Neal A. Maxwell Institute for Religious Scholarship at Brigham Young University (http://maxwellinstitute.byu.edu/).  

Requirements:
* Python (2.5 or newer, I think)
* µTidylib (http://utidylib.berlios.de/)
* pyquery (http://pyquery.readthedocs.org/en/latest/)

Instructions:
The book is specified by using the bookid from the book's url, e.g. for _Temple and the Cosmos_ (http://publications.maxwellinstitute.byu.edu/fullscreen/?pub=1123&index=1), the bookid is 1123.  The script will ask the user for the bookid, or it can be passed as an argument.  

Legal stuff:
GetBook.py is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License (http://creativecommons.org/licenses/by-nc-sa/3.0/).
Files created using GetBook.py should not be sold, made available, or otherwise distributed without express consent of the Maxwell institute.  

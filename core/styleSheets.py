style_sheet_good = """QLineEdit{
            background-color: rgba(63,64,66,255);
            border:1px solid green;
            height:25px;
            border-radius:5px;
            color:white;
            padding-left:5px;
            }
        QLineEdit:focus {
        background-color: rgba(63,64,66,255);
        border:1px solid green;
        }
        QLineEdit:hover{
        border:1px solid green;
        
        }
        """
style_sheet_bad = """QLineEdit{
        background-color: rgba(63,64,66,255);
        border:1px solid red;
        height:25px;
        border-radius:5px;
        color:white;
        padding-left:5px;
        }
        QLineEdit:focus {
        background-color: rgba(63,64,66,255);
        border:1px solid red;
        }
        QLineEdit:hover{
        border:1px solid red;
        }
        """
style_sheet_disabled = """QLineEdit{
        background-color: rgba(63,64,66,255);
        border:2px solid black;
        height:25px;
        border-radius:5px;
        color:white;
        padding-left:5px;
        }
        QLineEdit:focus {
        background-color: rgba(63,64,66,255);
        border:2px solid black;
        }
        QLineEdit:hover{
        border:2px solid black;
        }
        """

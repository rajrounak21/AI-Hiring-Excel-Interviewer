import pandas as pd

# Define the data
data = [
    {
        "id": 1,
        "question": "What is VLOOKUP in Excel and how is it used?",
        "ideal_answer": "VLOOKUP is a lookup function in Excel used to search for a value in the first column of a table and return a value in the same row from a specified column. The syntax is VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup]). It's commonly used for looking up prices, names, or other associated data."
    },
    {
        "id": 2,
        "question": "Explain the difference between absolute and relative cell references.",
        "ideal_answer": "An absolute reference (e.g., $A$1) refers to a fixed location in a spreadsheet and does not change when the formula is copied elsewhere. A relative reference (e.g., A1) adjusts based on the position of the cell in which it's used. Mixed references (e.g., $A1 or A$1) fix only the column or row."
    },
    {
        "id": 3,
        "question": "What are Pivot Tables and why are they used?",
        "ideal_answer": "Pivot Tables are powerful tools in Excel used to summarize, analyze, explore, and present large amounts of data. They allow users to drag and drop fields to rows, columns, and values to generate meaningful reports like totals, averages, and counts grouped by categories."
    },
    {
        "id": 4,
        "question": "How does the IF function work in Excel?",
        "ideal_answer": "The IF function is a logical function that returns one value if a condition is TRUE and another if FALSE. Syntax: IF(condition, value_if_true, value_if_false). Example: IF(A1>10, \"High\", \"Low\") checks if the value in A1 is greater than 10 and returns 'High' if true, otherwise 'Low'."
    },
    {
        "id": 5,
        "question": "What is conditional formatting and how can it be applied?",
        "ideal_answer": "Conditional Formatting allows users to automatically apply formatting like colors, bold text, or icons to cells based on the cell’s value. It’s commonly used to highlight duplicates, top/bottom values, or apply color scales. Accessible via Home > Conditional Formatting in the ribbon."
    },
    {
        "id": 6,
        "question": "What is the difference between COUNT, COUNTA, and COUNTIF functions?",
        "ideal_answer": "COUNT counts numeric values only, COUNTA counts non-empty cells including text, and COUNTIF counts the number of cells that meet a specified condition. For example, COUNTIF(A1:A10,\">5\") counts how many values in A1:A10 are greater than 5."
    },
    {
        "id": 7,
        "question": "How do you remove duplicates from a dataset in Excel?",
        "ideal_answer": "To remove duplicates, select the data range, go to Data tab → Remove Duplicates. You can choose which columns to check for duplicates. Excel will remove repeated rows based on selected criteria while keeping the first occurrence."
    },
    {
        "id": 8,
        "question": "How does data validation work in Excel?",
        "ideal_answer": "Data Validation restricts the type of data that can be entered into a cell. It can enforce rules like allowing only whole numbers, dates, or values from a dropdown list. It is set via Data → Data Validation. You can also display input messages and error alerts."
    },
    {
        "id": 9,
        "question": "Explain the use of INDEX and MATCH functions together.",
        "ideal_answer": "INDEX and MATCH are used together as a flexible alternative to VLOOKUP. MATCH finds the row/column number of a value, and INDEX returns the value at that location. Example: INDEX(B2:B10, MATCH(\"Product A\", A2:A10, 0)) returns the value in column B for 'Product A' in column A."
    },
    {
        "id": 10,
        "question": "What is the difference between a table and a range in Excel?",
        "ideal_answer": "A range is just a group of cells, while a table (Insert → Table) is a structured object with headers, automatic filtering, and features like structured references. Tables auto-expand, apply consistent formatting, and are easier to use in formulas like SUMIFS or structured references."
    },
    {
        "id": 11,
        "question": "What is the purpose of the CONCATENATE function (or CONCAT) in Excel?",
        "ideal_answer": "The CONCATENATE (or newer CONCAT) function joins two or more text strings into one. Example: CONCATENATE(\"First\", \" \", \"Last\") results in 'First Last'. It's useful for combining names, addresses, or codes from multiple cells."
    },
    {
        "id": 12,
        "question": "Explain how to use the TEXT function in Excel and give an example.",
        "ideal_answer": "The TEXT function formats numbers, dates, or values into specified text formats. Example: TEXT(TODAY(), \"dd-mm-yyyy\") converts the current date into a readable format. It’s often used to display currency, percentages, or date formats."
    },
    {
        "id": 13,
        "question": "What is the difference between a workbook and a worksheet in Excel?",
        "ideal_answer": "A workbook is the entire Excel file (.xlsx) that may contain multiple sheets. Each sheet (or worksheet) is a tab within the workbook, containing a grid of rows and columns for data entry. Workbooks are containers for organizing multiple datasets."
    },
    {
        "id": 14,
        "question": "How do you protect a worksheet or specific cells in Excel?",
        "ideal_answer": "To protect a sheet, go to Review → Protect Sheet, and set a password. To lock specific cells, first unlock all cells (Ctrl+A → Format Cells → Protection), then select only the cells to lock and protect the sheet. This prevents unwanted edits."
    },
    {
        "id": 15,
        "question": "What is the use of the INDIRECT function in Excel?",
        "ideal_answer": "INDIRECT returns the value of a cell specified by a text string. For example, INDIRECT(\"A1\") returns the value in cell A1. It’s useful for dynamically changing references, such as referring to a range based on input or variable sheet names."
    },
    {
        "id": 16,
        "question": "How can you apply filters to data in Excel?",
        "ideal_answer": "Select the header row of a dataset, then go to Data → Filter. Small dropdown arrows appear in each header cell, allowing you to filter based on values, text, numbers, or even by color. Useful for analyzing specific subsets of data."
    },
    {
        "id": 17,
        "question": "What does the LEN function do in Excel?",
        "ideal_answer": "LEN returns the number of characters in a cell, including spaces. Example: LEN(\"Excel Tips\") returns 10. It’s useful for cleaning or validating text, especially in data preparation or when trimming values."
    },
    {
        "id": 18,
        "question": "Explain how to create a dropdown list using Data Validation.",
        "ideal_answer": "To create a dropdown, select the cell(s), go to Data → Data Validation → Allow: List, then enter a list of comma-separated values (e.g., Yes, No, Maybe) or reference a cell range. This helps enforce consistent input from users."
    },
    {
        "id": 19,
        "question": "What is the use of the TRIM function in Excel?",
        "ideal_answer": "TRIM removes all extra spaces from text, leaving only single spaces between words. Example: TRIM(\"  Hello   World \") returns \"Hello World\". It’s especially useful when cleaning imported or user-entered data."
    },
    {
        "id": 20,
        "question": "What is the use of the Excel Table feature, and how is it different from a range?",
        "ideal_answer": "Excel Tables (Insert → Table) are structured data objects that automatically expand, apply consistent formatting, and enable structured references. Unlike normal ranges, tables auto-update in formulas, offer better filtering, and improve data clarity."
    }
]

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to Excel
df.to_csv("excel_questions.csv", index=False)

print("✅ Dataset created and saved as 'excel_questions.csv'")

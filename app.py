import PySimpleGUI as sg
import sqlite3

#All this function is doing is fetching the data thats already in the database
def fetch_data_from_db(database_name, query="SELECT * FROM DiningHall_Rating"):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()  #fetching each row in db
        headers = [desc[0] for desc in cursor.description]  #setting up to create headers for each column of data
        connection.close()
        return headers, rows
    except sqlite3.Error as e:
        sg.popup_error(f"Database error: {e}")
        return [], []

#WINDOW LAYOUT
def create_main_window(db_name):
    sg.theme('TealMono')
    headers, data = fetch_data_from_db(db_name)

    #this converts the list of tuples to a list of lists (this is required)
    data = [list(row) for row in data]

    #display layout (This will change once functionality is all set)
    layout = [
        [sg.Text("Dining Hall Ratings")],
        [sg.Table(values=data,
                  headings=headers,
                  display_row_numbers=False,
                  auto_size_columns=True,
                  justification='center',
                  num_rows=min(25, len(data)),
                  enable_events=True, #fixing text field being cut off
                  key='-TABLE-')],
        [sg.Text("Sort by:"),
         #using combo for a dropdown box, it looks better easier to use
         sg.Combo(headers, default_value=headers[0], key= '-SORT_COLUMN-', readonly=True),
         sg.Button("Sort")],[sg.Text("Full Feedback:"),
         #creating textbox so when data is selected the full text can be seen
         sg.Multiline(size=(70, 5), disabled=True, key='-FEEDBACK_DISPLAY-')],
        [sg.Button("Exit")]
    ]

    return sg.Window("Survey Data Viewer", layout, finalize=True)
#main function to run app and have button functions have a working operation
def main():
    database_name = 'BSU_Reviews.db'
    window = create_main_window(database_name)

    while True:
        event, values = window.read()
        #exit function
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        elif event == "-TABLE-":
            #selected row index
            selected_row = values['-TABLE-']
            if selected_row:
                #taking feedback from selected row
                selected_row_index = selected_row[0]
                feedback_text = window['-TABLE-'].Values[selected_row_index][-1]  #feedback is last column
                window['-FEEDBACK_DISPLAY-'].update(feedback_text)
            #sorting function
        elif event == "Sort":
            sort_column = values['-SORT_COLUMN-']
            if sort_column:
                query = f"SELECT * FROM DiningHall_Rating ORDER BY {sort_column}"
                headers, sorted_data = fetch_data_from_db(database_name, query)
                sorted_data = [list(row) for row in sorted_data]
                # refreshing window with new sorted data from user request
                window['-TABLE-'].update(values=sorted_data)
            else:
                sg.popup("Select a column to sort by.")

    window.close()

if __name__ == '__main__':
    main()

def foo(a: int = 0, b: int = 0, c=0):
    return (a * b) + c


def bar(x, greeting='hello'):
    return f"{greeting} {x}"


def confuser(a: int = 0, x: float = 3.14):
    return (a ** 2) * x


funcs = [foo, bar, confuser]

if __name__ == '__main__':

    import PySimpleGUI as sg

    # All the stuff inside your window.
    layments = list()
    layments.append([sg.Text('a')])

    layout = [[sg.Text('Some text on Row 1')],
              [sg.Text('Enter something on Row 2'), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):  # if user closes window or clicks cancel
            break
        print('You entered ', values[0])

    window.close()

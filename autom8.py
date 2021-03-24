import pyautogui as pg
import dearpygui.core as dpg
import dearpygui.simple as sdpg
import uuid





class Autom8App:
    def __init__(self, m8s):
        self.m8s = m8s

    def __render(self, sender, data):
        """Run every frame to update the GUI.
        Updates the table by clearing it and inserting rows with the data.
        """
        dpg.clear_table('m8s')
        for m8 in self.m8s:
            dpg.add_row('m8s', [m8['id'], m8['type'], m8['action'], m8['active']])

    def clear_input_options(self):
        print("input options cleared")
        pass

    def show_keyboard_options(self):
        print("displaying keyboard options")
        pass

    def show_mouse_options(self):
        print("displaying mouse options")
        pass

    def __on_input_selected(self, sender, data):
        """Change interface.
        Update the interface to show keyboard or mouse options.
        """
        input_selected = dpg.get_value('input-type')
        if input_selected == "keyboard":
            self.clear_input_options()
            self.show_keyboard_options()
        elif input_selected == "mouse":
            self.clear_input_options()
            self.show_mouse_options()
        else:
            self.clear_input_options()

    def __add_m8(self, sender, data):
        """Add a new m8.
        Get the data from the input text, append a new m8 to the m8s list
        and then clear the text of the input.
        """
        new_m8_content = dpg.get_value('input-type')
        new_m8 = {'id': uuid.uuid4().hex, 'content': new_m8_content, 'done': False}
        self.m8s.append(new_m8)
        dpg.set_value('new-m8-title', '')

    def __toggle_m8(self, sender, data):
        """Toggle a m8 active to True of False.
        Get the selected cell of the table (list of [row index, column index])
        and uses the row index to update the m8 at that index in the m8s
        list. Then, saves the selected row index in the case you would want to
        delete that m8.
        """
        m8_row = dpg.get_table_selections("m8s")
        m8 = self.m8s[m8_row[0][0]]
        m8['done'] = not m8['done']
        dpg.add_data('selected-m8-index', self.m8s.index(m8))
        dpg.set_value('Selected m8:', f"Selected id: {m8['id']}")

    def __remove_m8(self, sender, data):
        """Remove a m8 from the m8s list based on the selected row."""
        m8_index = dpg.get_data('selected-m8-index')
        self.m8s.pop(m8_index)

    def __clear_m8s(self, sender, data):
        """Clear all the m8s."""
        self.m8s = []

    def show(self):
        screen_size = pg.size()
        half_width = screen_size.width/2
        half_height = screen_size.height/2
        """Start the gui."""
        with sdpg.window("Main Window"):
            dpg.set_main_window_size(int(half_width), int(half_height))
            dpg.set_main_window_pos(int(half_width/2), int(half_height/2))
            dpg.set_main_window_resizable(False)
            dpg.set_main_window_title("autom8")

            dpg.add_text("Easy Keyboard and Mouse Automation")
            dpg.add_text("select keyoard or mouse input", bullet=True)
            dpg.add_text("set input options", bullet=True)
            dpg.add_text("add input to autom8 list", bullet=True)
            dpg.add_separator()

            dpg.add_spacing(count=10)
            dpg.add_combo("Input Type", source="input-type", items=["keyboard", "mouse"], callback=self.__on_input_selected)
            dpg.add_combo("Click Type", source="click-type", items=["left click", "right click", "middle click"])
            dpg.add_input_text("New m8 Title", source="new-m8-title")
            dpg.add_button("Add m8", callback=self.__add_m8)
            dpg.add_spacing(count=10)
            dpg.add_separator()

            dpg.add_table('m8s', ['ID', 'Type', 'Action', 'Active'], height=200, callback=self.__toggle_m8)
            dpg.add_separator()
            dpg.add_text("Selected m8:")
            dpg.add_button("Remove m8", callback=self.__remove_m8)
            dpg.add_button("Clear m8s", callback=self.__clear_m8s)

            # Render Callback and Start gui
            dpg.set_render_callback(self.__render)
        dpg.start_dearpygui(primary_window="Main Window")


if __name__ == '__main__':
    m8s = [
        {'id': uuid.uuid4().hex, 'type': 'mouse', 'action': 'move', 'active': False},
        {'id': uuid.uuid4().hex, 'type': 'keyboard','action': 'keypress', 'active': False},
        {'id': uuid.uuid4().hex, 'type': 'mouse', 'action': 'scroll', 'active': True},
    ]

    autom8_app = Autom8App(m8s)
    autom8_app.show()



# pg.moveTo(half_width, half_height, duration=0.05)  # move mouse to XY coordinates over num_second seconds

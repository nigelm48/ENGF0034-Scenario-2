from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from plyer import notification
import re

class MedicationReminderApp(App):
    def build(self):
        self.medicines = []
        self.schedule = {}
        self.root = BoxLayout(orientation='vertical')
        self.med_input = TextInput(hint_text='Enter medicine name')
        self.add_button = Button(text='Add Medicine', on_press=self.add_medicine)
        self.root.add_widget(Label(text='Medication Reminder'))
        self.root.add_widget(self.med_input)
        self.root.add_widget(self.add_button)
        return self.root

    def add_medicine(self, instance):
        medicine_name = self.med_input.text
        popup = SchedulePopup(self.add_schedule)
        popup.open()

        def callback(instance):
            self.medicines.append((medicine_name, self.schedule.get(medicine_name, [])))
            notification.notify(
                title='Medication Reminder',
                message=f"Don't forget to take {medicine_name}",
                app_icon=None,  # Add path to custom icon if desired
                timeout=10  # Reminder notification timeout in seconds
            )
            self.med_input.text = ''  # Clear the input field

        popup.bind(on_dismiss=callback)

    def add_schedule(self, medicine_name, schedule):
        self.schedule[medicine_name] = schedule

class SchedulePopup(Popup):
    def __init__(self, callback, **kwargs):
        super(SchedulePopup, self).__init__(**kwargs)
        self.callback = callback

        layout = BoxLayout(orientation='vertical')
        self.content = layout

        self.schedule_input = TextInput(hint_text='Enter schedule (e.g., 8:00 AM, 12:00 PM)')
        self.add_button = Button(text='Add Schedule', on_press=self.add_schedule)
        layout.add_widget(Label(text='Enter Schedule'))
        layout.add_widget(self.schedule_input)
        layout.add_widget(self.add_button)

    def add_schedule(self, instance):
        schedule_input_text = self.schedule_input.text
        schedule_regex = r'(\d{1,2}:\d{2}\s(?:AM|PM))'
        matches = re.findall(schedule_regex, schedule_input_text)
        if matches:
            schedule = [match.strip() for match in matches]
            self.callback(schedule_input_text, schedule)
            self.dismiss()
        else:
            invalid_input_popup = InvalidInputPopup()
            invalid_input_popup.open()

class InvalidInputPopup(Popup):
    def __init__(self, **kwargs):
        super(InvalidInputPopup, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        self.content = layout

        ok_button = Button(text='OK', on_press=self.dismiss)
        layout.add_widget(Label(text='Invalid schedule format. Please enter in the format "8:00 AM, 12:00 PM"'))
        layout.add_widget(ok_button)

if __name__ == '__main__':
    MedicationReminderApp().run()

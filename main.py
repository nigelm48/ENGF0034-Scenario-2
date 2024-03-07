from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from plyer import notification
import re


class MedicationReminderApp(App):
    def __init__(self, **kwargs):
        super(MedicationReminderApp, self).__init__(**kwargs)
        self.reminders = []

    def build(self):
        self.root = BoxLayout(orientation='vertical')
        self.root.add_widget(Label(text='Phainder', font_size=24))

        # Button to set medication reminder
        set_medication_button = Button(
            text='Set Medication Reminder', font_size=20)
        set_medication_button.bind(on_press=self.set_medication_reminder)
        self.root.add_widget(set_medication_button)

        # Button to set refill reminder
        set_refill_button = Button(text='Set Refill Reminder', font_size=20)
        set_refill_button.bind(on_press=self.set_refill_reminder)
        self.root.add_widget(set_refill_button)

        # Button to see all reminders
        view_reminders_button = Button(text='View Reminders', font_size=20)
        view_reminders_button.bind(on_press=self.view_reminders)
        self.root.add_widget(view_reminders_button)

        # Button to exit the app
        exit_button = Button(text='Exit', font_size=20)
        exit_button.bind(on_press=exit)
        self.root.add_widget(exit_button)

        return self.root

    def set_medication_reminder(self, instance):
        popup = MedicineNamePopup(self.add_medication_schedule)
        popup.open()

    def set_refill_reminder(self, instance):
        popup = MedicineNamePopup(self.add_refill_schedule, is_date=True)
        popup.open()

    def add_medication_schedule(self, medicine_name):
        popup = SchedulePopup(
            self.add_schedule, reminder_type='Medication', medicine_name=medicine_name)
        popup.open()

    def add_refill_schedule(self, medicine_name, date):
        # Schedule notification using Plyer for refill reminder
        notification_title = 'Refill Reminder'
        notification_message = f"Don't forget to refill {medicine_name} on {date}"
        notification.notify(
            title=notification_title,
            message=notification_message,
            timeout=10  # Reminder notification timeout in seconds
        )
        self.reminders.append((medicine_name, date))

    def add_schedule(self, medicine_name, schedule, reminder_type):
        # Schedule notification using Plyer for medication reminder
        notification_title = 'Medication Reminder'
        notification_message = f"Don't forget to take {medicine_name} at {', '.join(schedule)}"
        notification.notify(
            title=notification_title,
            message=notification_message,
            timeout=10  # Reminder notification timeout in seconds
        )
        self.reminders.append((medicine_name, schedule, reminder_type))

    def get_all_reminders(self):
        # Get all scheduled reminders
        return self.reminders

    def view_reminders(self, instance):
        reminder = self.get_all_reminders()
        RemindersPopup(reminder).open()


class MedicineNamePopup(Popup):
    def __init__(self, callback, is_date=False, **kwargs):
        super(MedicineNamePopup, self).__init__(**kwargs)
        self.title = 'Enter Medicine Name'
        self.callback = callback
        self.is_date = is_date

        layout = BoxLayout(orientation='vertical')
        self.content = layout

        self.med_name_input = TextInput(
            hint_text='Enter medicine name', multiline=False)
        layout.add_widget(Label(text='Enter Medicine Name', font_size=18))
        layout.add_widget(self.med_name_input)

        if is_date:
            self.date_input = TextInput(
                hint_text='Enter date (dd/mm/yyyy)', multiline=False)
            layout.add_widget(Label(text='Enter Refill Date', font_size=18))
            layout.add_widget(self.date_input)
        else:
            self.date_input = None

        add_button = Button(text='Next', font_size=16)
        add_button.bind(on_press=self.get_input)
        layout.add_widget(add_button)

    def get_input(self, instance):
        medicine_name = self.med_name_input.text.strip()
        if self.is_date:
            date = self.date_input.text.strip()
            self.callback(medicine_name, date)
        else:
            self.callback(medicine_name)
        self.dismiss()


class SchedulePopup(Popup):
    def __init__(self, callback, reminder_type, medicine_name, **kwargs):
        super(SchedulePopup, self).__init__(**kwargs)
        self.title = 'Set Schedule'
        self.callback = callback
        self.reminder_type = reminder_type
        self.medicine_name = medicine_name

        layout = BoxLayout(orientation='vertical')
        self.content = layout

        self.schedule_input = TextInput(
            hint_text='Enter schedule (e.g., 8:00 AM, 12:00 PM)', multiline=False)
        layout.add_widget(
            Label(text=f'Enter {reminder_type} Schedule', font_size=18))
        layout.add_widget(self.schedule_input)

        add_button = Button(text='Add Schedule', font_size=16)
        add_button.bind(on_press=self.add_schedule)
        layout.add_widget(add_button)

    def add_schedule(self, instance):
        schedule_input_text = self.schedule_input.text
        schedule_regex = r'(\d{1,2}:\d{2}\s(?:AM|PM))'
        matches = re.findall(schedule_regex, schedule_input_text)
        if matches:
            schedule = [match.strip() for match in matches]
            self.callback(self.medicine_name, schedule, self.reminder_type)
            self.dismiss()
        else:
            invalid_input_popup = InvalidInputPopup()
            invalid_input_popup.open()


class RemindersPopup(Popup):
    def __init__(self, reminders, **kwargs):
        super(RemindersPopup, self).__init__(**kwargs)
        self.title = 'Reminders'

        layout = BoxLayout(orientation='vertical')
        self.content = layout

        close_button = Button(text='Close', on_press=self.dismiss)
        layout.add_widget(Label(text='Reminders', font_size=30))
        for reminder in reminders:
            layout.add_widget(Label(text=str(reminder), font_size=20))
        layout.add_widget(close_button)


class InvalidInputPopup(Popup):
    def __init__(self, **kwargs):
        super(InvalidInputPopup, self).__init__(**kwargs)
        self.title = 'Invalid Input'

        layout = BoxLayout(orientation='vertical')
        self.content = layout

        ok_button = Button(text='OK', on_press=self.dismiss)
        layout.add_widget(Label(
            text='Invalid schedule format. Please enter in the format "8:00 AM, 12:00 PM"', font_size=16))
        layout.add_widget(ok_button)


if __name__ == '__main__':
    MedicationReminderApp().run()
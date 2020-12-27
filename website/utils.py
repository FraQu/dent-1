from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Appointment

class WeekScheduler(HTMLCalendar):
	def __init__(self):
		super(WeekScheduler, self).__init__()

	#returns current 5 week days MON-FRI
	def current_week(self, scheduled_date):
		one_day = timedelta(days=1)
		day_id = scheduled_date.weekday()
		date = scheduled_date - timedelta(days=day_id)
		week = []
		for n in range(5):
			week.append(date)
			date += one_day
		return week

	#returns events in separate cell for given date
	def daily_appointments(self, date, all_appointments):
		day_appointments = all_appointments.filter(start_time__date=date)
		single_appointment = ''
		for appointment in day_appointments:
			single_appointment += f'<li class="list-group-item list-group-item-action"> {appointment.get_html_url} </li>'

		if date != 0:
			return f"<td><ul class='list-group list-group-flush'> {single_appointment} </ul></td>"
		return '<td></td>'

	def caltabcreator(self, scheduled_date):
		all_appointments = Appointment.objects.all()
		current_week = self.current_week(scheduled_date)

		table = f'<table class="table table-dark table-bordered customized-card">\n'
		table += f'<tr>' \
			f'<th scope="col">Monday {current_week[0]}</th>' \
			f'<th scope="col">Tuesday {current_week[1]}</th>' \
			f'<th scope="col">Wednesday {current_week[2]}</th>' \
			f'<th scope="col">Thursday {current_week[3]}</th>' \
			f'<th scope="col">Friday {current_week[4]}</th></tr>'
		table += f'<tr>'
		for date in current_week:
			eventsforday = self.daily_appointments(date, all_appointments)
			table += f'{eventsforday}'
		table += f'</tr>'

		return table

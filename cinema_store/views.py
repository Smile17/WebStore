from io import BytesIO
from pathlib import Path

from django.shortcuts import render
from cinema_store.models import Cinema, Session, Film
from datetime import date, datetime, timedelta
from django.http import FileResponse
from django.http import HttpResponse
from reportlab.pdfgen import canvas

def index(request):
    # start time
    start_time = "07:00:00"
    start_time = datetime.strptime(start_time, "%H:%M:%S")
    today = date.today()
    session_date = request.GET.get('session_date', today)
    #session_date = today - timedelta(days=1)
    cinemas = Cinema.get_all_cinemas()
    cinemas_with_films = []
    for cinema in cinemas:
        #halls = cinema.hall_set.filter(session__date=session_date)
        halls = cinema.hall_set.all()
        sessions_by_films = {}
        #print(cinema.name)
        if halls:
            for hall in halls:
                sessions = hall.session_set.filter(date=session_date)
                if sessions:
                    for s in sessions:
                        end_time = s.time.strftime("%H:%M")
                        t = datetime.strptime(end_time, "%H:%M")
                        delta = t - start_time
                        offset = (delta.total_seconds() / 3660 ) * 5
                        d = {'time': end_time, 'offset': offset, 'price': s.price, 'session_id':s.id}
                        if s.film_id in sessions_by_films.keys():
                            film = sessions_by_films[s.film_id]
                            if s.hall_id in film.keys():
                                film[s.hall_id].append(d)
                            else:
                                film[s.hall_id] = [d]
                        else:
                            sessions_by_films[s.film_id] = {s.hall_id:[d]}
                #print(sessions_by_films)
            cinema_data = {
                'id': cinema.id,
                'name': cinema.name,
                'location': cinema.location,
                'image': cinema.image,
                'phone': cinema.phone,
                'email': cinema.email,
                'sessions_by_films': sessions_by_films
            }
            cinemas_with_films.append(cinema_data)

    #print(cinemas_with_films)
    data = {}
    data['cinemas_with_films'] = cinemas_with_films
    return render(request, 'index.html', data)

def film_page(request, film_id):
    film = Film.objects.get(id=film_id)
    context = {"film": film}
    return render(request, "film.html", context)

def session_page(request, session_id):
    session = Session.objects.get(id=session_id)
    film = session.film_id
    tickets = session.ticket_set.filter(is_available=True)
    #tickets = session.ticket_set.all() # for testing
    context = {"film": film, "session": session, 'tickets': tickets}
    return render(request, "session.html", context)


from django.http import JsonResponse
from .models import Ticket
#from django.http import HttpResponse
import json

#@login_required
def buy_tickets(request):
  if request.method == 'POST':
      json_data = json.loads(request.body)
      selected_tickets = json_data.get('selected_tickets')  # Retrieve selected ticket IDs
      # Example logic for updating ticket status (assuming a boolean field `is_available`)
      print(selected_tickets)
      for ticket_id in selected_tickets:
          ticket = Ticket.objects.get(pk=ticket_id)  # Retrieve the ticket object
          ticket.is_available = False
          ticket.save()
      # Generate PDF content
      try:
          response = HttpResponse(content_type='application/pdf')
          response['Content-Disposition'] = 'attachment; filename=ticket.pdf'  # Set download filename
          generate_pdf_file(response, selected_tickets)
          return response
      except Exception as e:
          # Catch errors and provide a more informative response
          print(f"An error occurred during PDF generation: {e}")
          return JsonResponse({'message': 'An error occurred while generating the ticket PDF. Please try again later.'},
                              status=500)
  else:
      return JsonResponse({'error': 'Invalid request method'}, status=400)


from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts

from reportlab.lib.utils import rl_isfile, open_for_read
import os
#fn = '/Roboto-Regular.ttf'

def generate_pdf_file(response, selected_tickets):
    BASE_DIR = Path(__file__).resolve().parent.parent
    fn = BASE_DIR / 'cinema_store/static/Roboto-Regular.ttf'
    pdfmetrics.registerFont(ttfonts.TTFont('Roboto', fn, 'UTF-8'))
    default_font = 'Roboto'

    p = canvas.Canvas(response)
    p.setFont(default_font, 12)  # Set font and size

    tickets = Ticket.objects.filter(id__in=selected_tickets)
    # Create a PDF document
    p.drawString(100, 750, "Tickets")

    y = 700
    for ticket in tickets:
        session = ticket.session
        p.drawString(100, y, f"Film: {session.film_id.name}".encode('utf-8'))
        p.drawString(100, y - 20, f"Cinema: {session.hall_id.cinema_id.name}".encode('utf-8'))
        p.drawString(100, y - 40, f"Hall: {session.hall_id.name}".encode('utf-8'))
        p.drawString(100, y - 60, f"Date time: {session.date} - {session.time}".encode('utf-8'))
        p.drawString(100, y - 80, f"Price: {ticket.price}₴".encode('utf-8'))
        y -= 100

    p.showPage()
    p.save()

    return p
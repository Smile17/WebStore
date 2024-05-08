from django.shortcuts import render
from cinema_store.models import Cinema, Session
from datetime import date, datetime, timedelta

def index(request):
    # start time
    start_time = "07:00:00"
    start_time = datetime.strptime(start_time, "%H:%M:%S")
    today = date.today()
    session_date = today - timedelta(days=1)
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
                        d = {'time': end_time, 'offset': offset}

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
from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import csv
from django.core.paginator import Paginator

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


# generate the pdf file for venues

def venue_pdf(request):
    # create Bytestream, buffer
    buf = io.BytesIO()
    #     Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # add some lines of text

    # lines = [
    #     "This is line 1",
    #     "This is line 1",
    #     "This is line 1",
    # ]

    venues = Venue.objects.all()

    lines = []

    # append
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)

    # loop
    for line in lines:
        textob.textLine(line)

    # finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # return something

    return FileResponse(buf, as_attachment="true", filename='venue.pdf')


# venue csv
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues-list.csv'

    # create a csv writer to

    writer = csv.writer(response)

    # designate the mode
    # takes everything from venue object
    venues = Venue.objects.all()

    # Add column headings to the csv files

    writer.writerow(['Venue Name', 'Address', 'Phone number', 'Zip Code', "Phone Number", "Web Address", "Email"])

    for venue in venues:
        writer.writerow(
            [venue.name, venue.address, venue.phone, venue.zip_code, venue.phone, venue.web, venue.email_address])

    return response


# genrate text file from venues

def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues-list.txt'

    # designate the mode
    # takes everything from venue object
    venues = Venue.objects.all()

    lines = []
    # loop through it
    for venue in venues:
        # adds everything to lines array
        lines.append(
            f'{venue.name}\n{venue.address}\n{venue.phone}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n')
    # lines = ["This is line 1\n ", "This is on the line two \n", "this is line three \n"]

    #      write to the text file

    response.writelines(lines)
    return response


# Create your views here.
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('list-events')


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                # form.save()
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        # just going to the page, not submitting,
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {
        'form': form,
        'submitted': submitted,
    })


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 'events/update_event.html', {
        'event': event,
        'form': form,
    })


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, 'events/update_venue.html', {
        'venue': venue,
        'form': form,
    })


def search_venue(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html', {
            'searched': searched,
            'venues': venues,
        })

    else:
        return render(request, 'events/search_venues.html', {

        })


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, 'events/show_venue.html', {
        'venue': venue,
    })


def list_venues(request):
    # venue_list = Venue.objects.all().order_by('?')
    venue_list = Venue.objects.all()
    # Setup pagination here
    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages

    return render(request, 'events/venue.html', {
        'venues': venues,
        "venue_list": venue_list,
        'nums': nums,
    })


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id  # logged in user
            venue.save()
            # form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_venue.html', {
        'form': form,
        'submitted': submitted,
    })


def all_events(request):
    event_list = Event.objects.all().order_by('?')

    return render(request, 'events/event_list.html', {
        'event_list': event_list,
    })


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Rokas"
    month = month.capitalize()
    # Convert month name to number

    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    #  crate calendar

    cal = HTMLCalendar().formatmonth(
        year,
        month_number,
    )
    # get current year

    now = datetime.now()
    current_year = now.year

    # get current time

    time = now.strftime('%I:%M %p')

    return render(request, 'events/home.html', {
        "name": name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": time,
    })

#  done super easy

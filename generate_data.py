import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# List of DJs with varying frequencies
djs = [
    ('Carl Cox', 'Techno'),
    ('Amelie Lens', 'Techno'),
    ('Charlotte de Witte', 'Techno'),
    ('Nina Kraviz', 'Techno'),
    ('David Guetta', 'EDM'),
    ('Adam Beyer', 'Techno'),
    ('Armin van Buuren', 'Trance'),
    ('Deadmau5', 'Progressive House'),
    ('Solomun', 'Deep House'),
    ('Richie Hawtin', 'Techno'),
    ('Peggy Gou', 'House'),
    ('The Martinez Brothers', 'House'),
    ('Dixon', 'Deep House'),
    ('Black Coffee', 'Afro House'),
    ('Skrillex', 'Dubstep'),
    ('Eric Prydz', 'Progressive House'),
    ('Jamie Jones', 'Tech House'),
    ('Marco Carola', 'Techno'),
    ('Disclosure', 'House'),
    ('Paul Kalkbrenner', 'Techno'),
    ('Reinier Zonneveld', 'Techno'),
    ('Boris Brejcha', 'Minimal Techno'),
    ('Netsky', 'Drum & Bass'),
    ('Flume', 'Future Bass'),
    ('Bicep', 'Electronic'),
    ('Tiësto', 'EDM'),
    ('Four Tet', 'Electronic'),
    ('CamelPhat', 'Tech House'),
    ('Bonobo', 'Electronica'),
    ('RÜFÜS DU SOL', 'Live Electronic'),
    ('Jamie xx', 'Electronic'),
    ('Fisher', 'House'),
    ('Sasha & John Digweed', 'Progressive House'),
    ('Martin Garrix', 'EDM'),
]

# Assign number of events per DJ (some DJs have more events)
dj_event_counts = {
    'Carl Cox': 15,
    'Amelie Lens': 12,
    'Charlotte de Witte': 10,
    'Nina Kraviz': 8,
    'David Guetta': 7,
    # Other DJs get fewer events
    'Adam Beyer': 5,
    'Armin van Buuren': 5,
    'Deadmau5': 4,
    'Solomun': 4,
    'Richie Hawtin': 4,
    'Peggy Gou': 3,
    'The Martinez Brothers': 3,
    'Dixon': 3,
    'Black Coffee': 3,
    'Skrillex': 3,
    'Eric Prydz': 3,
    'Jamie Jones': 2,
    'Marco Carola': 2,
    'Disclosure': 2,
    'Paul Kalkbrenner': 2,
    'Reinier Zonneveld': 2,
    'Boris Brejcha': 2,
    'Netsky': 2,
    'Flume': 2,
    'Bicep': 2,
    'Tiësto': 2,
    'Four Tet': 2,
    'CamelPhat': 2,
    'Bonobo': 2,
    'RÜFÜS DU SOL': 2,
    'Jamie xx': 2,
    'Fisher': 2,
    'Sasha & John Digweed': 2,
    'Martin Garrix': 2,
}

# List of event types
event_types = ['Festival', 'Club Gig', 'Concert']

# List of venues (you can expand this list)
venues = [
    # (venue_name, city, country, latitude, longitude)
    ('Bayfront Park', 'Miami', 'USA', 25.7801, -80.1826),
    ('Gashouder', 'Amsterdam', 'Netherlands', 52.3867, 4.8731),
    ('United Center', 'Chicago', 'USA', 41.8807, -87.6742),
    ('Empire Polo Club', 'Indio', 'USA', 33.6803, -116.2377),
    ('Pacha', 'Ibiza', 'Spain', 38.9185, 1.4434),
    ('Boom', 'Boom', 'Belgium', 51.0926, 4.3717),
    ('Printworks', 'London', 'UK', 51.4985, -0.0429),
    ('Fira Montjuïc', 'Barcelona', 'Spain', 41.3722, 2.1540),
    ('Warung Beach Club', 'Itajaí', 'Brazil', -26.9536, -48.6301),
    ('Hart Plaza', 'Detroit', 'USA', 42.3296, -83.0458),
    ('Output', 'New York', 'USA', 40.7213, -73.9577),
    ('Exchange LA', 'Los Angeles', 'USA', 34.0486, -118.2551),
    ('Wembley Arena', 'London', 'UK', 51.4985, -0.0429),  # Harmonized coordinates for London
    ('Maimarkthalle', 'Mannheim', 'Germany', 49.4707, 8.5140),
    ('Hi Ibiza', 'Ibiza', 'Spain', 38.9185, 1.4434),  # Harmonized coordinates for Ibiza
    ('Las Vegas Motor Speedway', 'Las Vegas', 'USA', 36.2733, -115.0119),
    ('DC10', 'Ibiza', 'Spain', 38.9185, 1.4434),  # Harmonized coordinates for Ibiza
    ('Petrovaradin Fortress', 'Novi Sad', 'Serbia', 45.2520, 19.8610),
    ('Red Rocks Amphitheatre', 'Morrison', 'USA', 39.6654, -105.2057),
    ('Berghain', 'Berlin', 'Germany', 52.5111, 13.4416),
    # Add more venues as needed
]

# Generate dates between Jan 1, 2022 and Dec 31, 2024
start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = [start_date + timedelta(days=x) for x in range(0, (end_date - start_date).days)]

events = []

for dj, genre in djs:
    num_events = dj_event_counts.get(dj, 1)
    dj_dates = random.sample(date_range, num_events)
    for date in dj_dates:
        event_type = random.choice(event_types)
        venue = random.choice(venues)
        event_name = f"{event_type} featuring {dj}"
        attendance = random.randint(1000, 70000)
        ticket_price = random.randint(50, 400)
        events.append({
            'date': date.strftime('%Y-%m-%d'),
            'dj_name': dj,
            'event_type': event_type,
            'event_name': event_name,
            'venue': venue[0],
            'city': venue[1],
            'country': venue[2],
            'latitude': venue[3],
            'longitude': venue[4],
            'genre': genre,
            'attendance': attendance,
            'ticket_price': ticket_price
        })

# Convert to DataFrame
df = pd.DataFrame(events)

# If the number of events is less than 200, add more events
while len(df) < 200:
    dj, genre = random.choice(djs)
    date = random.choice(date_range)
    event_type = random.choice(event_types)
    venue = random.choice(venues)
    event_name = f"{event_type} featuring {dj}"
    attendance = random.randint(1000, 70000)
    ticket_price = random.randint(50, 400)
    df = df.append({
        'date': date.strftime('%Y-%m-%d'),
        'dj_name': dj,
        'event_type': event_type,
        'event_name': event_name,
        'venue': venue[0],
        'city': venue[1],
        'country': venue[2],
        'latitude': venue[3],
        'longitude': venue[4],
        'genre': genre,
        'attendance': attendance,
        'ticket_price': ticket_price
    }, ignore_index=True)

# Remove duplicates and limit to 200 rows
df.drop_duplicates(subset=['date', 'dj_name', 'venue'], inplace=True)
df = df.head(200)

# Save to CSV
df.to_csv('dj_events_200.csv', index=False)

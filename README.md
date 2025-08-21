 **StayBangla DRF Hotel Management System** 

````markdown
# StayBangla – Hotel Management System (DRF)

**StayBangla** is a Django REST Framework (DRF) based Hotel Management System that allows users to browse hotels, check room availability, make bookings, cancel bookings, and submit reviews. Admins can manage hotels, rooms, bookings, and reviews.  

---

## Features

### User Features
- User registration and login (JWT Authentication)  
- Browse hotels and room types  
- Check room availability by date  
- Make a booking for available rooms  
- Cancel booking (with automatic room availability update)  
- Submit reviews and ratings for hotels  
- Profile management  

### Admin Features
- Add, edit, delete hotels  
- Add, edit, delete rooms (room type, capacity, price)  
- View, update, cancel bookings  
- View hotel reviews and manage approval  

---

## Tech Stack

- **Backend:** Python, Django, Django REST Framework (DRF)  
- **Database:** PostgreSQL / SQLite  
- **Authentication:** JWT (Djoser + Simple JWT)  
- **File Storage:** Cloudinary for images  
- **Hosting:** Vercel  

---

## Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/Atiar-Rahman/stay_bangla
cd StayBangla
````

### 2. Create Virtual Environment

```bash
python3 -m venv .st_env
source .st_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=<your-django-secret-key>
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/staybangla
CLOUDINARY_CLOUD_NAME=<your_cloud_name>
CLOUDINARY_API_KEY=<your_api_key>
CLOUDINARY_API_SECRET=<your_api_secret>
```

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Server

```bash
python manage.py runserver
```

---

## API Endpoints

### Authentication

* `POST /auth/users/` → Register user
* `POST /auth/jwt/create/` → Obtain JWT token
* `POST /auth/jwt/refresh/` → Refresh JWT token

### Hotels

* `GET /api/v1/hotels/` → List hotels
* `POST /api/v1/hotels/` → Add hotel (admin only)
* `GET /api/v1/hotels/{id}/` → Hotel details

### Rooms

* `GET /api/v1/hotels/{hotel_id}/rooms/` → List rooms
* `POST /api/v1/hotels/{hotel_id}/rooms/` → Add room (admin only)
* `GET /api/v1/hotels/{hotel_id}/rooms/{room_id}/` → Room details

### Bookings

* `POST /api/v1/hotels/{hotel_id}/rooms/{room_id}/bookings/` → Create booking
* `GET /api/v1/hotels/{hotel_id}/rooms/{room_id}/bookings/` → List bookings
* `POST /api/v1/hotels/{hotel_id}/rooms/{room_id}/bookings/{booking_id}/cancel/` → Cancel booking

### Reviews

* `POST /api/v1/hotels/{hotel_id}/reviews/` → Add review
* `GET /api/v1/hotels/{hotel_id}/reviews/` → List reviews

---

## Models Overview

### User

* Email, first\_name, last\_name, phone\_number, address, profile\_picture

### Hotel

* Name, address, description, images

### Room

* Hotel (FK), room\_type, price\_per\_night, capacity, total\_rooms, available\_rooms, is\_available

### Booking

* User (FK), Hotel (FK), Room (FK), check\_in/out, num\_guests, num\_rooms, amount, status, booking\_reference, cancellation\_allowed

### Review

* User (FK), Hotel (FK), rating, title, comment, image, is\_approved

---

## Booking Logic

1. **Room Auto-Selection:** User provides room\_type → system selects first available room with sufficient availability.
2. **Amount Calculation:** `amount = price_per_night * nights * num_rooms`
3. **Cancel Booking:** Updates booking status to `cancelled` and restores room availability.
4. **Booking Reference:** Auto-generated unique reference `REF-XXXXXXXXXX`.

---

## Admin Panel

* `/admin/` → Django admin for managing hotels, rooms, bookings, and reviews.

---

## File Uploads

* All hotel images, room images, and review images are stored on **Cloudinary**.

---

## Testing

```bash
python manage.py test
```

---

## Contributing

1. Fork the repo
2. Create a feature branch
3. Make changes
4. Submit a pull request

---

## License

MIT License © 2025 StayBangla



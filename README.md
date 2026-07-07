# Portal Content Visibility API

This project is a small backend exercise for a shareholders portal.

The API allows shareholders to view content based on visibility rules.

## Main Visibility Rule

A content item is visible to a shareholder if:

1. The content is shared with all shareholders, or
2. The content is restricted and the shareholder belongs to at least one allowed group assigned to that content.

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite

## Setup Instructions

Clone the repository:

```bash
git clone <repository-url>
cd Portal_visibility
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

## API Endpoints

### List visible content for a user

```http
GET /api/contents/?user_id=1
```

With pagination:

```http
GET /api/contents/?user_id=1&limit=10&offset=0
```

### Get content details

```http
GET /api/contents/{id}/?user_id=1
```

If the content is visible to the user, the API returns `200 OK`.

If the content is not visible to the user, the API returns `403 Forbidden`.

## Fake Authentication

For simplicity, real authentication was not implemented.

The current authenticated user is faked using the `user_id` query parameter.

Example:

```http
GET /api/contents/?user_id=1
```

## Data Models

The project includes models for:

- Users/shareholders using Django's built-in `User` model
- Investor groups
- User memberships
- Content items
- Content audience groups

## Pagination

Pagination was implemented using `limit` and `offset`.

Example:

```http
GET /api/contents/?user_id=1&limit=10&offset=0
```

This avoids returning too many content records at once.

## Running Tests

```bash
python manage.py test
```

The tests cover:

- Allowed access to content shared with all shareholders
- Allowed access to restricted content when the user belongs to the allowed group
- Denied access to restricted content when the user does not belong to the allowed group

## Assumptions

- A shareholder is represented by Django's built-in `User` model.
- Authentication is mocked using a `user_id` query parameter.
- Content can be either an announcement or a document metadata record.
- File uploads are not required.
- Restricted content should have at least one allowed group.
- Pagination was chosen instead of search.

## Time Spent

Approximately 2 hours.
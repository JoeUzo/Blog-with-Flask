# Blog with Flask

A simple blog application built using Python and Flask. This project demonstrates a variety of functionalities, including user authentication, blog post creation, commenting, and more.

## Table of Contents

- [Project Overview](#project-overview)
- [Installation Instructions](#installation-instructions)
  - [Using Docker](#using-docker)
  - [Manual Installation](#manual-installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [Docker Image](#docker-image)
- [License](#license)
  

## Project Overview

The "Blog with Flask" project is a web application that allows users to create, read, update, and delete blog posts. Users can register and log in to the site, create new blog posts, and leave comments on posts. The application uses Flask for the backend, SQLAlchemy for database interactions, and various Flask extensions for additional functionalities.

## Installation Instructions

### Using Docker

1. **Pull the Docker Image:**
   ```bash
   docker pull joeuzo/flask-blog:latest
   ```

2. **Prepare the `.env` File:**
   Create a `.env` file in your working directory with the following content:
   ```makefile
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///path/to/database.db  # Or your preferred database URL
   EMAIL_KEY=your_email_app_key
   EMAIL_ADDRESS=your_email@example.com
   ```

3. **Run the Docker Container:**
   ```bash
   docker run --env-file .env -p 5000:5000 joeuzo/flask-blog:latest
   ```

### Manual Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/JoeUzo/Blog-with-Flask.git
   cd Blog-with-Flask
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables:**
   Create a .env file in the root directory and add the following variables:
   ```makefile
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///blog.db  # Or your preferred database URL
   ```

5. **Initialize the Database:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

6. **Run the Application:**
   ```bash
   flask run
   ```

## Usage

Once the application is running, you can access it in your web browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/). You can register a new account, log in, and start creating blog posts. As an admin user (with user ID 1), you have additional privileges such as editing and deleting any posts and comments.

## Features

- User Authentication (Registration, Login, Logout)
- Create, Read, Update, and Delete (CRUD) operations for blog posts
- Commenting system
- Admin privileges for managing posts and comments
- Basic contact form functionality

## Contributing

Contributions are welcome! If you would like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes and commit them (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## Docker Image

You can find the Docker image for this project on Docker Hub:

[![Docker Image](https://img.shields.io/badge/Docker%20Hub-flask--blog-blue)](https://hub.docker.com/r/joeuzo/flask-blog)

To run the Docker image:

```sh
docker pull joeuzo/flask-blog:latest
docker run --env-file .env -p 5000:5000 joeuzo/flask-blog:latest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

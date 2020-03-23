# Description of the solution

First I have made a simple design of how the components should interact between them and how to "split" the code. I decided to use a separate data layer, so I could decouple the
caching solution from the business logic.
Instead of creating everything from "scratch" I decided to use established libraries that I have used before (like Flask and Flask-RESTful) or that had a good feedback from the community ( case of Flash-Caching).
I opted for using already existing libraries to avoid "reinventing the wheel" and focusing on the design of the solution.
To start the coding, I used a TDD approach so I could refine the code as I went.

The biggest time investment was Docker. The last time I used it was more the three years ago and I needed to "refresh" my knowledge about it. 
The requirements were clear and did not let to ambiguity.

## Usage

curl http://localhost:5000/website_info/google.com.br

result:
```
{
    "url": "http://google.com.br",
    "title": "Google",
    "headers": {},
    "links": {
        "internal": [
            "http://google.com.br/preferences",
            "http://google.com.br/advanced_search",
            "http://www.google.com.br/setprefs",
            "http://www.google.com.br/setprefs",
            "http://google.com.br/intl/en/ads/",
            "http://google.com.br/intl/en/about.html",
            "http://www.google.com.br/setprefdomain",
            "http://google.com.br/intl/en/policies/privacy/",
            "http://google.com.br/intl/en/policies/terms/"
        ],
        "external": [
            "http://www.google.ie/imghp",
            "http://maps.google.ie/maps",
            "https://play.google.com/",
            "http://www.youtube.com/",
            "http://news.google.ie/nwshp",
            "https://mail.google.com/mail/",
            "https://drive.google.com/",
            "https://www.google.ie/intl/en/about/products",
            "http://www.google.ie/history/optout",
            "https://accounts.google.com/ServiceLogin",
            "http://www.google.ie/intl/en/services/"
        ],
        "unreachable": []
    },
    "has_login": true
}
```

----

## Analyzing websites

### The task

The objective is to build an API service that does some analysis of a web-page/URL.

## Functional Requirements

- The application should accept the URL of the webpage being analyzed.

- After submitting the URL to the server, trigger the server-side analysis process.

- After processing the results should be shown returned to the user. The response comprises the following information:

  - What HTML version has the document?

  - What is the page title?

  - How many headings of what level are in the document?

  - How many internal and external links are in the document? Are there any inaccessible links and how many?

  - Did the page contain a login-form?

In case the requested URL is not reachable, an error message should be returned. The message should contain the HTTP status-code and some useful error description.

## Non-Functional Requirements:

The backend should cache the scraping results for each URL for 24 hours such that your backend does not have to redo the scraping for any given URL within the next 24 hours.
Your application server as well as your data store should be run in separate Docker containers such that they can later on be scaled independently.

## Your Solution

Please write an application handling all the wanted features. HINT: for document analysis consider using a library.
Feel free to use a technology stack of your preference.

## Submission of Results

Please provide the result as a Git repository with this content:

1. The project with all source files.

2. A docker-compose setup to run the backend.

3. A short text document that lists the main steps of building your solution as well as all assumptions/decisions you made in case of unclear requirements or missing information

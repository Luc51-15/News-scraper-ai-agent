# BBC News Scraper & AI Summariser
**Scrapes the latest articles from BBC News by topic, summarises them using a local AI model via Ollama, and lets you ask questions about the news.**

This is my CS50 project. To learn ai agent creation i followed a guide on ai agents with python, here i learned to run ollama locally, prompt, and call.
To scrape the articles i followed a quick 10 min video and dived into documentation of beautifulsoup. It was interesting to learn this and very useful for the future.
I used almost all my knowledge from the course like: creating function's, lists, dicts, loops, error handling, printing, and much more.
I present with honor my final project. 

url = https://youtu.be/CIBVtEm7UjY

## What it does
    1. Asks to enter a subject. 
    2. Scrapes the 10 most recent articles under that subject from bbc news.
    3. Saves them to a csv file.
    4. Returns a summary using a local ollama model.
    5. Lets you asks follow-up questions.

## Requirements
    - python 3.10+
    - ollama installed and running locally with llama3.2 model or other modern model.

## Installation
    1. Download the project files into a folder.
    2. install dependencies with: (pip/pip3 install -r requirmements.txt).
    3. Ollama with: ollama pull llama3.2

## How to run
    First open terminal and run: project.py

    then you will be prompted a subject, make sure you choose a subject from the list or the program will prompt you again.
    The program will scrape articles, summarise, answer questions. 
    To see the articles with url and body open the created csv file.

## How to run tests
    pytest test_project.py

## Structure 
    project.py          — main application
    test_project.py     — pytest tests
    requirements.txt    — Python dependencies
    articles.csv        — saved articles (generated when you run the program)

## Functions

    **get_headlines(query) = Scrapes headline and URL pairs from a BBC topic page**
        this function first requests to get information on the url. After successfully doing so it uses beautiful soup to find all 
        with under the html class. Then a for loop is used to find the text and url. After the loop 
        is successfull the text is appended to a list.

    **get_articles(url) = Fetches the body text from a single article URL**
        After the url is passed down this function searches for the article body that goes with it and only returns the first 3 rows of the 
        article. 

    **get_all_articles(query) = Combines both — returns a list of dicts with title, url, and body** 
        Uses a time.sleep to safely scrape from bbc

    **create_csv_file(articles) = saves the articles list to articles.csv**
        Writes the list in format using fieldnames

    **get_template() = Returns the summary prompt template for the AI**
        To let the llm (ollama) do his job correctly it needs to have instructions. The instructions are written very clear, so the ai is 
        not confused.

    **get_question_template() = Returns the question answering prompt template for the AI**
        Same goes for this function, i seperated the two prompts to not cause confusion.

    **main() = runs full pipeline**
        This makes sure the list of subjects is printed, the user can than input a subject(query) which is passed to other functions. 
        After that it calls the prompts of the ai agent and runs it with chain.invoke. 

    

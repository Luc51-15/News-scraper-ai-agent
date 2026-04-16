from bs4 import BeautifulSoup 
import requests
import time
import csv 
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.2")

def get_headlines(query):
    Bbc_news_scrape = requests.get(f"https://www.bbc.com/{query}")
    soup = BeautifulSoup(Bbc_news_scrape.text, "html.parser")
    titles = soup.find_all("h2")
    url = soup.find_all("a")
    title_list = []
    for i,title in enumerate(titles,1):
        text = title.get_text(strip=True)
        parent_link = title.find_parent("a")
        if parent_link:
            url = parent_link.get("href")
        if text and url:
            title_list.append({
                "title": text,
                "url": f"https://www.bbc.com{url}"
            })

    return title_list

def get_articles(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        article = soup.find("article")
        if article is None:
            return None
        body = article.find_all("p")[:3]
        return " ".join(p.get_text(strip=True)for p in body)
    except Exception as e:
        return None
    
def get_all_articles(query):
    headlines = get_headlines(query)[:10]
    for item in headlines:
        item["body"] = get_articles(item["url"])
        time.sleep(1.5)
    return headlines
    
def create_csv_file(articles):

    with open('articles.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'url', 'body']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(articles)

def get_template():
    template = """
    You are a professional news journalist. Below are 10 news articles on diffrent topics. write a single
    well structured news summary that weaves these articles into one coherent story.
    Cover the most important points, connect related themes, and write in a clear journalistic style.
    Do not list articles separately. Write flowing paragraphs.

    here are the articles: {articles}
    """
    return template

def get_question_template():
    question_template = """
    You are a helpful news assistant. You have been given a set of news articles.
    A user will ask you a question. The answer will always be found somewhere in the articles below.
    Search carefully through all articles before responding.
    If the answer is there, state it clearly and mention which article it came from.
    Only say you cannot find something if it is genuinely not mentioned anywhere.

    questions: {questions}
    
    articles: {articles}
    """
    return question_template
def main():
    subjects = ["news", "business", "technology", "health", "culture", "arts", "travel", "earth"]
    
    while True:
        print("-----------------")
        print(subjects)
        print("-----------------")
        query = input("\nEnter a subject: ").strip().lower()
        
        if query in subjects:
            selected = query
            break
        
        print("Invalid input. Please try again.")
    
    print(f"\nScraping articles from: {selected}")
    articles = get_all_articles(selected)
    create_csv_file(articles)
    print(f"Successfully saved {len(articles)} articles to articles.csv")


    formatted = "\n\n".join(
        f"Title: {a['title']}\nBody: {a['body']}"
        for a in articles if a['body']
    )


    template = get_template()
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    summary = chain.invoke({"articles": formatted})
    print("----------------")
    print(summary)
    print("-----------------")

    Question_template = get_question_template()
    Question_prompt = ChatPromptTemplate.from_template(Question_template)
    Question_chain = Question_prompt | model
    while True:
        questions = input("ask youre question (q to quit)")
        if questions == "q":
            break
        result = Question_chain.invoke({"articles": formatted, "questions": questions})
        print("-----ANSWER-----")
        print(result)
        print("----------------")

if __name__ == "__main__":
    main()
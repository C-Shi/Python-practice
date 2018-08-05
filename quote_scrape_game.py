# This is a small gaming guessing the author of a quote
# Reminder: Be EXTRA careful when you scrape. Please consult robots.txt if you are allowed to scrape


from csv import writer, reader
from bs4 import BeautifulSoup
from random import choice
import requests

# ************************ scraping session ***************************
# Open an csv file to write the file on
with open("quote.csv", "w") as file:
  csv_writer = writer(file)
  # set the start page at 1, and check if there is next page, if there is an next page button then loop back to scrape the next page
  page = 1
  next_page = True
  while next_page:

    # ************scrape the current page that we are on ***************
    response = requests.get(f"http://quotes.toscrape.com/page/{page}/")
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all(class_="quote")

    for article in articles:
      quote = article.find(class_="text")
      author = article.find(class_="author")

      # ******* scrape the author page to get the info for author ************
      this_author = author.get_text().replace(" ", "-").replace(".", "-").replace("--", "-").replace("é","e").replace("'","")
      if this_author[-1] == "-":
        this_author = this_author[:-1]

      print(this_author)
      author_res = requests.get(f"http://quotes.toscrape.com/author/{this_author}/")
      author_soup = BeautifulSoup(author_res.text, "html.parser")
      born = author_soup.find(class_="author-born-date") #scrape the author's birthday
      location = author_soup.find(class_="author-born-location") # scrape author's birth place
      # **********************************************************************

      csv_writer.writerow([quote.get_text(), author.get_text(), born.get_text(), location.get_text()])

    # ************** check if there is a next page, if yes and loop back to scrape the next page ******************
    next_page = soup.find(text="Next ")
    # print(next_page)
    page+=1
# *********************** scraping session finishe ********************


# ********** gaming session **********
with open("quote.csv") as file:
  csv_reader = list(reader(file))
  play_again = True
  while play_again:
    clear()
    question = choice(csv_reader)
    # question[0] is quote, question[1] is author, question[2] is birthday, quesiton[3] is location
    correct = False
    count = 4
    print(f'Who say this? {count}')
    print(question[0])
    answer = input("This quote is delievered by:  ")
    while not correct:
      if answer == question[1]:
        print("Congratulation! You get it correct! ")
        correct = True
      else:
        count -= 1
        print("Sorry. He/She is not the correct author, please try again")
        if count == 3:
          print(f"Hint, this author is born in {question[3]}")
        elif count == 2:
          print(f"Hint, this author is born on {question[2]}")
        elif count == 1:
          print(f"Hint, this author first name start with {question[1][0]}")
        else:
          print("You have run out of chance. You LOST. Haha")
          break
        answer = input(f"Who say this? {count} ")
    repeat = input("Do you want to play again? Y/N")
    if repeat[0].upper() == "N":
      play_again = False



















import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import codecs
import csv

def main():
    get_link_to_file('https://sandbox.acrl.org/contributors')
    #get_link_by_file()
    #get_link('https://sandbox.acrl.org/contributors?page=12')
    #scrap('csabbar','https://sandbox.acrl.org/users/csabbar')
    # for i in range(2, 21):
    #     get_link('https://mingyanjiaju.org/lizhimingyan/list_1_' + str(i) + '/')

def get_link_to_file(page):
    r = requests.get(page)
    html = r.text.encode('utf8')
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(html, 'lxml')
        '''
        news_list = soup.find_all(class_ = "views-field views-field-field-first-name")
        for a in news_list:
            id_list = a.find_all('a')
            for id in id_list:
                id = id.get('href')
                #print(id)
            fn = open("C:/Users/user/Desktop/scraping/id_list.txt", "a", encoding="utf8")
            fn.write(id + '\n')
        
        job_list = soup.find_all(class_ = "views-field views-field-field-job-title")
        for job in job_list:
            job = job.text
            fn = open("C:/Users/user/Desktop/scraping/job_list.txt", "a", encoding="utf8")
            fn.write(job + '\n')
        '''
        name_list = soup.find_all(class_ = "views-field views-field-field-first-name")
        for name in name_list:
            name = name.text
            fn = open("C:/Users/user/Desktop/scraping/name_list.txt", "a", encoding="utf8")
            fn.write(name + '\n')

        next_link = soup.find('a', {'title' :'Go to next page'})
        print(next_link)
        if next_link != None:
            full_next_link = 'https://sandbox.acrl.org' + next_link.get('href')
            print('NEXT:' + full_next_link)
            get_link_to_file(full_next_link)

def get_link_by_file():
    for id in open('C:/Users/user/Desktop/scraping/id_list.txt', encoding="utf8"):
        id = id.replace('\n','')
        fullpath = 'https://sandbox.acrl.org/' + id
        print(fullpath)
        try:
            scrap(id, fullpath)
            fn = open("C:/Users/user/Desktop/scraping/success.txt", "a", encoding="utf8")
            fn.write(id + '\n')
        except:
            fn = open("C:/Users/user/Desktop/scraping/error.txt", "a", encoding="utf8")
            fn.write(id + '\n')


def get_link(page):
    r = requests.get(page)
    html = r.text.encode('utf8')
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(html, 'lxml')
        news_list = soup.find_all(class_ = "views-field views-field-field-first-name")
        for a in news_list:
            id_list = a.find_all('a')
            for id in id_list:
                id = id.get('href')
            #name = a.get_text()
            fullpath = id
            print(fullpath)
            try:
                scrap(id, fullpath)
                fn = open("C:/Users/user/Desktop/scraping/success.txt", "a", encoding="utf8")
                fn.write(id + '\n')
            except:
                fn = open("C:/Users/user/Desktop/scraping/error.txt", "a", encoding="utf8")
                fn.write(id + '\n')

        next_link = soup.find('a', {'title' :'Go to next page'})
        if next_link != None:
            full_next_link = 'https://sandbox.acrl.org' + next_link.get('href')
            print('NEXT:' + full_next_link)
            get_link(full_next_link)

def scrap(id, url):
    arg = ''
    res = ''
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome('C:/Users/user/Desktop/scraping/chromedriver.exe') #, chrome_options=chrome_options
    driver.get(url)
    #buttons = driver.find_element_by_class_name('views-field views-field-view-node readmore')
    #for btn in buttons:
        #btn.click()
        #driver.find_element_by_link_text('readmore').click()
    r = requests.get(url)
    html = r.text.encode('utf8')
    soup = BeautifulSoup(html, 'lxml')

    names = soup.find_all("h1", {"class": "title"})
    for name in names:
        name = name.string
    
    institutions = soup.find_all(class_ = "field field-name-field-institution field-type-entityreference field-label-hidden field-wrapper")
    for institution in institutions:
        institution = institution.string
    
    states = soup.find_all(class_ = "field field-name-field-us-state field-type-list-text field-label-hidden field-wrapper")
    for state in states:
        state = state.string
    
    try:
        bios = soup.find_all(class_ = "field field-name-field-bio field-type-text-long field-label-above field-wrapper")
        if len(bios) == 0:
            bio = "None"
        else:
            for bio in bios:
                inner_text = bio.text
                strings = inner_text.split("\xa0")
                bio= strings[1]
    except: 
        bio = "None"

    try:
        blogs = soup.find(class_ = "field field-name-field-personal-blog field-type-link-field field-label-above field-wrapper").find_all('a')
        for blog in blogs:
            blog = blog.get('href')
    except:
        blog = "None"
    
    try:
        resources = soup.find_all(class_ = "views-field views-field-title")
        all_resources = []
        for resource in resources:
            inner_text = resource.text
            strings = inner_text.split("\n")
            for i in range(len(strings)):
                resource = strings[i]
                all_resources.append(resource)
        s = ","
        resource = s.join(all_resources)
    except:
        resource = "None"

    with open('test.csv', 'a', newline='',encoding = 'utf8') as csvfile:  
        writer = csv.writer(csvfile, delimiter='"')
        writer.writerow([name+'\t'+institution+'\t'+state +'\t'+str(bio)+'\t'+str(blog)+'\t'+resource])
        

if __name__ == '__main__':
    main()



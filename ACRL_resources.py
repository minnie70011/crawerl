import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import codecs
import csv

def main():
    #get_link_to_file('https://sandbox.acrl.org/resources')
    #get_link_by_file()
    get_link('https://sandbox.acrl.org/resources')
    #scrap('digital-shred-workshop','https://sandbox.acrl.org/library-collection/digital-shred-workshop')
    # for i in range(2, 21):
    #     get_link('https://mingyanjiaju.org/lizhimingyan/list_1_' + str(i) + '/')

def get_link_to_file(page):
    r = requests.get(page)
    html = r.text.encode('utf8')
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(html, 'lxml')
        news_list = soup.find_all(class_ = "views-field views-field-title")
        for a in news_list:
            id_list = a.find_all('a')
            for id in id_list:
                id = id.get('href')
                #print(id)
            fn = open("C:/Users/user/Desktop/scraping/id_list.txt", "a", encoding="utf8")
            fn.write(id + '\n')
        
        date_list = soup.find_all(class_ = "views-field views-field-created postdate")
        for date in date_list:
            date = date.string
            #print(date)
            fn = open("C:/Users/user/Desktop/scraping/date_list.txt", "a", encoding="utf8")
            fn.write(date + '\n')

        next_link = soup.find('a', {'title' :'Go to next page'})
        #print(next_link)
        if next_link != None:
            full_next_link = 'https://sandbox.acrl.org' + next_link.get('href')
            #print('NEXT:' + full_next_link)
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
        news_list = soup.find_all(class_ = "views-field views-field-title")
        for a in news_list:
            id_list = a.find_all('a')
            for id in id_list:
                id = id.get('href')
            #name = a.get_text()
            fullpath = 'https://sandbox.acrl.org/' + id
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
            #print('NEXT:' + full_next_link)
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
    titles = soup.find_all("h1", {"class": "title"})
    for title in titles:
        title = title.string
    """ 
    try:
        summaries = soup.find_all(class_ = "field field-name-field-description field-type-text-with-summary field-label-hidden field-wrapper")
        for summary in summaries:
            summary = summary.string
    except:
        summary = "None"
    """
    try:
        attachments = soup.find(class_ = "field field-name-field-resource-attachments field-type-file field-label-above field-wrapper").find_all('a')
        
        for attachment in attachments:
            attachment = attachment.text
            
            all_attachments = []
            step1_attachments = soup.find_all(class_ = "file")

            for a in step1_attachments:
                step2_attachments = a.find_all('a')
                for attachments in step2_attachments:
                    inner_text = attachments.string
                    strings = inner_text.split("\n")
                    for i in range(len(strings)):
                        attachment = strings[i]
                        all_attachments.append(attachment)
            s = ","
            attachment = s.join(all_attachments)
    except:
        attachment = "None"

    """
    try:
        links = soup.find(class_ =  "field field-name-field-resource-link field-type-link-field field-label-above field-wrapper").findAll('a')
        all_link = []
        for link in links:
            inner_text = link.text
            strings = inner_text.split("\n")
            for i in range(len(strings)):
                link = strings[i]
                all_link.append(link)
        s = ","
        final_link = s.join(all_link)
    except:
        final_link = "None"
    """
            
    try:
        resource_types = soup.find(class_ = "field field-name-field-resource-type-term field-type-taxonomy-term-reference field-label-above field-wrapper clearfix").findAll('a')
        all_resouce = []
        for resource_type in resource_types:
            inner_text = resource_type.text
            strings = inner_text.split("\n")
            for i in range(len(strings)):
                resource = strings[i]
                all_resouce.append(resource)
        s = ","
        resource_type = s.join(all_resouce)
    except:
        resource_type = "None"
    """
    try:
        informations = soup.find(class_ = "field field-name-field-literacy field-type-taxonomy-term-reference field-label-above field-wrapper clearfix").findAll('a')
        for information in informations:
            information = information.string
    except:
        information = "None"
    
    try:
        disciplines = soup.find(class_ = "field field-name-field-discipline-term field-type-entityreference field-label-above field-wrapper").findAll('a')
        all_discipline = []
        for discipline in disciplines:
            inner_text = discipline.text
            strings = inner_text.split("\n")
            for i in range(len(strings)):
                discipline = strings[i]
                all_discipline.append(discipline)
        s = ","
        final_discipline = s.join(all_discipline)
    except:
        final_discipline = "None"
    
    try:
        institutions = soup.find(class_ = "field field-name-field-institution-type field-type-taxonomy-term-reference field-label-above field-wrapper clearfix").findAll('a')
        all_institution = []
        for institution in institutions:
            inner_text = institution.text
            strings = inner_text.split("\n")
            for i in range(len(strings)):
                institution = strings[i]
                all_institution.append(institution)
        s = ","
        final_institution = s.join(all_institution)
    except:
        final_institution = "None"
    """
    try:
        scopes = soup.find(class_ = "field field-name-field-scope field-type-taxonomy-term-reference field-label-above field-wrapper clearfix").find_all('a')
        all_scope = []
        for scope in scopes:
            inner_text = scope.text
            strings = inner_text.split("\n")
            for i in range(len(strings)):
                scopes = strings[i]
                all_scope.append(scopes)
        s = ","
        scope = s.join(all_scope)
    except:
        scope = "None"
    """
    try:
        licenses = soup.find_all(class_ = "field field-name-field-license field-type-list-text field-label-above field-wrapper")
        for license_ in licenses:
            inner_text = license_.text
            strings = inner_text.split("\xa0")
            license_ = strings[1]
    except:
        license_ = "None"

    try:
        add_cons = soup.find(class_ = "field field-name-field-collaborators field-type-entityreference field-label-above field-wrapper").find_all('a')
        all_add = []
        for add_con in add_cons:
            add_con = add_con.get('href')
            
            strings = add_con.split("/users/")
            for i in range(len(strings)):
                add_con = strings[i]
                all_add.append(add_con)
            s = ","
            add_con = s.join(all_add)
    except:
        add_con = "None"

    try:
        other_attrs = soup.find_all(class_ = "field field-name-field-other-attribution-informat field-type-text-long field-label-above field-wrapper")
        for other_attr in other_attrs:
            inner_text = other_attr.text
            strings = inner_text.split("\xa0")
            other_attrs = strings[1]
    except:
        other_attrs = "None"


    try:
        tags = soup.find(class_ = "field field-name-field-tags field-type-taxonomy-term-reference field-label-above field-wrapper clearfix").findAll('li')
        all_tag = []
        for tag in tags:
            inner_text = tag.text
            strings = inner_text.split("\n")
            for i in range(len(strings)):
                tag = strings[i]
                all_tag.append(tag)
        s = ","
        final_tag = s.join(all_tag)
    except:
        final_tag = "None"
    """

    with open('test.csv', 'a', newline='',encoding = 'utf8') as csvfile:  
        writer = csv.writer(csvfile, delimiter='"')
        writer.writerow([title +'\t'+str(attachment) +'\t'+str(resource_type)  +'\t'+str(scope)])
        #writer.writerow([title +'\t' +str(summary) +'\t'+str(attachment)+'\t'+str(final_link) +'\t'+str(resource_type) +'\t'+str(information) +'\t'+str(final_discipline) +'\t'+str(final_institution) +'\t'+str(scope) +'\t'+str(license_)+'\t' +str(add_con)+'\t'+str(other_attrs)+'\t'+str(final_tag)])

if __name__ == '__main__':
    main()



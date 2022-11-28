from flask import Flask,render_template, request
#from flask_ngrok import run_with_ngrok
import webbrowser
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from json import dumps
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service



#browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

app = Flask(__name__)

@app.route('/',methods = ["POST","GET"])

def index():
    if request.method =="POST":
        global username
        username = request.form.get("Username")
        global password
        password = request.form.get("Password")
        title()
        #dummy=Extract_info(P_link)
        dummy = Extract_info('https://www.linkedin.com/in/saisravyabhupathiraju/')
        connections1=get_connections('https://www.linkedin.com/in/saisravyabhupathiraju/')
        connections2=get_connections('https://www.linkedin.com/in/pavan-mallina/')
        with open(r'C:\Users\admin\Downloads/100links.txt', 'w') as fp:
            count=0
            for dic in (connections1,connections2):
                for person in dic:
                    fp.write(f"{person['Profile_link']}\n")
                    count+=1
            print(count)    
        # Opening file
        file1 = open('100links.txt', 'r')
        count = 0
        List_info=[]
        
        # Using for loop
        for line in file1:
            count += 1
            List_info.append(Extract_info(line))
            print(count)
        
        # Closing files
        file1.close()
        print(len(List_info))
        print(List_info)
        #create json
        js = List_info
        data = dumps(js, sort_keys=False, indent = 4)
        with open('100Pinfo.json', 'w') as f:
            f.write(data)

    return render_template("index.html")

def title():
    global browser

    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    browser.get('https://www.linkedin.com/uas/login')

    elementID= browser.find_element(By.ID,'username')
    elementID.send_keys(username)

    elementID= browser.find_element(By.ID,'password')
    elementID.send_keys(password)
    elementID.submit()

    global P_link

    P_link = 'https://www.linkedin.com/in/saisravyabhupathiraju/'

    return None


def Extract_info(profile_link):
    
    browser.get(profile_link)
    # scroll to the bottom to completely load the page
    start = time.time()

    initial_scroll = 0
    final_scroll = 1000

    while True:
        browser.execute_script(f"window.scrollTo({initial_scroll},{final_scroll})")
        initial_scroll = final_scroll
        final_scroll += 1000
        time.sleep(1)
        end = time.time()

        if round(end - start) > 20:
            break
    
    src = browser.page_source
    soup = BeautifulSoup(src, features="html.parser")
    
    
    
    name = soup.find(class_="text-heading-xlarge inline t-24 v-align-middle break-words").get_text()
    position = soup.find(class_="text-body-medium break-words").get_text().strip()
    current_org =  soup.find_all(class_="inline-show-more-text")[0].get_text().strip()
    previous_org=  soup.find_all(class_="inline-show-more-text")[1].get_text().strip()
    location = soup.find(class_="text-body-small inline t-black--light break-words").get_text().strip().split(',')
    #check
    #connections = soup.find_all(class_="link-without-visited-state")[1].get_text().strip() 
    
    
    Profile_Info={}
    Profile_Info['Name'] = name
    Profile_Info['Tagline'] = position
    Profile_Info['Current_org'] = current_org
    Profile_Info['Previous_org'] = previous_org 
    #Profile_Info['Number_of_Connections'] = connections
    Profile_Info['Location'] = location
    
    
    
    h=soup.find_all(class_="artdeco-card ember-view relative break-words pb3 mt2")
    # h is a list containing of all sections
    headings=h
    Profile_Info['Highlights']= []
    Profile_Info['Activity'] = []
    Profile_Info['Education'] = []
    Profile_Info['Interests']= []
    Profile_Info['Skills']= []
    Profile_Info['Licenses & certifications']=[]
    Profile_Info['Experience']=[]
    #count=1
    for x in headings:
        section_name=x.find("span", class_="visually-hidden").get_text().strip()
        #print(section_name)   

        #Section name is printed 

        #Sometimes the class of the headings section is changing depending upon if there are multiple highlights or a single highlight

        # h2 contians info of each section 
        h2=x.find_all(class_="artdeco-list__item pvs-list__item--line-separated pvs-list__item--two-column")
        #print(len(h2))

        if len(h2)== 0: #if no such class 
            h2=x.find_all(class_="artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column")
            #print(len(h2))

        # First we are assigning it the class assuming it contains multiple parts in section..
        #Then we are assigning it the other class

        #For About section...only element p is enough
        #if x.find('p'):
            #print(x.find('p').find("span", class_="visually-hidden").get_text().strip())
            #\print('p_element')



        if len(h2)== 0:  # h2 is empty ...print('not both classes')
            if x.find(class_="inline-show-more-text inline-show-more-text--is-collapsed"):
                inline_about = x.find(class_="inline-show-more-text inline-show-more-text--is-collapsed").get_text().strip()
            #print(inline_about)
            #print(len(h2))
            #print('inline_about')
                Profile_Info['About'] = inline_about 



        else : # h2 is not empty
            #print('else loop')

            for list_item in h2:
                mr1=None
                mr1_hoverable=None            
                each_b = None
                link_A = None
                line= None
                de=None
                de2=None
                line=None
                activity_list = None
                desc= None
                item_incline1=None
                m_pos=None
                m_time=None
                link=None
                link_a=None
                
                t_black= []

                if list_item.find(class_="mr1 t-bold"):
                    item=list_item.find(class_="mr1 t-bold")
                    item=item.find("span", class_="visually-hidden").get_text().strip()
                    #print('mr1')
                    mr1=item
                    #print(mr1)


                if list_item.find(class_="mr1 hoverable-link-text t-bold") and section_name not in ('Education','Recommendations','Interests'):
                    item=list_item.find(class_="mr1 hoverable-link-text t-bold")
                    item=item.find("span", class_="visually-hidden").get_text().strip()
                    #print('mr1 hoverable')
                    mr1_hoverable = item
                    #print(mr1_hoverable)

                if list_item.find_all('a') and section_name in ('Experience') :
                    first_A = list_item.find('a')
                    link=list_item.find('a')['href']
                    #print(link)
                    #print('company link')
                    if first_A.find("span", class_="visually-hidden"): 
                        a_txt=first_A.find("span", class_="visually-hidden").get_text().strip()
                        #print(a_txt)
                        #print('text from a')

                link_a=None
                if list_item.find_all('a') and section_name not in ('Highlights','Experience') : 
                    all_A = list_item.find_all('a')
                    link_a=list_item.find('a')['href']
                    #print(link_a)
                    #print('Link A')
                    activity_list=[]
                    for each_A in all_A:  
                        if section_name =='Activity':
                            link_a=list_item.find('a')['href']
                            timeframe=each_A.get_text().strip().split(' • ')[0]
                            activity_list.append(timeframe)
                            #print(timeframe)
                            #print('act')
                            if each_A.find("span", class_="visually-hidden"): 
                                each_b=each_A.find("span", class_="visually-hidden").get_text().strip()
                            #print(each_b)
                            #print('a')
                                activity_list.append(each_b)

                if list_item.find(class_='display-flex flex-row justify-space-between') and section_name == 'Licenses & certifications':
                        list_item = list_item.find(class_='display-flex flex-row justify-space-between')
                        if list_item.find('a'):
                            link_A=list_item.find('a')['href']
                        else:
                            link_A=None
                        #print(link_A)
                        #print('Certification')                

                if list_item.find(class_="t-14 t-normal"):
                    description=list_item.find_all(class_="t-14 t-normal")
                    for each_line in description:
                        fgh=each_line.find("span", class_="visually-hidden")
                        if fgh:    
                            line=fgh.get_text().strip()
                        #print(line)
                        #print('line')
                        #print('t-normal')
                #flag=0
                if list_item.find('ul') and section_name == 'Experience' : 
                    #print('mr1 hoverable')
                    #print((type(mr1_hoverable)))
                    #print('mr1')
                    #print(type(mr1))
                    #flag=0
                    all_positions=  list_item.find('ul')
                    positions = all_positions.find_all('li')
                    m_pos =[]
                    m_time=[]
                    for each_pos in positions:
                        if each_pos.find(class_="mr1 hoverable-link-text t-bold"): #and section_name not in ('Education','Recommendations','Interests'):
                            item=each_pos.find(class_="mr1 hoverable-link-text t-bold")
                            item=item.find("span", class_="visually-hidden").get_text().strip()
                            #print(item)
                            #print('mr1 hoverable')
                            #flag=1
                        if each_pos.find_all(class_="t-14 t-normal t-black--light"):
                            description=each_pos.find_all(class_="t-14 t-normal t-black--light")
                            for each_line in description:
                                de=each_line.find("span", class_="visually-hidden").get_text().strip()
                                #print(de)
                                #print('t-black')
                                #flag=1

                        m_pos.append([item])
                        m_time.append([de])

                        #print(m_pos)
                        #print('multiple')
                    #print(m_pos)

                    #if flag==1:
                     #   print('-----------------------------------------------------------------------------')



                if list_item.find_all(class_="t-14 t-normal t-black--light") :#and flag!=1:
                    description=list_item.find_all(class_="t-14 t-normal t-black--light")
                    for each_line in description:
                        de2=each_line.find("span", class_="visually-hidden").get_text().strip()
                        #print(de2)   
                        t_black.append(de2)
                        #print(t_black)
                        #print('t-black')

                if  list_item.find(class_="display-flex align-items-center t-14 t-normal t-black"):# and flag!=1:
                    item=list_item.find(class_= "display-flex align-items-center t-14 t-normal t-black")
                    item=item.find("span", class_="visually-hidden").get_text().strip()
                    #print(item)
                    #print('display-flex align-items-center t-14 t-normal t-black')   
                if  list_item.find(class_="inline-show-more-text inline-show-more-text--is-collapsed") and section_name not in ('Skills','Education'):# and flag!=1:
                    item=list_item.find(class_="inline-show-more-text inline-show-more-text--is-collapsed")
                    item_incline1=item.find("span", class_="visually-hidden").get_text().strip()
                    #print(item_incline1)
                    #print('inline show more text 1')      

                if section_name ==  'Education':
                    if  list_item.find(class_='pvs-list'):
                        item=list_item.find(class_="pvs-list")
                        #print(item.prettify())
                        if item.find_all(class_="inline-show-more-text inline-show-more-text--is-collapsed"):
                            description=item.find_all(class_="inline-show-more-text inline-show-more-text--is-collapsed")
                            desc=[]
                            for each_ele in description:
                                strings=each_ele.find("span", class_="visually-hidden").get_text().strip()
                                #print(strings)
                                desc.append(strings)

                            #print('inline show more text 2')
                            #print(desc)
                    else : 
                        desc = []
                        #print(desc)


                #print('-----------------------------------------------------------------------------')
                # prints --- after every element in a section

                if section_name == 'Highlights':
                    Profile_Info['Highlights'].append(( mr1_hoverable,line ))
                if section_name == 'Education' :
                    Profile_Info['Education'].append((each_b,link_a,line,de2,desc))
                if section_name == 'Interests':
                    Profile_Info['Interests'].append((each_b,link_a,line,de2))
                if section_name == 'Activity':
                    Profile_Info['Activity'].append((link_a,activity_list))
                if section_name == 'Skills' :
                    Profile_Info['Skills'].append((mr1_hoverable,each_b))
                if section_name == 'Licenses & certifications' :
                    Profile_Info['Licenses & certifications'].append((mr1 if mr1 is not None else mr1_hoverable ,link_A,line,link_a,de2))           
                if section_name == 'Experience':
                    if type(mr1_hoverable) == str:

                        Profile_Info['Experience'].append((mr1_hoverable,link,line,m_pos,m_time))
                    else :
                        Profile_Info['Experience'].append((mr1,line,link,t_black,item_incline1))# if mr1 is not None else (mr1_hoverable,link_A,de,m_pos))





    ### Profile_Info['Connections_list'] = get_connections(P_link)    
    return(Profile_Info)
    

def get_connections(profilelink):
    #connection link
    driver=browser
    driver.back
    driver.get(profilelink)
    src = driver.page_source
    soup = BeautifulSoup(src, features="html.parser")


    z=soup.find(class_="pv-top-card--list pv-top-card--list-bullet display-flex mt2")  
    #should use class names without hard coding them
    url= z.find('a')['href']
    dv= z.find('a')['id']
    connections_link= f'https://www.linkedin.com{url}{dv}'

    click_button = driver.find_element(by=By.LINK_TEXT, value="500+ connections")
    click_button.click()
    time.sleep(3)

   
    from pydoc import cli

    previousurl = ""
    connectionlist = []
    while len(connectionlist) <=40 : 
        connectionurl = driver.current_url
        if connectionurl == previousurl:
            print('No more connections')
            break
        driver.get(connectionurl)
        src = driver.page_source
        soup = BeautifulSoup(src, features="html.parser")

        #Scroll through page
        last_height = driver.execute_script('return document.body.scrollHeight')
        for i in range(3):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(5)
            new_height =    driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            last_height = new_height

        individual = soup.find_all(class_ = 'entity-result__item')
        for i in individual:
            dictionary = {}
            x = i.find(class_ = 'entity-result__title-text t-16')
            name = x.find("span", {"aria-hidden" : "true"}).get_text()
            dictionary['Name'] = name
            link = x.find(class_ = 'app-aware-link')['href']
            dictionary['Profile_link'] = link
            connectionlist.append(dictionary)

        previousurl = connectionurl
        click_button = driver.find_element(by=By.XPATH, value = "//button[@aria-label='Next']")
        driver.execute_script("arguments[0].click();", click_button)
        #click_button.click()
        time.sleep(5)
         
    #print(len(connectionlist))
    return connectionlist 





#List_info







import pymongo
import json

# client = pymongo.MongoClient()
# mydb = client["100ConnectionsTest1"]
# #print(client.list_database_names())
# collection = mydb['List_info']
# a = List_info
# x = collection.insert_many(a)

#dummy=Extract_info(P_link)

if (__name__=="__main__"):
    #run_with_ngrok(app)
    app.run()
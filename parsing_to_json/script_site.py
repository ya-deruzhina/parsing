from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import requests, json, datetime

def search_1 ():
    url = 'https://dentalia.com/clinicas'
    page = requests.get(url)
    list_of_data = []

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        name_clinics = soup.findAll(class_="dg-map_clinic-card w-dyn-item")

        for i in name_clinics:
            name = i['m8l-c-filter-name']
            address = i['m8l-c-filter-location']
            latlon =list((round(float(t.strip()),7)) for t in i['m8l-c-list-coord'].split(','))
            phones = i.findAll('a')[-1]['href'][5:].split(',')

            list_data = i.text.split('\n')
            while list_data.count('') != 0:
                list_data.remove('')
            
            data_week = {
                "L":"mon",
                "M":"tue",
                "M ":"wed",
                "J":"thu",
                "V":"fri",
                "S":"sat",
                "D":"sun"
            }
            count = 0
            working_hours=list_data[2].replace(" - ","-").replace(", ",".")
            for i in data_week.keys():
                if i == "M ":
                    i = "M"
                if working_hours.count(i) != 0:
                    index = working_hours.index(i)
                    if i == "M" and count == 0:
                            working_hours = working_hours[:index] + "tue" + working_hours[index+1:]
                            count +=1
                    elif i == "M" and count == 1:
                        working_hours = working_hours.replace(i,"wed")
                    else:
                        working_hours = working_hours.replace(i,data_week[i])
                if working_hours [index-1] == " ":
                    working_hours = working_hours[:index-1] + "," + working_hours[index:]
            working_hours = working_hours.replace(" a "," - ").replace(" a"," - ").replace(" y,","-").replace("  "," ").replace(",","!").replace(".",",").split("!")

            data = {
                "name":name,
                "address":address,
                "latlon":latlon,
                "phones": phones,
                "working_hours":working_hours
            }

            list_of_data.append(data)

    with open("script_site_1.json", "w") as fh:
        json.dump(list_of_data, fh, ensure_ascii=False, indent=5)
search_1()


def search_2():
    url_2 = 'https://omsk.yapdomik.ru/about'
    page = requests.get(url_2)
    list_of_data = []

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        script = soup.findAll('script')[4]

        data_site =json.loads(("{" + script.text + "}").replace("=",":").replace('window.initialState','"window.initialState"'))['window.initialState']

        phones = data_site['city']['callCenterPhoneParameters']['number'].split(',')
        data_shops = data_site['shops']

        for i in range(len(data_shops)):
            name = data_shops[i]['name']
            address = "Омск, " + data_shops[i]['address']
            latlon_data = [data_shops[i]['coord']['latitude'],data_shops[i]['coord']['longitude']]
            latlon = list(float(t.strip()) for t in latlon_data)            
            
            working_hours_data = data_shops[i]['workingHours']

            data_time = {}
            numbers_day = {
                1:"Пн",
                2:"Вт",
                3:"Ср",
                4:"Чт",
                5:"Пт",
                6:"Сб",
                7:"Вс",
            }

            for work_day in working_hours_data:
                if work_day["type"] == "default":
                    day = work_day['day']

                    time_from = datetime.datetime.fromtimestamp(int(work_day['from'])).strftime('%M:%S')
                    time_to = datetime.datetime.fromtimestamp(int(work_day['to'])).strftime('%M:%S')
                    working_time = time_from + " - " + time_to

                    data_time[day] = working_time
            
            working_hours = data_time.copy()
            for datas in data_time.keys():
                if datas > 1 and datas < 7:
                    if data_time[datas] == data_time[int(datas)-1] and data_time[datas] == data_time[int(datas)+1]:
                        del working_hours[datas]
            
            work = {}
            keys = []
            for test in working_hours.keys():
                keys.append(test)
                if test == 1:
                    pass
                if test >1:
                    if working_hours[test] == working_hours[keys[-2]]:
                        data_1 = numbers_day[keys[-2]]
                        data_2 = numbers_day[test]
                        key_for_work = data_1 + " - " + data_2
                        work [key_for_work] = working_hours[test]
                        if data_1 in work.keys():
                            del work[data_1]
                            keys.remove(keys[-2])
                    else:
                        data_3 = numbers_day[test]
                        work [data_3] = working_hours[test]
                        
            working_hours = ''
    
            for item in work.keys():
                if len(work.keys()) == 1:
                    working_hours = item + " " + work[item]
                else:
                    work_1 = item + " " + work[item] + ","
                    working_hours += work_1
            if len(working_hours) > 22:
                working_hours = working_hours[:-1]
            
            working_hours = working_hours.split(",")

            

            data = { 
                "name": name,
                "address": address, 
                "latlon": latlon,
                "phones": phones,
                "working_hours": working_hours
            } 
            list_of_data.append(data)

    with open("script_site_2.json", "w") as fh:
        json.dump(list_of_data, fh, ensure_ascii=False, indent=5)


search_2()

def search_3():
    url_3 = 'https://www.santaelena.com.co/tiendas-pasteleria/'
    page = requests.get(url_3)
    list_of_data = []
    address_list = []
    

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        text = soup.findAll(class_='elementor-sub-item')
        count_point = len(text)

        links = {}

        for link in range(count_point):
            links[text[link].text.replace('Pastelerías en ','')] = text[link]['href']

        for url in links.keys():
            page = requests.get(links[url])

            if page.status_code == 200:

                if links[url].startswith('https://www.santaelena.com.co/tiendas-pasteleria/'):
                    souper = BeautifulSoup(page.text, "html.parser")
                    data_location = souper.findAll(class_='elementor-widget-text-editor')
                    names_list = []
                    names = souper.findAll('h3')
                    for n in range (len(names)):
                        if names[n].text != "":
                            names_list.append(names[n].text)
                    counter = 0


                    for i in range(len(data_location)):
                        if (data_location[i].text.count('Horario de atención')) == 1:

                            correct_data = json.loads('{'+data_location[i].text.replace('\n','').replace(':','-').replace('\xa0','').replace('Dirección- ','"Dirección":"').replace('Dirección-','"Dirección":"').replace('Teléfono- ','","Teléfono":"').replace('Teléfono-','","Teléfono":"').replace('Horario de atención- ','","Horario de atención":"').replace('Horario de atención-','","Horario de atención":"')+'"}')
                            address_data = url + ', ' + correct_data['Dirección']

                            if address_data not in address_list:
                                name = names[counter].text.replace('                        ','').replace('\n','')
                                counter +=1

                                address = address_data.replace('Pastelería en','')
                                if address.count('#') > 0:
                                    index_a = address.index('#')
                                elif address.count('Km 4') != 0:
                                    index_a = 26
                                elif address.count('020516')>0:
                                    index_a = 12 
                                elif len(address)>30 and address.count('Km 10') == 0:
                                    index_a = 20
                                else:
                                    index_a = 16
                                address = address[:index_a]

                                geolocator = Nominatim(user_agent="Tester")
                                location = geolocator.geocode(address)[-1]
                                latlon = []

                                for i in range(len(location)):
                                    latlon.append(round(location[i],6))

                                phones = correct_data['Teléfono'].replace('Contacto- ','').replace(' ','').replace('ext',' ext ').split(',')
                                working_hours = correct_data['Horario de atención'].replace('-',':').replace(' a.m. – ',' - ').replace(' a. m. / ',' - ').replace(' a.m. / ',' - ').replace(' a.m. ','').replace(' a. m./ ',' - ').replace('Sábados, Domingos y festivos: ','sat, sun with hol ').replace('Lunes a sábado: ','mon - sat ').replace('Lunes a Sábado: ','mon - sat ').replace('Domingos: ','sun ').replace('Lunes a viernes: ','mon - fri ').replace('Sábados: ','sat ').replace('Domingos y festivos: ','sun and hol ').replace('Domingos y Festivos – ','sun and hol ').replace('Domingos y Festivos: ','sun and hol ').replace('Domingo y festivos: ','sun and hol ').replace('Prestamos servicio ','round the clock ').replace('Lunes a domingos incluye festivos','mon - sat with hol ').replace('Lunes a domingos: ','mon - sat ').replace('Lunes a domingo: ','mon - sat ').replace('las','')
                                
                                while working_hours.count(' p.m.') > 0:
                                    index_time = working_hours.index(' p.m.')
                                    working_hours = (working_hours[:index_time-5] + ' ' + str(int(working_hours[index_time-5:index_time-3])+12) + ':00,' + working_hours[index_time+5:]).replace('  ',' ')
                                while working_hours.count(' p.m ') > 0:
                                    index_time = working_hours.index(' p.m ')
                                    working_hours = (working_hours[:index_time-5] + ' ' + str(int(working_hours[index_time-5:index_time-3])+12) + ':00,' + working_hours[index_time+5:]).replace('  ',' ')

                                if working_hours[-2]+ working_hours[-1] == ', ':
                                    working_hours = working_hours[:-2]

                                if working_hours[-1] == ',' or working_hours[-1] == ' ':
                                    working_hours = working_hours[:-1]

                                working_hours = working_hours.split(',')

                                data = { 
                                "name": name,
                                "address": address_data,
                                "latlon": latlon, 
                                "phones": phones,
                                "working_hours": working_hours
                                } 
                                
                                list_of_data.append(data)
                                address_list.append(address_data)

    with open("script_site_3.json", "w") as fh:
        json.dump(list_of_data, fh, ensure_ascii=False, indent=5)


search_3()
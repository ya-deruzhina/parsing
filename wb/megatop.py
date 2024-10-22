import requests
import json
import pandas as pd

def find_category (category,salary_sheet):
    for l in category['childs']:
        salary_sheet['ID'].append(l['id'])
        salary_sheet['Category'].append(l['name'])
        return salary_sheet


def megatop ():
    url = 'https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v2.json'
    response = requests.get(url)
    text = json.loads(response.text)


    salary_sheets = {}
    
    for k in text:
        salary_sheet = {'ID': [],
            'Category': [],
            'nesting': []
        }

        if 'childs' in k.keys():
            find_category(k,salary_sheet)
            salary_sheet['nesting'].append(2)
            for i in k['childs']:
                if 'childs' in i.keys():
                    find_category(i,salary_sheet)
                    salary_sheet['nesting'].append(3)
                    for m in i['childs']:
                        if 'childs' in m.keys():
                            find_category(m,salary_sheet)
                            salary_sheet['nesting'].append(4)
                            for n in m['childs']:
                                if 'childs' in n.keys():
                                    find_category(n,salary_sheet)
                                    salary_sheet['nesting'].append(5)
                                    for w in n['childs']:
                                        if 'childs' in w.keys():
                                            find_category(w,salary_sheet)
                                            salary_sheet['nesting'].append(6)
                                        else:
                                            url_catalog = 'https://www.wildberries.ru'+w['url']
                                            # print (url_catalog)
                                else:
                                    url_catalog = 'https://www.wildberries.ru'+n['url']
                                    # print (url_catalog)
                        else:
                            url_catalog = 'https://www.wildberries.ru'+m['url']
                            # print (url_catalog)
                else:
                    url_catalog = 'https://www.wildberries.ru'+k['url']
                    # print (url_catalog)
        else:
            url_catalog = 'https://www.wildberries.ru'+k['url']
            print (url_catalog)


        salary_sheets[k['name']] = pd.DataFrame(salary_sheet)
    writer = pd.ExcelWriter('./salaries.xlsx', engine='xlsxwriter')

    for sheet_name in salary_sheets.keys():
        salary_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer._save()
        
megatop()


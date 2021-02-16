import json
import traceback
from termcolor import colored

def DuplicatePages():
    try:
        print('Removing Duplicate Pages Process Started')

        #Load json to script and creating empty dict
        f = open('pages.json',)
        data = json.load(f)
        removed_pages=0
        pages = {}

        #checking duplicate page names with nested for loop. When it finds, change name to 'NULL' for remove once.
        for i in data:
            page_name = str(data[i]['Page-Name'])
            for j in data:
                name = str(data[j]['Page-Name'])
                if name == page_name and i!=j and name != 'NULL':
                    #logging dublicate page name and change its name to 'NULL'
                    print(colored('Dublicate page :', 'green') + str(data[j]['Page-Name']))
                    data[j]["Page-Name"] = 'NULL'

        #resetting index for travel dictionary again
        index = 0
        for i in data:
            page_name = str(data[i]['Page-Name'])
            #checking page name is NULL or Not
            if page_name != 'NULL':
                pages[index] = data[i]
                index=index+1
            else:
                #counting removed pages
                removed_pages = removed_pages + 1

        #Writing dictionary to json file
        with open('pages.json', 'w', encoding='utf-8') as json_file:
            json.dump(pages, json_file, ensure_ascii=False,
                      indent=2, sort_keys=False)

        #Succesfully complete message
        complete_msg = str(removed_pages) + ' pages removed as a duplicate!'
        print(colored(complete_msg, 'green'))

    #Error Handling
    except Exception:
        traceback.print_exc()

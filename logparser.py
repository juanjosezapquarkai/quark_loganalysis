from googlesearch import search
import argparse
import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

def write_queries(data):
    with open('queries.json', 'w') as f:
        json.dump(data, f)

def write_no_results(data):
    with open('noresults.json', 'w') as f:
        json.dump(data, f)

def parseHtml(url):
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    delay = 5 # seconds
    result_dict = {}
    try:
        container_div = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'dashContainer')))
        divs = container_div.find_elements(By.XPATH, './div')
        for div_index, div in enumerate(divs):
            if div_index > 3:
                break
            if div_index == 0:
                div_text = div.text
                div_text_list = div_text.split('\n')
                result_dict['bug_header'] = div_text_list[0]
                result_dict['bug_desc'] = div_text_list[1]
            if div_index == 1:
                div_text = div.text
                div_text_list = div_text.split('\n')
                result_dict['lastmodified'] = div_text_list[1]
            if div_index == 2:
                div_text = div.text
                div_text_list = div_text.split('\n')
                result_dict['products'] = div_text_list[1]
            if div_index == 3:
                div_text = div.text
                div_text_list = div_text.split('\n')
                result_dict['affectedrelease'] = div_text_list[1]

    except TimeoutException:
        print("Loading took too much time!")

    return result_dict

def parse_logfile(logfile):
    print('parsing ' + logfile)
    log_list = []

    with open(logfile) as logf:
        log_data = logf.readlines()

    for log_item in log_data:
        log_item_sep = log_item.split(":")
        #if not log_item_sep[4].strip().startswith("%"):
        #    print(log_item_sep[4])
        #print(log_item_sep)
        log_dict = {}
        log_dict['logmessage'] = log_item
        tmp_log_message_date = log_item_sep[0:2]
        tmp_msg_date = ''
        try:
            tmp_msg_date = log_item_sep[2].split(' ')[0]
        except:
            print('error with ' + str(log_item_sep))
            print('log_item = ' + str(log_item))
            print('logfile = ' + logfile)
        log_message_date = ':'.join(tmp_log_message_date) + ':' + tmp_msg_date
        log_dict['date'] = log_message_date
        log_message_data = []
        for sep_log_index, sep_log_item in enumerate(log_item_sep):
            if sep_log_item.strip().startswith('%'):
                log_message_data = log_item_sep[sep_log_index:]
                log_dict['query'] = sep_log_item
                query_lower = sep_log_item.lower()
                if 'error' in query_lower:
                    log_dict['errorlevel'] = 'error'
                elif 'alert' in query_lower:
                    log_dict['errorlevel'] = 'alert'
                else:
                    log_dict['errorlevel'] = 'error'
                break
        flagged_data = False
        for item in log_message_data:
            lower_item = item.lower()
            if "alert" in lower_item:
                flagged_data = True
                break
        # if we want to query all entries, then set flagged_data to True
        if flagged_data:
            log_list.append(log_dict)
        #print(log_message_data)

    query_dict = {} #load_queries()
    query_html_data = {}
    query_gpt = {}
    no_results = [] #load_no_results()
    print('log_list = ' + str(len(log_list)))
    for item_index, item in enumerate(log_list):
        if 'query' in item:
            query = item['query'].strip()
            #print('query = ' + query)
            #print(query_html_data)
            #print(query_gpt)
            if query in query_html_data:
                item['html_data'] = query_html_data[query]
            if query in query_gpt:
                item['gpt'] = query_gpt[query]
            log_list[item_index] = item
            if query in query_dict:
                continue
            if query in no_results:
                continue
            res = search(query, num=10, stop=10, pause=2)
            found = False
            for j in search("site:cisco.com " + query, num=10, stop=10, pause=2):  #tld="cisco", num=10, stop=10, pause=2):
                if j.startswith('https://quickview.cloudapps.cisco.com/quickview'):
                    query_dict[query] = j
                    found = True
                    print(query + ': ' + j)
                    item['query_result'] = j
                    html_data = parseHtml(j)
                    if len(html_data) > 0:
                        query_html_data[query] = html_data
                        query_gpt[query] = 'placeholder'
                    break
            if not found:
                no_results.append(query)
            time.sleep(5)

            print('got here 1')
            print(query_html_data)
            print(query_gpt)
            if query in query_html_data:
                print('got here 2')
                item['html_data'] = query_html_data[query]
            if query in query_gpt:
                print('got here 3')
                item['gpt'] = query_gpt[query]
            log_list[item_index] = item

    write_queries(query_dict)
    write_no_results(no_results)
    print('num queries = ' + str(len(query_dict)))
    print('no results = ' + str(len(no_results)))

    with open(logfile + '_.json', 'w') as outfile:
        json.dump(log_list, outfile)

    return log_list

def main(args):
    allFiles = getListOfFiles(args.dir)
    for aFile in allFiles:
        if aFile.endswith('_.json'):
            continue
        #elif os.path.isfile(aFile + '_.json'):
        #    continue
        else:
            parse_logfile(aFile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, default=None, help='Name of directory containint data')

    args = parser.parse_args()
    main(args)

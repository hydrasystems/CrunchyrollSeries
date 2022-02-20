from bs4 import BeautifulSoup
import cfscrape
import time

urls = []
names = []
links = []
lang = []


# Gets Crunchyroll URL from user.
print('Welcome to Crunchyroll Batch file creation tool v1.0')
url_i = input('Enter Crunchyroll Series Url: ')


# Reverses Url and gets name of series and appends it to normal url.
def url_format(u):
    print('# Reading url input')
    time.sleep(1)
    ap = u[::-1]
    count_u = -1w
    for c in ap:
        count_u += 1
        if c == '/':
            break
    apx = ap[:count_u]
    apr = 'https://www.crunchyroll.com/' + apx[::-1]
    print('# url format complete')
    time.sleep(1)
    print('# Requesting site')
    time.sleep(1)
    return apr


# Uses Format function on Url input.
url_input = url_format(url_i)


# Requests site with cfscrape with the Url that has been formatted.
# Also creates a Beautiful soup object that's formatted in lxml.
soup = BeautifulSoup(cfscrape.create_scraper().get(url_input).text, 'lxml')
print('# Html received')


# Takes name from url.
def series_name(u):
    ap = u[::-1]
    count_u = -1
    for c in ap:
        count_u += 1
        if c == '/':
            break
    apx = ap[:count_u]
    apr = apx[::-1]
    return apr


file_name_i = series_name(url_i)

# Writes all 'a' tags and content with class 'portrait-element block-link titlefix episode' to txt file.
f = open(file_name_i + '.txt', 'w')
els = soup.find_all('a', class_='portrait-element block-link titlefix episode')
f.write(str(els))
f.close()
print('# File will save in working directory as ' + file_name_i + '.txt')
print('# Parsing html for links')
time.sleep(1)


# Creates a batch file of links of input series.
def create_batch():
    # initialize all language lists.
    global lang
    urls_jap = []
    urls_eng = []
    urls_sp = []
    urls_pr = []
    urls_ru = []
    urls_fr = []
    urls_ger = []
    count_lang = -1
    # Opens text file with all the 'a' tags and their content.
    jk = open(file_name_i + '.txt', 'r')
    # Goes through line by line and saves only the lines that start with </a> or [<a to a list.
    # </a> is for the first line., [<a is for all the other lines.
    # </a>] is the last item that is not appended to the list.
    for line in jk:
        if line[:4] == '</a>' or line[:3] == '[<a':
            if line != '</a>]':
                links.append(line)
            else:
                print('# Finished creating list for sorting')
    # Grabs Url from 'a' tag by splitting it at every " and then indexing off of the ' href=' location.
    # Also adds the name of the episode to names list. Which is used to create the lang(language) list.
    for link in links:
        split = link.split('"')
        count = 0
        count = split.index(' href=', count)
        names.append(split[count + 3])
        urls.append('https://www.crunchyroll.com' + split[count + 1])
    jk.close()
    # adds which language for each episode.
    for x in names:
        count_lang += 1
        # finds the Dub language for that episode.
        rep = x.replace(')', '(')
        split_lang = rep.split('(')
        # Checks if split worked aka if its dubbed or not.
        if len(split_lang) == 3:
            dub = split_lang[1]
        # sets dub to the dub language for that episode example 'English Dub'.
        # if language is japanese and there are no dubs. dub is set to episode tittle and counted on jap_num
        # so if there is an error with other language filter or a language is not supported it will fall into japanese.
        else:
            dub = split_lang

        # Writes each supported dub language and according link to its own list.
        if dub == 'English Dub':
            urls_eng.append(urls[count_lang])
        elif dub == 'Spanish Dub':
            urls_sp.append(urls[count_lang])
        elif dub == 'Portuguese Dub':
            urls_pr.append(urls[count_lang])
        elif dub == 'Russian':
            urls_ru.append(urls[count_lang])
        elif dub == 'French Dub':
            urls_fr.append(urls[count_lang])
        elif dub == 'German Dub':
            urls_ger.append(urls[count_lang])
        else:
            urls_jap.append(urls[count_lang])
    # prints all available dub languages and asks user to pick one.
    print('Pick Audio: ')
    if len(urls_jap) > 0:
        print('{1} Episodes with japanese audio: ' + str(len(urls_jap)))
    if len(urls_eng) > 0:
        print('{2} Episodes with english audio: ' + str(len(urls_eng)))
    if len(urls_sp) > 0:
        print('{3} Episodes with spanish audio: ' + str(len(urls_sp)))
    if len(urls_pr) > 0:
        print('{4} Episodes with portuguese audio: ' + str(len(urls_pr)))
    if len(urls_ru) > 0:
        print('{5} Episodes with russian audio: ' + str(len(urls_ru)))
    if len(urls_fr) > 0:
        print('{6} Episodes with french audio: ' + str(len(urls_fr)))
    if len(urls_ger) > 0:
        print('{7} Episodes with german audio: ' + str(len(urls_ger)))

    lang_choice = int(input('#: '))

    if lang_choice == 1:
        lang = urls_jap.copy()
    if lang_choice == 2:
        lang = urls_eng.copy()
    if lang_choice == 3:
        lang = urls_sp.copy()
    if lang_choice == 4:
        lang = urls_pr.copy()
    if lang_choice == 5:
        lang = urls_ru.copy()
    if lang_choice == 6:
        lang = urls_fr.copy()
    if lang_choice == 7:
        lang = urls_ger.copy()

    # Final print of urls and write with a \n.
    x = open(file_name_i + '.txt', 'w')
    for u in lang:
        x.write(u + '\n')
    x.close()


create_batch()

print_true = input('Print Output Y/N:')
if print_true == 'y' or print_true == 'Y':
    for line_z in lang:
        print(line_z)
else:
    print('# Exiting')
    exit(0)

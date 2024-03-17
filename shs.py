import re, json
from time import time
from typing import List, Tuple, Dict
from urllib import request as lib_req, error
from urllib import parse
from bs4 import BeautifulSoup

def get_response(url:str, request) -> str:
    '''
    Send a http request and get a response
        decode it
        then return the data
    '''
    # send response
    with lib_req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    
    # return response data
    return data

def write_session_and_area_in_file(bookname:str, datas:List) -> None:
    '''
    Just as the name write Session and Area in a file
        file name is Sessions_Areas_of_{bookname}.txt
    '''
    if interactive:
        now = 0
        length = len(datas)
        width = 30
    with open(file=f"ALL_Sessions_Areas_of_{bookname}.txt", mode="a", encoding="utf-8") as file:
        file.write(f"This is ALL the SESSIONS and AREAS of {bookname}")
        file.write("\n\n\n")
        for id,session,area in datas:
            file.write(f"Session:{session} ; Area:{area}\n")
            if interactive:
                process = int(now/length*width)
                bar = f"Writing Session and Area [{ '#' * process}{ "-" * (width-process)}]"
                now+=1
                print(bar,end="\r")
    if interactive:
        print(f"Writing Session and Area [{ '#' * width }]",end="\r")
        print()

def write_content_in_file(session:str, area:str, keys:List, values:List) -> None:
    '''
    pass
    '''
    with open(file=f"みんなの{bookname}", mode="a", encoding="utf-8") as file:
        file.write(f"------- Session:{session} | Area:{area} -------\n")
        for key,value in zip(keys,values):
            file.write(f"{key}\n")
            file.write(f"{value}\n\n")
        file.write("\n\n\n")

def get_sessions_and_areas() -> Tuple[List,Dict[int,str]]:
    '''
    Have a index of the website, then i can search the book
        First use HTTP GET
        Second filter
        then return Sessions and dic_number_with_area_name
    Ex:
        Sessions: -> List
            ['1130310', '1121010', '1120310']
        dic_number_with_area_name: -> Dict
            {'1': '新北', '2': '高二', '3': '高雄'}
    '''
    contest_sessions = []
    areas = []
    dic_number_with_area_name={}

    # the request
    url = "https://www.shs.edu.tw/Customer/Winning/OverIndex"
    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    request=lib_req.Request(url,headers= headers)
    # http get
    resp = get_response(url,request=request)
    # parsing response to HTML DOM
    root = BeautifulSoup(resp,"html.parser")

    # get the Competition Sessions and the City name
    area_go = False
    value_root = root.find_all("option")
    for value in value_root:
        v_string = value.string
        # match the "Session" string
        pattern_of_Sessions = r"^[\d]{7}$"
        if re.match(pattern=pattern_of_Sessions,string=v_string):
            contest_sessions.append(v_string)
            continue
 
        # get "areas", which is between "--選擇分區--" and "[不拘]"
        if "選擇分區" in v_string:
            area_go = True
            continue
        if "不拘" in v_string:
            area_go = False
        if area_go:
            areas.append(v_string)
    
    # make a dictionary of Number and areas
    for number_base_one in range(1,len(areas)+1):
        dic_number_with_area_name[number_base_one]=areas[number_base_one-1]

    return contest_sessions, dic_number_with_area_name

def get_id_sessions_area_of_target(booktitle:str, contest_sessions:List[str], dic_number_with_area_name:Dict[int,str]) -> List[Tuple[str,str,str]]:
    '''
    to use the data from "get_sessions_and_areas" to find where has the data we want
        make a double loop (Sessions and Area)
        HTTP GET it
        check if target exit
        return id and Sessions and Area
    '''
    id_sessions_and_areas_of_target=[]

    # searching the target in loop
    for session in contest_sessions:
        if interactive:
            print(f"Session:{session} -> ",end="",flush=True)
        # order of Areas (base one)
        for area_number_base_one in dic_number_with_area_name.keys():
            # the API
            # Alert! Don't forget to change Sessions, Order and Booktitle on this URL
            url=f"https://www.shs.edu.tw/Customer/Winning/GetOverAll?draw=9&columns%5B0%5D%5Bdata%5D=Id&columns%5B0%5D%5Bname%5D=Id&columns%5B0%5D%5Bsearchable%5D=false&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=HistoryOverAreaName&columns%5B1%5D%5Bname%5D=HistoryOverAreaName&columns%5B1%5D%5Bsearchable%5D=false&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=HistoryEssayOverCityName&columns%5B2%5D%5Bname%5D=HistoryEssayOverCityName&columns%5B2%5D%5Bsearchable%5D=false&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=HistoryOverSchoolName&columns%5B3%5D%5Bname%5D=HistoryOverSchoolName&columns%5B3%5D%5Bsearchable%5D=false&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=HistoryOverUserGrade&columns%5B4%5D%5Bname%5D=HistoryOverUserGrade&columns%5B4%5D%5Bsearchable%5D=false&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=HistoryOverUserClass&columns%5B5%5D%5Bname%5D=HistoryOverUserClass&columns%5B5%5D%5Bsearchable%5D=false&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=HistoryOverUserName&columns%5B6%5D%5Bname%5D=HistoryOverUserName&columns%5B6%5D%5Bsearchable%5D=false&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=HistoryOverTeacherName1&columns%5B7%5D%5Bname%5D=HistoryOverTeacherName1&columns%5B7%5D%5Bsearchable%5D=false&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=HistoryOverTitleName&columns%5B8%5D%5Bname%5D=HistoryOverTitleName&columns%5B8%5D%5Bsearchable%5D=false&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=HistoryOverRanking&columns%5B9%5D%5Bname%5D=HistoryOverRanking&columns%5B9%5D%5Bsearchable%5D=false&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=Id&columns%5B10%5D%5Bname%5D=&columns%5B10%5D%5Bsearchable%5D=false&columns%5B10%5D%5Borderable%5D=false&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=4&order%5B0%5D%5Bdir%5D=asc&start=0&length=10&search%5Bvalue%5D=&search%5Bregex%5D=false&contestNo={session}&areaId={area_number_base_one}&schoolNo=&txtName={booktitle}&txtAuthorName=&grade=&ranking=&_=1667313681247"
            headers = {
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            request=lib_req.Request(url,headers= headers)
            # http GET
            resp = get_response(url,request=request)
            # parsing response to json form
            root=json.loads(resp)

            # check if target exit in this Session and Area
            if root["data"]:
                id = root["data"][0]["Id"]
                id_sessions_and_areas_of_target.append([id,session,dic_number_with_area_name[area_number_base_one]])
            if interactive :
                print(1 if root["data"] else 0,end="",flush=True)
        if interactive:
            print()
    # return the result and i forget what can id do ^_^
    return id_sessions_and_areas_of_target

def get_content(id:str, contest_session:str, area:str) -> None:
    '''
    i'm tired...
    '''
    # make a request
    url="https://www.shs.edu.tw/Customer/Winning/ShowWorkOver"
    requestdata=id
    request=lib_req.Request(url,headers={
                "content-Type":"application/json; charset=UTF-8",
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },data=json.dumps(requestdata).encode("utf-8"))
    # http GET
    resp = get_response(url=url, request=request)
    # praing with json form
    root=json.loads(resp)

    # get the data
    keys = []
    values = []
    for key,value in root["Data"].items():
        value = value.replace("<br/>","\n").replace("<br />","\n")
        keys.append(key)
        values.append(value)

    # write it in file  
    write_content_in_file(contest_session,area,keys,values)

def end_of_process() -> None:
    '''
    as u see, i'm just a description
    '''
    print("\n\n\n")
    print("  ██████  █    ██  ▄████▄   ▄████▄  ▓█████   ██████   █████▒█    ██  ██▓     ██▓   ▓██   ██▓   ▓█████▄ ▓█████   ██████  █    ██     ▐██▌ ")
    print("▒██    ▒  ██  ▓██▒▒██▀ ▀█  ▒██▀ ▀█  ▓█   ▀ ▒██    ▒ ▓██   ▒ ██  ▓██▒▓██▒    ▓██▒    ▒██  ██▒   ▒██▀ ██▌▓█   ▀ ▒██    ▒  ██  ▓██▒    ▐██▌ ")
    print("░ ▓██▄   ▓██  ▒██░▒▓█    ▄ ▒▓█    ▄ ▒███   ░ ▓██▄   ▒████ ░▓██  ▒██░▒██░    ▒██░     ▒██ ██░   ░██   █▌▒███   ░ ▓██▄   ▓██  ▒██░    ▐██▌ ")
    print("  ▒   ██▒▓▓█  ░██░▒▓▓▄ ▄██▒▒▓▓▄ ▄██▒▒▓█  ▄   ▒   ██▒░▓█▒  ░▓▓█  ░██░▒██░    ▒██░     ░ ▐██▓░   ░▓█▄   ▌▒▓█  ▄   ▒   ██▒▓▓█  ░██░    ▓██▒ ")
    print("▒██████▒▒▒▒█████▓ ▒ ▓███▀ ░▒ ▓███▀ ░░▒████▒▒██████▒▒░▒█░   ▒▒█████▓ ░██████▒░██████▒ ░ ██▒▓░   ░▒████▓ ░▒████▒▒██████▒▒▒▒█████▓     ▒▄▄  ")
    print("▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░░ ░▒ ▒  ░░░ ▒░ ░▒ ▒▓▒ ▒ ░ ▒ ░   ░▒▓▒ ▒ ▒ ░ ▒░▓  ░░ ▒░▓  ░  ██▒▒▒     ▒▒▓  ▒ ░░ ▒░ ░▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒     ░▀▀▒ ")
    print("░ ░▒  ░ ░░░▒░ ░ ░   ░  ▒     ░  ▒    ░ ░  ░░ ░▒  ░ ░ ░     ░░▒░ ░ ░ ░ ░ ▒  ░░ ░ ▒  ░▓██ ░▒░     ░ ▒  ▒  ░ ░  ░░ ░▒  ░ ░░░▒░ ░ ░     ░  ░ ")
    print("░  ░  ░   ░░░ ░ ░ ░        ░           ░   ░  ░  ░   ░ ░    ░░░ ░ ░   ░ ░     ░ ░   ▒ ▒ ░░      ░ ░  ░    ░   ░  ░  ░   ░░░ ░ ░        ░ ")
    print("      ░     ░     ░ ░      ░ ░         ░  ░      ░            ░         ░  ░    ░  ░░ ░           ░       ░  ░      ░     ░         ░    ")
    print("                  ░        ░                                                        ░ ░         ░                                        ")
    print("\n\n\n")

def not_end_of_process(error:str) -> None:
    print("\n\n\n")
    print(" ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░      ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ")
    print("░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░")
    print("░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░")
    print("░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░")
    print("░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░")
    print("░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░")
    print(" ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░    ░▒▓██████▓▒░ ")
    print("\n\n\n")
    if re.match(pattern=r"eval(.*)",string=bookname):
        print(f"You are EVIL !");return
    print(f"You got a '{error}' !!!")

def time_of_process() -> None:
    # max_length=max([len(func_name[0]) for func_name in time_total]) === 27
    sum_of_total_time = sum([process_time[1] for process_time in time_total])
    for func,cost_time in time_total:
        print(f"{func:27} |  process time:{cost_time:11.6f}s |  percent:{(cost_time/sum_of_total_time)*100:6.2f}%")
    print("-"*71)
    print(f"{"total time":27} |  process time:{sum_of_total_time:11.6f}s")

# main code
if __name__=="__main__":
    '''
    * require BeautifulSoup
        pip install beautifulsoup4
    
    build-in modules
        re for match string
        json for parse response
        time for timeit
        typing for comment
        urllib for HTTP GET
    
    Warning !
    If you search too vaguely, you may find a lot of irrelevant books.

    This is a python program to captures the 閱讀心得 on 中學生網站
        *set option
        some preparation to make a map
        search the target
        DONE
    '''

    ## ----- option -----
    # if you want a bar of progress
    interactive = True
    bookname=""
    # four round
    time_total=[["get the map",0],
                ["find the book",0],
                ["write session and area",0],
                ["get content and write it in",0]]

    try:
        ## ----- prepare -----
        # enter your book name ;;; default is "86―エイティシックス―"
        bookname = input("Give book title! -> ") or "86"
        # encode to URL
        booktitle = parse.quote(bookname)
        # get "the index of the website" (Sessions, Area)
        start_0=time()
        contest_sessions,dic_number_with_area_name = get_sessions_and_areas()
        end_0=time()
        time_total[0][1]=end_0-start_0

        ## ----- running -----
        # use "the index of the website" to find where have the target we want
        # use the result to get the book content
        start_1=time()
        id_sessions_and_areas_of_target = get_id_sessions_area_of_target(booktitle, contest_sessions, dic_number_with_area_name)        
        end_1=time()
        time_total[1][1]=end_1-start_1
        start_2=time()
        write_session_and_area_in_file(bookname=bookname,datas=id_sessions_and_areas_of_target)
        end_2=time()
        time_total[2][1]=end_2-start_2
        # get the content
        start_3=time()
        if interactive:
            now = 0
            length = len(id_sessions_and_areas_of_target)
            width = 30
        for each in id_sessions_and_areas_of_target:
            get_content(id=each[0], contest_session=each[1], area=each[2])
            if interactive:
                    process = int(now/length*width)
                    bar = f"Writing Content          [{ '#' * process}{ "-" * (width-process)}]"
                    now+=1
                    print(bar,end="\r")
        if interactive:
            print(f"Writing Content          [{ '#' * width }]",end="\r")
            print()
        end_3=time()
        time_total[3][1]=end_3-start_3

        ## ----- this is the END of this program -----
        end_of_process()
        time_of_process()
    
    except error.HTTPError as h:
        not_end_of_process(h)
    except PermissionError as p:
        not_end_of_process(p)
    except KeyboardInterrupt as k:
        not_end_of_process("STOP")
    except:
        not_end_of_process("Nothing")
import os
import requests
import gspread
import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import ast

# maiissmackersheettest@maiis-344006.iam.gserviceaccount.com

SheetName = "AMAN Digidevine Data"
WorkSheet = "After March 25"

key = "06196ddeb2a0252"
secrate = "636bc658b45bea7a5cddb4d7d3b390cfb04eb314"

def upload(file_path):
    img = open(file_path, 'rb')
    url = "https://api.imgur.com/3/image"
    header = {'Authorization' : f'Client-ID {key}'}
    dt = requests.post(url, img, headers=header).json()
    img.close()
    if dt.get('success', None):
        return dt['data']['link']
    else:
        return dt

def getDetails():
    sh = gspread.service_account(filename='api.json')
    she = sh.open(SheetName)
    global sheet
    sheet = she.worksheet(WorkSheet)
    """
    Here this function is used to get the data from the sheet
    """
    data = sheet.get_all_values()
    # sheet.update("A8", "61")
    return data

def update(position:str, data:str):
    """
    Here this function is used to update sheed according to given position
    """
    global sheet
    try:
        sheet.update(position, data)
    except:
        return False
    return True

def updateseq(cook:str, imglist:list, ids:str):
    # format -  email:['sno'] and also the list of the images
    mail = cook.split(':')[0]
    Poslis = ast.literal_eval(cook.split(':')[1])
    data = getDetails()
    data.pop(0)
    # 17, 20, 23, 26, 29, 32, 35, 38, 41, 44
    posit = [f"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W"]
    position = 2
    for dt in data:
        if dt[0] == ids:
            n = 0
            for link in imglist:
                if update(f"{posit[n]}{position}", link):
                    print(f"Data Updated : {posit[n]}{position}")
                else:
                    print(f"Error while updating data")
                n = n + 1
            break
        position = position + 1
    return True

def uploadFile(fileName:str):
    try:
        link = upload(fileName)
    except Exception as e:
        print(f"Error {e}")
        return None
    return link



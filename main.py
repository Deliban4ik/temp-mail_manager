import requests
from colorama import Fore
def get_messages(username, domain):
    get_messages_response=requests.get(api_url+"?action=getMessages&login=%s&domain=%s" % (username,domain))
    if get_messages_response.status_code==200:
        return get_messages_response.json()
    else:
        return None
def show_messages(username, domain):
    if (username, domain)==("demo", "1secmail.com"):
        return None
    else:
        messages_list=get_messages(username, domain)
        if not messages_list:
            return None
        if messages_list is not None:
            for message in messages_list[::-1]:
                for key, value in message.items():
                    print("%s: %s" % (key, value))
            return messages_list
        else:
            print(Fore.RED+"While updating the list, an unexpected error occurred! Please try again later."+Fore.RESET)
            return None
def get_message_content(username, domain, message):
    read_message_url=api_url+"?action=readMessage&"+auth+"&id=%s" % message.get("id")
    read_message_response=requests.get(read_message_url).json()
    print(
        "id=%s" % str(read_message_response.get("id")).strip(), 
        "from=%s" % read_message_response.get("from").strip(), 
        "date=%s" % read_message_response.get("date").strip(), 
        "text=%s" % read_message_response.get("textBody").strip(),
        "attachments=%s" % read_message_response.get("attachments"),
        sep="\n",
        end="\n\n"
        )
    return read_message_response
api_url="https://www.1secmail.com/api/v1/"
username="demo"
domain="1secmail.com"
generated_mail=None
messages_list=None
while True:
    action=int(input("1-update messages list, 2-generate new mail, 3-show mail, 4-read message, 5-download file:"))
    match action:
        case 1:
            messages_list=show_messages(username, domain)
            if generated_mail is None:
                print(Fore.RED+"You haven't mail! Please generate new mail"+Fore.RESET)
                continue
            elif messages_list is None:
                print(Fore.RED+"You haven't messages!"+Fore.RESET)
                continue
        case 2:
            generated_mail=requests.get(api_url+"?action=genRandomMailbox&count=1").json()[0]
            username=generated_mail.split("@")[0]
            domain=generated_mail.split("@")[1]
            print("Generated mail is %s" % generated_mail)
            auth="login=%s&domain=%s" % (username, domain)
        case 3:
            print(generated_mail if generated_mail is not None else Fore.RED+"You haven't mail! Please generate new mail"+Fore.RESET)
        case 4:
            messages_list=show_messages(username, domain)
            if generated_mail is None:
                print(Fore.RED+"You haven't mail! Please generate new mail"+Fore.RESET)
                continue
            elif messages_list is None:
                print(Fore.RED+"You haven't messages!"+Fore.RESET)
                continue
            while 0>=(message_number:=int(input("Enter the message number: "))) or message_number>len(messages_list):
                # print(0<message_number,message_number<len(messages_list),message_number, len(messages_list))
                ...
            current_message = messages_list[0-message_number]
            get_message_content(username, domain, current_message)
        case 5:
            if generated_mail is None:
                print(Fore.RED+"You haven't mail! Please generate new mail"+Fore.RESET)
                continue
            elif messages_list is None:
                print(Fore.RED+"You haven't messages!"+Fore.RESET)
                continue
            show_messages(username,domain)
            while 0>=(message_number:=int(input("Enter the message number: "))) or message_number>len(messages_list):
                # print(0<message_number,message_number<len(messages_list),message_number, len(messages_list))
                ...
            current_message = messages_list[0-message_number]
            print(current_message)
            attachments=get_message_content(username,domain,current_message).get("attachments")
            if not attachments:
                print(Fore.RED+"There are no attachments in this message"+Fore.RESET)
                continue
            
            attachment_number=0
            if len(attachments)>1:
                print(*[attachment for attachment in attachments], sep="\n")
                while 0>=(attachment_number:=int(input("Enter the attachment number: "))) or attachment_number>len(attachments):
                    ...
            download_file_url=api_url+"?action=download&"+auth+"&id=%s" % current_message.get("id") + "&file=%s" % attachments[attachment_number-1]["filename"]
            download_file_response=requests.get(download_file_url)
            with open(attachments[attachment_number-1]["filename"], 'wb') as f: 
                f.write(download_file_response.content)
            print(download_file_url)
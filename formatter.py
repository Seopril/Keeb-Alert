# Formats for email notifications
def email(gb_dict=None, ic_dict=None):
    message = "<h1>GeekHack Updates: </h1>\n<h2>Group Buy Updates</h2>\n"
    if gb_dict:
        for item, val in gb_dict.items():
            message = message + f"<p>{val} --> {item}</p>\n"
    else:
        message = message + f"<p><b>Not Checked</b></p>\n"
    message = message+"\n<h2>Interest Check Updates</h2>\n"
    if ic_dict:
        for item, val in ic_dict.items():
            message = message + f"<p>{val} --> {item}</p>\n"
    else:
        message = message + f"<p><b>Not Checked</b></p>\n"
    print (message)
    return message


# Formats for sms notifications
def sms(gb_dict=None, ic_dict=None):
    # Formats the message based on the items in the dictionary pased to it.
    message = "GeekHack Updates: \n"
    if gb_dict:
        message = message + "Group Buy Updates\n"
        for item, val in gb_dict.items():
            message = message + f"{val} --> {item}\n"
    if ic_dict:
        message = message+"\nInterest Check Updates\n"
        for item, val in ic_dict.items():
            message = message + f'{val} --> {item}\n'
    print(message)

    # Splits the text message to a size of 1500 characters (1600 Twilio limit)
    if len(message) > 1500:
        tlist = message.split('\n')
        mlist = []
        tstring = ''
        for i in tlist:
            if ((len(tstring) + len(i) + len("\n")) < 1500):
                tstring = tstring + i + "\n"
                print(tstring)
            else:
                mlist.append(tstring)
                tstring = ''
                tstring = tstring + i + "\n"
    else:
        mlist = [message]

    return mlist

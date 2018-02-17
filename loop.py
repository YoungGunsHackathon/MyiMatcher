


def create_intro_msg(name):
    intro = "Hey, " + name + "!" + " I’m Myia and I’ll help you get the most out of this awesome event.<br/>"
    continuation = "Below I suggested a few people with common interests. I’ll be happy to introduce you whenever you want!"

    return intro + " " + continuation


def create_suggestion_msg(id, match_name, interest1, interest2, interest3, addition):
    msg_first = match_name + " shares these interests: \n<br/>" + " - " + interest1 + "\n<br/>" + " - " + interest2 + "\n<br/>" + " - " + interest3 + "<br/>"

    buttons = """Do you want to connect with your match?
            <div style="margin-top: 10px">
            <button style="background: #222 url('css/themes/dark/img/voteUp.svg') no-repeat center center;background-size:64px 64px;width:55px;height:55px;padding: 0;margin-right: 10px;display:inline-block" onclick="this.style.backgroundImage = 'url(css/themes/dark/img/voteUpSelected.svg)';angular.element(document.body).injector().get('xinClientService').getData('http:' +'//10.37.1.217:5000/respond/{0}/{1}', 'GET')"></button><button style="background: #222 url('css/themes/dark/img/voteDown.svg') no-repeat center center;background-size:64px 64px;width:55px;height:55px;padding: 0;margin-right: 10px;display:inline-block" onclick="this.style.backgroundImage = 'url(css/themes/dark/img/voteDownSelected.svg)';angular.element(document.body).injector().get('xinClientService').getData('etwas' , 'GET')"></button>
            </div>""".format(id, match_name)
    msg_cont = ""
    if (addition == 0):
        msg_cont = ""
    elif (addition == 1):
        msg_cont = "In addition, " + match_name + " is looking for new employees!\n<br/>"
    elif (addition == 2):
        msg_cont = "In addition, " + match_name + " is looking for a job!\n<br/>"
    elif (addition == 3):
        msg_cont = "In addition, " + match_name + " is looking for investment opportunities!\n<br/>"
    elif (addition == 4):
        msg_cont = "In addition, " + match_name + " is looking for investors!<br/>"


    return msg_first + '\n' + msg_cont + buttons

def connected():
    return 'Wow you are now connected with Josef!'

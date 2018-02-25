# colors
blackf = '\033[38;5;235m'
blackb = '\033[48;5;235m'
blackdb = '\033[49m'
purplef = '\033[38;5;140m'
purpleb = '\033[48;5;140m'
redf = '\033[38;5;1m'
redb = '\033[48;5;1m'
whitef = '\033[39m'
redf = '\033[31m'
yellowf = '\033[33m'
#----------------( ͡ᵔ ͜ʖ ͡ᵔ )-------------------
resetAllAttr = '\033[0m'
bold = '\033[1m'
blink = '\033[97;5m'
clearToEndl = '\033[K'
hideCursor = '\033[?25l'
restoreCursor = '\033[?25h \033[K \033[F'
carriageReturn = '\r'
cls_term = '\033c'

icons={'user':'', 'username':'', 'tomato':'', 'breaktime':'', 'alarm':'',\
       'sep1':'', 'sep2':'', 'reset':'', 'pause':'', 'play':'', 'warn':''}

def separator(bar):
    '''
        (bar: str) -> str
        returns a separator.
    '''
    def sep_attr(sep_colors, sep_icon):
        return bar.format(fg=sep_colors[0],
                          bg=sep_colors[1],
                          icon=sep_icon,
                          resetAll=resetAllAttr)
    return sep_attr

def powerline(text, block_colors, block_icon):
    '''
        (bar: str) -> str
        returns a separator.
    '''
    return separator('{fg}{bg} {icon} {text} {{fg}}{{bg}}{{icon}}{{resetAll}}'\
                     .format(fg=block_colors[0],
                             bg=block_colors[1],
                             icon=block_icon,
                             text=text))

def warning_msg(msg):
    '''
        (bar: str) -> str
        returns a separator.
    '''
    print('{b}{iconwarn}{reset}{yf} {msg}{reset}'\
            .format(b=blink,
                    iconwarn=icons['warn'],
                    yf=yellowf,
                    msg=msg,
                    reset=resetAllAttr))

def error_msg(msg, err=''):
    '''
        (msg: str, err: str) -> ()
        shows an error message.
    '''
    print('{b}{iconwarn}{reset}{rf} {msg} {err}{reset}'\
            .format(b=blink,
                    iconwarn=icons['warn'],
                    rf=redf,
                    msg=msg,
                    err=err,
                    reset=resetAllAttr))

def welcome_msg(email):
    '''
        (email: str) -> ()
        shows a powerline with the user email.
    '''
    print(cls_term, end='')
    print(hideCursor, end='')
    print(powerline('User', (whitef, blackb), icons['user'])
          ((blackf, redb), icons['sep2'])
          + powerline(email, (blackf, redb), icons['username'])
          ((redf, blackdb), icons['sep1']), flush=True)

def pomo_time_print(pomo_time, chron_status, chron_icon):
    '''
        (pomo_time: str, chron_status: str, chron_icon: str) -> ()
        shows a powerline with the pomo time.
    '''
    print('{cg}{ctl}'.format(cg=carriageReturn, ctl=clearToEndl)\
                            + powerline(pomo_time, (whitef, blackb), icons['tomato'])\
                            ((blackf, redb), icons['sep2'])\
                            + powerline(chron_status, (blackf, redb), chron_icon)\
                            ((redf, blackdb), icons['sep1']), flush=True, end='')

def break_time_print(break_time):
    '''
        (email: str) -> ()
        shows a powerline with the break time.
    '''
    print('{cg}{ctl}'.format(cg=carriageReturn, ctl=clearToEndl)\
                + powerline(break_time, (whitef, blackb), icons['breaktime'])\
                ((blackf, blackdb), icons['sep1']), flush=True, end='')

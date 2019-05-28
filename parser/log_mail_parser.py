import re
import os
dictofsuccess = {}                                             # словарь успешных отправлений
successid = {}                                                 # словарь метка об успешных отправлениях
falseid = {}                                                   # словарь метка об не успешных отправлениях
dictoffalse = {}                                               # словарь не успешных отправлений
user_sessionid = {}

def file_open():                                                # открываем файл на построчное чтение
    try:
        if not os.path.exists(file_name):
            raise FileNotFoundError
    except FileNotFoundError:
        print('Error: file does not exist')
    theFile = open(file_name, 'r')
    FILE = theFile.readlines()
    theFile.close()
    return FILE

def makefalse(fail):                                           # создает словарь не успешных сессий
    email = user_sessionid[fail]
    if email not in dictoffalse:
        dictoffalse[email] = 1
    else:
        dictoffalse[email]+=1
    return dictoffalse

def makesaccess(success):                                      # создает словарь успешных сессий
    email = user_sessionid[success]
    if email not in dictofsuccess:
        dictofsuccess[email]=1
    else:
         dictofsuccess[email] +=1
    return dictofsuccess

def output (data: dict, output_file: str):                      # Выводим результаты в CSV
    with open(output_file, 'w') as file:
        if not data :
            print('something going wrong: ')
            return
        for address, count in data.items():
            try:
                file.write(f'{address} {count}\n')
            except KeyError:
                file.write('KeyError: wrong data')

def log_mail_parser( ):                                         # функция парсера
    for line in file_open():

        session = re.compile('^.+:+\s([A-Z0-9]*):\s.*sasl_method=.*sasl_username=(.+@.+ru)')
        flag = re.compile('^.+:\s([A-Z0-9]+):\sremoved')
        success = re.compile('^.*:\s([A-Z0-9]+):\sto=.*status=([a-z]+)\s\W')
        mail_session =session.search(line)
        id_removedFlag = flag.search(line)
        mail_success = success.search(line)
        if mail_session:                                            # создает словарь с записями id: email
            user_sessionid[mail_session.group(1)] = mail_session.group(2)

        if id_removedFlag:                                          # удаляет из словарей запись если id был освобожден и проверяет были ли успешные отправки
            id_remove = id_removedFlag.group(1)
            if id_remove in user_sessionid:
                if id_remove in falseid:
                    if id_remove not in successid:                   # если успешных отправок небыло, тогда считаем ссесию не успешной
                        makefalse(id_remove)                         # создаем запись в словаре о неуспешной отправки письма
                    del falseid[id_remove]                           # трем метку не успешной доставки
                if id_remove in successid:
                    del successid[id_remove]                        # трем метку успешной доставки
                del user_sessionid[id_remove]                       # освобождаем id для возможности переиспользовать
        if mail_success and mail_success.group(2)=='sent':          # заполняем словарь успешных отправлений
            if mail_success.group(1) in user_sessionid:             # проверяет в словаре - связке и заносит в словарь успешных отправлений
                successid[mail_success.group(1)] = 1                # ставим метку что сообщение было успешное
                makesaccess(mail_success.group(1))                  # добавляем запись в словарь
        if mail_success and mail_success.group(2) !='sent':         # заполняем ставим метку в словарь неуспешных отправлений
            if mail_success.group(1) in user_sessionid:             # проверяет в словаре - связке и заносит в словарь успешных отправлений
               falseid [mail_success.group(1)]=1                    # ставим метку что у сессии есть неуспешное отправление
    return (dictofsuccess)

def main():
    log_mail_parser()
    output(dictofsuccess, 'saccess_emails.csv' )
    output(dictoffalse, 'false_emails.csv')

if __name__ == '__main__':
    file_name = 'maillog'
    main()

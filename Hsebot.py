import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#парсинг
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/daniilorlov/Desktop/hseparser-261610-88adc33b312d.json', scope)
client = gspread.authorize(creds)

creds1 = ServiceAccountCredentials.from_json_keyfile_name('/Users/daniilorlov/Desktop/hseparser-261610-88adc33b312d.json', scope)
client1 = gspread.authorize(creds)
client1 = client.open("parser")
client2 = client.open("parser2")
sheet = client.open("parser").sheet1
list_of_hashes = sheet.get_all_records()
#токен
bot = telebot.TeleBot('726955643:AAESfCS5XpI8o-7taqLmX7VLk75TmheuqlQ')
#клавиатуры для работы с ботом
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard3 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard4 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('2019', '2018')
keyboard1.row('2017', '2016')
keyboard1.row('2015', '2014')
keyboard1.row('2013', '2012')
keyboard1.row('2011', 'RESTART')
keyboard2.row('Бюджет', 'Внебюджет')
keyboard2.row('Назад')
keyboard3.row('Поиск по профессии')
keyboard3.row('Поиск по региону')
keyboard3.row('Назад')
keyboard4.row('10','30','100')
#ключи для работы с ботом
vez=[]
a = []
g = []
j = [0]
labels=[]
score_means=[]
prof=[]
#стартовая команда
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Приветствую тебя", reply_markup=keyboard1)
#основной код для бота
@bot.message_handler(content_types=['text'])

def send_text(message):
    try:
        #перезапускаем программу
        if message.text.lower() == 'restart':
            bot.send_message(message.chat.id, 'Перезагружаю программу...', reply_markup=keyboard1)
            bot.send_message(message.chat.id, 'Выберите год, который вас интересует: ', reply_markup=keyboard1)
        elif message.text.lower() == 'назад':
            bot.send_message(message.chat.id, 'Перемещаюсь назад...', reply_markup=keyboard1)
            bot.send_message(message.chat.id, 'Выберите год, который вас интересует: ', reply_markup=keyboard1)
        #выбираем год
        elif message.text.lower() == '2019' or message.text.lower() == '2018' or message.text.lower() == '2017' or message.text.lower() == '2016' or message.text.lower() == '2015' or message.text.lower() == '2014' or message.text.lower() == '2013' or message.text.lower() == '2012' or message.text.lower() == '2011':
            god=(2019-int(message.text))*2
            a.append(god)
            bot.send_message(message.chat.id, 'Выберите основу обучения: Бюджет/внебюджет', reply_markup=keyboard2)
            print(god)
        #выбираем форму обучения
        elif message.text.lower()=='бюджет':
            bot.send_message(message.chat.id, 'Вы выбрали основу обучения : Бюджет')
            g.append(32)
            bot.send_message(message.chat.id, 'Выберите по какому критерию будет осуществляться поиск: ', reply_markup=keyboard3)
        elif message.text.lower()=='внебюджет':
            bot.send_message(message.chat.id, 'Вы выбрали основу обучения : Внебюджет')
            g.append(33)
            bot.send_message(message.chat.id, 'Выберите по какому критерию будет осуществляться поиск: ', reply_markup=keyboard3)
        #выбираем по какому критерию будет проводиться поиск
        elif message.text.lower()=='поиск по профессии':
            prof.append(63)
            bot.send_message(message.chat.id, 'Вы выбрали поиск по профессии')
            bot.send_message(message.chat.id, 'Выберите профессию: ')
        elif message.text.lower()=='поиск по региону':
            prof.append(64)
            bot.send_message(message.chat.id, 'Вы выбрали поиск по региону')
            bot.send_message(message.chat.id, 'Выберите регион: ')
        #профессии/бюджет
        elif a[-1] >= 0 and a[-1]<=18 and prof[-1]==63 and g[-1]==32:
            message.text = message.text.upper()[0] + message.text.lower()[1:]
            worksheet = client2.get_worksheet(a[-1])
            list_of_lists1=worksheet.get_all_values()
            cnt=0
            for p in list_of_lists1:
                r = str(p[1])
                k = r.find(message.text)
                if k == 0 and cnt<=100:
                    cnt+=1
                    bot.send_message(message.chat.id, '/' + str(p[0]) + ' Название вуза: ' + str(p[2])+'\n'+'Специальность: ' +str(p[1]))
            if message.text[0]=='/':
                num=int(message.text[1:])+1
                bot.send_message(message.chat.id, 'Название Вуза: ' + list_of_lists1[num][2] +'\n'+'Специальность: ' +list_of_lists1[num][1]+ '\n'+'Качество приема на основании среднего балла ЕГЭ зачисленных на бюджетные места 2019: ' + (list_of_lists1[num][3])+ '\n' + 'Рост/падение: ' +list_of_lists1[num][4]+'\n'+'Количество студентов, зачисленных на бюджетные места: '+(list_of_lists1[num][5])+'\n'+'Из них: без экзаменов: '+(list_of_lists1[num][6])+'\n'+'Ср.балл рассчитан с вычетом баллов за И.Д.?: '+(list_of_lists1[num][7]))
        # профессии/внебюджет
        elif a[-1] >= 0 and a[-1]<=20 and prof[-1]==63 and g[-1]==33:
            cnt=0
            message.text = message.text.upper()[0] + message.text.lower()[1:]
            worksheet = client2.get_worksheet(a[-1]+1)
            list_of_lists1=worksheet.get_all_values()
            for p in list_of_lists1:
                r = str(p[1])
                k = r.find(message.text)
                if k == 0 and cnt<=10:
                    bot.send_message(message.chat.id, '/' + (str(p[0]) + ' Название вуза: ' + str(p[2])+'\n'+'Специальность: ' +str(p[1])))
                    cnt+=1

            if message.text[0]=='/':
                num=int(message.text[1:])+1
                bot.send_message(message.chat.id, 'Название Вуза: ' + list_of_lists1[num][2] +'\n'+'Специальность: ' +list_of_lists1[num][1]+ '\n'+'Качество приема на основании среднего балла ЕГЭ зачисленных на бюджетные места 2019: '+list_of_lists1[num][3]+ '\n' + 'Рост/падение: ' +(list_of_lists1[num][4])+'\n'+'Количество студентов, зачисленных на бюджетные места: '+(list_of_lists1[num][5])+'\n'+'Из них: без экзаменов: '+(list_of_lists1[num][6])+'\n'+'Ср.балл рассчитан с вычетом баллов за И.Д.?: '+(list_of_lists1[num][7]))
        # регион/бюджет
        elif a[-1] >= 0 and a[-1]<=18 and g[-1]==32 and prof[-1]==64:
            message.text = message.text.upper()[0] + message.text.lower()[1:]
            worksheet = client1.get_worksheet(a[-1])
            list_of_lists = worksheet.get_all_values()
            for i in list_of_lists:
                r = str(i[1])
                k = r.find(message.text)
                if k == 0:
                    bot.send_message(message.chat.id, '/'+(str(i[0]) + ' Название вуза: ' + str(i[1])))
            if message.text[0]=='/':
                num=int(message.text[1:])+1
                bot.send_message(message.chat.id, 'Название Вуза: ' + (list_of_lists[num][1])+  '\n' +'Качество приема на основании среднего балла ЕГЭ зачисленных на бюджетные места 2019: '+ (list_of_lists[num][2]) + '\n' + 'Рост/падение: ' + (list_of_lists[num][3]) + '\n' + 'Количество студентов, зачисленных на бюджетные места: ' + (list_of_lists[num][4]) + '\n' + 'Из них: без экзаменов: ' + (list_of_lists[num][5]) + '\n' + 'Ср.балл рассчитан с вычетом баллов за И.Д.?: ' + (list_of_lists[num][6]))
        # регион/внебюджет
        elif a[-1] >=0 and a[-1]<=20 and g[-1]==33 and prof[-1]==64 :
            message.text=message.text.upper()[0]+message.text.lower()[1:]
            worksheet = client1.get_worksheet(a[-1]+1)
            list_of_lists = worksheet.get_all_values()
            for i in list_of_lists:
                r = str(i[1])
                k = r.find(message.text)
                if k == 0:
                    bot.send_message(message.chat.id, '/'+(str(i[0]) + ' Название вуза: ' + str(i[1])))
            if message.text[0]=='/':
                num=int(message.text[1:])+1
                bot.send_message(message.chat.id,  'Название Вуза: ' + (list_of_lists[num][1]) + '\n' +'Качество приема на основании среднего балла ЕГЭ зачисленных на бюджетные места 2019: '+ (list_of_lists[num][2]) + '\n' + 'Рост/падение: ' + (list_of_lists[num][3]) + '\n' + 'Количество студентов, зачисленных на бюджетные места: ' + (list_of_lists[num][4]) + '\n' + 'Из них: без экзаменов: ' + (list_of_lists[num][5]) + '\n' + 'Ср.балл рассчитан с вычетом баллов за И.Д.?: ' + (list_of_lists[num][6]))
#ошибки при работе с ботом
    except ValueError:
        print('ValueError')
    except IndexError:
        print('IndexError')



bot.polling()

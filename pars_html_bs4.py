from bs4 import BeautifulSoup
import datetime


def pars_schedule(group):
    result = ''
    try:
        days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

        today_day = datetime.datetime.today()
        datetime.datetime(today_day.year, today_day.month, today_day.day)
        day_of_week = days_of_week[datetime.datetime.today().weekday()]

        with open(f"pasr_schedule/html_groups/{group}.html", encoding="utf-8") as load_html:
            src = load_html.read()

        counter_pairs = 0 # количество пар
        soup = BeautifulSoup(src, "lxml")
        all_pars = soup.find_all("div", class_="schedule-day")
        pars = None
        for i in all_pars:
            if i.find("div", class_="bold schedule-day__title").text.split()[0] == day_of_week:
                pars = i.find_all("div", class_="pair")

        lst = str(pars)[1:-1].split('<div class="pair">')[1:]

        for i in lst:
            data_small = BeautifulSoup(i, "lxml")
            item_shulde = BeautifulSoup(str(data_small.select('div[class="schedule-lesson"]')), "lxml")
            if str(item_shulde) == "<html><body><p>[]</p></body></html>":
                continue
            counter_pairs += 1
            time = data_small.find("div", class_="time").text
            place = ', '.join([i[i.index(">")+1:-7] if i[i.index(">")+1:-7][1] != 'a' else f"{BeautifulSoup(i[i.index('>')+1:-7], 'lxml').text}, {i[i.index('>')+1:-7][i[i.index('>')+1:-7].index('href')+6:i[i.index('>')+1:-7].index(' target')-1]}" for i in str(item_shulde.find_all("div", "schedule-auditory")).split(', ')])
            subject = item_shulde.find("div", class_="bold small").text
            teacher = item_shulde.find("div", class_="teacher").text
            if place.split(', ')[0] not in ['🏠 Обучение LMS', '📷 Webinar']:
                result += f"{time}\n{place}\n{subject}\n{teacher}\n\n"
            else:
                place = place.split(', ')
                online_place = f"<a href='{place[1]}'>{place[0]}</a>"
                result += f"{time}\n{online_place}\n{subject}\n{teacher}\n\n"
        if counter_pairs == 0:
            return "Сегодня пар нет"
        return result
    except:
        return "Не нашлось расписание для данной группы на сегодня"

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# 1) Вычислите общую выручку за июль 2021 по тем сделкам, приход денежных средств которых не просрочен.

# Загрузка данных из Excel файла
data = pd.read_excel('data.xlsx')

# Преобразование столбца 'receiving_date' в формат datetime
data['receiving_date'] = pd.to_datetime(data['receiving_date'], format='%d.%m.%Y', errors='coerce')

# Удаление строк с отсутствующими датами
data = data.dropna(subset=['receiving_date'])

# Фильтрация данных для июля 2021 года и не просроченных сделок
july_data = data[(data['receiving_date'].dt.month == 7) & (data['receiving_date'].dt.year == 2021) & (data['status'] != 'ПРОСРОЧЕНО')]

# Расчет общей выручки
total_revenue_july = july_data['sum'].sum()
print(f"Общая выручка за июль 2021: {total_revenue_july}")

# 2) Как изменялась выручка компании за рассматриваемый период? Проиллюстрируйте графиком.

# Группировка данных по месяцам и расчет суммарной выручки
monthly_revenue = data.groupby(data['receiving_date'].dt.to_period('M'))['sum'].sum()

# Построение графика
plt.figure(figsize=(10, 6))
monthly_revenue.plot(kind='bar')
plt.title('Изменение выручки компании по месяцам')
plt.xlabel('Месяц')
plt.ylabel('Выручка')
plt.show()

# 3) Кто из менеджеров привлек для компании больше всего денежных средств в сентябре 2021?

# Фильтрация данных для сентября 2021 года
september_data = data[(data['receiving_date'].dt.month == 9) & (data['receiving_date'].dt.year == 2021)]

# Группировка данных по менеджерам и расчет суммарной выручки
revenue_by_manager = september_data.groupby('sale')['sum'].sum()

# Определение лучшего менеджера
top_manager = revenue_by_manager.idxmax()
top_revenue = revenue_by_manager.max()
print(f"Менеджер, привлекший больше всего денежных средств в сентябре 2021: {top_manager} - {top_revenue}")

# 4) Какой тип сделок (новая/текущая) был преобладающим в октябре 2021?

# Фильтрация данных для октября 2021 года
october_data = data[(data['receiving_date'].dt.month == 10) & (data['receiving_date'].dt.year == 2021)]

# Подсчет количества сделок каждого типа
deal_types = october_data['new/current'].value_counts()

# Определение преобладающего типа сделок
dominant_deal_type = deal_types.idxmax()
print(f"Преобладающий тип сделок в октябре 2021: {dominant_deal_type}")

# 5) Сколько оригиналов договора по майским сделкам было получено в июне 2021?

# Фильтрация данных для июня 2021 года
may_deals_june_received = data[
    (data['receiving_date'].dt.month == 6) &
    (data['receiving_date'].dt.year == 2021)
]

# Подсчет количества оригиналов договоров
count_may_deals_june_received = may_deals_june_received['document'].value_counts().get('оригинал', 0)

print(f"Количество оригиналов договоров по майским сделкам, полученных в июне 2021: {count_may_deals_june_received}")

# Задание

# Функция для расчета бонусов
def calculate_bonus(row):
    if row['new/current'] == 'новая' and row['status'] == 'ОПЛАЧЕНО' and row['document'] == 'оригинал':
        return row['sum'] * 0.07
    elif row['new/current'] == 'текущая' and row['status'] != 'ПРОСРОЧЕНО' and row['document'] == 'оригинал':
        if row['sum'] > 10000:
            return row['sum'] * 0.05
        else:
            return row['sum'] * 0.03
    return 0

# Применение функции расчета бонусов к каждой строке данных
data['bonus'] = data.apply(calculate_bonus, axis=1)

# Преобразование столбца 'receiving_date' в формат datetime (если это еще не сделано)
data['receiving_date'] = pd.to_datetime(data['receiving_date'])

# Фильтрация данных до 1 июля 2021 года и расчет суммы бонусов для каждого менеджера
july_bonus = data[data['receiving_date'] < '2021-07-01'].groupby('sale')['bonus'].sum()

print("Остаток бонусов на 01.07.2021:")
print(july_bonus)

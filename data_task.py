import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# 1) Вычислите общую выручку за июль 2021 по тем сделкам, приход денежных
# средств которых не просрочен.
data = pd.read_excel('data.xlsx')

data['receiving_date'] = pd.to_datetime(data['receiving_date'], format='%d.%m.%Y', errors='coerce')

data = data.dropna(subset=['receiving_date'])

july_data = data[(data['receiving_date'].dt.month == 7) & (data['receiving_date'].dt.year == 2021) & (data['status'] != 'ПРОСРОЧЕНО')]

total_revenue_july = july_data['sum'].sum()
print(f"Общая выручка за июль 2021: {total_revenue_july}")

# 2) Как изменялась выручка компании за рассматриваемый период? Проиллюстрируйте графиком.

monthly_revenue = data.groupby(data['receiving_date'].dt.to_period('M'))['sum'].sum()

plt.figure(figsize=(10, 6))
monthly_revenue.plot(kind='bar')
plt.title('Изменение выручки компании по месяцам')
plt.xlabel('Месяц')
plt.ylabel('Выручка')
plt.show()

# 3) Кто из менеджеров привлек для компании больше всего денежных средств в сентябре 2021?

september_data = data[(data['receiving_date'].dt.month == 9) & (data['receiving_date'].dt.year == 2021)]

revenue_by_manager = september_data.groupby('sale')['sum'].sum()

top_manager = revenue_by_manager.idxmax()
top_revenue = revenue_by_manager.max()
print(f"Менеджер, привлекший больше всего денежных средств в сентябре 2021: {top_manager} - {top_revenue}")

# 4) Какой тип сделок (новая/текущая) был преобладающим в октябре 2021?

october_data = data[(data['receiving_date'].dt.month == 10) & (data['receiving_date'].dt.year == 2021)]

deal_types = october_data['new/current'].value_counts()

dominant_deal_type = deal_types.idxmax()
print(f"Преобладающий тип сделок в октябре 2021: {dominant_deal_type}")

# 5) Сколько оригиналов договора по майским сделкам было получено в июне 2021?

may_deals_june_received = data[
    (data['receiving_date'].dt.month == 6) &
    (data['receiving_date'].dt.year == 2021)
]

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

data['bonus'] = data.apply(calculate_bonus, axis=1)

data['receiving_date'] = pd.to_datetime(data['receiving_date'])
july_bonus = data[data['receiving_date'] < '2021-07-01'].groupby('sale')['bonus'].sum()

print("Остаток бонусов на 01.07.2021:")
print(july_bonus)

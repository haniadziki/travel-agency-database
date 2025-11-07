--Znajdź najpopularniejsze rodzaje wycieczek, porównaj koszta i zyski, czy są opłacalne?

WITH 
PopTrips AS (
        SELECT offers.offer_id, COUNT(orders.order_id) AS number_of_orders,
        SUM(offers.overall_price) AS total 
        FROM orders 
        JOIN offers ON offers.offer_id = orders.offer_id 
        GROUP BY orders.offer_id
    ),

OfferCosts AS (
    SELECT offer_id, 
    plane_price + attractions_price + hotel_price AS total_cost 
    FROM offers
),

Profit AS (
    SELECT PopTrips.offer_id, 
    PopTrips.number_of_orders, 
    PopTrips.total, 
    OfferCosts.total_cost,
    (PopTrips.total - OfferCosts.total_cost) AS profit,
    offers.hotel_name
    FROM PopTrips 
    JOIN OfferCosts ON PopTrips.offer_id = OfferCosts.offer_id
    JOIN offers ON PopTrips.offer_id = offers.offer_id
)

SELECT 
    Profit.offer_id,
    Profit.number_of_orders,
    Profit.total,
    Profit.total_cost,
    Profit.profit,
    Profit.hotel_name,
    CASE 
        WHEN Profit.profit > 0 THEN 'Profitable'
        ELSE 'Not Profitable'
    END AS profitability
FROM Profit 
ORDER BY Profit.number_of_orders DESC;

--Znajdź liczbę obsłużonych klientów w każdym miesiącu działalności firmy, czy firma rośnie, czy podupada?

SELECT MONTH(order_date) AS month, COUNT(DISTINCT customer_id) AS number_of_customers
FROM orders
GROUP BY month
ORDER BY month;

--Sprawdź, po których wycieczkach klienci wracają na kolejne, a po których mają dość i więcej ich nie widzicie. Czy są takie, które być może powinny zniknąć z oferty?

WITH ranked_orders AS (
    SELECT 
        customer_id, 
        offer_id, 
        LEAD(trip_end) OVER (PARTITION BY customer_id ORDER BY trip_end) AS next_trip_end
    FROM orders
)
SELECT 
    offer_id, 
    ROUND(SUM(next_trip_end IS NOT NULL) * 100.0 / COUNT(*), 2) AS succes_rate

FROM ranked_orders
GROUP BY offer_id ORDER BY succes_rate DESC;

--Sporządź wykres odwiedzalności krajów i miast. Do którego kraju firma powinna zwiekszyć liczbę wycieczek.

SELECT country.country_id AS country_id, country.country AS country_name, COUNT(DISTINCT orders.customer_id) AS number_of_customers
FROM orders
JOIN offers ON orders.offer_id = offers.offer_id
JOIN city ON offers.city_id = city.city_id
JOIN country ON city.country_id = country.country_id
GROUP BY country_name
ORDER BY number_of_customers DESC;

SELECT offers.city_id AS city_id, city.city AS city_name, COUNT(DISTINCT customer_id) AS number_of_customers
FROM orders
JOIN offers ON orders.offer_id = offers.offer_id
JOIN city ON offers.city_id = city.city_id
GROUP BY city_id
ORDER BY city_name;

--Która sieć hoteli ma najwiekszy zysk, a która najmniejszy. Z którym hotelem firma powinna rozwiązać kontrakt.

WITH 
    HotelProfits AS (
        SELECT offers.hotel_name, 
               COUNT(DISTINCT orders.offer_id) AS number_of_trips, -- Liczba wycieczek
               SUM(offers.overall_price) AS total_revenue,
               SUM(offers.plane_price + offers.attractions_price + offers.hotel_price) AS total_cost,
               (SUM(offers.overall_price) - SUM(offers.plane_price + offers.attractions_price + offers.hotel_price)) AS profit
        FROM orders 
        JOIN offers ON orders.offer_id = offers.offer_id 
        GROUP BY offers.hotel_name
    ),

    RankedProfits AS (
        SELECT hotel_name, number_of_trips, total_revenue, total_cost, profit,
               RANK() OVER (ORDER BY profit DESC) AS profit_rank_desc,
               RANK() OVER (ORDER BY profit ASC) AS profit_rank_asc
        FROM HotelProfits
    )

    SELECT 
        hp.hotel_name AS hotel_with_highest_profit,
        hp.profit AS highest_profit,
        hp.number_of_trips AS highest_profit_trips, -- Liczba wycieczek dla hotelu z najwyższym zyskiem
        lp.hotel_name AS hotel_with_lowest_profit,
        lp.profit AS lowest_profit,
        lp.number_of_trips AS lowest_profit_trips -- Liczba wycieczek dla hotelu z najniższym zyskiem
    FROM (SELECT * FROM RankedProfits WHERE profit_rank_desc = 1) hp
    JOIN (SELECT * FROM RankedProfits WHERE profit_rank_asc = 1) lp;

--Ktory pracownik najlepiej zarobił dla firmy, a który najgorzej.

SELECT 
        staff_id, 
        SUM(finance.balance) AS total_profit
    FROM 
        orders
    JOIN 
        finance ON orders.offer_id = finance.offer_id
    GROUP BY 
        staff_id
    ORDER BY 
        total_profit DESC;

--Znajdź klienta, który wydał w firmie najwięcej. Wypisz 10 najbardziej zasłużonych klientów, aby przydzielić im rabat 5%.

SELECT customer_id, SUM(overall_price) AS total_spent
    FROM orders 
    JOIN offers ON orders.offer_id = offers.offer_id
    GROUP BY customer_id
    ORDER BY total_spent DESC
    LIMIT 10;

--Jak zarabia firma w każdym miesiącu 
SELECT YEAR(order_date) AS year, MONTH(order_date) AS month, SUM(balance) AS monthly_revenue
FROM orders 
JOIN offers ON orders.offer_id = offers.offer_id 
JOIN finance ON offers.offer_id = finance.offer_id
GROUP BY year, month
ORDER BY year, month;
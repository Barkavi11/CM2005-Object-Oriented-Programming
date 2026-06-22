#include "OrderBook.h"
#include "CSVReader.h"
#include <map>
#include <algorithm>
#include <iostream>

OrderBook::OrderBook(std::string filename)
{
    orders = CSVReader::readCSV(filename);
}

std::vector<std::string> OrderBook::getKnownProducts()
{
    std::vector<std::string> products;
    std::map<std::string,bool> prodMap;

    for (OrderBookEntry& e : orders)
    {
        prodMap[e.product] = true;
    }

    for (auto const& e : prodMap)
    {
        products.push_back(e.first);
    }

    return products;
}

std::vector<OrderBookEntry> OrderBook::getOrders(OrderBookType type,
                                                 std::string product,
                                                 std::string timestamp)
{
    std::vector<OrderBookEntry> orders_sub;
    for (OrderBookEntry& e : orders)
    {
        if (e.orderType == type &&
            e.product == product &&
            e.timestamp == timestamp)
        {
            orders_sub.push_back(e);
        }
    }
    return orders_sub;
}

std::vector<OrderBookEntry> OrderBook::getOrdersByProductType(OrderBookType type,
                                                              std::string product)
{
    std::vector<OrderBookEntry> filtered;

    for (OrderBookEntry& e : orders)
    {
        if (e.orderType == type && e.product == product)
        {
            filtered.push_back(e);
        }
    }

    return filtered;
}

std::vector<OrderBookEntry> OrderBook::getOrdersByProductTypeDateRange(OrderBookType type,
                                                                       std::string product,
                                                                       std::string startDate,
                                                                       std::string endDate)
{
    std::vector<OrderBookEntry> filtered;

    for (OrderBookEntry& e : orders)
    {
        std::string date = getDate(e.timestamp);

        if (e.orderType == type &&
            e.product == product &&
            date >= startDate &&
            date <= endDate)
        {
            filtered.push_back(e);
        }
    }

    return filtered;
}

std::string OrderBook::getDate(std::string timestamp)
{
    return timestamp.substr(0, 10);
}

std::vector<OHLCEntry> OrderBook::getOHLC(std::string product, OrderBookType type)
{
    std::vector<OrderBookEntry> filtered = getOrdersByProductType(type, product);
    std::vector<OHLCEntry> result;

    if (filtered.size() == 0)
    {
        return result;
    }

    std::string currentDate = getDate(filtered[0].timestamp);
    double open = filtered[0].price;
    double high = filtered[0].price;
    double low = filtered[0].price;
    double close = filtered[0].price;

    for (unsigned int i = 1; i < filtered.size(); ++i)
    {
        std::string rowDate = getDate(filtered[i].timestamp);

        if (rowDate == currentDate)
        {
            if (filtered[i].price > high)
            {
                high = filtered[i].price;
            }

            if (filtered[i].price < low)
            {
                low = filtered[i].price;
            }

            close = filtered[i].price;
        }
        else
        {
            result.push_back(OHLCEntry(currentDate, open, high, low, close));

            currentDate = rowDate;
            open = filtered[i].price;
            high = filtered[i].price;
            low = filtered[i].price;
            close = filtered[i].price;
        }
    }

    result.push_back(OHLCEntry(currentDate, open, high, low, close));

    return result;
}

std::vector<OHLCEntry> OrderBook::getOHLC(std::string product,
                                          OrderBookType type,
                                          std::string startDate,
                                          std::string endDate)
{
    std::vector<OrderBookEntry> filtered = getOrdersByProductTypeDateRange(type, product, startDate, endDate);
    std::vector<OHLCEntry> result;

    if (filtered.size() == 0)
    {
        return result;
    }

    std::string currentDate = getDate(filtered[0].timestamp);
    double open = filtered[0].price;
    double high = filtered[0].price;
    double low = filtered[0].price;
    double close = filtered[0].price;

    for (unsigned int i = 1; i < filtered.size(); ++i)
    {
        std::string rowDate = getDate(filtered[i].timestamp);

        if (rowDate == currentDate)
        {
            if (filtered[i].price > high)
            {
                high = filtered[i].price;
            }

            if (filtered[i].price < low)
            {
                low = filtered[i].price;
            }

            close = filtered[i].price;
        }
        else
        {
            result.push_back(OHLCEntry(currentDate, open, high, low, close));

            currentDate = rowDate;
            open = filtered[i].price;
            high = filtered[i].price;
            low = filtered[i].price;
            close = filtered[i].price;
        }
    }

    result.push_back(OHLCEntry(currentDate, open, high, low, close));

    return result;
}

double OrderBook::getHighPrice(std::vector<OrderBookEntry>& orders)
{
    double max = orders[0].price;
    for (OrderBookEntry& e : orders)
    {
        if (e.price > max) max = e.price;
    }
    return max;
}

double OrderBook::getLowPrice(std::vector<OrderBookEntry>& orders)
{
    double min = orders[0].price;
    for (OrderBookEntry& e : orders)
    {
        if (e.price < min) min = e.price;
    }
    return min;
}

std::string OrderBook::getEarliestTime()
{
    return orders[0].timestamp;
}

std::string OrderBook::getNextTime(std::string timestamp)
{
    std::string next_timestamp = "";
    for (OrderBookEntry& e : orders)
    {
        if (e.timestamp > timestamp)
        {
            next_timestamp = e.timestamp;
            break;
        }
    }
    if (next_timestamp == "")
    {
        next_timestamp = orders[0].timestamp;
    }
    return next_timestamp;
}

void OrderBook::insertOrder(OrderBookEntry& order)
{
    orders.push_back(order);
    std::sort(orders.begin(), orders.end(), OrderBookEntry::compareByTimestamp);
}

std::vector<OrderBookEntry> OrderBook::matchAsksToBids(std::string product, std::string timestamp)
{
    std::vector<OrderBookEntry> asks = getOrders(OrderBookType::ask, product, timestamp);
    std::vector<OrderBookEntry> bids = getOrders(OrderBookType::bid, product, timestamp);

    std::vector<OrderBookEntry> sales;

    if (asks.size() == 0 || bids.size() == 0)
    {
        std::cout << " OrderBook::matchAsksToBids no bids or asks" << std::endl;
        return sales;
    }

    std::sort(asks.begin(), asks.end(), OrderBookEntry::compareByPriceAsc);
    std::sort(bids.begin(), bids.end(), OrderBookEntry::compareByPriceDesc);

    std::cout << "max ask " << asks[asks.size()-1].price << std::endl;
    std::cout << "min ask " << asks[0].price << std::endl;
    std::cout << "max bid " << bids[0].price << std::endl;
    std::cout << "min bid " << bids[bids.size()-1].price << std::endl;

    for (OrderBookEntry& ask : asks)
    {
        for (OrderBookEntry& bid : bids)
        {
            if (bid.price >= ask.price)
            {
                OrderBookEntry sale{ask.price, 0, timestamp,
                    product,
                    OrderBookType::asksale};

                if (bid.username == "simuser")
                {
                    sale.username = "simuser";
                    sale.orderType = OrderBookType::bidsale;
                }
                if (ask.username == "simuser")
                {
                    sale.username = "simuser";
                    sale.orderType = OrderBookType::asksale;
                }

                if (bid.amount == ask.amount)
                {
                    sale.amount = ask.amount;
                    sales.push_back(sale);
                    bid.amount = 0;
                    break;
                }

                if (bid.amount > ask.amount)
                {
                    sale.amount = ask.amount;
                    sales.push_back(sale);
                    bid.amount = bid.amount - ask.amount;
                    break;
                }

                if (bid.amount < ask.amount &&
                    bid.amount > 0)
                {
                    sale.amount = bid.amount;
                    sales.push_back(sale);
                    ask.amount = ask.amount - bid.amount;
                    bid.amount = 0;
                    continue;
                }
            }
        }
    }
    return sales;
}
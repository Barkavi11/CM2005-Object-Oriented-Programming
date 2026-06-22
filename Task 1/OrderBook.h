#pragma once
#include "OrderBookEntry.h"
#include "CSVReader.h"
#include "OHLCEntry.h"
#include <string>
#include <vector>

class OrderBook
{
    public:
        OrderBook(std::string filename);

        std::vector<std::string> getKnownProducts();

        std::vector<OrderBookEntry> getOrders(OrderBookType type,
                                              std::string product,
                                              std::string timestamp);

        std::vector<OrderBookEntry> getOrdersByProductType(OrderBookType type,
                                                           std::string product);

        std::vector<OrderBookEntry> getOrdersByProductTypeDateRange(OrderBookType type,
                                                                    std::string product,
                                                                    std::string startDate,
                                                                    std::string endDate);

        std::vector<OHLCEntry> getOHLC(std::string product, OrderBookType type);

        std::vector<OHLCEntry> getOHLC(std::string product,
                                       OrderBookType type,
                                       std::string startDate,
                                       std::string endDate);

        static std::string getDate(std::string timestamp);

        std::string getEarliestTime();

        std::string getNextTime(std::string timestamp);

        void insertOrder(OrderBookEntry& order);

        std::vector<OrderBookEntry> matchAsksToBids(std::string product, std::string timestamp);

        static double getHighPrice(std::vector<OrderBookEntry>& orders);
        static double getLowPrice(std::vector<OrderBookEntry>& orders);

    private:
        std::vector<OrderBookEntry> orders;
};
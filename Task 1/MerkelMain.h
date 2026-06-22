#pragma once

#include <vector>
#include "OrderBookEntry.h"
#include "OrderBook.h"
#include "Wallet.h"
#include "OHLCEntry.h"

class MerkelMain
{
    public:
        MerkelMain();
        void init();

    private:
        void printMenu();
        void printHelp();
        void printMarketStats();
        void enterAsk();
        void enterBid();
        void printWallet();
        void gotoNextTimeframe();
        void printOHLCData();
        void printOHLCVector(std::vector<OHLCEntry>& ohlc);

        int getUserOption();
        void processUserOption(int userOption);

        std::string currentTime;

        OrderBook orderBook{"20200601.csv"};
        Wallet wallet;
};
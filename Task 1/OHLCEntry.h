#pragma once
#include <string>

class OHLCEntry
{
public:
    OHLCEntry(std::string _date,
              double _open,
              double _high,
              double _low,
              double _close);

    std::string date;
    double open;
    double high;
    double low;
    double close;
};
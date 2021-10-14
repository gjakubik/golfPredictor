#!/bin/sh

if [ $# -ne 2 ]; then
    echo "Usage: $0 START_YEAR END_YEAR";
    exit 1;
fi;

start=$1
end=$2

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path/scraper"

for year in `seq $start $end`; do
    echo "Fetching Data for year: $year"
    scrapy crawl pga_stats -a year=$year 2> /dev/null
done;

echo "Combining Data"
./combiner.py data 2&> /dev/null

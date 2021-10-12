import scrapy


DEFAULT_YEAR = 2020


class PgaStatsSpider(scrapy.Spider):
    """Spider used to collect each of the html pages containing PGA tour stats"""

    name = 'pga_stats'
    allowed_domains = ['pgatour.com']
    start_urls = ['http://pgatour.com/stats/']

    def __init__(self, year=DEFAULT_YEAR, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.year = int(year)

    def parse(self, response):
        links = response.xpath(
            "*//ul[contains(@class, 'nav-tabs-drop')]/li/a[not(@data-toggle)]/@href")[1:8]  # exclude the first and last url as those don't matter

        for link in links:
            stats_page = link.get()
            print("stats_page: ", stats_page)
            yield response.follow(stats_page, callback=self.parse_stats)

        # parse next year's OWGR once
        yield response.follow(f'/stats/stat.186.y{self.year + 1}.html', callback=self.parse_stats_table)

    def parse_stats(self, response):
        relevant_links = set([f"/stats/stat.{stat_num}.html" for stat_num in [
            '02675',
            '02564',
            '02674',
            '02568',
            '02569'
        ]])

        links = response.xpath("*//div[contains(@class, 'table-content')]//a/@href") 

        for link in links:
            if link.get() not in relevant_links:
                continue

            stats_table = link.get()[:-5] + f".y{self.year}.html"
            yield response.follow(stats_table, callback=self.parse_stats_table)

    def parse_stats_table(self, response):
        pga_stats = {}

        pga_stats['stat_group'] = response.xpath(
            "*//ul[contains(@class, 'nav-tabs-drop')]//li[@class='active']/a/text()").get()

        pga_stats['stat_name'] = response.xpath(
            "*//div[@class='header']/h1/text()").get()

        pga_stats['stat_table'] = response.xpath("*//table[@id='statsTable']").get()

        pga_stats['year'] = self.year

        yield pga_stats


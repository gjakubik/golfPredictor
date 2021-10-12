import scrapy


DEFAULT_YEAR = 2020


class PgaStatsSpider(scrapy.Spider):
    """Spider used to collect each of the html pages containing PGA tour stats"""

    name = 'pga_stats'
    allowed_domains = ['pgatour.com']
    start_urls = ['http://pgatour.com/stats/']

    def __init__(self, year=DEFAULT_YEAR, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.year = year

    def parse(self, response):
        links = response.xpath(
            "*//ul[contains(@class, 'nav-tabs-drop')]/li/a[not(@data-toggle)]/@href")[1:8]  # exclude the first and last url as those don't matter

        for link in links:
            stats_page = link.get()
            yield response.follow(stats_page, callback=self.parse_stats)

    def parse_stats(self, response):
        relevant_links = set([f"/stats/stat.{stat_num}.html" for stat_num in [
            '02675',
            '02564',
            '02674',
            '02568',
            '02569',
            '186'
        ]])

        links = [
            link.get() for link in response.xpath("*//div[contains(@class, 'table-content')]//a/@href")
            if link.get() in relevant_links
        ]

        # add OWGR
        links += '/stats/stat.186.html'

        for link in links:
            stats_table = link[:-5] + f".y{self.year}.html"
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


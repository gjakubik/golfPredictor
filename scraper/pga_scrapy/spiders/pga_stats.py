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
        links = [f"/stats/stat.{stat_num}.y{self.year}.html" for stat_num in [
            "02674",    # SG_TeeToGreen (SG_OffTheTee, SG_Approach, SG_Around), Measured Rounds
            "02564",    # SG_Putting
            "130",      # Scrambling_%,
            "120",      # Adjusted_Scoring_Avg
            "102",      # Driving_Acc_% (> some threshold of rounds)
            "103",      # GIR_%
            "101",      # Avg_Driving_Dist
            "138",      # Top_10s
        ]]

        for link in links:
            yield response.follow(link, callback=self.parse_stats_table)

        # OWGR - avg_points
        years = [self.year, self.year+1, self.year+2]
        for year in years:
            yield response.follow(f'/stats/stat.186.y{year}.html', callback=self.parse_stats_table)

    def parse_stats_table(self, response):
        pga_stats = {
            'year': self.year,
            'stat_group': response.xpath("*//ul[contains(@class, 'nav-tabs-drop')]//li[@class='active']/a/text()").get(),
            'stat_name': response.xpath("*//div[@class='header']/h1/text()").get(),
            'stat_table': response.xpath("*//table[@id='statsTable']").get()
        }

        # special case for owgr (since we grab both current and next year)
        if 'stat.186.y' in response.url:
            pga_stats['owgr_year'] = int(response.url.split('stat.186.y')[1][:4])

        yield pga_stats


import scrapy;
 
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://dichvucong.danang.gov.vn/dich-vu-cong?p_p_id=dichvucong_WAR_dngdvcportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=0&_dichvucong_WAR_dngdvcportlet_javax.portlet.action=loadDanhSachDichVuCong&_dichvucong_WAR_dngdvcportlet_jspPage=%2Fhtml%2Fdichvucongtructuyen%2Fdanhsachdichvucong.jsp&email=default%40liferay.com&tenDichVuCong=&idCoQuan=0&maLinhVuc=&mucDo=-1&href=https%3A%2F%2Fdichvucong.danang.gov.vn%2Fdich-vu-cong&noiBo=0&nhomId=0&count=0",
    ]
 
    def parse(self, response):
        links = response.css("li div div.tb-td-3 a::attr(href)")
        if len(links) > 0:
            current_url = str(response.request.url);
            print(current_url);
            params = current_url.split("&");
            for i, param in params:
                if "count=" not in param:
                    continue;
                (_, count) = param.split("=");
                params[i] = "count=" + (int(count) + 1);
            next_url = "&".join(params);
            return response.follow(next_url, callback=self.parse);
        for link in links:
            return response.follow(link, callback=self.parse_doc);
 
    # TODO: crawl each page
    def parse_doc(self, response):
        print(response.request.url);
        
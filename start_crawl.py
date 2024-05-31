import csv
import scrapy;
from bs4 import BeautifulSoup;
 
file_name = str.maketrans(
    r'\/:*?"<>| ',
    r'__________'
)
 
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://dichvucong.danang.gov.vn/dich-vu-cong?p_p_id=dichvucong_WAR_dngdvcportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=0&_dichvucong_WAR_dngdvcportlet_javax.portlet.action=loadDanhSachDichVuCong&_dichvucong_WAR_dngdvcportlet_jspPage=%2Fhtml%2Fdichvucongtructuyen%2Fdanhsachdichvucong.jsp&email=default%40liferay.com&tenDichVuCong=&idCoQuan=1210&maLinhVuc=&mucDo=-1&href=https%3A%2F%2Fdichvucong.danang.gov.vn%2Fdich-vu-cong&noiBo=0&nhomId=0&count=0",
    ]
    def parse(self, response):
        yield ["Thủ tục", "Mã thủ tục", "Lĩnh vực", "Thông tin công bố", "Cách thức nộp trực tuyến", "Thời hạn giải quyết", "Mức trực tuyến", "Lệ phí", "Phí", "Văn bản quy định lệ phí", "Cơ quan thực hiện", "Cơ quan có thẩm quyền quyết định", "Đối tượng thực hiện", "Cách thức thực hiện", "Điều kiện thực hiện", "Số bộ hồ sơ", "Kết quả thực hiện", "Địa chỉ tiếp nhận hồ sơ", "Mẫu đơn, tờ khai", "Trình tự thực hiện", "Căn cứ pháp lý", "Tình trạng hiệu lực", ];
        links = response.css("li div div.tb-td-3 a::attr(href)").getall();
        if len(links) > 0:
            current_url = str(response.request.url);
            params = current_url.split("&");
            [count_index, *_] = [i for i in range(len(params)) if params[i].split("=")[0] == "count" ]
            count = params[count_index];
            count_value = count.replace("count=", "");
            new_count = "count=" + str(int(count_value) + 6);
            params[count_index] = new_count;
            [_, count_value] = count.split("=")
            next_url = "&".join(params);
            yield response.follow(next_url, callback=self.parse);
        
        for link in links:
            yield response.follow(link, callback=self.parse_doc);
 
    def parse_doc(self, response):
        title: str = response.css("h2.tieude-h2::text").get().replace("/", " __ ");
        row_subject = response.css("table.table > tbody > tr > td.td-1::text").getall();
        row_content = response.css("table.table > tbody > tr > td:not(.td-1)").getall();
        row_count = max(len(row_subject), len(row_content));

        value = [BeautifulSoup(row, "html5lib").get_text() for row in row_content];
        data = dict(zip(row_subject, value));

        yield {"title": title, **data};
        
        # with open("./docs/" + title.translate(file_name)[:250] + '.csv', 'w+', newline='', encoding="utf-8") as file:
        #     writer = csv.writer(file, delimiter=',')
        #     for i in range(row_count):
        #         soup = BeautifulSoup(row_content[i], "html5lib");
        #         data = [row_subject[i], soup.get_text()];
        #         writer.writerow(data);
        
- export FLASK_APP=flaskr
- export FLASK_ENV=development
- flask run

- crawl data:
	+ xpath
	+ tính số kích thước chỉ mục
- tách từ:
	+ build lại solr
	+ Override lớp tách từ.


- report:
 + thu thập:
   - chu trình thu thập -> chính sách lưu tài liệu gốc -> tách nội dung văn bản (xpath) -> phạm vi thu thập (domain)
   - vận hành tự động hóa
 + tìm kiếm:
   - cấu trúc văn bản (các trường). các kĩ thuật phân tích văn bản (tách từ, lọc từ dừng, filtering).
   - ngôn ngữ truy vấn (api solr: khai thác các api nào ( ký tự đại diện, truy vấn câu, tìm kiếm trên trường nào)
   - mô hình xếp hạng: solr (vector và bm25)
   - phần thêm: lịch sử tìm kiếm (phân tích)
 + giao diện tìm kiếm:
  -  tự thiết kế các thông tin: số lượng kết quả, thời gian truy vấn 
  - phân trang 
  - khuyến khích xây dựng 2 giao diện: tìm kiếm tự do (chỉ có 1 trường ô nhập tìm kiếm) và nâng cao (bán cấu trúc: có nhiều ô nhập truy vấn, cho phép người dùng chọn luật and, or)

 + ngày bảo vệ: thiết lập hệ thống tìm kiếm cho mọi người có thể dùng thử. triển khai localhost 0.0.0.0. wifi thầy cung cấp không có internet.


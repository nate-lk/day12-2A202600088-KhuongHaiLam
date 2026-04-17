# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Bài tập 1.1: Các lỗi thiết kế (Anti-patterns) tìm thấy
1. **Hardcode thông tin nhạy cảm:** Các mã khóa API (`OPENAI_API_KEY`) và URL cơ sở dữ liệu (`DATABASE_URL`) được viết trực tiếp trong mã nguồn. Đây là rủi ro bảo mật nghiêm trọng nếu mã nguồn được đưa lên các nền tảng như GitHub.
2. **Cố định Port và Host:** Ứng dụng được cấu hình cứng để chạy trên `localhost:8000`. Điều này khiến ứng dụng không thể truy cập được từ bên ngoài khi chạy trong Docker container hoặc trên các nền tảng đám mây (nơi Port thường được cấp phát động qua biến môi trường).
3. **Thiếu quản lý cấu hình:** Các thiết lập như `DEBUG` hay `MAX_TOKENS` được viết cứng trong code, gây khó khăn khi muốn thay đổi hành vi của ứng dụng giữa các môi trường khác nhau (phát triển, kiểm thử, thực tế) mà không cần sửa mã nguồn.
4. **Không có Endpoint kiểm tra sức khỏe (Health Check):** Thiếu các đường dẫn `/health` và `/ready`, khiến các hệ thống quản lý đám mây không thể tự động phát hiện nếu ứng dụng bị treo hoặc chưa sẵn sàng nhận dữ liệu.
5. **Sử dụng lệnh Print cơ bản:** Sử dụng `print()` thay vì ghi log có cấu trúc (structured logging) khiến việc theo dõi, tìm kiếm và phân tích lỗi trên hệ thống lớn trở nên cực kỳ khó khăn.
6. **Không xử lý tắt ứng dụng an toàn (Graceful Shutdown):** Ứng dụng không bắt tín hiệu `SIGTERM`, có thể dẫn đến việc mất dữ liệu hoặc ngắt kết nối đột ngột khi hệ thống yêu cầu dừng ứng dụng.
7. **Chế độ Debug trong Production:** Việc chạy ứng dụng với `reload=True` không chỉ gây tốn tài nguyên mà còn tiềm ẩn nguy cơ bảo mật trong môi trường thực tế.

### Bài tập 1.3: Bảng so sánh
| Tính năng | Phát triển (Develop) | Thực tế (Production) | Tại sao quan trọng? |
|-----------|----------------------|----------------------|---------------------|
| **Cấu hình** | Viết cứng trong `app.py`. | Quản lý tập trung qua biến môi trường (.env). | Bảo mật thông tin nhạy cảm và linh hoạt tùy chỉnh. |
| **Ghi Log** | Sử dụng `print()` đơn giản. | Log định dạng JSON có cấu trúc. | Hỗ trợ phân tích tự động và giám sát hệ thống tốt hơn. |
| **Health Check**| Không có. | Có endpoint `/health` và `/ready`. | Cần thiết để hệ thống tự động phục hồi và duy trì tính ổn định. |
| **Port/Host** | Cố định `localhost:8000`. | Sử dụng `PORT` động và bind `0.0.0.0`. | Cho phép ứng dụng chạy được trong container và trên Cloud. |
| **Vòng đời** | Tắt đột ngột. | Xử lý `SIGTERM` và `lifespan`. | Đảm bảo hoàn tất các yêu cầu đang xử lý trước khi dừng hẳn. |
| **Bảo mật** | Không có CORS, lộ key. | Middleware CORS và bảo mật qua Env. | Ngăn chặn truy cập trái phép và bảo vệ mã khóa dịch vụ. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: 
Base image được sử dụng là python:3.11.
Đây là một bản phân phối đầy đủ (full distribution) dựa trên Debian, cung cấp môi trường thực thi Python phiên bản 3.11 cùng các công cụ xây dựng cần thiết.

2. Working directory: [Your answer]
Thư mục làm việc trong container được xác định là /app.
Mọi tác vụ sao chép dữ liệu (COPY) và thực thi câu lệnh (RUN, CMD) đều được thực hiện cục bộ tại đường dẫn tuyệt đối này bên trong file system của container.

3. Tại sao COPY requirements.txt trước?
Việc tách biệt và thực thi COPY requirements.txt trước khi sao chép mã nguồn nhằm tối ưu hóa Docker Layer Caching:
- Tính ổn định của Dependencies: Các thư viện phụ thuộc thường ít thay đổi hơn so với logic mã nguồn.
- Hiệu quả xây dựng (Build Efficiency): Bằng cách cài đặt dependencies trước, Docker sẽ lưu trữ lớp (layer) này vào bộ nhớ đệm. Trong các lần build tiếp theo, nếu tệp requirements.txt không có thay đổi, hệ thống sẽ bỏ qua bước pip install (vốn tốn nhiều thời gian và băng thông), chỉ thực hiện cập nhật các lớp chứa mã nguồn phía sau.

4. CMD vs ENTRYPOINT khác nhau thế nào?
CMD và ENTRYPOINT đều chỉ định lệnh khởi chạy container nhưng khác nhau về khả năng ghi đè. ENTRYPOINT thiết lập lệnh cố định, biến container thành một tệp thực thi mà các tham số truyền thêm sẽ được nối tiếp vào sau. Trong khi đó, CMD chỉ cung cấp giá trị mặc định, cho phép người dùng ghi đè hoàn toàn lệnh khởi động khi thực hiện docker run. Trong Dockerfile này, CMD được ưu tiên để linh hoạt chuyển đổi giữa việc chạy ứng dụng hoặc truy cập terminal khi cần debug.

### Exercise 2.3: Image size comparison
- Develop: [1.66] GB
- Production: [236.44] MB
- Difference: [$86.09]%

### 1. Vai trò của Stage 1 (Builder)
Stage 1 đóng vai trò là môi trường chuẩn bị và xây dựng các thành phần phụ thuộc (dependencies) cho ứng dụng:
* **Cài đặt công cụ biên dịch:** Sử dụng các gói như `gcc` và `libpq-dev` để biên dịch các thư viện Python đặc thù từ mã nguồn.
* **Xây dựng Artifacts:** Thực hiện cài đặt các thư viện vào thư mục bộ nhớ đệm cục bộ (`/root/.local`) để sẵn sàng chuyển sang giai đoạn tiếp theo.
* **Phạm vi:** Giai đoạn này chỉ tồn tại trong quá trình xây dựng image; toàn bộ các công cụ biên dịch nặng nề sẽ không xuất hiện trong sản phẩm cuối cùng.

### 2. Vai trò của Stage 2 (Runtime)
Stage 2 tạo ra môi trường thực thi chính thức cho ứng dụng:
* **Tối ưu hóa môi trường:** Khởi tạo từ bản `slim` (rút gọn) để loại bỏ các tệp tin hệ thống không cần thiết cho việc vận hành Python.
* **Kế thừa chọn lọc:** Chỉ sao chép các thư viện đã được biên dịch hoàn tất từ Stage 1 (`COPY --from=builder`) và mã nguồn ứng dụng.
* **Thiết lập vận hành:** Cấu hình bảo mật với người dùng không có quyền root (`appuser`), thiết lập biến môi trường và cơ chế kiểm tra sức khỏe hệ thống (`HEALTHCHECK`).

### 3. Nguyên nhân kích thước image nhỏ hơn
Việc giảm dung lượng từ 1.66 GB xuống dưới 500 MB đạt được thông qua các cơ chế sau:
* **Sử dụng Slim Base Image:** Thay thế bản phân phối Python đầy đủ bằng bản `slim`, vốn đã loại bỏ các bộ công cụ phát triển và tài liệu hướng dẫn của hệ điều hành.
* **Loại bỏ Build Tools:** Các công cụ chiếm dung lượng lớn như `gcc` và các thư viện liên kết chỉ nằm lại ở Stage 1. Image Runtime cuối cùng hoàn toàn sạch bóng các công cụ này.
* **Trích xuất Artifacts:** Kỹ thuật Multi-stage cho phép chỉ giữ lại kết quả cuối cùng của quá trình cài đặt (các tệp .pyc, binary), loại bỏ hoàn toàn các tệp tin tạm, mã nguồn thư viện chưa biên dịch và cache phát sinh trong quá trình build.

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- URL: https://your-app.railway.app
- Screenshot: [Link to screenshot in repo]

## Part 4: API Security

### Exercise 4.1-4.3: Test results
[Paste your test outputs]

### Exercise 4.4: Cost guard implementation
[Explain your approach]

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
[Your explanations and test results]
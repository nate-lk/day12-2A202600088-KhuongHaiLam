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
1. Base image: [Your answer]
2. Working directory: [Your answer]
...

### Exercise 2.3: Image size comparison
- Develop: [X] MB
- Production: [Y] MB
- Difference: [Z]%

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
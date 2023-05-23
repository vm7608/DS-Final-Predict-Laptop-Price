<h1>Hướng dẫn chạy chương trình</h1>

## 1. Cào dữ liệu

### 1.1 Driver chrome

- Lựa chọn phiên bản phù hợp và tải về tại [đây](https://chromedriver.chromium.org/downloads)
- Giải nén và đặt file chromedriver.exe vào thư mục crawl_code
- Đối với dự án này, phiên bản chromedriver.exe được sử dụng là ChromeDriver 114.0.5735.16. Tải tại [đây](https://chromedriver.storage.googleapis.com/index.html?path=114.0.5735.16/)

### 1.2 Cài đặt package

Cài đặt các package cần thiết

```
pip install -r requirements.txt
```

### 1.3 Cào dữ liệu

Chạy lệnh sau để cào dữ liệu:

- Đối với windows

```
cd crawl_code
run_win.ps1
```

- Đối với linux và mac

```
cd crawl_code
run.sh
```

Sau khi chạy xong, dữ liệu sẽ được lưu vào thư mục crawl_code/raw
Dữ liệu sau khi cào bao gồm các file sau:

- laptop_basic.csv chứa các thông tin cơ bản và đường dẫn đến trang thông tin chi tiết của các sản phẩm.
- laptop_detail.csv chứa các thông tin chi tiết của các sản phẩm.
- cpuben.csv chứa thông tin về CPU của các sản phẩm.
- gpuben.csv chứa thông tin về GPU của các sản phẩm.

## 2. Chạy file notebook (Cần cài đặt pandas, numpy, sklearn, matplotlib, seaborn)

Có hai folder chứa file notebook: khdl_1k và khdl_10k. Mỗi folder chứa 3 file notebook:

- data_cleaning.ipynb chứa code để làm sạch dữ liệu.
- eda.ipynb chứa code để phân tích dữ liệu.
- main.ipynb chứa code để thực hiện các bước xử lý và xây dựng model.

Folder khdl_1k có chứa thêm folder raw1k chứa dữ liệu gốc và có thêm file clean_data_1k.csv chứa dữ liệu sau khi làm sạch và để sử dụng cho quá trình xử lý.

Thứ tự chạy các file notebook:

- data_cleaning.ipynb - sau khi chạy sẽ có file clean_data_1k.csv chứa dữ liệu sau khi làm sạch.
- eda.ipynb - chạy để phân tích dữ liệu.
- main.ipynb - chạy để thực hiện các bước xử lý và xây dựng model.
目录结构和简要说明


        ├── Adam
        │   ├── cases   # 测试用例目录
        │   │   ├── __init__.py
        │   │   ├── global
        │   │   │   ├── __init__.py
        │   │   │   └── test_login.py
        │   │   └── zeus
        │   │       ├── __init__.py
        │   │       └── test_01_table_management_list.py
        │   ├── chromedirver
        │   ├── commons     # 通用方法封装
        │   │   ├── __init__.py
        │   │   ├── basepage.py
        │   │   ├── db.py
        │   │   ├── driver.py
        │   │   ├── element.py
        │   │   ├── errors.py
        │   │   ├── fixtures.py
        │   │   ├── utils.py
        │   ├── config.py
        │   ├── drivers
        │   │   ├── chromedirver_linux32
        │   │   ├── chromedirver_linux64
        │   │   └── chromedirver_mac
        │   ├── pages       # pageObject模型定义
        │   │   ├── __init__.py
        │   │   ├── cas
        │   │   │   ├── __init__.py
        │   │   │   ├── login_page.py
        │   │   └── zeus
        │   │       ├── __init__.py
        │   │       ├── table_management_list_page.py
        │   ├── reports
        │   │   └── 2017_07_23_155548.html
        │   ├── runner.py
        ├── Dockerfile
        ├── Eve     # Chrome插件Eve
        ├── EveServer   # Eve调用的接口服务
        ├── README.md
        ├── config.py
        ├── gunicorn.py
        ├── manager.py
        └── requirements.txt


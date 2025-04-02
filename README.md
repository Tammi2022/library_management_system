# library_management_system
图书管理系统
### 使用技术栈：
python, django, celery

### 笔试题目：
1. 设计一个图书馆管理系统，维护图书相关的属性
2. 提供图书的查询、录入、修改和销毁的 API
3. 提供借书、还书的 API
4. 图书借阅期限为 30 天，每天 08:00 发通知将在 7 天内到期的图书借阅者，提醒还书
5. 实现一个中间件，记录每个 API 请求的参数和耗时


测试：
celery -A library_management_system worker --pool=solo --loglevel=info
pytest test/test_celery.py -s

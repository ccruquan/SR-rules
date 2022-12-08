# About

从 [clash-rules](https://github.com/Loyalsoldier/clash-rules)生成 ShadowRocket 的脚本

## 使用方法

1. Clone 项目代码
2. 按需求查看/编辑 [general.txt](./general.txt)
3. 按需求查看/编辑 [rules-set.yaml](./rules-set.yaml)
4. 按需求查看/编辑 [main.py](./main.py)
5. 安装依赖

```sh
poetry install
```

6. 生成 sr_rule.conf

```sh
poetry run python main.py
```

7. 启动一个简单服务器

```sh
python -m http.server
```

8. 小火箭添加配置: http://`your-pc-ip`:`port`/sr_rule.conf

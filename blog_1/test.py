import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_proj_2")

    import django

    django.setup()

#这里写数据查询代码
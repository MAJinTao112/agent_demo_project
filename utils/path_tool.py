import os


def get_project_root():
    """返回项目根目录的绝对路径。

    当前文件位于 utils/path_tool.py，回溯一级父目录即为项目根目录。

    Returns:
        str: 项目根目录的绝对路径
    """
    # 获取当前文件所在目录的绝对路径（utils/）
    current_dir = os.path.abspath(os.path.dirname(__file__))
    # 回溯一级父目录（utils/ → 项目根目录）
    root = os.path.dirname(current_dir)

    return root


# 模块加载时直接缓存根目录，便于其他文件导入后复用。
project_root = get_project_root()


def get_abs_path(relative_path: str) -> str:
    """将相对路径拼接项目根目录，返回绝对路径。

    Args:
        relative_path: 相对于项目根目录的相对路径

    Returns:
        str: 拼接后的绝对路径
    """
    return os.path.join(project_root, relative_path)


if __name__ == '__main__':
    print(f"项目根目录: {project_root}")
    print(f"data 目录绝对路径: {get_abs_path('data')}")
    print(f"main.py 绝对路径: {get_abs_path('main.py')}")


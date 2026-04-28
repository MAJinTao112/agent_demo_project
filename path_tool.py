import os


def get_project_root():
    """返回约定的项目根目录绝对路径。

    这里不依赖运行时工作目录，而是从当前模块文件的位置出发，
    连续回溯两级父目录来推导“项目根目录”。

    Returns:
        str: 通过当前文件位置推导出的根目录绝对路径
    """
    # 先定位到当前文件所在目录，避免受调用方 cwd 影响。
    current_dir = os.path.abspath(os.path.dirname(__file__))
    # 第一次回溯：进入当前文件所在目录的父目录。
    current_dir = os.path.dirname(current_dir)
    # 第二次回溯：继续进入上一级，作为项目根目录返回。
    # 这依赖当前文件在项目中的目录层级是固定的。
    root = os.path.dirname(current_dir)

    return root


# 模块加载时直接缓存根目录，便于其他文件导入后复用。
project_root = get_project_root()

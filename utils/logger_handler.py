# 导入 datetime 模块中的 datetime 类，用于获取当前时间
from datetime import datetime
# 导入 Python 标准日志模块
import logging
# 导入操作系统接口模块，用于文件和路径操作
import os


# 从项目路径工具模块中导入获取绝对路径的函数
from utils.path_tool import get_abs_path

# 日志文件存放的根目录（项目根目录下的 logs/ 文件夹）
LOG_ROOT = get_abs_path("logs")


# 确保日志目录存在，不存在则自动创建
os.makedirs(LOG_ROOT, exist_ok=True)

# 默认日志格式：时间 - 日志器名称 - 级别 - 文件名:行号 - 消息
DEFAULT_LOG_FORMAT = logging.Formatter(
    # asctime 是日志记录的时间，name 是日志器名称
    # levelname 是日志级别，filename 是文件名，lineno 是行号
    # message 是实际的日志消息内容
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)


# 定义获取日志器的函数
def get_logger(
        name: str = "agent",              # 日志器名称，同时也是日志文件名的一部分
        console_lever: int = logging.INFO,  # 控制台输出级别，默认 INFO
        file_lever: int = logging.DEBUG,    # 文件输出级别，默认 DEBUG
        log_file=None,                      # 自定义日志文件路径，为 None 则自动生成
) -> logging.Logger:                        # 返回值类型是 Logger 对象
    """获取配置好的日志器，同时输出到控制台和文件。

    Args:
        name: 日志器名称，也是日志文件名的一部分
        console_lever: 控制台日志级别，默认 INFO
        file_lever: 文件日志级别，默认 DEBUG
        log_file: 自定义日志文件路径，为 None 则自动按日期生成

    Returns:
        配置好的 Logger 对象
    """
    # 通过 logging.getLogger 获取或创建一个指定名称的日志器
    logger = logging.getLogger(name)
    # 设置日志器的全局级别为 DEBUG（所有级别都记录）
    logger.setLevel(logging.DEBUG)

    # 如果日志器已经绑定了处理器，说明已配置过，直接返回
    if logger.handlers:
        return logger

    # 创建控制台处理器，用于在终端输出日志
    console_handler = logging.StreamHandler()
    # 设置控制台处理器的日志级别
    console_handler.setLevel(console_lever)
    # 设置控制台处理器的日志格式
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    # 将控制台处理器添加到日志器
    logger.addHandler(console_handler)

    # 如果未指定日志文件路径，则自动按日期生成文件名
    if not log_file:
        # 生成日志文件路径：logs/{名称}_{日期}.log
        log_path = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
    else:
        # 如果指定了路径，则直接使用
        log_path = log_file
    # 创建文件处理器，用于将日志写入文件（UTF-8 编码）
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    # 设置文件处理器的日志级别
    file_handler.setLevel(file_lever)
    # 设置文件处理器的日志格式
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    # 将文件处理器添加到日志器
    logger.addHandler(file_handler)

    # 返回配置完成的日志器
    return logger


# 创建默认的日志器实例，其他模块可以直接通过 import 使用
logger = get_logger()

# 如果直接运行此脚本，则执行以下测试代码
if __name__ == "__main__":
    # 输出一条 INFO 级别的测试日志
    logger.info("信息日志")
    # 输出一条 ERROR 级别的测试日志
    logger.error("错误日志")

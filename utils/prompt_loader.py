# 导入提示词配置字典，包含各提示词模板文件的路径
from utils.config_handler import prompts_conf
# 导入路径工具函数，用于将相对路径转为绝对路径
from utils.path_tool import get_abs_path
# 导入项目自定义的日志器
from utils.logger_handler import logger


def load_system_prompts():
    """加载主对话的系统提示词"""
    try:
        # 从配置中读取主提示词文件路径，并转为绝对路径
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        # 配置中缺少 main_prompt_path 键时记录错误日志
        logger.error(f"[load_system_prompts]在yaml配置项中没有main_prompt_path配置项")
        # 重新抛出异常，让上层调用者处理
        raise e

    try:
        # 以只读模式打开提示词文件，读取全部内容并返回
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        # 文件读取或解析失败时记录错误日志
        logger.error(f"[load_system_prompts]解析系统提示词出错，{str(e)}")
        # 重新抛出异常，让上层调用者处理
        raise e


def load_rag_prompts():
    """加载 RAG 摘要的提示词"""
    try:
        # 从配置中读取 RAG 摘要提示词文件路径，并转为绝对路径
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        # 配置中缺少 rag_summarize_prompt_path 键时记录错误日志
        logger.error(f"[load_rag_prompts]在yaml配置项中没有rag_summarize_prompt_path配置项")
        # 重新抛出异常，让上层调用者处理
        raise e

    try:
        # 以只读模式打开提示词文件，读取全部内容并返回
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        # 文件读取或解析失败时记录错误日志
        logger.error(f"[load_rag_prompts]解析RAG总结提示词出错，{str(e)}")
        # 重新抛出异常，让上层调用者处理
        raise e


def load_report_prompts():
    """加载报告生成的提示词"""
    try:
        # 从配置中读取报告提示词文件路径，并转为绝对路径
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        # 配置中缺少 report_prompt_path 键时记录错误日志
        logger.error(f"[load_report_prompts]在yaml配置项中没有report_prompt_path配置项")
        # 重新抛出异常，让上层调用者处理
        raise e

    try:
        # 以只读模式打开提示词文件，读取全部内容并返回
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        # 文件读取或解析失败时记录错误日志
        logger.error(f"[load_report_prompts]解析报告生成提示词出错，{str(e)}")
        # 重新抛出异常，让上层调用者处理
        raise e


# 当脚本直接运行时执行以下测试代码
if __name__ == '__main__':
    print('PyCharm')

    print("\n===== System Prompts =====")
    print(load_system_prompts())

    print("\n===== RAG Prompts =====")
    print(load_rag_prompts())

    print("\n===== Report Prompts =====")
    print(load_report_prompts())
import concurrent.futures
import threading
from queue import Queue
import time
from utils.logger_config import get_logger

# 获取模块日志器
logger = get_logger(__name__)


class ThreadPoolManager:
    """
    线程池管理器，用于异步处理任务
    """

    def __init__(self, max_workers=5, queue_size=10):
        """
        初始化线程池管理器
        
        Args:
            max_workers: 最大工作线程数
            queue_size: 任务队列大小
        """
        self.max_workers = max_workers
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.task_queue = Queue(maxsize=queue_size)
        self.results = {}
        self.lock = threading.Lock()
        self.running = False
        self.worker_thread = None
        # 添加任务追踪集合，用于防止重复提交任务
        self.pending_tasks = set()
        self.task_id_mapping = {}  # 用于映射自定义标识符到任务ID

    def start(self):
        """
        启动线程池管理器
        """
        if not self.running:
            self.running = True
            self.worker_thread = threading.Thread(target=self._process_queue)
            self.worker_thread.daemon = True
            self.worker_thread.start()
            logger.info(f"线程池管理器已启动，最大线程数: {self.max_workers}")

    def stop(self):
        """
        停止线程池管理器
        """
        if self.running:
            self.running = False
            if self.worker_thread:
                self.worker_thread.join(timeout=1)
            self.thread_pool.shutdown(wait=True)
            logger.info("线程池管理器已停止")

    def add_task(self, task_id, func, *args, **kwargs):
        """
        添加任务到队列
        
        Args:
            task_id: 任务ID
            func: 要执行的函数
            *args: 函数参数
            **kwargs: 函数关键字参数
            
        Returns:
            bool: 是否成功添加任务
        """
        try:
            # 检查是否有重复的任务ID
            with self.lock:
                if task_id in self.pending_tasks:
                    logger.warning(f"任务 {task_id} 已在队列中，跳过重复提交")
                    return False
                
                # 如果有自定义标识符，检查是否重复
                custom_id = None
                if 'task_info' in kwargs and isinstance(kwargs['task_info'], dict) and 'username' in kwargs['task_info']:
                    custom_id = kwargs['task_info']['username']
                    
                if custom_id and custom_id in self.task_id_mapping:
                    existing_task_id = self.task_id_mapping[custom_id]
                    logger.warning(f"账号 {custom_id} 已有任务 {existing_task_id} 在队列中，跳过重复提交")
                    return False
                
                # 添加到追踪集合
                self.pending_tasks.add(task_id)
                if custom_id:
                    logger.debug(f"将账号 {custom_id} 映射到任务ID {task_id}")
                    self.task_id_mapping[custom_id] = task_id
            
            task = (task_id, func, args, kwargs)
            self.task_queue.put(task, block=False)
            logger.debug(f"任务 {task_id} 已添加到队列")
            return True
        except Exception as e:
            logger.error(f"添加任务 {task_id} 失败: {str(e)}")
            return False

    def _process_queue(self):
        """
        处理任务队列
        """
        while self.running:
            try:
                if not self.task_queue.empty():
                    task_id, func, args, kwargs = self.task_queue.get(block=False)
                    future = self.thread_pool.submit(func, *args, **kwargs)
                    future.add_done_callback(lambda f, tid=task_id: self._task_done(tid, f))
                    logger.debug(f"任务 {task_id} 已提交到线程池")
                else:
                    time.sleep(0.1)
            except Exception as e:
                logger.error(f"处理任务队列出错: {str(e)}")
                time.sleep(0.1)

    def _task_done(self, task_id, future):
        """
        任务完成回调
        
        Args:
            task_id: 任务ID
            future: Future对象
        """
        try:
            result = future.result()
            with self.lock:
                self.results[task_id] = {"status": "completed", "result": result}
                # 从追踪集合中移除
                self.pending_tasks.discard(task_id)
                
                # 如果有自定义标识符映射，保留映射关系用于结果查询
                # 不再自动删除映射关系，由外部代码在收集完结果后统一清理
                
            logger.debug(f"任务 {task_id} 已完成")
        except Exception as e:
            with self.lock:
                self.results[task_id] = {"status": "error", "error": str(e)}
                # 从追踪集合中移除
                self.pending_tasks.discard(task_id)
                
                # 同样保留映射关系用于结果查询
                
            logger.error(f"任务 {task_id} 执行出错: {str(e)}")

    def get_result(self, task_id):
        """
        获取任务结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            dict: 任务结果
        """
        with self.lock:
            return self.results.get(task_id)

    def submit_task(self, func, *args, **kwargs):
        """
        直接提交任务到线程池并返回Future对象
        
        Args:
            func: 要执行的函数
            *args: 函数参数
            **kwargs: 函数关键字参数
            
        Returns:
            Future: Future对象
        """
        # 检查是否是登录任务，如果是，检查是否有自定义标识符
        if len(args) > 0 and isinstance(args[0], dict) and 'username' in args[0]:
            username = args[0]['username']
            # 检查是否已经有相同账号的任务在处理中
            with self.lock:
                if username in self.task_id_mapping:
                    logger.warning(f"账号 {username} 已有任务在处理中，跳过重复提交")
                    # 返回一个已完成的Future，带有错误信息
                    future = concurrent.futures.Future()
                    future.set_exception(Exception(f"账号 {username} 有重复任务"))
                    return future
                
                # 记录这个账号对应的Future
                task_id = str(id(func)) + "_" + username
                logger.debug(f"直接提交任务: 将账号 {username} 映射到任务ID {task_id}")
                self.task_id_mapping[username] = task_id
                self.pending_tasks.add(task_id)
                
        return self.thread_pool.submit(func, *args, **kwargs)

# 创建全局线程池实例
thread_pool = ThreadPoolManager()

# 导出名称
__all__ = ['ThreadPoolManager', 'thread_pool']
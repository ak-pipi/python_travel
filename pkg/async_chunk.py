
from pkg.deepseek_conf import DeepSeekModel
import asyncio

async def task_one():
    llm_model = DeepSeekModel()
    # 1.定义模型
    model = llm_model.llm

    chunks = []

    async for chunk in model.astream("天空是什么颜色？"):
        chunks.append(chunk)
        # 判断chunks长度为1的时候，打印chunks[0]
        if len(chunks) == 2:
            print(f"Received first chunk: {chunks[0]}")
        print(chunk.content,end="|",flush=True)



async def task_two():
    llm_model = DeepSeekModel()
    # 1.定义模型
    model = llm_model.llm

    chunks = []

    async for chunk in model.astream("地球是圆的吗？"):
        chunks.append(chunk)
        # 判断chunks长度为1的时候，打印chunks[0]
        if len(chunks) == 2:
            print(f"Received first chunk: {chunks[0]}")
        print(chunk.content,end="|",flush=True)


async def main():
    # 同步调用task_one和task_two
    await task_one()
    await task_two()

    # 使用asyncio.gather来并发执行任务
    # 创建两个任务
    # task1 = asyncio.create_task(task_one())
    # task2 = asyncio.create_task(task_two())
    # # 等待任务完成
    # await asyncio.gather(task1, task2)

if __name__ == "__main__":
    asyncio.run(main())
import asyncio
import re
import os
import shutil
from oslk import oslk_generator
from osc import osc_generator, osc_generator_from_intention


genarateion_path = "generated_scenarios"
os.makedirs(genarateion_path, exist_ok=True)

def slugify(text: str) -> str:
    """简单把中文/空格/特殊字符转为文件名友好格式"""
    # 把空白改为下划线，去掉不安全字符
    text = re.sub(r'\s+', '_', text.strip())
    text = re.sub(r'[^\w\u4e00-\u9fff_-]', '', text)  # 保留字母数字中文下划线和短横
    # 可选：把中文保留原样或转为拼音，这里保留原样
    return text

def force_move(src, dst):
    """
    强制移动文件或目录
    如果目标已存在，则先删除再移动
    """
    # 如果目标存在，删除它
    if os.path.exists(dst):
        if os.path.isdir(dst):
            shutil.rmtree(dst)  # 删除目录
            print(f"Removed existing directory: {dst}")
        else:
            os.remove(dst)  # 删除文件
            print(f"Removed existing file: {dst}")
    
    # 移动源到目标位置
    return shutil.move(src, dst)

def get_existing_folders():
    """
    获取generated_scenarios目录下已存在的文件夹名称
    """
    existing_folders = set()
    if os.path.exists(genarateion_path):
        for item in os.listdir(genarateion_path):
            item_path = os.path.join(genarateion_path, item)
            if os.path.isdir(item_path):
                existing_folders.add(item)
    return existing_folders

async def _worker(sem: asyncio.Semaphore, intention_text: str, save_name: str):
    async with sem:
        # 提取文件夹名称（去掉.osc扩展名）
        folder_name = save_name[:-4]
        
        # 检查文件夹是否已存在，如果存在则跳过
        if folder_name in get_existing_folders():
            print(f"Skip (already exists): {folder_name}")
            return
        
        print(f"Start: {intention_text[:50]}... -> {save_name}")
        try:
            await osc_generator_from_intention(intention_text, save_name)
            
            # Create folder and move generated files
            folder_name = os.path.join(genarateion_path, save_name[:-4])  # Remove .osc extension
            if os.path.exists(folder_name):
                if os.path.isdir(folder_name):
                    shutil.rmtree(folder_name)
                else:
                    os.remove(folder_name)
            os.makedirs(folder_name, exist_ok=True)
            
            # Move generated files to folder
            force_move("conversation_history.json", os.path.join(folder_name,"conversation_history.json"))
            force_move(save_name.replace(".osc", ".json"), os.path.join(folder_name,save_name.replace(".osc", ".json")))
            force_move(save_name, os.path.join(folder_name,save_name))
            
            print(f"Done: {save_name}")
        except Exception as e:
            print(f"Error for {save_name}: {e}")

async def run_batch(items, concurrency=2):
    sem = asyncio.Semaphore(concurrency)
    tasks = [
        asyncio.create_task(_worker(sem, q, name))
        for q, name in items
    ]
    await asyncio.gather(*tasks)

def build_items_from_intention_file(intention_file_path: str, start_line: int = 0, max_lines: int = None):
    """
    从intention.txt文件逐行读取意图，生成 (intention_text, save_name) 对列表
    
    Args:
        intention_file_path: intention.txt文件路径
        start_line: 从第几行开始读取（0-based）
        max_lines: 最多读取多少行，None表示读取所有
    
    Returns:
        List of (intention_text, save_name) tuples
    """
    items = []
    
    with open(intention_file_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            # Skip lines before start_line
            if idx < start_line:
                continue
            
            # Stop if we've reached max_lines
            if max_lines is not None and idx >= start_line + max_lines:
                break
            
            intention_text = line.strip()
            if not intention_text:
                continue
            
            # Generate filename from line number and first few words
            # Use line number to ensure uniqueness
            fname_prefix = f"intention_{idx+1}"
            fname = f"{fname_prefix}.osc"
            
            items.append((intention_text, fname))
    
    # 获取已存在的文件夹名称
    existing_folders = get_existing_folders()
    
    # 过滤掉已存在的文件夹对应的项目
    filtered_items = []
    skipped_count = 0
    for intention_text, save_name in items:
        folder_name = save_name[:-4]  # 去掉.osc扩展名
        if folder_name in existing_folders:
            skipped_count += 1
            continue
        filtered_items.append((intention_text, save_name))
    
    print(f"Skipped {skipped_count} existing folders, processing {len(filtered_items)} remaining items")
    
    return filtered_items

def build_items_from_list(queries):
    """
    从一个字符串列表生成 (initial_query, save_name) 对列表。
    如有需要可在这里做更多的"处理数据"逻辑。
    """
    items = []
    for q, name in queries.items():
        fname = slugify(name)
        if not fname:
            continue
        # 统一扩展名为 .osc
        if not fname.lower().endswith('.osc'):
            fname = f"{fname}.osc"
        items.append((q, fname))
    
    # 获取已存在的文件夹名称
    existing_folders = get_existing_folders()
    
    # 过滤掉已存在的文件夹对应的项目
    filtered_items = []
    skipped_count = 0
    for intention_text, save_name in items:
        folder_name = save_name[:-4]  # 去掉.osc扩展名
        if folder_name in existing_folders:
            skipped_count += 1
            continue
        filtered_items.append((intention_text, save_name))
    
    print(f"Skipped {skipped_count} existing folders, processing {len(filtered_items)} remaining items")
    
    return filtered_items

def main_query():
    # 示例输入列表：可以替换为从文件/数据库读取
    queries = {
        "前车急刹至停止，ego 2 m 内刹停":"FullStop",
        "前车从 100 km/h 降速至 60 km/h，ego 往左变道超车":"RapidDecel",
        "插入车急刹，ego 减速保持车距":"CutInBrake",
        "前车突然遇到障碍减速后加速，ego 同步":"BrakeFollow",
        "前车连续三次急停，ego 每次保持足够车距制动":"MultiStop"
    }

    items = build_items_from_list(queries)
    # 可以通过修改concurrency控制并发量（注意模型/代理资源）
    concurrency = 1  # 推荐先用 1 或 2，避免并发占满远端模型资源
    asyncio.run(run_batch(items, concurrency=concurrency))

def main():
    """
    Main function to process intentions from intention.txt file
    """
    intention_file_path = "/workspace/pro/selfInstruct/cursor-agent-intention-data-augmentation/data/intention.txt"
    
    # Read intentions from file
    # You can adjust start_line and max_lines to process specific ranges
    # For example: start_line=0, max_lines=10 will process first 10 intentions
    items = build_items_from_intention_file(
        intention_file_path, 
        start_line=0,      # Start from first line
        max_lines=None     # Process all lines (set to a number to limit)
    )
    
    print(f"Total intentions to process: {len(items)}")
    
    # Process with concurrency=1 to avoid overwhelming the system
    asyncio.run(run_batch(items, concurrency=1))

if __name__ == "__main__":
    main()
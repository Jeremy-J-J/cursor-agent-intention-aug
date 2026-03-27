from pathlib import Path
import sys
parent_dir = str(Path(__file__).parent.parent.parent.absolute())
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    
import asyncio
import json
import requests
from cursor_agent_tools import create_agent, run_agent_interactive
from intention import IntentionGenerator
from cursor_agent_tools import PermissionOptions

async def osc_generator(initial_query: str, save_name: str):

    #attention = 'ego 连续超车'
    #save_name = 'ego_overtake_multiple_qwennext.oslk'

    #ego_overtake_right.osc
    permissions = PermissionOptions(
        yolo_mode=True,
        command_allowlist=["ls", "echo", "git","cat", "cp", "mv", "mkdir","find", "grep", "head"],
        command_denylist=["python3"],
        delete_file_protection=True
    )

    # Create a Claude agent instance
    agent = create_agent(
        model='remote-holo-model',
        permissions=permissions
    )
    intentionrewriter = IntentionGenerator(agent)
    intention = await intentionrewriter.generate_intention(initial_query)
    print("Generated Intention:", intention)
    agent.register_default_tools()

    await run_agent_interactive(
        # model='claude-3-5-sonnet-latest',
        initial_query='''基于rag_osc/standard_test_scenarios 文件夹下的例子，写一个测试意图为{}的dsl代码,
                        注意以下一些常见的问题:
                        1. 只生成一个osc文件就可以了，千万不要生成多个osc文件；
                        2. 注释用 #，而不是 //，注释不要用中文，注释请使用英文；
                        3. 开头使用 import 导入osc文件，不要使用 include 导入osc文件；
                        4. 使用 extend test_config: 来导入地图文件；
                        5. 写文件使用create_file工具, 注意create_file的路径传参用file_path参数，不要多余explanation参数;
                        6. 生成了osc文件后就停止，不要多余操作；
                        7. 如果需要用到新的scenarios, 请参考在 rag_osc/basic_scenarios下面的内容，如有需要需要自己创建一个scenarios
                        最终结果保存到当前目录下的{}文件中，不要生成其他文件'''.format(intention, save_name), max_iterations=15,
        agent=agent
        #user_info=user_info,
        # auto_continue=True is the default - agent continues automatically
        # To disable automatic continuation, set auto_continue=False
    )

def format_intention_with_llm(intention_text: str, api_url: str = "http://localhost:8007/v1", model_id: str = "holo-model") -> str:
    """
    使用大模型API将意图文本格式化为结构化JSON
    
    Args:
        intention_text: 原始意图文本
        api_url: API服务地址
        model_id: 模型ID
    
    Returns:
        格式化后的JSON字符串
    """
    system_prompt = """作为自动驾驶场景理解专家，请基于以下的要求对于输入的意图片段进行理解，并生成结构化的输出:
要求包含以下几个关键要素：
1.输出意图描述的道路场景：json 字段名称为"道路场景"，输出的内容为当前输入描述的道路场景，可能是高速公路路口、城市交叉路口，分合流的路口，环岛等。
2.输出意图中场景的参与制：json 字段名称为"场景参与者"，输出的内容为当前输入描述中场景的主要参与者，包含主车和其他交通参与者，如NPC车辆、行人、自行车，静止物体，VRU等。
3.输出意图中场景的参与者的初始位置：json 字段名称为"初始位置"，输出内容为主要参与者与主车之间的空间关系，如：在主车对向车道20m，左侧右侧车道，前方/后方 100m等
4.输出意图中场景的主要参与者的动作：json 字段名称为"运动方向"，输出内容为当前输入描述中场景的场景参与者的动作描述，如：变道，超车，转弯，紧急制动，行人横穿马路等。
5.输出意图中主车的行驶意图：json 字段名称为"主车意图"，输出内容为当前输入描述中主车的行驶意图，如：左转弯，右转弯，直行，通过路口，避让行人，并入高速，驶出高速等。
6.输出意图中场景的触发条件：json 字段名称为"触发条件"，输出内容为当前输入描述中场景的触发条件，如：当主车与前车距离小于10米时，前车开始紧急制动等。
7.输出意图中的测试场景意图，json 字段名称为"测试意图"，输出内容为当前输入描述中场景的测试意图，如：测试鬼探头，测试车辆切入场景等。
输出的格式为 json 格式，示例如下:
{
    "道路场景": "...",
    "场景参与者": "...",
    "初始位置": "...",
    "运动方向": "...",
    "主车意图": "...",
    "触发条件": "...",
    "测试意图": "..."
}
不要生成无关的信息，字数控制在500字以内。只输出JSON，不要输出其他内容。"""
    
    # 构造请求
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": intention_text}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    print(f"[DEBUG] Calling LLM API: {api_url}/chat/completions")
    print(f"[DEBUG] Model: {model_id}")
    print(f"[DEBUG] Input text length: {len(intention_text)}")
    
    try:
        response = requests.post(
            f"{api_url}/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        print(f"[DEBUG] Response status code: {response.status_code}")
        response.raise_for_status()
        
        result = response.json()
        print(f"[DEBUG] API response keys: {result.keys()}")
        
        llm_output = result['choices'][0]['message']['content'].strip()
        print(f"[DEBUG] LLM output length: {len(llm_output)}")
        print(f"[DEBUG] LLM output preview: {llm_output[:200]}")
        
        # 尝试提取JSON部分（如果模型输出包含其他文本）
        start_idx = llm_output.find('{')
        end_idx = llm_output.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            json_str = llm_output[start_idx:end_idx+1]
            # 验证是否为有效JSON
            parsed = json.loads(json_str)
            print(f"[DEBUG] Successfully parsed JSON with keys: {parsed.keys()}")
            return json_str
        else:
            print(f"[WARNING] Could not extract JSON from LLM output")
            print(f"[WARNING] Full output: {llm_output}")
            return llm_output
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] HTTP request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"[ERROR] Response content: {e.response.text}")
        raise
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        raise

async def osc_generator_from_intention(intention_text: str, save_name: str):
    """
    Generate OSC file directly from intention text
    
    Args:
        intention_text: The intention text read from intention.txt
        save_name: The output OSC file name
    """
    permissions = PermissionOptions(
        yolo_mode=True,
        command_allowlist=["ls", "echo", "git","cat", "cp", "mv", "mkdir","find"],
        delete_file_protection=True
    )

    # Create a Claude agent instance
    agent = create_agent(
        model='remote-holo-model',
        permissions=permissions
    )
    
    # Format intention using LLM API
    print(f"Formatting intention with LLM: {intention_text[:100]}...")
    intention_json = await asyncio.to_thread(format_intention_with_llm, intention_text)
    
    print("Formatted Intention JSON:", intention_json)
    
    agent.register_default_tools()
    
    # Save the intention JSON
    with open(save_name.replace(".osc", ".json"), "w", encoding='utf-8') as f:
        f.write(intention_json)

    await run_agent_interactive(
        initial_query='''基于rag_osc/standard_test_scenarios 文件夹下的例子，写一个测试意图为{}的dsl代码,
                        注意以下一些常见的问题:
                        1. 只生成一个osc文件就可以了，千万不要生成多个osc文件；
                        2. 注释用 #，而不是 //，注释不要用中文，注释请使用英文；
                        3. 开头使用 import 导入osc文件，不要使用 include 导入osc文件；
                        4. 使用 extend test_config: 来导入地图文件；
                        5. 写文件使用create_file工具, 注意create_file的路径传参用file_path参数，不要多余explanation参数;
                        6. 生成了osc文件后就停止，不要多余操作；
                        7. 如果需要用到新的scenarios, 请参考在 rag_osc/basic_scenarios下面的内容，如有需要需要自己创建一个scenarios
                        最终结果保存到当前目录下的{}文件中，不要生成其他文件'''.format(intention_json, save_name), 
        max_iterations=15,
        agent=agent
    )
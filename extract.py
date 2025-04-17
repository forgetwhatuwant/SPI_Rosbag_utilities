import rosbag
from rosbag import Bag

def extract_true_segments(input_file, output_template='output_segment_{}.bag'):
    # 读取所有状态消息
    status_data = []
    with Bag(input_file, 'r') as bag:
        for topic, msg, t in bag.read_messages(topics=['/upi/status/is_action']):
            status_data.append((t.to_sec(), msg.data))

    # 检测连续true片段
    segments = []
    current_segment = None
    for timestamp, value in status_data:
        if value:  # 当前为true
            if not current_segment:  # 新片段开始
                current_segment = {
                    'start': timestamp,
                    'end': timestamp,
                    'start_msg_time': None,
                    'end_msg_time': None
                }
            else:  # 延续当前片段
                current_segment['end'] = timestamp
        else:  # 当前为false
            if current_segment:  # 结束当前片段
                segments.append(current_segment)
                current_segment = None

    # 处理最后一个片段
    if current_segment:
        segments.append(current_segment)

    # 分割原始bag文件
    for i, seg in enumerate(segments):
        output_file = output_template.format(i+1)
        print(f"Processing segment {i+1}: {seg['start']} to {seg['end']}")

        with Bag(input_file, 'r') as inbag:
            with Bag(output_file, 'w') as outbag:
                # 遍历所有消息
                for topic, msg, t in inbag.read_messages():
                    msg_time = t.to_sec()
                    if seg['start'] <= msg_time <= seg['end']:
                        outbag.write(topic, msg, t)

    return len(segments)

if __name__ == '__main__':
    input_bag = 'input.bag'  # 修改为你的bag文件路径
    num_segments = extract_true_segments(input_bag)
    print(f"共找到 {num_segments} 个连续true片段")

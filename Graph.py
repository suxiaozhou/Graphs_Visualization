import networkx as nx
from pyvis.network import Network
import math

def main():
    # 读取数据
    with open("hh.in", "r") as f:
        n, m = map(int, f.readline().split())
        a = [int(f.readline().strip()) for _ in range(n)]  # 节点特性列表
        edges = [tuple(map(int, f.readline().split())) for _ in range(m)]
    
    # 创建有向图（仅包含有连接的节点）
    G = nx.DiGraph()
    connected_nodes = set()
    for u, v in edges:
        G.add_edge(u, v)
        connected_nodes.update([u, v])
    valid_nodes = sorted(connected_nodes)
    G = G.subgraph(valid_nodes).copy()
    
    # 计算度数（使用指数缩放）
    degrees = {node: G.in_degree(node) + G.out_degree(node) for node in G.nodes}
    max_degree = max(degrees.values(), default=1)
    
    # 创建网络实例
    net = Network(height="800px", width="100%", directed=True, notebook=False,
                 font_color="#333333", select_menu=True, filter_menu=True)
    
    # 添加节点（优化显示参数）
    for node in G.nodes:
        size = 3 + 10 * math.sqrt(degrees[node]/max_degree)
        color = '#FF69B4' if a[node-1]==0 else '#1E90FF'  # 更鲜明的颜色
        net.add_node(node,
                    label=str(node),#label="unshown",#str(node),#隐藏节点编号
                    color=color,
                    size=size,
                    font={'size': 1001, 'face': 'Arial'},##############
                    borderWidth=0.2,
                    shadow=True)
    
    # 添加边（优化箭头显示）
    for u, v in G.edges:
        au = a[u-1]
        av = a[v-1]
        color = '#32CD32' if au != av else ('#FF4500' if au==0 else '#4169E1')
        net.add_edge(u, v, 
                    color=color, 
                    width=1.2,
                    arrows={'to': {'scaleFactor': 2}},
                    smooth={'type': 'dynamic'})
    
    # 布局配置系统（修复模式问题）
    flag = 2  # 可修改此处测试布局模式
    
    layout_config = {
        2: {  # 力导向布局
            "physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -150,
                    "centralGravity": 0.1,
                    "springLength": 20,
                    "springConstant": 0.02,
                    "damping": 0.4
                },
                "solver": "forceAtlas2Based"
            }
        }
    }
    
    # 应用布局配置
    net.set_options(f"""
    {{
        "nodes": {{
            "scaling": {{
                "min": 20,
                "max": 60
            }}
        }},
        "layout": {layout_config[flag].get('layout', {})},
        "physics": {layout_config[flag].get('physics', {})}
    }}
    """)
    
    # 生成交互页面
    net.show("graph.html", notebook=False)

if __name__ == "__main__":
    main()
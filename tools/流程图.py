#import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowEdge,StreamlitFlowNode
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import TreeLayout

nodes=[
    StreamlitFlowNode(
        id="1",
        pos=(0,0),
        data={"content":"[Desmos 图形计算器](https://www.desmos.com/calculator)"},
        node_type="input",
        source_position="right"
    ),
    StreamlitFlowNode(
        id="2",
        pos=(0,0),
        data={"content":"Node 2"},
        node_type="default",
        source_position="right",
        target_position="left",
    ),
    StreamlitFlowNode(
        id="3",
        pos=(0,0),
        data={"content":"Node 3"},
        node_type="default",
        source_position="right",
        target_position="left"
    ),
    StreamlitFlowNode(
        id="4",
        pos=(0,0),
        data={"content":"Node 4"},
        node_type="output",
        target_position="left"
    ),
    StreamlitFlowNode(
        id="5",
        pos=(0,0),
        data={"content":"Node 5"},
        node_type="output",
        target_position="left"
    ),
    StreamlitFlowNode(
        id="6",
        pos=(0,0),
        data={"content":"Node 6"},
        node_type="output",
        target_position="left"
    ),
    StreamlitFlowNode(
        id="7",
        pos=(0,0),
        data={"content":"Node 7"},
        node_type="output",
        target_position="left",
    )
]
edges=[
    StreamlitFlowEdge(
        "1-2",
        "1",
        "2",
        animated=True,
    ),
    StreamlitFlowEdge(
        "1-3",
        "1",
        "3",
        animated=True,
    ),
    StreamlitFlowEdge(
        "2-4",
        "2",
        "4",
        animated=True,
    ),
    StreamlitFlowEdge(
        "2-5",
        "2",
        "5",
        animated=True,
    ),
    StreamlitFlowEdge(
        "3-6",
        "3",
        "6",
        animated=True,
        marker_end={"type":"arrow"}
    ),
    StreamlitFlowEdge(
        "3-7",
        "3",
        "7",
        animated=True,
    )
]
state=StreamlitFlowState(nodes,edges)
streamlit_flow(
    "流程图",
    state,
    layout=TreeLayout(direction="right",node_node_spacing=75),
    hide_watermark=True,
    get_node_on_click=True,
    )



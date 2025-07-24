import json
import os

def get_node_type(elem):
    tag = elem.get("tagName", "")
    if tag == "a":
        return "link"
    elif tag == "button":
        return "button"
    elif tag == "input":
        return "input"
    elif tag == "select":
        return "select"
    elif tag == "img":
        return "img"
    else:
        return tag or "generic"

def get_node_text(elem):
    return elem.get("description") or elem.get("aria-label") or elem.get("tagName") or ""

def get_focusable(elem):
    return get_node_type(elem) in ["link", "button", "input", "select"]

def in_viewport(bbox, viewport):
    if not bbox:
        return False
    x_min = viewport["scrollX"]
    y_min = viewport["scrollY"]
    x_max = x_min + viewport["width"]
    y_max = y_min + viewport["height"]
    return not (
        bbox["bRx"] < x_min or bbox["tLx"] > x_max or
        bbox["bRy"] < y_min or bbox["tLy"] > y_max
    )

def action_representation(target_elem, local_idx=None):
    node_type = get_node_type(target_elem)
    node_text = get_node_text(target_elem)
    focusable = get_focusable(target_elem)
    if local_idx is not None:
        line = f"Action: click [{local_idx}] {node_type} '{node_text}'"
    else:
        line = f"Action: click {node_type} '{node_text}'"
    if focusable:
        line += " focusable: True"
    return line

def get_webpage_and_action_repr(annotation_dir):
    """
    输入: annotation文件夹路径
    输出: (webpage_repr, action_repr)
    """
    dtls_path = os.path.join(annotation_dir, "annot_dtls.json")
    elems_path = os.path.join(annotation_dir, "interact_elems.json")

    with open(dtls_path, "r", encoding="utf-8") as f:
        dtls = json.load(f)
    with open(elems_path, "r", encoding="utf-8") as f:
        elems = json.load(f)

    viewport = dtls["viewportInfo"]
    target_elem = dtls["targetElementData"]
    target_idx = target_elem.get("interactivesIndex", None)

    lines = []
    lines.append("[0] RootWebArea")
    idx = 1
    local_idx_of_action = None
    for elem in elems:
        bbox = elem.get("boundingBox")
        if in_viewport(bbox, viewport):
            node_type = get_node_type(elem)
            node_text = get_node_text(elem)
            focusable = get_focusable(elem)
            line = f"    [{idx}] {node_type} '{node_text}'"
            if focusable:
                line += " focusable: True"
            lines.append(line)
            if elem.get("interactivesIndex", None) == target_idx:
                local_idx_of_action = idx
            idx += 1

    webpage_repr = "\n".join(lines)
    action_repr = action_representation(target_elem, local_idx_of_action)
    return webpage_repr, action_repr

# 用法示例
if __name__ == "__main__":
    annotation_dir = "/Users/zheng.2372/PycharmProjects/web-monitor-neurips/data_processing/annotation_examples/annot_batch_Economic_News_id_d7cb5c09-b44f-4da1-a51b-a1c9d9210334_from_www_cnbc_com_economy_/act_annots/annot_HIGH_Tgt_Create_Account_6c347d03-4971-414d-a99d-fc87c01c692b"
    webpage_repr, action_repr = get_webpage_and_action_repr(annotation_dir)
    print("Webpage Representation (a11y-tree):")
    print(webpage_repr)
    print("\nAction Representation:")
    print(action_repr)

    print()


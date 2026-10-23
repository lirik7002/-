"""Загрузка VFS из XML."""
import base64
import xml.etree.ElementTree as ET

from src.vfs import Vfs, VfsNode

def load_vfs_from_xml(path: str) -> Vfs:
    """Загружает VFS из XML-файла."""
    tree = ET.parse(path)
    root_el = tree.getroot()
    vfs_name = root_el.get("name", "vfs")
    root_node = VfsNode(name="/", is_dir=True)

    def walk(el, parent):
        for child in el:
            name = child.get("name")
            if child.tag == "dir":
                node = VfsNode(name=name, is_dir=True, parent=parent)
                parent.children[name] = node
                walk(child, node)
            elif child.tag == "file":
                enc = child.get("encoding", "utf-8")
                raw = (child.text or "").strip()
                if enc == "base64":
                    data = base64.b64decode(raw)
                else:
                    data = raw.encode("utf-8")
                node = VfsNode(
                    name=name, is_dir=False, content=data, parent=parent
                )
                parent.children[name] = node

    walk(root_el, root_node)
    return Vfs(name=vfs_name, root=root_node)

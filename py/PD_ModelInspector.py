"""
PD模型检查器节点
用于检查model对象的结构和属性，特别是查看是否包含lora名称信息
"""

class PD_ModelInspector:
    """
    PD模型检查器节点
    功能：检查model对象的所有属性和方法，查看是否包含lora相关信息
    """
    
    @classmethod
    def INPUT_TYPES(s):
        """
        定义节点输入参数类型
        """
        return {
            "required": {
                "model": ("MODEL", ),  # 输入模型对象
            },
        }

    RETURN_TYPES = ("MODEL", "STRING")  # 返回模型和检查信息字符串
    RETURN_NAMES = ("model", "inspection_info")
    FUNCTION = "inspect_model"
    CATEGORY = "PD/Model"

    def inspect_model(self, model):
        """
        检查model对象的结构和属性
        
        参数：
        - model: 输入的模型对象
        
        返回：
        - model: 原样返回模型对象
        - inspection_info: 检查信息字符串
        """
        info_lines = []
        info_lines.append("=" * 60)
        info_lines.append("Model对象检查报告")
        info_lines.append("=" * 60)
        
        # 检查对象类型
        info_lines.append(f"\n对象类型: {type(model)}")
        info_lines.append(f"对象类名: {model.__class__.__name__}")
        
        # 检查所有属性
        info_lines.append("\n" + "-" * 60)
        info_lines.append("所有属性 (dir()):")
        info_lines.append("-" * 60)
        attrs = dir(model)
        for attr in attrs:
            if not attr.startswith('__'):
                try:
                    attr_value = getattr(model, attr)
                    attr_type = type(attr_value).__name__
                    # 如果是字符串或数字，显示值；否则只显示类型
                    if isinstance(attr_value, (str, int, float, bool)):
                        info_lines.append(f"  {attr}: {attr_value} ({attr_type})")
                    else:
                        info_lines.append(f"  {attr}: <{attr_type}>")
                except Exception as e:
                    info_lines.append(f"  {attr}: <无法访问: {e}>")
        
        # 检查是否有lora相关的属性
        info_lines.append("\n" + "-" * 60)
        info_lines.append("LoRA相关信息检查:")
        info_lines.append("-" * 60)
        lora_attrs = [attr for attr in attrs if 'lora' in attr.lower()]
        if lora_attrs:
            info_lines.append(f"找到 {len(lora_attrs)} 个可能相关的属性:")
            for attr in lora_attrs:
                try:
                    attr_value = getattr(model, attr)
                    if isinstance(attr_value, (str, int, float, bool, list, dict)):
                        info_lines.append(f"  {attr}: {attr_value}")
                    else:
                        info_lines.append(f"  {attr}: <{type(attr_value).__name__}>")
                except Exception as e:
                    info_lines.append(f"  {attr}: <无法访问: {e}>")
        else:
            info_lines.append("未找到包含'lora'的属性")
        
        # 检查是否有name相关的属性
        info_lines.append("\n" + "-" * 60)
        info_lines.append("名称相关信息检查:")
        info_lines.append("-" * 60)
        name_attrs = [attr for attr in attrs if 'name' in attr.lower()]
        if name_attrs:
            info_lines.append(f"找到 {len(name_attrs)} 个可能相关的属性:")
            for attr in name_attrs:
                try:
                    attr_value = getattr(model, attr)
                    if isinstance(attr_value, (str, int, float, bool, list, dict)):
                        info_lines.append(f"  {attr}: {attr_value}")
                    else:
                        info_lines.append(f"  {attr}: <{type(attr_value).__name__}>")
                except Exception as e:
                    info_lines.append(f"  {attr}: <无法访问: {e}>")
        else:
            info_lines.append("未找到包含'name'的属性")
        
        # 尝试访问常见的模型属性
        info_lines.append("\n" + "-" * 60)
        info_lines.append("常见属性检查:")
        info_lines.append("-" * 60)
        common_attrs = ['model', 'model_config', 'model_options', 'patches', 'patches_list']
        for attr in common_attrs:
            if hasattr(model, attr):
                try:
                    attr_value = getattr(model, attr)
                    info_lines.append(f"  {attr}: <{type(attr_value).__name__}>")
                    # 如果是字典，尝试查找lora相关信息
                    if isinstance(attr_value, dict):
                        lora_keys = [k for k in attr_value.keys() if 'lora' in str(k).lower()]
                        if lora_keys:
                            info_lines.append(f"    包含lora相关的键: {lora_keys}")
                except Exception as e:
                    info_lines.append(f"  {attr}: <无法访问: {e}>")
        
        info_lines.append("\n" + "=" * 60)
        
        inspection_info = "\n".join(info_lines)
        print(inspection_info)  # 同时打印到控制台
        
        return (model, inspection_info)


# 节点类映射：将类名映射到实际的类
NODE_CLASS_MAPPINGS = {
    "PD_ModelInspector": PD_ModelInspector,
}

# 节点显示名称映射：定义在UI中显示的节点名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "PD_ModelInspector": "PD Model Inspector",
}



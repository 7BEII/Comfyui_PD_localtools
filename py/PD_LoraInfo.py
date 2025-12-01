"""
PD LoRA信息输出节点
该模块提供了输出LoRA名称和作用信息的节点
"""

import folder_paths
import os


class PD_LoraInfo:
    """
    PD LoRA信息输出节点
    功能：输出LoRA的名称和作用信息（对model和clip的强度）
    """
    
    @classmethod
    def INPUT_TYPES(s):
        """
        定义节点输入参数类型
        """
        # 获取lora文件列表
        lora_list = folder_paths.get_filename_list("loras")
        
        return {
            "required": {
                "model": ("MODEL", ),  # 输入模型对象
                "clip": ("CLIP", ),  # 输入CLIP对象
                "lora_name": (lora_list, ),  # LoRA文件名列表
                "strength_model": ("FLOAT", {
                    "default": 1.0,
                    "min": -10.0,
                    "max": 10.0,
                    "step": 0.01,
                    "display": "slider"
                }),  # LoRA对model的作用强度
                "strength_clip": ("FLOAT", {
                    "default": 1.0,
                    "min": -10.0,
                    "max": 10.0,
                    "step": 0.01,
                    "display": "slider"
                }),  # LoRA对clip的作用强度
            },
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "STRING")
    RETURN_NAMES = ("model", "clip", "lora_name", "lora_info")
    FUNCTION = "get_lora_info"
    CATEGORY = "PD/Model"

    def get_lora_info(self, model, clip, lora_name, strength_model, strength_clip):
        """
        获取并输出LoRA信息
        
        参数：
        - model: 模型对象
        - clip: CLIP对象
        - lora_name: LoRA文件名
        - strength_model: LoRA对model的作用强度
        - strength_clip: LoRA对clip的作用强度
        
        返回：
        - model: 原样返回模型对象
        - clip: 原样返回CLIP对象
        - lora_name: LoRA名称字符串
        - lora_info: LoRA详细信息字符串
        """
        # 提取纯文件名（去除路径和扩展名）
        lora_base_name = os.path.splitext(os.path.basename(lora_name))[0]
        
        # 构建详细信息字符串
        info_lines = []
        info_lines.append("=" * 60)
        info_lines.append("LoRA 信息")
        info_lines.append("=" * 60)
        info_lines.append(f"LoRA 名称: {lora_base_name}")
        info_lines.append(f"完整路径: {lora_name}")
        info_lines.append(f"Model 强度: {strength_model:.2f}")
        info_lines.append(f"CLIP 强度: {strength_clip:.2f}")
        info_lines.append("=" * 60)
        
        # 添加作用说明
        if strength_model != 0:
            if strength_model > 0:
                info_lines.append(f"✓ LoRA 对 Model 有正向作用 (强度: {strength_model:.2f})")
            else:
                info_lines.append(f"✓ LoRA 对 Model 有负向作用 (强度: {strength_model:.2f})")
        else:
            info_lines.append("○ LoRA 对 Model 无作用")
            
        if strength_clip != 0:
            if strength_clip > 0:
                info_lines.append(f"✓ LoRA 对 CLIP 有正向作用 (强度: {strength_clip:.2f})")
            else:
                info_lines.append(f"✓ LoRA 对 CLIP 有负向作用 (强度: {strength_clip:.2f})")
        else:
            info_lines.append("○ LoRA 对 CLIP 无作用")
        
        lora_info = "\n".join(info_lines)
        
        # 打印到控制台
        print(lora_info)
        
        return (model, clip, lora_base_name, lora_info)


class PD_LoraInfoSimple:
    """
    PD LoRA信息输出节点（简化版）
    功能：仅输出LoRA的名称和作用信息，不需要model和clip输入
    """
    
    @classmethod
    def INPUT_TYPES(s):
        """
        定义节点输入参数类型
        """
        # 获取lora文件列表
        lora_list = folder_paths.get_filename_list("loras")
        
        return {
            "required": {
                "lora_name": (lora_list, ),  # LoRA文件名列表
                "strength_model": ("FLOAT", {
                    "default": 1.0,
                    "min": -10.0,
                    "max": 10.0,
                    "step": 0.01,
                    "display": "slider"
                }),  # LoRA对model的作用强度
                "strength_clip": ("FLOAT", {
                    "default": 1.0,
                    "min": -10.0,
                    "max": 10.0,
                    "step": 0.01,
                    "display": "slider"
                }),  # LoRA对clip的作用强度
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("lora_name", "lora_info")
    FUNCTION = "get_lora_info_simple"
    CATEGORY = "PD/Model"

    def get_lora_info_simple(self, lora_name, strength_model, strength_clip):
        """
        获取并输出LoRA信息（简化版）
        
        参数：
        - lora_name: LoRA文件名
        - strength_model: LoRA对model的作用强度
        - strength_clip: LoRA对clip的作用强度
        
        返回：
        - lora_name: LoRA名称字符串
        - lora_info: LoRA详细信息字符串
        """
        # 提取纯文件名（去除路径和扩展名）
        lora_base_name = os.path.splitext(os.path.basename(lora_name))[0]
        
        # 构建详细信息字符串
        info_lines = []
        info_lines.append("=" * 60)
        info_lines.append("LoRA 信息")
        info_lines.append("=" * 60)
        info_lines.append(f"LoRA 名称: {lora_base_name}")
        info_lines.append(f"完整路径: {lora_name}")
        info_lines.append(f"Model 强度: {strength_model:.2f}")
        info_lines.append(f"CLIP 强度: {strength_clip:.2f}")
        info_lines.append("=" * 60)
        
        # 添加作用说明
        if strength_model != 0:
            if strength_model > 0:
                info_lines.append(f"✓ LoRA 对 Model 有正向作用 (强度: {strength_model:.2f})")
            else:
                info_lines.append(f"✓ LoRA 对 Model 有负向作用 (强度: {strength_model:.2f})")
        else:
            info_lines.append("○ LoRA 对 Model 无作用")
            
        if strength_clip != 0:
            if strength_clip > 0:
                info_lines.append(f"✓ LoRA 对 CLIP 有正向作用 (强度: {strength_clip:.2f})")
            else:
                info_lines.append(f"✓ LoRA 对 CLIP 有负向作用 (强度: {strength_clip:.2f})")
        else:
            info_lines.append("○ LoRA 对 CLIP 无作用")
        
        lora_info = "\n".join(info_lines)
        
        # 打印到控制台
        print(lora_info)
        
        return (lora_base_name, lora_info)


class PD_LoraInfoMulti:
    """
    PD 多LoRA信息输出节点
    功能：支持多个LoRA，输出所有LoRA的名称和作用信息
    """
    
    @classmethod
    def INPUT_TYPES(s):
        """
        定义节点输入参数类型
        """
        # 获取lora文件列表
        lora_list = folder_paths.get_filename_list("loras")
        
        return {
            "required": {
                "model": ("MODEL", ),  # 输入模型对象
                "clip": ("CLIP", ),  # 输入CLIP对象
            },
            "optional": {
                "lora_1_name": (["None"] + lora_list, {"default": "None"}),
                "lora_1_strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lora_1_strength_clip": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lora_2_name": (["None"] + lora_list, {"default": "None"}),
                "lora_2_strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lora_2_strength_clip": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lora_3_name": (["None"] + lora_list, {"default": "None"}),
                "lora_3_strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lora_3_strength_clip": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "STRING")
    RETURN_NAMES = ("model", "clip", "lora_names", "lora_info")
    FUNCTION = "get_multi_lora_info"
    CATEGORY = "PD/Model"

    def get_multi_lora_info(self, model, clip, **kwargs):
        """
        获取并输出多个LoRA信息
        
        参数：
        - model: 模型对象
        - clip: CLIP对象
        - kwargs: 包含多个lora的参数
        
        返回：
        - model: 原样返回模型对象
        - clip: 原样返回CLIP对象
        - lora_names: 所有LoRA名称（逗号分隔）
        - lora_info: 所有LoRA详细信息字符串
        """
        lora_list = []
        info_lines = []
        info_lines.append("=" * 60)
        info_lines.append("多 LoRA 信息")
        info_lines.append("=" * 60)
        
        # 处理最多3个LoRA
        for i in range(1, 4):
            lora_name_key = f"lora_{i}_name"
            strength_model_key = f"lora_{i}_strength_model"
            strength_clip_key = f"lora_{i}_strength_clip"
            
            if lora_name_key in kwargs and kwargs[lora_name_key] != "None":
                lora_name = kwargs[lora_name_key]
                strength_model = kwargs.get(strength_model_key, 1.0)
                strength_clip = kwargs.get(strength_clip_key, 1.0)
                
                # 提取纯文件名
                lora_base_name = os.path.splitext(os.path.basename(lora_name))[0]
                lora_list.append(lora_base_name)
                
                # 添加信息
                info_lines.append(f"\nLoRA {i}:")
                info_lines.append(f"  名称: {lora_base_name}")
                info_lines.append(f"  Model 强度: {strength_model:.2f}")
                info_lines.append(f"  CLIP 强度: {strength_clip:.2f}")
        
        if not lora_list:
            info_lines.append("\n未配置任何 LoRA")
            lora_names = "无"
        else:
            lora_names = ", ".join(lora_list)
            info_lines.append(f"\n总计: {len(lora_list)} 个 LoRA")
        
        info_lines.append("=" * 60)
        
        lora_info = "\n".join(info_lines)
        
        # 打印到控制台
        print(lora_info)
        
        return (model, clip, lora_names, lora_info)


# 节点类映射：将类名映射到实际的类
NODE_CLASS_MAPPINGS = {
    "PD_LoraInfo": PD_LoraInfo,
    "PD_LoraInfoSimple": PD_LoraInfoSimple,
    "PD_LoraInfoMulti": PD_LoraInfoMulti,
}

# 节点显示名称映射：定义在UI中显示的节点名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "PD_LoraInfo": "PD LoRA Info",
    "PD_LoraInfoSimple": "PD LoRA Info (Simple)",
    "PD_LoraInfoMulti": "PD LoRA Info (Multi)",
}


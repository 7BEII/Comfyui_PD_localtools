import torch

class PD_ImageCrop_Multi:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),  # 输入图像 [B, H, W, C]
                "n": ("INT", {"default": 3, "min": 2, "max": 64, "step": 1}),
                "axis": (["Y (Vertical)", "X (Horizontal)"], {"default": "Y (Vertical)"}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "crop_multi"
    CATEGORY = "PD_Nodes"

    def crop_multi(self, image, n, axis):
        # 获取图像维度 [Batch, Height, Width, Channels]
        B, H, W, C = image.shape
        
        output_slices = []

        if axis == "Y (Vertical)":
            # 基于 Y 轴（上下）平分
            slice_size = H // n  # 使用整除确保尺寸一致
            for i in range(n):
                start = i * slice_size
                end = start + slice_size
                # 切片维度：[批次, 高度范围, 宽度, 通道]
                output_slices.append(image[:, start:end, :, :])
        else:
            # 基于 X 轴（左右）平分
            slice_size = W // n
            for i in range(n):
                start = i * slice_size
                end = start + slice_size
                # 切片维度：[批次, 高度, 宽度范围, 通道]
                output_slices.append(image[:, :, start:end, :])

        # 将所有切片在 Batch 维度 (dim=0) 上合并
        # 如果原始 B=1, n=3，合并后结果为 [3, H_new, W_new, C]
        combined_batch = torch.cat(output_slices, dim=0)

        return (combined_batch,)

NODE_CLASS_MAPPINGS = {
    "PD_ImageCrop_Multi": PD_ImageCrop_Multi
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PD_ImageCrop_Multi": "PD Image Crop Multi (Batch)"
}
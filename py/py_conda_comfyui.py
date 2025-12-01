# 1. 创建并激活环境
conda create -n comfyui python=3.8
conda activate comfyui

# 2. 安装 PyTorch
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118

# 3. 安装 transformers
pip install transformers==4.32.0

# 4. 安装其他依赖
pip install Pillow
pip install huggingface-hub

# 5. 安装 ComfyUI 依赖
pip install -r requirements.txt

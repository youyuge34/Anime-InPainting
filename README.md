## AnimeInPaint: An demo application of [Edge-Connect](https://github.com/knazeri/edge-connect) (WIP)
[ArXiv](https://arxiv.org/abs/1901.00212) | [BibTex](#citation)

English | [中文版介绍](#jump_zh)     

### Demo show time
#### Demo results:
<img src="files/demo_shortcut2.jpg" width="450" height="240">
<img src="files/demo_house.jpg" width="425" height="400">

#### Demo using
<img src="files/cut2.gif" width="425" height="425">


Well trained model validation sample (weights files are provided below):
<img src="files/2069500.png" width="640" height="380">

### Introduction:
This is an optimized demo application has a frontend based on opencv, whose backend used [Edge-Connect](https://github.com/knazeri/edge-connect). Make sure you have read their awesome work and license thoroughly.
Compared with the original work, this project has such improvements:    
- Add demo application modes
- Optimize the training phase
  - Auto-save and auto-load latest weights files
  - Add a fast training phase combined with origin phase 2 and 3
- bugs fixed (most of them are merged into the original work)
- Add config of print frequency
- ... ...



## Prerequisites
- Python 3
- PyTorch `1.0` (`0.4` is not supported)
- NVIDIA GPU + CUDA cuDNN

## Installation
- Clone this repo
- Install PyTorch and dependencies from http://pytorch.org
- Install python requirements:
```bash
pip install -r requirements.txt
```

## Datasets

> continuous...

# <span id="jump_zh">中文版介绍 (WIP)</span>
魔改版……
填完坑再写readme



## License
Licensed under a [Creative Commons Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/).

Except where otherwise noted, this content is published under a [CC BY-NC](https://creativecommons.org/licenses/by-nc/4.0/) license, which means that you can copy, remix, transform and build upon the content as long as you do not use the material for commercial purposes and give appropriate credit and provide a link to the license.


## Citation
If you use this code for your research, please cite our paper <a href="https://arxiv.org/abs/1901.00212">EdgeConnect: Generative Image Inpainting with Adversarial Edge Learning</a>:

```
@inproceedings{nazeri2019edgeconnect,
  title={EdgeConnect: Generative Image Inpainting with Adversarial Edge Learning},
  author={Nazeri, Kamyar and Ng, Eric and Joseph, Tony and Qureshi, Faisal and Ebrahimi, Mehran},
  journal={arXiv preprint},
  year={2019},
}
```


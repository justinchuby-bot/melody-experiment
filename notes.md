# 🎵 Melody Experiment — Notes

## 2026-04-23: 三个音乐实验

### 实验1: Canon (对位法) — `canon_experiment.py`
- 三声部卡农：Violin I → Violin II (延迟2小节) → Cello (延迟4小节，低八度)
- 主题8小节，C大调，tempo=72
- 发现：低八度大提琴进入时整个织体突然变厚实，很好听

### 实验2: Phase Shift (Steve Reich) — `phase_shift.py`
- 两个马林巴声部弹同一个8音循环 (E F# G A B C B A)
- 声部2每循环比声部1提前0.25拍，33个循环后重新对齐
- 发现：中间产生的"幻影旋律"效果很明显，尤其在相位差=半个循环时

### 实验3: Blues Night — `blues_night.py`
- A blues scale, 12-bar blues, tempo=78 (慢，深夜感)
- 配器：Rhodes + Upright Bass (walking) + Brushes
- Swing feel 用 2/3+1/3 拍分割实现
- 场景：Kirkland 深夜 I-405，random seed = 405 🛣️
- 发现：Eb (blue note) 出现的地方情感张力最强

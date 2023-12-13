## 框架结构设计

### 矩阵位移法计算

源码位于`frame_structure\matrix_displacement_method`

### opensees验证

源码位于`frame_structure\opensees_code`

### D值法自动化计算与可视化

**源码位置**

* 计算源码位于`frame_structure\D_value_code`
* 网页可视化服务端源码位于`frame_structure\flask-server`
* 客户端源码位于`frame_structure\web-site`

**介绍**

为了体现“智能建造课程设计VI-框架结构设计”中的智能性，次程序主要讨论编程的思想实现简单结构下D值法的自动计算，作为课程设计的拓展部分。

（1）D值法手算存在的问题

在D值法的计算中，涉及到的流程如图下所示，主要可以概括为三个核心步骤。首先是D值的计算，该计算过程中涉及到的侧移刚度修正系数的求解，这需要进行复杂且繁琐的计算。第二步是确定反弯点的位置，这一步骤需要参考多个表格，而这些表格往往有着各种不同的规则。最后一步是计算弯矩值，这一步涉及到重复而复杂的迭代计算。因此，手动进行D值法计算将会是一个十分繁杂的过程。在工程实践中，我们通常只关注最终的分析结果，而计算过程本身却可能耗费大量的时间和精力。若能使用自动化的程序对D值法这些重复的步骤进行计算，将会大大节省时间并将精力集中于分析受力结果。

![img](https://github.com/Asionm/structure-design/blob/main/README.assets/clip_image002.png)

（2）编程实现D值法计算

计算所使用的编程语言为Python，程序的处理流程如下图所示。该流程首先涉及到将模型的几何结构、受力信息以及材料截面等信息写入系统。接着，这些信息以类和对象的形式存储，其中包括节点与杆件的详细信息以及它们之间的空间关系。随后，系统载入包含反弯点数据的json文件，并执行插值操作以便于后续使用。基于节点的空间信息，系统遍历计算出每个节点的𝛼𝑐值。然后，利用楼层信息和i值来确定反弯点的高度比v。接下来，系统计算D值，然后计算每个反弯点处的剪力Vim。有了这些数据，系统进一步计算出各个节点的弯矩值。最后，利用这些计算结果绘制出弯矩图，为结构分析提供直观的视图。

![img](https://github.com/Asionm/structure-design/blob/main/README.assets/clip_image002-17024619459071.png)

**可视化网页程序**

演示网页位于：https://asionm.github.io/structure-design/

![demo](https://github.com/Asionm/structure-design/blob/main/README.assets/demo.gif)

*注意：程序尚未完善，因此只能输入简单的结构与受力情况，且层数不能超过12层。*


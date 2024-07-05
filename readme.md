# GameQuick 教程

## GameQuick 简介

GameQuick 是一个基于 pygame 的游戏开发框架，旨在帮助开发者快速构建游戏原型和游戏开发。它提供了一套较为完整的工具和组件，使得开发者可以更加高效地进行游戏开发。

## GameQuick 安装

你可以通过 pip 安装 GameQuick：

```bash
pip install gamequick
```

## GameQuick 使用

### GameQuick 基本概念

在 GameQuick 中，游戏被分为了多个部分：游戏窗口（Stage）、游戏对象（Sprite）和游戏脚本。

#### 游戏窗口（Stage）

游戏窗口是游戏运行的环境，所有的游戏对象都在游戏窗口中显示和交互。游戏窗口的大小、标题、背景等属性可以通过 Stage 类进行设置。

#### 游戏对象（Sprite）

游戏对象是游戏中的基本元素，如角色、道具、背景等。游戏对象可以通过 Sprite 类来创建，并可以设置游戏对象的图片等。

#### 游戏脚本

游戏脚本用于控制游戏对象的行为和逻辑。游戏脚本可以设置游戏对象的属性、方法，并可以通过事件机制来响应游戏对象的状态变化。

游戏脚本被游戏窗口控制（而不是游戏对象），这使得游戏对象的创建与游戏脚本的编写可以相互独立开来，因此更利于新手入门。

### GameQuick 第一个程序

#### 创建窗口

在开始一切游戏编写之前，我们应该先创建一个游戏窗口。

```python
from gamequick import Stage

stage = Stage(800, 600)
stage.title("GameQuick")
stage.add_background_load("background.png")

...

stage.mainloop()
```

这会显示一个800x600 的窗口，窗口的标题是 "GameQuick"，背景图片是 "background.png"。

如果你的图片尺寸不是800x600，不用担心，GameQuick 会自动调整图片尺寸以适应窗口。

接下来，我们创建一个角色。

#### 创建角色

```python
from gamequick import Stage, Sprite

stage = Stage(800, 600)
stage.title("GameQuick")
stage.add_background_load("background.png")

player = Sprite(stage, SpImage.load("player.png"), (400, 300))

stage.mainloop()
```

这会创建一个角色，角色的图片是 "player.png"，角色的位置是 (400, 300)，角色被添加到游戏窗口中，游戏窗口会显示角色。

接下来，我们需要让角色动起来。

#### 创建脚本

让我们先从最简单的脚本开始。我们需要让图片向上移动起来。

```python
... # 这里填入上面的代码

def move():
    speed = 100
    while True:
        delta = yield
        player.move(speed * delta)

stage.add_script(move())

stage.mainloop()
```

这会创建一个脚本，脚本会不断向上移动角色，移动的速度是 100 像素每秒。当你启动程序后，你的角色应该会很快移动出屏幕外面。

自此，你已经完成了你的第一个 GameQuick 程序。

### GameQuick 角色的移动和旋转

#### 角色移动

让我们还是回到我们的第一个程序。

```python
from gamequick import Stage, Sprite

stage = Stage(800, 600)
stage.title("GameQuick")
stage.add_background_load("background.png")

player = Sprite(stage, SpImage.load("player.png"), (400, 300))

stage.mainloop()
```

现在，让我们让角色动起来。

```python
def move():
    speed = 100
    while True:
        delta = yield
        player.move(speed * delta)

stage.add_script(move())
```

`Sprite.move`接受一个参数，即移动的距离。然后Sprite会朝着自己的方向（见下一节）移动这段距离。

为什么我们使用yield？因为即使 GameQuick 在不断控制 fps，但是仍然会有一些时间差，因此我们需要使用yield来控制移动的速度。`delta`就是时间差，单位是秒。这样，我们就可以让角色以恒定的速度移动。这在游戏开发中是非常常见的做法。

在 GameQuick 中，一个yield便是一帧。

#### 角色旋转

角色旋转和移动十分类似，只需要调用 `Sprite.rotate`即可。

```python
def rotate():
    omega = 360
    while True:
        delta = yield
        player.rotate(omega * delta)

stage.add_script(rotate())
```

`Sprite.rotate`接受一个参数，即旋转的角度，单位是角度。然后 Sprite 会朝着自己的方向旋转这个角度。

当角色角度为 0 时，角色朝向上方。当角色角度为 90 时，角色朝向右方。

为什么我们使用角度值而不是弧度制？尽管弧度制在数学计算上更为便捷，但是角度制更符合人类直觉，而且角度制在游戏开发中更常用。

#### 角色转圈

现在你可以将 `move`和 `rotate`组合起来，让角色转圈。

```python
def circle():
    speed = 100
    omega = 360
    while True:
        delta = yield
        player.move(speed * delta)
        player.rotate(omega * delta)

stage.add_script(circle())
```

现在，你的角色应该会转圈了。

#### 角色的另一种转圈——旋转中心

在 GameQuick 中，还有一个非常重要的概念，便是旋转中心。

旋转中心是角色旋转的基准点，也是角色移动时的基准点。当你获取角色坐标时，你实际获取的，其实是角色旋转中心的坐标。默认情况下，旋转中心是角色图片的中心。

你可以在一开始输入图片时设置角色的旋转中心：

```python
from gamequick import Stage, Sprite

stage = Stage(800, 600)
stage.title("GameQuick")
stage.add_background_load("background.png")

# 设置图片的旋转中心为(0,0)点，即图片的左上角
player = Sprite(stage, SpImage.load("player.png", (0, 0)), (400, 300))

# 旋转图片
def rotate():
    omega = 360
    while True:
        delta = yield
        player.rotate(omega * delta)

stage.add_script(rotate())

stage.mainloop()
```

这时，你会看到，角色会绕着左上角开始旋转。

实际上，角色的旋转中心并不一定在角色图片内部，因此你只通过设置旋转中心，便可以让角色绕着任何一点旋转。
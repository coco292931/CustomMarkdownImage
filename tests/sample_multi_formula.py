import pillowmd

"""
回归测试：同一段文本中多个行内/行间公式的渲染

修复前（v0.7.3）的 BUG：
    当某个公式渲染出的子图数量恰好等于它在源码中占用的字符数时
    （例如 "x"、"y=x" 这类简单公式），绘制阶段的
    `nowlatexImageIdx >= len(images)` 分支永远不会触发，
    导致 `del latexs[0]` 不执行、过期条目滞留在 latexs[0]，
    其后的所有公式都会匹配不到绘制窗口、退化成字面文本。

修复后（v0.7.4）：
    在绘制循环开头丢弃 end 已被 idx 越过的过期条目，
    下方所有公式都能被正确消费、渲染为公式图像。

人工核对要点（运行后看弹出的图）：
    - 简单公式 $y=x$、$x$ 之后的 $\\frac{...}$ 应为公式而非字面文本
    - 用户实测用例中的 f_x(0,0)、f_y(0,0)、末尾的复杂分式应全部为公式
"""


def run():
    text = (
        "## 多公式回归用例\n\n"
        # 简单公式在前，之前会毒化其后的所有公式
        "一行多个：$y=x$ 和 $\\frac{x}{y}$ 完\n\n"
        "简单打头：$x$，随后 $\\frac{a}{b}$、$\\frac{c}{d}$\n\n"
        # 用户实测用例
        "用定义 $f_x(0,0) = \\lim\\limits_{h\\to0}\\frac{f(h,0)-0}{h} = 0$，"
        "同理 $f_y(0,0) = 0$\n\n"
        "沿 $y=x$ 路径 $\\frac{x^3/(2x^2)}{\\sqrt{2}|x|} = "
        "\\frac{x}{2\\sqrt{2}|x|} \\not\\to 0$\n"
    )
    import pillowmd

    img = pillowmd.SampleStyles.STYLE1.Render(text, title="多公式回归")
    img.image.show()


if __name__ == "__main__":
    run()

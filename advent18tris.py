# best solution (not from me)
import re


class x(int):
    def __floordiv__(self, other):
        return x(int(self) + other)

    def __mul__(self, other):
        return x(int(self) * other)

    def __pow__(self, other):
        return x(int(self) + other)


lines = open("input18.txt").readlines()
eval_ex = lambda ex, ol: eval(re.sub(r"(\d+)", r"x(\1)", ex.replace("+", ol)))
print(sum(eval_ex(line, "//") for line in lines))
print(sum(eval_ex(line, "**") for line in lines))

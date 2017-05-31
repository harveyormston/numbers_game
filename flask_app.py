from flask import Flask
from flask import render_template
from flask import request
import random


def random_op(a, b):

    ops = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
    }

    keys = ['+', '-']

    if a != 1 and b != 1:
        ops["x"] = lambda x, y: x * y
        keys.append('x')

    if a % b == 0 and b != 1:
        ops['/'] = lambda x, y: x // y
        keys.append('/')

    while 1:
        oname = random.choice(keys)
        op = ops[oname]

        if a > b and oname == '-':
            tmp = a
            a = b
            b = tmp

        ans = op(a, b)
        step = "{0} {1} {2} = {3}".format(a, oname, b, ans)
        if ans > 0:
            break

    return ans, step


def gen_answer(numbers):

    steps = []

    a = numbers[0]
    b = numbers[1]
    total, step = random_op(a, b)
    steps.append(step)

    i = 2
    tmp = None
    while i <= 5:

        if tmp is not None:
            a = total
            b = tmp
            total, step = random_op(a, b)
            steps.append(step)
            tmp = None
        elif random.randint(0, 1) == 1 or i >= 4:
            a = total
            b = numbers[i]
            i += 1
            total, step = random_op(a, b)
            steps.append(step)
        else:
            a = numbers[i]
            b = numbers[i + 1]
            i += 2
            tmp, step = random_op(a, b)
            steps.append(step)

        if random.randint(1, 20) == 20:
            if tmp is not None:
                steps.pop()
            break

    return total, steps


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def countdown():

    show = 'ShowSolution' in request.form

    if show:
        top = request.form['top']
        numbers = request.form['numbers']
        target = request.form['target']
        solution = request.form['solution']
    else:
        bottom_row = list(range(1, 11))
        top_row = [100, 75, 50, 25]
        numbers = []
        top = random.randint(0, 4)

        for _ in range(top):
            numbers.append(random.choice(top_row))

        for _ in range(6 - top):
            numbers.append(random.choice(bottom_row))

        random.shuffle(numbers)
        while 1:
            total, steps = gen_answer(numbers)
            if total > 99 and total < 999:
                break

        random.shuffle(numbers)

        numbers = u", ".join(str(n) for n in numbers)
        target = u"{0}.".format(total)
        solution = u"; ".join(str(step) for step in steps)

    return render_template(
        'template.html',
        top=str(top),
        numbers=numbers,
        target=target,
        solution=solution,
        show=show)

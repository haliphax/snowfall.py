from random import seed, randint
from sys import stdout
from blessed import Terminal

layers = ([], [], [],)
term = Terminal()
lastrow = [u' ' for i in range(term.width)]
snow = (term.bright_black(u'.'), term.white(u','), term.bright_white(u'*'))
progress_template = u' _.,m%#@'
prog_len = len(progress_template)
progress = {}
seed()
iteration = 0
layers_length = len(layers)
last = layers_length - 1
rollover = last * 2


def generate_line(layer):
    line = []
    limit = layer * 10
    threshold = layer * 9.9

    for i in range(term.width):
        if randint(0, limit) < threshold:
            line.append(False)
        else:
            line.append(True)

    return line

for i in range(layers_length):
    offset = 1 if i < last else 0

    for j in range(term.height - offset):
        layers[i].append(generate_line(i + 1))

for i in range(prog_len - 1):
    progress[progress_template[i]] = progress_template[i + 1]

progress[progress_template[prog_len - 1]] = progress_template[prog_len - 1]

with term.fullscreen(), term.hidden_cursor():
    while not term.inkey(timeout=0.15):
        out = term.move(0, 0)

        for i in range(term.height - 1):
            for j in range(term.width):
                any = False

                for k in reversed(range(len(layers))):
                    if layers[k][i][j]:
                        any = True
                        out += snow[k]
                        break

                if not any:
                    out += u' '

            out += u'\n'

        if iteration == 0:
            for j in range(term.width):
                if layers[2][term.height - 1][j]:
                    lastrow[j] = progress[lastrow[j]]

            out += term.bright_white(u''.join(lastrow))

        stdout.write(out)
        stdout.flush()
        iteration = (iteration + 1) % rollover
        layers[last].pop()
        layers[last].insert(0, generate_line(1))

        for i in reversed(range(1, last)):
            if iteration % (i * 2) == 0:
                layers[i].pop()
                layers[i].insert(0, generate_line(i + 1))

        if iteration == 0:
            layers[0].pop()
            layers[0].insert(0, generate_line(layers_length))

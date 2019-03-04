

def strip_lines(astr):
    lines = []
    for l in astr.split('\n'):
        lines.append(l.strip())
    return ''.join(lines)
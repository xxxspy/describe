

def strip_lines(astr):
    lines = []
    for l in astr.split('\n'):
        lines.append(l.strip())
    return ''.join(lines)

def valid_fpath(fpath: str):
    return fpath.replace('|', ' ')
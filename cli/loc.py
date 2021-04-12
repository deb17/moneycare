import os


def file_len(filename, comment):

    line_count = 0
    with open(filename) as f:
        for line in f:
            if line.strip().startswith(comment):
                continue
            if line.strip():
                line_count += 1

    return line_count


def walk(path='.'):

    loc = 0
    for root, dirs, files in os.walk(path):
        if '.git' in root or 'venv' in root:
            continue
        for file in files:
            filepath = os.path.join(root, file)
            if file.endswith('.py'):
                loc += file_len(filepath, '#')
            elif file.endswith('.html'):
                if file in ('privacy_policy.html', 'tac.html'):
                    continue
                loc += file_len(filepath, '<!--')
            elif file.endswith('.css'):
                if file == 'jquery.tagsinput-revisited.css':
                    continue
                loc += file_len(filepath, '/*')
            elif file.endswith('.js'):
                if file == 'jquery.tagsinput-revisited.js':
                    continue
                loc += file_len(filepath, '//')

    return loc

from datetime import datetime

def parse_poems(file_path):
    with open(file_path, 'r') as f:
        content = f.read().split('===')

    poems = []
    for block in content:
        block = block.strip()
        if not block:
            continue
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        if lines[0].startswith('TITLE:'):
            title = lines[0].split('TITLE:', 1)[1].strip()
            content = '\n'.join(lines[1:])
            poems.append({'title': title, 'content': content})
    return poems

def generate_page(poems):
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>Poetry and Notes</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="../styles.css">
    <style>
        .poem-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin: 1rem 0;
        }}

        .poem-cell {{
            padding: 1rem;
            background: #fffec4dd;
            border-radius: 5px;
            text-align: left;  /* Left-align all text in cell */
        }}

        .poem-content {{
            white-space: pre-wrap;
            line-height: 1.6;
            text-align: left;  /* Left-align poem content */
        }}

        @media screen and (max-width: 800px) {{
            .poem-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
<table class="table">
    <tr>
        <td><h1>Poetry and Notes</h1></td>
    </tr>
    <tr>
        <td class="intable">
            <div class="poem-grid">
                {''.join([f'''
                <div class="poem-cell">
                    <h2 style="text-align: left;">{poem["title"]}</h2>
                    <div class="poem-content">{poem["content"]}</div>
                </div>
                ''' for poem in poems])}
            </div>
        </td>
    </tr>
</table>
</body>
</html>
'''

if __name__ == '__main__':
    poems = parse_poems('poems.txt')
    with open('poetry.html', 'w') as f:
        f.write(generate_page(poems))

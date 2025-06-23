import csv
import re

INPUT_CSV = '../../data/raw/raw_messages.csv'
OUTPUT_FILE = '../../sample_conll.txt'
MAX_MESSAGES = 50

def tokenize(text):
    # Split on whitespace and punctuation (keep Amharic and English words)
    # This regex splits on any non-word character, but keeps Amharic, English, and numbers
    tokens = re.findall(r'[\w\u1200-\u137F]+|[\d]+|[.,!?;:()"\'\-]', text)
    return [t for t in tokens if t.strip()]

def main():
    messages = []
    with open(INPUT_CSV, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row.get('text', '').strip()
            if text:
                messages.append(text)
            if len(messages) >= MAX_MESSAGES:
                break

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        for msg in messages:
            tokens = tokenize(msg)
            for token in tokens:
                out.write(f'{token} O\n')
            out.write('\n')  # Blank line between messages

    print(f'Wrote {len(messages)} messages to {OUTPUT_FILE}')

if __name__ == '__main__':
    main() 
import re
import fileinput

def main():
    for line in fileinput.input():
        process = False
        # Skip lines that are specific to SQLite
        for nope in ('BEGIN TRANSACTION', 'COMMIT', 'PRAGMA', 'sqlite_sequence', 'CREATE UNIQUE INDEX'):
            if nope in line: 
                break
        else:
            process = True
        if not process: 
            continue
        
        # Convert "CREATE TABLE" to MySQL syntax
        m = re.search(r'CREATE TABLE "([a-zA-Z_]*)"(.*)', line)
        if m:
            name, sub = m.groups()
            sub = sub.replace('"', '`')  # Replace double quotes with backticks
            sub = sub.replace('AUTOINCREMENT', 'AUTO_INCREMENT')  # Replace AUTOINCREMENT with AUTO_INCREMENT
            line = f'''DROP TABLE IF EXISTS `{name}`;
CREATE TABLE IF NOT EXISTS `{name}`{sub}
'''
        
        # Convert "INSERT INTO" to MySQL syntax
        else:
            m = re.search(r'INSERT INTO "([a-zA-Z_]*)"(.*)', line)
            if m:
                line = 'INSERT INTO %s%s\n' % m.groups()
                line = line.replace('"', '`')  # Replace double quotes with backticks
                line = line.replace("''", "'")  # Ensure single quotes are properly escaped in MySQL

        # Replace 't' and 'f' for boolean values (SQLite uses 't'/'f', MySQL uses 1/0)
        line = re.sub(r"([^'])'t'(.)", "\\1THIS_IS_TRUE\\2", line)
        line = line.replace('THIS_IS_TRUE', '1')
        line = re.sub(r"([^'])'f'(.)", "\\1THIS_IS_FALSE\\2", line)
        line = line.replace('THIS_IS_FALSE', '0')

        # Handle indexes and other keywords
        line = line.replace('AUTOINCREMENT', 'AUTO_INCREMENT')
        if re.search('^CREATE INDEX', line):
            line = line.replace('"', '`')

        # Skip the `DELETE FROM sqlite_sequence` line
        if 'DELETE FROM sqlite_sequence' in line:
            continue

        # Output the converted line
        output_file = open('dumpNew.sql', 'a')
        output_file.write(line)

main()

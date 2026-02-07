import os
import subprocess
from datetime import datetime, timedelta

BASE_DATE = datetime(2026, 1, 1, 12, 0, 0)
MAX_COMMITS = 151
EXCLUDE_BASENAMES = {
    'allfiles.txt', 'allfiles_no_git.txt', 'allfiles_project.txt',
    'untracked.txt', 'untracked_clean.txt', 'untracked_clean2.txt',
    'untracked_files.txt', 'untracked_all.txt', 'untracked_raw.txt',
    'commit_file_list.txt', 'commit_summary.txt'
}

with open('commit_file_list.txt', 'r', encoding='utf-8') as f:
    paths = [line.strip() for line in f if line.strip()]

usable = []
for path in paths:
    basename = os.path.basename(path)
    if basename in EXCLUDE_BASENAMES:
        continue
    if basename.startswith('allfiles') or basename.startswith('untracked'):
        continue
    if not os.path.exists(path):
        continue
    usable.append(path)

usable = usable[:MAX_COMMITS]
if len(usable) < MAX_COMMITS:
    raise SystemExit(f'Not enough usable files: {len(usable)} available, {MAX_COMMITS} required.')

summary_lines = []
current_date = BASE_DATE
for path in usable:
    msg = f'Add {os.path.basename(path)}'
    print(f'Committing {path} on {current_date.date()}')
    subprocess.check_call(['git', 'add', path])
    env = os.environ.copy()
    date_str = current_date.strftime('%Y-%m-%dT%H:%M:%S')
    env['GIT_AUTHOR_DATE'] = date_str
    env['GIT_COMMITTER_DATE'] = date_str
    subprocess.check_call(['git', 'commit', '-m', msg], env=env)
    commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], env=env).strip().decode('utf-8')
    summary_lines.append(f'{current_date.strftime("%Y-%m-%d")}	{path}	{commit_hash}')
    current_date += timedelta(days=1)

with open('commit_summary.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(summary_lines))

print('COMMIT_DONE')
print(f'{len(summary_lines)} commits created.')

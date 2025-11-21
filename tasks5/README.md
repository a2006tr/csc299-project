Tasker — simple JSON-backed task CLI
===================================

Quick prototype demonstrating separation between a storage module and a CLI.

Run the CLI (from the repo root):

python -m tasker.cli --data ./.tasker/tasks.json add "Buy milk" --description "2 liters"
python -m tasker.cli --data ./.tasker/tasks.json list
python -m tasker.cli --data ./.tasker/tasks.json search milk

Run tests:

Install dev deps:
pip install -r requirements.txt

Then run:
pytest -q

# Pythonchess

## How to install

Download `pyhton3` and `git`. `pyhton3.10` is recommendable but others work too.

The following instructions are for linux. If you don't know how to apply them for your OS
(i.e. windows or mac), consider prompting ChatGPT to translate them to your OS.

```
git clone https://github.com/PraxTube/chess-ai.git
cd chess-ai
python3.10 -m venv venv
```

Now for linux
```
source venv/bin/activate
```


And for windows

```
venv/Scripts/activate
```

After that install the requirements for this project
```
pip install -r requirements.txt
pip install -e .
```

You can now run the project file with
```
pyhton main.py
```

### Milestone II

- \[X\] Alpha-beta search
- \[X\] Sophisticated Better evaluation function
- \[ \] Unit tests for legal moves
- \[X\] Unit tests for chess engine
- \[ \] Benchmarks that test different depths

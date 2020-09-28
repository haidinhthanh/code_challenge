from os import path
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]
CONSTANT_PATH = path.join(ROOT_PATH, "constant")
LOG_PATH = path.join(ROOT_PATH, "log")
TEST_PATH = path.join(ROOT_PATH, "test_data")
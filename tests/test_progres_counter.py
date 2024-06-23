from scripts.progres_counter import ProgresCounter
import pytest


def test_set_new_task_progres_reset():
    pc = ProgresCounter(0, 100)
    pc.set_new_task('test', 10)
    assert pc.progres == 0


def test_complate_subtask_without_task_set():
    pc = ProgresCounter(0, 100)
    with pytest.raises(ValueError):
        pc.complate_subtask()

    with pytest.raises(ValueError):
        pc.complate_task()


def test_set_new_task_sub_task_compleate():
    pc = ProgresCounter(0, 100)
    pc.set_new_task('test', 4)
    assert pc.progres == 0
    pc.complate_subtask()
    assert pc.progres == 25
    pc.complate_subtask()
    assert pc.progres == 50
    pc.complate_subtask()
    assert pc.progres == 75
    pc.complate_subtask()
    assert pc.progres == 100
    pc.complate_subtask()
    assert pc.progres == 100


def test_set_new_task_task_compleate():
    pc = ProgresCounter(0, 100)
    pc.set_new_task('test', 4)
    assert pc.progres == 0
    pc.complate_task()
    assert pc.progres == 100

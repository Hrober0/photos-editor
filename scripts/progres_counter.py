class ProgresCounter:
    def __init__(self, min: float, max: float) -> None:
        """clas to track long task progress and raport task status in console.
        Data from it can be easy represent by progress bar.
        When new task is set progrs is 0, while subtasks wii be completing
        progress value will be scall to fit aproximated task status.

        Args:
            min: min value
            max: max value
        """
        self._min = min
        self._max = max
        self._progres = None
        self._task_name = None
        self._number_of_tasks = None

    @property
    def progres(self):
        return self._progres

    def set_new_task(self, task_name: str, number_of_tasks: int) -> None:
        """_summary_

        Args:
            task_name: name of procesing tast to display
            number_of_tasks: number of steps(subtasks) in whole task
        """
        self._progres = self._min
        self._task_name = task_name
        self._number_of_tasks = number_of_tasks
        print(f'\nset new long task named: {task_name}\n')

    def complate_subtask(self) -> None:
        """mark part of whole task as done and increase progres

        Raises:
            ValueError: task was not set
        """
        if self._task_name is None:
            raise ValueError('ProgressCounter task was not set')
        self._progres += self._max / self._number_of_tasks
        print(f'\ncomplated subtask {round(self._progres)}/{self._max}\n')
        if self._progres > self._max:
            self.complate_task()

    def complate_task(self) -> None:
        """marks whole task as complteated

        Raises:
            ValueError: task was not set
        """

        if self._task_name is None:
            raise ValueError('ProgressCounter task was not set')
        if (self._progres == self._max):
            return
        self._progres = self._max
        print('\ncomplated task\n')

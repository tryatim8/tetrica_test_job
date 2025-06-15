def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Объединяет пересекающиеся интервалы.
    Если интервалы перекрываются или соприкасаются, они объединяются в один.
    :param intervals: Список интервалов в виде кортежей (начало, конец)
    :return: Новый список объединённых неперекрывающихся интервалов
    """

    if not intervals:
        return []

    intervals.sort()
    merged_intervals = [intervals[0]]

    for start, end in intervals[1:]:
        last_start, last_end = merged_intervals[-1]
        if start <= last_end:
            merged_intervals[-1] = (last_start, max(last_end, end))
        else:
            merged_intervals.append((start, end))

    return merged_intervals


def crop_to_lesson(intervals: list[tuple[int, int]], lesson_start: int, lesson_end: int) -> list[tuple[int, int]]:
    """
    Обрезает интервалы по границам урока.
    Каждый интервал будет приведён к пересечению с интервалом урока,
    или отброшен, если не пересекается с ним.
    :param intervals: Список интервалов
    :param lesson_start: Начало урока
    :param lesson_end: Конец урока
    :return: Список интервалов, обрезанных по границам урока
    """

    cropped_intervals = []

    for start, end in intervals:
        clipped_start = max(start, lesson_start)
        clipped_end = min(end, lesson_end)
        if clipped_start < clipped_end:
            cropped_intervals.append((clipped_start, clipped_end))

    return cropped_intervals


def intersect_intervals(intervals_a: list[tuple[int, int]], intervals_b: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Находит пересечения между двумя списками интервалов.
    Оба списка должны быть отсортированы и не содержать перекрывающихся интервалов внутри себя.
    :param intervals_a: Первый список интервалов (ученик)
    :param intervals_b: Второй список интервалов (учитель)
    :return: Список интервалов, в которых пересекаются интервалы из обоих списков
    """

    intersection_intervals = []
    index_a = index_b = 0

    while index_a < len(intervals_a) and index_b < len(intervals_b):
        start_a, end_a = intervals_a[index_a]
        start_b, end_b = intervals_b[index_b]

        start = max(start_a, start_b)
        end = min(end_a, end_b)

        if start < end:
            intersection_intervals.append((start, end))

        if end_a < end_b:
            index_a += 1
        else:
            index_b += 1

    return intersection_intervals


def appearance(intervals: dict[str, list[int]]) -> int:
    """
    Вычисляет общее время одновременного присутствия ученика и учителя на уроке.
    :param intervals: Словарь с ключами 'lesson', 'pupil', 'tutor'
    :return: Общее время (в секундах) совместного присутствия
    """

    lesson_start, lesson_end = intervals['lesson']

    pupil_intervals_raw = list(zip(intervals['pupil'][::2], intervals['pupil'][1::2]))
    tutor_intervals_raw = list(zip(intervals['tutor'][::2], intervals['tutor'][1::2]))

    pupil_intervals_cropped = crop_to_lesson(pupil_intervals_raw, lesson_start, lesson_end)
    tutor_intervals_cropped = crop_to_lesson(tutor_intervals_raw, lesson_start, lesson_end)

    pupil_intervals = merge_intervals(pupil_intervals_cropped)
    tutor_intervals = merge_intervals(tutor_intervals_cropped)
    overlapping_intervals = intersect_intervals(pupil_intervals, tutor_intervals)

    return sum(end - start for start, end in overlapping_intervals)

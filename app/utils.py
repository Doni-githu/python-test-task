def find_average(arr):
    values = []
    for i in arr:
        values.append(i.value)
    average = sum(values) / len(values)
    return round(average, 1)
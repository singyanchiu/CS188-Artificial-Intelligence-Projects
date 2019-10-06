def quickSort(lst):
    if len(lst) <= 1:
        return lst
    smaller = [x for x in lst[1:] if x < lst[0]]
    larger = [x for x in lst[1:] if x >= lst[0]]
    return quickSort(smaller) + [lst[0]] + quickSort(larger)


# Main Function
if __name__ == '__main__':
    lst = [51,315,1,306,307,29,79,2,8]
    print(quickSort(lst))

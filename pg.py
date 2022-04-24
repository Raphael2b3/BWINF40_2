def find_cheapest_euler_combination(elements, combination_container):
    if len(elements) == 0:
        print(combination_container)
        return
    paar = [elements.pop(-1)]
    for i in range(len(elements)):
        choice = elements.pop(i)
        paar.append(choice)
        combination_container.append(paar)
        find_cheapest_euler_combination(elements, combination_container)
        combination_container.pop(-1)
        elements.insert(i, choice)
        paar.pop(-1)
    elements.append(paar[0])


find_cheapest_euler_combination([1, 2, 3, 4, 5, 6], [])

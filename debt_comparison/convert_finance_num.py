def convert_num(num):
    itera = -1
    k = 0
    for i in num[::-1]:
        if i == '+':
            k += int(num[itera+1:])
            num = num[:itera-1]
            return float(num) * (10 ** k)
        itera -= 1
    try:
        return float(num)
    except:
        return 0


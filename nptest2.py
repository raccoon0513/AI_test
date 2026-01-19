def merge_line(line):
    # 1. 0이 아닌 숫자만 앞으로 모으기
    non_zero = line[line != 0]
    
    # 2. 인접한 숫자가 같으면 합치기
    res = []
    skip = False
    for i in range(len(non_zero)):
        if skip:
            skip = False
            continue
        if i + 1 < len(non_zero) and non_zero[i] == non_zero[i+1]:
            res.append(non_zero[i] * 2)
            skip = True # 합쳐졌으니 다음 숫자는 건너뜀
        else:
            res.append(non_zero[i])
            
    # 3. 나머지를 0으로 채워서 길이 4 맞추기
    return np.array(res + [0] * (4 - len(res)))
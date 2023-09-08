from typing import List, TypeVar, Dict, Unpack
from collections import Counter
import itertools

# 制約 部屋の人数
'''
rooms = [2,10,2,6,10,2,10,6,6,6,6,5,5,5,6,3]

# 制約 各グループの人数
members = {
    "18B" : 6,
    "19B" : 8,
    "20B" : 14,
    "21B" : 6,
    "22B" : 19,
    "23B" : 37,
    "lady" : 5
}
'''

class NoSolutionException(Exception):
    pass

''' 自然数値を与えられた要素を組み合わせて分割
'''
def partition_integer(target : int, units : List[int]) -> List[Counter[int]]:
    # listの先頭を含めるか否か？でDP
    def partition_helper(target: int, units: List[int], current_partition:List[int], all_partitions: List[Counter[int]]) -> None:
        if target == 0:
            # 分割成功
            counter = Counter(current_partition)
            if counter not in all_partitions:
                all_partitions.append(counter)
            return
        if target < 0 or not units:
            # 分割失敗
            return

        # 現在の数を分割パターンに含める場合
        new_partition = current_partition + [units[0]]
        partition_helper(target - units[0], units[1:], new_partition, all_partitions)

        # 現在の数を分割パターンに含めない場合
        partition_helper(target, units[1:], current_partition, all_partitions)

    all_partitions : List[Counter[int]] = []
    partition_helper(target, units, [], all_partitions)
    
    if len(all_partitions) == 0:
        raise NoSolutionException("unsatisfiable")
    return all_partitions

T = TypeVar("T")

# 合法な部屋割か判定
def is_valid_partition(rooms: Counter[int], candidates:List[Counter[int]]) -> bool:
    sum :Counter[int] = Counter()
    for c in candidates:
        sum += c
    #print(sum)
    return rooms == sum
        
def counter2list(counters: Counter[T]) -> List[T]:
    ret : List[T] = []
    for key, val in counters.items():
        for _ in range(val):
            ret.append(key)
    return ret
        
def generate_valid_partition(rooms: List[int], groups: Dict[str, int]) -> List[Dict[str, List[int]]]:
    
    rooms_counter = Counter(rooms)
    partition_candidates : List[List[Counter[int]]] = []
    names : List[str] = []
    # 各グループについて分割候補を生成
    for g,v in groups.items():
        try:
            p = partition_integer(v,rooms)
        except NoSolutionException:
            return []
        partition_candidates.append(p)
        names.append(g)
    
    # 各分割候補が部屋割条件を満たすか全探索
    patterns = itertools.product(*partition_candidates)
    valid_patterns : List[Dict[str, List[int]]] = []
    for pt in patterns:
        valid = is_valid_partition(rooms_counter, list(pt))
        if valid:
            dic : Dict[str, List[int]] = {}
            for key, val in zip(names, pt):
                dic[key] = counter2list(val)
            valid_patterns.append(dic)
    return valid_patterns

'''
rooms = [2,3,5,2,4,4,2]
members = {
    "a" : 5,
    "b" : 2,
    "c" : 5,
    "d" : 10,
}

'''
# 制約 部屋の人数
rooms = [2,10,2,6,10,2,10,6,6,6,6,5,5,5,6,3,5]

# 制約 各グループの人数
members = {
    "18B" : 6,
    "19B" : 8,
    "20B" : 14,
    "21B" : 6,
    "22B" : 19,
    "23B" : 37,
    "lady" : 5
}

print(sum(rooms))
print(sum(members.values()))


ans = generate_valid_partition(rooms, members)
for a in ans:
    print(a)


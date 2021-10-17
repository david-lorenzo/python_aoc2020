from pathlib import Path

data = Path("input9.txt").read_text().split("\n")
nums = list(map(int, data[:-1]))

win_size = 25
window_set = set(nums[:win_size])

pos, target = -1, -1
for i, n in enumerate(nums[win_size:], win_size):
    test = any((n-s1) in window_set for s1 in window_set)
    if not test:
        print(i, n)
        pos, target = i, n
        break
    # updating the window
    window_set.add(n)
    window_set.discard(nums[i-win_size])

try:
    candidates = None
    for group_size in range(2, len(nums)):
        for start_pos in range(0,  len(nums) - group_size):
            group_nums = nums[start_pos:start_pos+group_size]
            res = sum(group_nums)
            if res == target:
                candidates = sorted(group_nums)
                raise StopIteration
except StopIteration:
    pass

low = candidates[0]
high = candidates[-1]
print(low, high, low + high)

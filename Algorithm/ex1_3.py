# -*- coding:utf-8 -*-

# @Time: 2024/1/9 15:23
# @Project: test
# @File: ex1_3.py
# @Author: WSM
"""总和区间最大问题
给定一个实数序列，设计一个最有效的算法，找到一个总和最大的区间。
例如给定序列：1.5,-12.3,3.2,-5.5,23.2,3.2,-1.4,-12.2,34.2,5.4,-7.8,1.1,-4.9
总和最大的区间是从第5个数（23.2）到第10个数（5.4）。
另外一种表述是：寻找一只股票最长的有效增长期。研究股票投资的人都想了解一只股票最长的有效增长期是哪一个时间段，即从哪一天买进到哪一天卖出，收益最大。上面这一组数字可以认为是一只股票每天的涨跌幅度（扣除大盘影响后）。
"""


# 第一种：3重循环
def method1(exlist):
    l = -1
    r = -1
    M = -10e100
    for i in range(len(exlist)):
        for j in range(i, len(exlist)):
            temp = 0
            for t in range(i, j):
                temp += exlist[t]
            if M < temp:
                l = i
                r = j
                M = temp
    print("最大区间左边界序号：", l + 1, exlist[l])
    print("最大区间右边界序号：", r + 1, exlist[r])
    print("最大总和是：", M)


# 第二种：2重循环
def method2(exlist2):
    l = -1
    r = -1
    M = -10e100
    for i in range(len(exlist2)):
        temp = exlist2[i]
        for j in range(i + 1, len(exlist2)):
            temp += exlist2[j]
            if M < temp:
                l = i
                r = j
                M = temp
    print("最大区间左边界序号：", l + 1, exlist2[l])
    print("最大区间右边界序号：", r + 1, exlist2[r])
    print("最大总和是：", M)


# 第三种：分治+递归
def method3(exlist3):
    n = len(exlist3)
    print("n//2=", n // 2)
    if n == 1:
        return exlist3[0]
    else:
        max_left = method3(exlist3[0:n // 2])
        max_right = method3(exlist3[n // 2:n])

    max_l = exlist3[n // 2 - 1]
    temp = 0
    left = 0
    # range (<起点>, <终点>, <增量>)
    for i in range(n // 2 - 1, -1, -1):
        temp += exlist3[i]
        if temp > max_l:
            max_l = temp
            left = i

    max_r = exlist3[n // 2]
    temp = 0
    right = 0
    for j in range(n // 2, n, 1):
        temp += exlist3[j]
        if temp > max_r:
            max_r = temp
            right = j

    print("最大总和是：", max(max_r + max_l, max_left, max_right))
    print("最大区间左边界序号：", left, exlist3[left])
    print("最大区间右边界序号：", right, exlist3[right])
    return max(max_r + max_l, max_left, max_right)


# 第四种：双向线性扫描
def method4(exlist4):
    left, right = 0, 0
    lm, rm = 0, 0
    l, r = 0, 0
    max = 0
    for i in range(len(exlist4)):
        left += exlist4[i]
        if left > lm:
            lm = left
            l = i
    for j in range(len(exlist4) - 1, -1, -1):
        right += exlist4[j]
        if right > rm:
            rm = right
            r = j
    for k in range(r, l + 1, 1):
        max += exlist4[k]
    print("最大总和是：", max)
    print("最大区间左边界序号：", r + 1, exlist4[r])
    print("最大区间右边界序号：", l + 1, exlist4[l])


# 考虑左边界比右边界大这种复杂情况
'''
maxendinghere置0的判断即此时累计的总和<0，
那就意味着之前的较大总和区间在此处往后累加无法得到最大总和。
那此时需将left移至下一位，从下一位开始寻找较大总和。最终得到最大总和及对应区间。
'''
def getMaxSumIntervel4(arrays):
    maxsofar = 0
    maxendinghere = 0
    maxintervel = (0, 0)
    left, right = 0, 0
    for i in range(len(arrays)):
        if maxendinghere + arrays[i] > 0:
            maxendinghere = maxendinghere + arrays[i]
        else:
            maxendinghere = 0
            left = i + 1
        if maxendinghere > maxsofar:
            maxsofar = maxendinghere
            right = i
            maxintervel = (left, right)
    print(maxintervel)
    return maxintervel


if __name__ == '__main__':
    exlist = [1.5, -12.3, 3.2, -5.5, 23.2, 3.2, -1.4, -12.2, 34.2, 5.4, -7.8, 1.1, -4.9]
    method4(exlist)
    method3(exlist)

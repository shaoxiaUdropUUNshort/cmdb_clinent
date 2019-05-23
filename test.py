#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "nothing"
# Date: 2019/5/23


def sift(li, left, right):
    tmp = li[left]
    while left < right:
        while left < right and li[right] >= tmp:
            right -= 1
        li[left] = li[right]
        while left < right and li[left] <= tmp:
            left += 1
        li[right] = li[left]
    li[left] = tmp
    return left


def quick_sort(li, left, right):
    if left < right:
        mid = sift(li, left, right)
        quick_sort(li, left, mid - 1)
        quick_sort(li, mid + 1, right)


li = [4, 5, 8, 9, 6, 4, 8, 7, 3, 5, 4, 4, 6, 8, 0]


def crete_dui(li, low, high):
    i = low
    j = 2 * i + 1
    tmp = li[low]
    while j <= high:
        if j+1 <= high and li[j+1] > li[j]:
            j += 1
        if li[j] > tmp:
            li[i] = li[j]
            i = j
            j = 2 * i + 1
        else:
            break
    li[i] = tmp


def heap_sort(li):
    n = len(li)
    for i in range((n-2)//2, -1, -1):
        crete_dui(li, i, n-1)
    for j in range(n-1, -1, -1):
        li[j], li[0] = li[0], li[j]
        crete_dui(li, 0, j-1)


heap_sort(li)
print(li)







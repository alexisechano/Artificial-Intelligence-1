#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6
import sys
from math import pi, acos, sin, cos
import tkinter
import time
import queue


def calcd(y1, x1, y2, x2):
    y1 = float(y1)
    x1 = float(x1)
    y2 = float(y2)
    x2 = float(x2)
    r = 3958.76
    y1 *= pi/180.0
    x1 *= pi/180.0
    y2 *= pi/180.0
    x2 *= pi/180.0
    return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * r


def readNodes():
    fopen = open("rrNodes.txt")
    nodes = dict()
    for node in fopen:
        nodes[node[:7]] = (float(node[8:17]),float(node[18:28]))
    return nodes


def assignCities():
    fopen = open("rrNodeCity.txt")
    cities = dict()
    for city in fopen:
        coord = city[:7]
        name = city[8:].replace("\n","")
        name = name.replace(" ","_")
        cities[name] = coord
        cities[coord] = name
    return cities


def makeEdges():
    fopen = open("rrEdges.txt")
    edges = dict()
    for edge in fopen:
        start = edge[:7]
        finish = edge[8:15]
        if start in edges.keys():
            edges[start].add(finish)
        else:
            edges[start] = {finish}
        if finish in edges.keys():
            edges[finish].add(start)
        else:
            edges[finish] = {start}
    return edges


# def sumOfEdges(nodes,edges):
#     alreadySeen = set()
#     sum = 0
#     dsum = dict()
#     for start in edges:
#         scoord = nodes[start]
#         for end in edges[start]:
#             if (end,start) in alreadySeen:
#                 continue
#             else:
#                 alreadySeen.add((start,end))
#                 ecoord = nodes[end]
#                 d = calcd(scoord[0],scoord[1],ecoord[0],ecoord[1])
#                 sum += d
#                 dsum[start,end] = d
#     return sum, dsum


def findManhattan(start,goal,nodes):
    sCoord1, sCoord2 = nodes[start]
    gCoord1, gCoord2 = nodes[goal]
    return abs(abs(gCoord1) - abs(sCoord1)) + abs(abs(gCoord2) - abs(sCoord2))


# def puzzling(C, start, goal, nodes, edges, vfactor, wfactor, xscale, yscale, cwidth, circles, lines):
#     # puzzlesRemove = 0
#     # improve = 0
#     # counts = dict()
#     # keysSeen = set()
#     num = 0
#     sums = dict()
#     closedSet = dict()
#     openSet = queue.PriorityQueue()
#     # keysSeen.add(start)
#     # counts[start] = 0
#     if start == goal:
#         # return closedSet, openSet.qsize(), puzzlesRemove, improve
#         return closedSet
#     openSet.put((findManhattan(start, goal, nodes),start,""))
#     sums[start] = 0
#     while openSet:
#         element = openSet.get(0)
#         var = element[1]
#         parent = element[2]
#         # puzzlesRemove += 1
#         # count = counts[var]
#         newList = edges[var]
#         for i in newList:
#             num += 1
#             if i == goal:
#                 # print("var:",var)
#                 closedSet[i] = var
#                 # print(closedSet[i])
#                 closedSet[var] = parent
#                 # print(closedSet[var])
#                 # scoord1, scoord2 = nodes[var]
#                 # x1 = scoord2 * wfactor + xscale
#                 # y1 = -scoord1 * vfactor + yscale
#                 # # print(x1 - cwidth, y1 - cwidth, x1 + cwidth, y1 + cwidth)
#                 C.itemconfig(circles[var],fill="green")
#                 # oval = C.create_oval(x1 - cwidth, y1 - cwidth, x1 + cwidth, y1 + cwidth, fill="green")
#                 # print("parent:", parent, "parentnodes:", nodes[parent])
#                 # ecoord1, ecoord2 = nodes[parent]
#                 # x2 = ecoord2 * wfactor + xscale
#                 # y2 = -ecoord1 * vfactor + yscale
#                 C.itemconfig(circles[parent],fill="green")
#                 # oval = C.create_oval(x2 - cwidth, y2 - cwidth, x2 + cwidth, y2 + cwidth, fill="green")
#                 # line = C.create_line(x1, y1, x2, y2, fill="red")
#                 # C.update()
#                 # time.sleep(0.5)
#                 # scoord1, scoord2 = nodes[i]
#                 # x1 = scoord2 * wfactor + xscale
#                 # y1 = -scoord1 * vfactor + yscale
#                 # print(x1 - cwidth, y1 - cwidth, x1 + cwidth, y1 + cwidth)
#                 C.itemconfig(circles[i],fill="green")
#                 # oval = C.create_oval(x1 - cwidth, y1 - cwidth, x1 + cwidth, y1 + cwidth, fill="green")
#                 # print("parent:", var, "parentnodes:", nodes[var])
#                 # ecoord1, ecoord2 = nodes[var]
#                 # x2 = ecoord2 * wfactor + xscale
#                 # y2 = -ecoord1 * vfactor + yscale
#                 # oval = C.create_oval(x2 - cwidth, y2 - cwidth, x2 + cwidth, y2 + cwidth, fill="green")
#                 # line = C.create_line(x1, y1, x2, y2, fill="red")
#                 # C.update()
#                 # time.sleep(0.5)
#                 # return closedSet, openSet.qsize(), puzzlesRemove, improve
#                 return closedSet
#             if i in closedSet.keys(): continue
#             print("sums[var]:",sums[var])
#             sums[i] = sums[var] + calcd(abs(nodes[var][0]),abs(nodes[var][1]),abs(nodes[i][0]),abs(nodes[i][1]))
#             print("sums[i]:",sums[i])
#             heuristic = findManhattan(i, goal, nodes) + sums[var]
#             print("var:",i,"heuristic:",heuristic)
#             openSet.put((heuristic, i, var))
#             # scoord1, scoord2 = nodes[i]
#             # x1 = scoord2 * wfactor + xscale
#             # y1 = -scoord1 * vfactor + yscale
#             C.itemconfig(circles[i],fill="blue")
#             # C.create_oval(x1 - cwidth, y1 - cwidth, x1 + cwidth, y1 + cwidth, fill="blue")
#             # C.update()
#             # time.sleep(0.5)
#             # counts[i] = count + 1
#         closedSet[var] = parent
#         # print("var:",var,"varnodes:",nodes[var])
#         # scoord1, scoord2 = nodes[var]
#         # x1 = scoord2 * wfactor + xscale
#         # y1 = -scoord1 * vfactor + yscale
#         # print(x1 - cwidth, y1 - cwidth, x1 + cwidth, y1 + cwidth)
#         C.itemconfig(circles[var],fill="green")
#         # oval = C.create_oval(x1 - cwidth, y1 - cwidth, x1 + cwidth, y1 + cwidth, fill="green")
#         # C.update()
#         # time.sleep(0.5)
#         if parent != "":
#             # print("parent:", parent, "parentnodes:", nodes[parent])
#             # ecoord1, ecoord2 = nodes[parent]
#             # x2 = ecoord2 * wfactor + xscale
#             # y2 = -ecoord1 * vfactor + yscale
#             C.itemconfig(circles[parent],fill="green")
#             # oval = C.create_oval(x2 - cwidth, y2 - cwidth, x2 + cwidth, y2 + cwidth, fill="green")
#             # C.itemconfig(lines[(var,parent)],fill="red")
#             # line = C.create_line(x1, y1, x2, y2, fill="red")
#         # C.update()
#         # time.sleep(0.5)
#         if num >= 10:
#             C.update()
#             time.sleep(0.001)
#     # return [], openSet.qsize(), puzzlesRemove, improve
#     return closedSet


def puzzling(C, start, goal, nodes, edges, vfactor, wfactor, xscale, yscale, cwidth, circles, lines):
    num = 0
    sums = dict()
    closedSet = dict()
    openSet = queue.PriorityQueue()
    if start == goal:
        return closedSet
    openSet.put((findManhattan(start, goal, nodes),start,""))
    sums[start] = 0
    while openSet:
        element = openSet.get(0)
        var = element[1]
        parent = element[2]
        newList = edges[var]
        for i in newList:
            num += 1
            if i == goal:
                closedSet[i] = var
                closedSet[var] = parent
                C.itemconfig(circles[var],fill="green")
                C.itemconfig(circles[parent],fill="green")
                C.itemconfig(circles[i],fill="green")
                return closedSet
            if i in closedSet.keys(): continue
            # print("sums[var]:",sums[var])
            sums[i] = sums[var] + calcd(abs(nodes[var][0]),abs(nodes[var][1]),abs(nodes[i][0]),abs(nodes[i][1]))
            # print("sums[i]:",sums[i])
            # heuristic = findManhattan(i, goal, nodes) + sums[var]
            heuristic = calcd(abs(nodes[i][0]),abs(nodes[i][1]),abs(nodes[goal][0]),abs(nodes[goal][1])) + sums[var]
            # print("var:",i,"heuristic:",heuristic)
            openSet.put((heuristic, i, var))
            C.itemconfig(circles[i],fill="blue")
        closedSet[var] = parent
        C.itemconfig(circles[var],fill="green")
        if parent != "":
            C.itemconfig(circles[parent],fill="green")
        # print(num)
        if num >= 1000:
            C.update()
            time.sleep(0.0001)
    return closedSet


def drawMap(C, nodes, edges, vfactor, wfactor, xscale, yscale, cwidth):
    circles = dict()
    lines = dict()
    for point in edges:
        scoord = nodes[point]
        for epoint in edges[point]:
            end = nodes[epoint]
            # print("end:",end)
            # oval = C.create_oval(abs(float(scoord[0]))*wfactor - cwidth, abs(float(scoord[1]))*vfactor - cwidth, abs(float(scoord[0]))*wfactor + cwidth, abs(float(scoord[1]))*vfactor + cwidth, fill="black")
            # line = C.create_line(abs(float(scoord[0]))*wfactor,abs(float(scoord[1]))*vfactor,abs(float(end[0]))*wfactor,abs(float(end[1]))*vfactor, fill="black")
            x1 = -abs(float(scoord[1])) * wfactor + xscale
            y1 = -abs(float(scoord[0])) * vfactor + yscale
            x2 = -abs(float(end[1])) * wfactor + xscale
            y2 = -abs(float(end[0])) * vfactor + yscale
            # print("x1:", x1, "y1:", y1, "x2:", x2, "y2:", y2)
            oval = C.create_oval(x1 - cwidth, y1 - cwidth, x1 + cwidth, y1 + cwidth, fill="black")
            line = C.create_line(x1, y1, x2, y2, fill="black",width=2)
            circles[point] = oval
            lines[(point,epoint)] = line
            lines[(epoint,point)] = line
    return circles,lines

startTime = time.clock()
nodes = readNodes()
cities = assignCities()
edges = makeEdges()
start = input("start")
goal = input("goal")
# print(nodes[cities[start]])
# print(nodes[cities[goal]])
# print(findManhattan(cities[start],cities[goal],nodes))
# # s,d = sumOfEdges(nodes,edges)
# # print("Sum:",s,"miles")
# # print("cities:",cities)
# # print("edges:",edges)
# # print("nodes:",nodes)
# wfactor = 20
# vfactor = 20
wfactor = 12
vfactor = 12
h = 131 * vfactor
w = 70 * wfactor
xscale = 1600
yscale = 800
cwidth = 2
# h = 1700
# w = 800
count = 0
top = tkinter.Tk()
C = tkinter.Canvas(top, bg="white", height=h, width=w)
circles, lines = drawMap(C, nodes, edges, vfactor, wfactor, xscale, yscale, cwidth)
C.pack()
closeSet = puzzling(C, cities[start], cities[goal], nodes, edges, vfactor, wfactor, xscale, yscale, cwidth, circles, lines)
l = list()
print(closeSet)
var = cities[goal]
while len(var) > 0:
    l.append(var)
    var = closeSet[var]
l = l[::-1]
sum = 0
for i in range(len(l) - 1):
    if l[i] in cities.keys():
        print("City:",cities[l[i]].replace("_"," "))
    else:
        print("City:",l[i])
    scoord1,scoord2 = nodes[l[i]]
    x1 = scoord2 * wfactor + xscale
    y1 = -scoord1 * vfactor + yscale
    ecoord1,ecoord2 = nodes[l[i + 1]]
    x2 = ecoord2 * wfactor + xscale
    y2 = -ecoord1 * vfactor + yscale
    C.itemconfig(lines[(l[i], l[i + 1])], fill="red")
    d = calcd(scoord1, scoord2, ecoord1, ecoord2)
    print("Distance to next city:",d,"miles")
    sum += d
print("Sum:",sum,"miles")
print("Time:", str(time.clock() - startTime),"s")

# for num in range(1,10):
#     blep = C.create_oval(0,0,num * 10,num * 10)
#     C.update()
#     time.sleep(3)
top.mainloop()
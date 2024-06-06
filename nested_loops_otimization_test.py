
import time
import pprint

member_ratio_max = [['1', 0.399], ['2', 0.274], ['3', 0.396], ['4', 0.344], ['5', 0.556], ['6', 0.404], ['7', 0.453], ['8', 0.528], ['9', 0.44], ['10', 1.7], ['11', 0.621], ['12', 0.322], ['13', 0.403], ['14', 0.207], ['15', 1.704], ['16', 1.696], ['17', 0.621], ['18', 0.323], ['19', 0.406], ['20', 0.207], ['21', 1.703], ['22', 1.658], ['23', 0.609], ['24', 0.311], ['25', 0.374], ['26', 0.192], ['27', 1.663], ['28', 1.657], ['29', 0.609], ['30', 0.311], ['31', 0.375], ['32', 0.191], ['33', 1.662], ['34', 0.41], ['35', 0.274], ['36', 0.395], ['37', 0.339], ['38', 0.555], ['39', 0.404], ['40', 0.473], ['41', 0.528], 
['42', 0.44], ['43', 7.19], ['44', 1.229], ['45', 4.41], ['46', 6.36], ['47', 7.189], ['48', 0.561], ['49', 0.186], ['50', 0.571], ['51', 0.566], ['52', 0.561], ['53', 0.589], ['54', 0.22], ['55', 0.622], ['56', 0.602], ['57', 0.588], ['58', 0.561], ['59', 0.185], ['60', 0.571], ['61', 0.567], ['62', 0.562], ['63', 7.181], ['64', 1.228], ['65', 4.458], ['66', 6.352], ['67', 7.181], ['68', 0.05], ['69', 0.045], ['70', 0.05], ['71', 0.045], ['72', 0.196], ['73', 0.196], ['74', 0.197], ['75', 0.197], ['76', 0.164], ['77', 0.164], ['78', 0.072], ['79', 0.072], ['80', 0.072], ['81', 0.072], ['82', 0.163], ['83', 0.163], ['84', 0.328], ['85', 0.2], ['86', 0.192], ['87', 0.375], ['88', 0.374], ['89', 0.369], ['90', 1.731], ['91', 0.329], ['92', 0.892], ['93', 1.726], ['94', 0.2], ['95', 1.755], ['96', 0.193], ['97', 1.726], ['98', 0.369], ['99', 1.725], ['100', 0.374], ['101', 1.728], ['102', 1.732], ['103', 0.892], ['104', 1.725], ['105', 1.755], ['106', 1.726], ['107', 1.725], ['108', 0.892], ['109', 0.368], ['110', 0.309], ['111', 0.197], ['112', 0.331], ['113', 0.614], ['114', 0.367], ['115', 0.309], ['116', 0.196], ['117', 0.33], ['118', 0.614], ['119', 1.154], ['120', 0.374], ['121', 1.154], ['122', 0.374], ['123', 0.373], ['124', 1.723], ['125', 1.736], ['126', 1.725], ['127', 1.725], ['128', 1.728], ['129', 0.892], ['130', 1.723], ['131', 1.736], ['132', 1.725], ['133', 1.725], ['134', 1.154], ['135', 1.154], ['136', 0.337], ['137', 0.207], ['138', 0.209], ['139', 0.39], ['140', 0.407], ['141', 0.406], ['142', 0.406], ['143', 0.388], ['144', 0.321], ['145', 0.203], ['146', 0.339], ['147', 0.624], ['148', 1.731], ['149', 0.892], ['150', 1.726], ['151', 1.755], ['152', 1.726], ['153', 1.725], ['154', 1.732], ['155', 0.892], ['156', 1.726], ['157', 1.755], ['158', 1.726], ['159', 
1.725], ['160', 1.154], ['161', 1.154], ['162', 0.335], ['163', 0.207], ['164', 0.208], ['165', 0.389], ['166', 0.403], ['167', 0.403], ['168', 0.403], ['169', 0.387], ['170', 0.321], ['171', 0.203], ['172', 0.337], ['173', 0.623], ['174', 1.734], ['175', 0.892], ['176', 1.729], ['177', 1.775], ['178', 1.727], ['179', 1.726], ['180', 1.735], ['181', 0.892], ['182', 1.729], ['183', 1.774], ['184', 1.727], ['185', 1.726], ['186', 1.155], ['187', 1.155], ['188', 0.277], ['189', 0.365], ['190', 0.544], ['191', 0.104], ['192', 0.275], ['193', 0.33], ['194', 0.289], ['195', 0.104], ['196', 0.385], ['197', 0.385], ['198', 0.276], ['199', 0.277], ['200', 1.734], ['201', 0.892], ['202', 1.729], ['203', 1.775], ['204', 1.727], ['205', 1.726], ['206', 1.735], ['207', 0.892], ['208', 1.729], ['209', 1.774], ['210', 1.727], ['211', 1.726], ['212', 1.155], ['213', 1.155], ['214', 0.276], ['215', 0.364], ['216', 0.543], ['217', 0.104], ['218', 0.27], ['219', 0.325], ['220', 0.283], ['221', 0.104], ['222', 0.384], ['223', 0.384], ['224', 0.276], ['225', 0.277]]

# member_ratio_max = [['1', 0.399], ['2', 0.274], ['3', 0.396], ['4', 0.344], ['5', 0.556], ['6', 0.404], ['7', 0.453], ['8', 0.528], ['9', 0.44], ['10', 1.7], ['11', 0.621], ['12', 0.322], ['13', 0.403], ['14', 0.207], ['15', 1.704]]


member_ratio_max.extend(member_ratio_max)
member_ratio_max.extend(member_ratio_max)
member_ratio_max.extend(member_ratio_max)
member_ratio_max.extend(member_ratio_max)
member_ratio_max.extend(member_ratio_max)
# # member_ratio_max.extend(member_ratio_max)
# member_ratio_max.extend(member_ratio_max)
# member_ratio_max.extend(member_ratio_max)

member_stability_max = [['1', 0.399], ['6', 0.404], ['7', 0.453], ['8', 0.528], ['9', 0.44], ['10', 1.7], ['11', 0.621], ['12', 0.322], ['13', 0.403], ['14', 0.207], ['15', 1.704], ['16', 1.696], ['17', 0.621], ['18', 0.323], ['19', 0.406], ['20', 0.207], ['21', 1.703], ['22', 1.658], ['23', 0.609], ['24', 0.311], ['25', 0.374], ['26', 0.192], ['27', 1.663], ['28', 1.657], ['29', 0.609], ['30', 0.311], ['31', 0.375], ['32', 0.191], ['33', 1.662], ['34', 0.41], ['39', 0.404], ['40', 0.473], ['41', 0.528], ['42', 0.44], ['43', 1.833], ['44', 0.743], ['45', 1.182], ['46', 1.689], ['47', 1.834], ['48', 0.392], ['49', 0.186], ['50', 0.422], ['51', 0.408], ['52', 0.392], ['53', 0.459], ['54', 0.144], ['55', 0.55], ['56', 0.496], ['57', 0.456], ['58', 0.393], ['59', 0.185], ['60', 0.422], ['61', 0.409], ['62', 0.394], ['63', 1.826], ['64', 0.742], ['65', 1.183], ['66', 1.683], ['67', 1.827], ['84', 0.328], ['85', 0.2], ['86', 0.192], ['87', 0.375], ['88', 0.374], ['89', 0.369], ['91', 0.329], ['94', 0.2], ['96', 0.193], ['98', 0.369], ['100', 0.374], ['109', 0.368], ['110', 0.309], ['111', 0.197], ['112', 0.331], ['113', 0.614], ['114', 0.367], ['115', 0.309], ['116', 0.196], ['117', 0.33], ['118', 0.614], ['120', 0.374], ['122', 0.374], ['123', 0.373], ['136', 0.337], ['137', 0.207], ['138', 0.209], ['139', 0.39], ['140', 0.407], ['141', 0.406], ['142', 0.406], ['143', 0.388], ['144', 0.321], ['145', 0.203], ['146', 0.339], ['147', 0.624], ['162', 0.335], ['163', 0.207], ['164', 0.208], ['165', 0.389], ['166', 0.403], ['167', 0.403], ['168', 0.403], ['169', 0.387], ['170', 0.321], ['171', 0.203], ['172', 0.337], ['173', 0.623]]

# member_stability_max = [['1', 0.399], ['6', 0.404], ['7', 0.453], ['8', 0.528], ['9', 0.44], ['10', 1.7], ['11', 0.621], ['12', 0.322], ['13', 0.403], ['14', 0.207], ['15', 1.704]]


member_stability_max.extend(member_stability_max)
member_stability_max.extend(member_stability_max)
member_stability_max.extend(member_stability_max)
member_stability_max.extend(member_stability_max)
member_stability_max.extend(member_stability_max)
# member_stability_max.extend(member_stability_max)
# member_stability_max.extend(member_stability_max)
# member_stability_max.extend(member_stability_max)

print(len(member_ratio_max))
print(len(member_stability_max))
t0 = time.time()
ratios_list = []
operations = 0
for max_list in member_ratio_max:
    operations +=1
    for stability_list in member_stability_max:
        operations +=1
        if max_list[0] == stability_list[0]:
            if max_list[1] == 0:
                max_list[1] = 0.001

            ratios_list.append([round( (stability_list[1]/max_list[1]) , 3), max_list[0]])

print()
t1 = time.time()
print(len(ratios_list))
# pprint.pprint(ratios_list)
print(operations)
print(f'{t1-t0}')


print('\n\n')


# print(len(member_ratio_max))
# print(len(member_stability_max))
# t0 = time.time()
# ratios_list = []
# operations = 0
# for max_list in member_ratio_max:
#     operations +=1
#     for stability_list in member_stability_max:
#         operations +=1
#         if max_list[0] == stability_list[0]:
#             if max_list[1] == 0:
#                 max_list[1] = 0.001

#             ratios_list.append([round( (stability_list[1]/max_list[1]) , 3), max_list[0]])
#             break
        

# t1 = time.time()
# print(len(ratios_list))
# # pprint.pprint(ratios_list)
# print(operations)
# print(f'{t1-t0}')



# # print('\n\n')


# # print(len(member_ratio_max))
# # print(len(member_stability_max))
# # t0 = time.time()
# # ratios_list = []
# # i = 0
# # result_found = False
# # operations = 0
# # for max_list in member_ratio_max:
# #     operations += 1
# #     result_found = False
# #     for i, stability_list in enumerate(member_stability_max):
# #         operations +=1
# #         if max_list[0] == stability_list[0]:
# #             if max_list[1] == 0:
# #                 max_list[1] = 0.001
# #             ratios_list.append([round( (stability_list[1]/max_list[1]) , 3), max_list[0]])
# #             result_found = True
# #         if result_found:
# #             break
        

# # t1 = time.time()
# # print(len(ratios_list))
# # # pprint.pprint(ratios_list)
# # print(operations)
# # print(f'{t1-t0}')





print('\n\n')


print(len(member_ratio_max))
print(len(member_stability_max))




t0 = time.time()

# operations = 0


ratios_list = []
loop_range2 = len(member_stability_max)
loop_range2_maxval = member_stability_max[len(member_stability_max)-1]
print(loop_range2_maxval)
startpoint = 0
operations = 0
for max_list in member_ratio_max:
    operations +=1

    if int(max_list[0]) > int(loop_range2_maxval[0]):
        # cannot use break statement, because in case of repeating datasets
        # some of the data will be ignored
        continue

    for j in range(startpoint, loop_range2, 1):
        operations +=1
        stability_list = member_stability_max[j]

        if stability_list[0] > max_list[0]:
            break

        if max_list[0] == stability_list[0]:
            if max_list[1] == 0:
                max_list[1] = 0.001

            ratios_list.append([round( (stability_list[1]/max_list[1]) , 3), max_list[0]])
            startpoint = j+1
            break




print()
t1 = time.time()
print(len(ratios_list))
# pprint.pprint(ratios_list)
print(operations)
print(f'{t1-t0}')


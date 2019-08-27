
with open("../data/label_test_education_all_train_test_dev.txt", "r") as f: #label_tes_40_epch_segmentationt.txt #/label_test_600_epoch_segment.txt 
    match_cnt = 0
    mismatch_cnt = 0
    true_pos_dict = dict()
    false_pos_dict = dict()

    space_cnt = 0

    for line in f:
        line = line.strip()
        tokens = line.split("\t")
        print(line)
        print(tokens)
        if len(tokens)==3:
            if tokens[1]==tokens[2]:
                label = tokens[2]
                match_cnt += 1
                if label not in true_pos_dict.keys():
                    true_pos_dict[label] = 0
                true_pos_dict[label] += 1
            else:
                label = tokens[1]
                mismatch_cnt += 1
                if label not in false_pos_dict.keys():
                    false_pos_dict[label] = 0
                false_pos_dict[label] += 1
        elif len(tokens)<3:
            space_cnt += 1

    print("new_lint_cnt: ", space_cnt)
    print("match:", match_cnt)
    print("mis match:", mismatch_cnt)
    print("accuracy:", match_cnt/(match_cnt + mismatch_cnt))

    print(true_pos_dict)
    print(false_pos_dict)
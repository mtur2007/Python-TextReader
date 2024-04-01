#  inpirt / PIL, matplorlib, numpy

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


'''
-----------------------------------------------------------------------------------------------------------------
写真加工関数⬇️
'''

# function / 'set_image'
# (イメージ更新プログラム)

def set_image(image,wariai):
    
    image = Image.open(image)
    color_image = np.array(image)

    image = image.resize((int(color_image.shape[1]*wariai), int(color_image.shape[0]*wariai)))
    color_image = np.array(image)

    return color_image



# function / 'removal_background'
# 背景くり抜きプログラム

def zettai(num): #絶対値
    if num >= 0:
        return num
    if num < 0:
        return num * -1

def removal_background(color_image,RGB,kyoyou):
    Red, Green, Blue = RGB[0], RGB[1], RGB[2] #背景の色
    kyoyou = 38 #背景色の除外範囲

    code0list = np.ones((color_image.shape[0], color_image.shape[1]), dtype='i1') #一旦0で埋める


    for y in range(color_image.shape[0]):
        for x in range(color_image.shape[1]):
            if zettai(Red - color_image[y, x][0]) > kyoyou:
                if zettai(Green - color_image[y, x][1]) > kyoyou:
                    if zettai(Blue - color_image[y, x][2]) > kyoyou:
                        code0list[y, x] = 0 #背景色と類似(許容(kyoyou)範囲内)なら1で書き換え、そうでなければ0のまま


    with open("test.txt","w") as f:
        for y in range(code0list.shape[0]):
            txt = ""
            for x in range(code0list.shape[1]):
                txt = txt + str(code0list[y,x])
            f.write(txt + "\n")

    return code0list
    



# function / 'CUT'
# ブロック可視化プログラム


def sisyagonyu(num):
    if num - int(num) >= 0.5:
        return int(num) + 1
    else:
        return int(num - (num - int(num)))

def CUT(color_image,code0list,txtx,txty,width,hight,sahight):
    
    linelen = int((color_image.shape[0] - txty + sahight) // (hight + sahight))
    txtlen = int((color_image.shape[1] - txtx) // width)
    print(f"行数{linelen}, 文字数{txtlen}")

    with open("test_txtcode.txt","w") as f:
        for line in range(linelen): #行数

            for liney in range(hight):  #高さ

                txt = ""
                x = txtx

                for nouse in range(txtlen):  #文字数
                    for txtline in code0list[(liney+txty) + sisyagonyu(line*(hight+sahight)) ,sisyagonyu(x):sisyagonyu(x+width)]:
                        txt = txt + str(txtline)

                    txt = txt + "   "
                    x += width
                
                f.write(txt + "\n")
        
            f.write("\n")



# function / 'advice'
# 比率計算

def seach_txt(code0list,wariai,direction):
    seach = "background"
    txt_sfx_sy = []

    for x in range(int(code0list.shape[1])):
        if direction == 'Reversal':
            x = code0list.shape[1] - x -1

        for y in range(int(code0list.shape[0]*wariai)):
            if direction == 'Reversal':
                y = code0list.shape[0] - y -1

            if code0list[y, x] == 0:

                if seach == "background":
                    seach = "txt"
                    txt_sfx_sy.append([y, x, ""])

                break

        else:
            if seach == "txt":
                seach = "background"
                txt_sfx_sy[-1][2] = x-1

                if direction != "penetration":
                    return txt_sfx_sy[0]
                
    else: #"penetrationのみ"
        return txt_sfx_sy



def advice(code0list,wariai,hight,sahight,width):
    #写真(返答値は最初の文字[Normal])
    #ylen = color_image.shape[0]
    #line_image = np.array(image)
    #line_image[int((ylen*wariai)-ylen*0.005):int((ylen*wariai)+ylen*0.005),:] = np.array([200,0,0])
    #plt.imshow(line_image)

    block = (seach_txt(code0list, wariai, "penetration"))
    interval = []
    minimum_interval = 1000 #1000は仮置き
    for line in range(len(block)-1):
        Beforeblock = block[line][1] + (block[line][2]-block[line][1])
        Afterblock = block[line+1][1] + (block[line+1][2]-block[line+1][1])

        if minimum_interval > Afterblock - Beforeblock:
            minimum_interval = Afterblock - Beforeblock

        interval.append(Afterblock - Beforeblock)


    txtlen = 0
    word_count = 0
    for line in interval:
        word_count += line // minimum_interval
        print(line)
        txtlen += line

    print(txtlen/word_count)

    #print(f"枠 : 縦[ {hight} + (描画範囲外:{sahight}) ]  *  幅[{width}]\nブロックの大きさ(1)に対し写真側は({width/(count/txtlen)} ※これはあくまでも目安です。)")
    


# function / 'insertlist'

def insertlist(color_image,code0list,txtx,txty,width,hight,sahight):

    linelen = int((color_image.shape[0] - txty + sahight) // (hight + sahight))
    txtlen = int((color_image.shape[1] - txtx) // width)
    print(f"行数{linelen}, 文字数{txtlen}")


    Max = 0 #最大データ量調べ
    x = txtx
    for nouse in range(txtlen):
        if Max < (sisyagonyu(x + width) - sisyagonyu(x)):
            Max = (sisyagonyu(x + width) - sisyagonyu(x))
        x += width
        
    txtcode = np.array([], dtype='i1')

    with open("txtcode.txt", "w") as f:

        for line in range(linelen): #行数
            x = txtx
            for nouse in range(txtlen):  #文字数

                for liney in range(hight):  #高さ

                    txtdata = (code0list[(liney+txty) + sisyagonyu(line*(hight+sahight)) ,sisyagonyu(x):sisyagonyu(x+width)])

                    if zettai(20 - len(txtdata)) != 0:
                        for nouse in range(zettai(20 - len(txtdata))):
                            txtdata = np.insert(txtdata,0,np.array(1))
    
                    txtcode = np.append(txtcode, txtdata)
                    
                x += width

        txtcode = txtcode.reshape(linelen ,txtlen, hight, Max)


        for line in range(txtcode.shape[0]):
            for txtline in range(txtcode.shape[1]):
                for txthight in range(txtcode.shape[2]):
                    f.write(f"{(txtcode[line][txtline][txthight])}\n")
                f.write("\n")


    return txtcode,linelen,txtlen,hight,Max 


#調整が終わったら起動していくプログラム
def seach_strat(color_image,code0list,txtx,txty,width,hight,sahight):
    txtcode,linelen,txtlen,hight,Max = insertlist(color_image,code0list,txtx,txty,width,hight,sahight)
    print(f"\ntxtcode.shape{txtcode.shape}\n{txtcode}\n----------------------------")


    txt = ""
    for i in range(linelen):
        txt = ""
        for a in range(txtlen):
            a,b = seach(txtcode[i,a],Unicode)
            txt = txt + guide[b]

        print(txt)


'''
-----------------------------------------------------------------------------------------------------------------
識字元の定義関数⬇️
'''

#検出対象の文字定義

seach_txttype = []
seach = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!$%&'()*+,-./:;<=>?@[\]^_`{|}~#"
for txt in seach:
    seach_txttype.append(txt)

print(seach_txttype)



# function / backup_txtcode / [ * 重要 * : 現在までの文字コードを保存しておく] / (seach_txtcode, filename)

def backup_txtcode(seach_txtcode,filename):
    with open (filename,"w") as f: #文字コードの内容を保存しておく為のファイル[削除厳禁]
        for i in range(len(seach_txtcode)):
            f.write(f"'{str(seach_txttype[i])}'\n")

            if len(seach_txtcode[i]) == 36:

                for y in range(len(seach_txtcode[i])):

                    txt = "[ "
                    for x in range(len(seach_txtcode[i][y])-1):
                        txt = txt + f"{seach_txtcode[i][y][x]}, "
                    txt = f"{txt}{seach_txtcode[i][y][-1]} ]" 
                    f.write(txt + "\n")
            else:
                f.write("None" + "\n")

            f.write("\n")
        
        f.write("END")



# function / txtcode_selection / [実用可能な文字コードをまとめる] / (backup_filename, hight, Max) / return 指標リスト, 文字コード

def txtcode_selection(filename):
    seach_code_test = np.array([],dtype='i8')
    seach_type_test = []
    onetxt = np.array([0])
    seach = "None"
    txttype, seach_txttype = "",[]
    Nonetype = []

    with open(filename,"r") as f:
        for line in f:
            line = line.strip()

            if len(line) == 3:
                if seach == "txtdata":
                    seach_code_test = np.append(seach_code_test,onetxt)
                    seach_type_test.append(txttype)
                txttype = line[1]
                        
                txt = line[1]
                seach_txttype.append(txt)
                onetxt = np.array([],dtype='i8')

            elif line == "None":
                seach = "None"
                Nonetype.append(txttype)

            elif line != "":
                seach = "txtdata"
                for txt in line:
                    if txt == "0":
                        onetxt = np.append(onetxt,0)

                    elif txt == "1":
                        onetxt = np.append(onetxt,1)

    linelen = seach_code_test.shape[0]/(36*20)
    seach_code_test = seach_code_test.reshape(int(linelen),36,20)

    print(Nonetype)

    return seach_type_test, seach_code_test, seach_txttype



# function / restoration / [seach_txtcode復旧用プログラム] / (バックアップファイル名) / return seach_txtcode

def restoration(filename):

    seach_txtcode = []
    numlist = ""
    txt = ""

    with open(filename,"r") as f:
        for line in f:
            line = line.strip()
            if len(line) == 3:
                if len(numlist) > 1:
                    seach_txtcode.append(numlist.reshape(36,20))
                else:
                    seach_txtcode.append(txt)

                numlist = np.array([],dtype='i8')
                txt = line[1]

            elif line != "" and line != "None":
                for num in line:
                    if num == "0":
                        numlist = np.append(numlist,0)
                    elif num == "1":
                        numlist = np.append(numlist,1)

    seach_txtcode = seach_txtcode[1:]

    return seach_txtcode



# function / set_txtcode / [seach_txtcodeへ、文字コードの追加または再更新。] / (参照元のリスト, 対象のリスト, 入れる文字のタイプ, 行数, 字数)

def set_txtcode(seach_txtcode, txttype, line,txtline, txtcode):

    for num in range(len(seach_txttype)):
        if seach_txttype[num] == txttype:
            
            seach_txtcode[num] = txtcode[line,txtline]
            print(txtcode[line,txtline])

            break

    else:
        print("該当なし")
    

    return seach_txtcode

#seach_txtcode = set_txtcode(seach_txtcode,"#",6,4,txtcode)


# 文字識別関数
def seach(txtcode,Unicode):
    hozonn = 0
    line = 0

    for Uniline in range (len(Unicode)):
        a = (np.count_nonzero(txtcode == Unicode[Uniline]))
        
        if a > hozonn :
            hozonn = a
            line = Uniline
    
    return hozonn,line


#識字コードの定義
backupfile_name = "thin_seach_txtcode.txt" # このファイルに情報が入っている
guide,Unicode,seach_txttype = txtcode_selection(backupfile_name)


"""
============================================================================================================================================
"""


# マニュアル操作

imagename = "/Users/matsuurakenshin/WorkSpace/development/version=1&uuid=373F890D-0E09-4AFD-A766-6EA15D4186CB&mode=compatible&noloc=0.jpeg"

color_image = set_image(imagename,0.89) #イメージとその比率
code0list = removal_background(color_image,[36,36,36],2) #イメージ,背景色,背景色範囲

#変更可能 /  一番初めの文字の左上の位置を(txtx,txty)に代入する
txtx = 4 #一番最初の文字の一番左の座標
txty = 11 #一番最初の文字の一番上の座標

#変更不可 // ブロックの幅を変えることに対応していないので(width,hight,sahight)の値は変える事はできない
width = 19.81   #文字の幅　
hight = 36      #文字の高さ
sahight = 13.25 #余分な高さ

#CUT(color_image,code0list,txtx,txty,width,hight,sahight)
advice(code0list,1,hight,sahight,width) 

#final
#seach_strat(color_image,code0list,txtx,txty,width,hight,sahight)


#識字コードの詳細な定義

#backupfile_name = "thin_seach_txtcode.txt"

#set_txtcode(txtcode, seach_txtcode, inserttxt, linenum, txtlennum):
#backup_txtcode(seach_txtcode, backupfile_name)
#seach_txtcode = restoration(backupfile_name)



#np.count_nonzero(txtcode[10,48] == Unicode[41])
#txtcode[10,48]
#guide[41]

#shifxtnum = 2

#anser = Unicode[0,0]
#for y in range(Unicode[0,0].shape[0]):
#    for x in range(Unicode[0,0].shape[1]-shifxtnum):
#        anser[y,x+shifxtnum] = Unicode[0,0,y,x]

#print(anser)
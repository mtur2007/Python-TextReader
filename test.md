Pythonを使って、文字を認識して比較をする事ができるプログラム

line : 366 ~ 400

   1  : imagename に 写真のパスか相対パスを代入。
 code ; imagename = "_" 
                     ^

   2  : (set_image)関数の 
   　　　第１引数に  イメージのパス
   　　　第２引数に  比率(100分率ではない方)  
        を代入する。
 code ; color_image = set_image(imagename, ___ ) #イメージとその比率
                                           ^^^

   3  : (color_image)関数の
   　　　第１引数に  カラーイメージ
   　　　第２引数に  背景色 [ Red, Green, Bule ] を代入する。
        第３引数に  背景色範囲を代入する。
 code ; code0list = removal_background(color_image, [ __ , __ , __ ] , __ ) #カラーイメージ,背景色,背景色範囲
                                                      ^^   ^^   ^^     ^^

   4  : 初期描画位置の指定… 一番初めの文字の左上の位置を(txtx,txty)に代入する
 code ; #変更可能 /  一番初めの文字の左上の位置を(txtx,txty)に代入する
        txtx = __ #一番最初の文字の一番左の座標
        txty = __ #一番最初の文字の一番上の座標
               ^^

一通りできたら実行。


重労働 : ファイル [ "test_codetxt" ] を開きブロックと文字が合うまで 2 ~ 4 を続ける

final : seach_strat(color_image,code0list,txtx,txty,width,hight,sahight)を起動
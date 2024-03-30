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
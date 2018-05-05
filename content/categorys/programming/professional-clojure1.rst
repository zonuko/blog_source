Profession Clojureメモその 1
################################

:date: 2018-05-05 23:00
:tags: Clojure
:slug: pro-clojure
:summary: Profession Clojureを読む第1章

Profession Clojureって本を買ったのでメモしていこうと思います。

.. raw:: html

  <div class="kaerebalink-box" style="text-align:left;padding-bottom:20px;font-size:small;/zoom: 1;overflow: hidden;"><div class="kaerebalink-image" style="float:left;margin:0 15px 10px 0;"><a href="https://www.amazon.co.jp/exec/obidos/ASIN/B01G7S4SGK/zonuko-22/" target="_blank" ><img src="https://images-fe.ssl-images-amazon.com/images/I/51PAVy95uvL._SL160_.jpg" style="border: none;" /></a></div><div class="kaerebalink-info" style="line-height:120%;/zoom: 1;overflow: hidden;"><div class="kaerebalink-name" style="margin-bottom:10px;line-height:120%"><a href="https://www.amazon.co.jp/exec/obidos/ASIN/B01G7S4SGK/zonuko-22/" target="_blank" >Professional Clojure</a><div class="kaerebalink-powered-date" style="font-size:8pt;margin-top:5px;font-family:verdana;line-height:120%">posted with <a href="http://kaereba.com" rel="nofollow" target="_blank">カエレバ</a></div></div><div class="kaerebalink-detail" style="margin-bottom:5px;">Jeremy Anderson,Michael Gaare,Justin Holguín,Nick Bailey,Timothy Pratley Wrox 2016-05-25    </div><div class="kaerebalink-link1" style="margin-top:10px;"></div></div><div class="booklink-footer" style="clear: left"></div></div>

ちなみに章ごとです。今回は第1章です。 

第1章ではClojureが他の言語と異なる箇所について説明されています。 

============================================
再帰
============================================

Programming Clojureなり読んでると今更な感もあるんですが、触れられていました。 

通常の再帰は以下の感じになる。

.. code-block:: Clojure
  :linenos:

  (defn factorial [n]
    (if (= n 1)
      1
      (* n (factorial (- n 1)))))

上記のような再帰すると以下みたいな感じで実行されるのでメモリを食いつぶします。

.. code-block:: Clojure
  :linenos: 
   
  (factorial 6)
  (* 6 (factorial 5))
  (* 6 (* 5 (factorial 4)))
  (* 6 (* 5 (* 4 (factorial 3))))
  (* 6 (* 5 (* 4 (* 3 (factorial 2)))))
  (* 6 (* 5 (* 4 (* 3 (* 2 (factorial 1))))))
  (* 6 (* 5 (* 4 (* 3 (* 2 1)))))
  (* 6 (* 5 (* 4 (* 3 2))))
  (* 6 (* 5 (* 4 6)))
  (* 6 (* 5 24))
  (* 6 120)
  720

これを防ぐために ``recur`` を使って末尾再帰します。 ただし、 JVMは末尾呼び出し最適化をサポートしてないのでシュミレートしているだけのようです。('tail call optimazation'とあったので末尾呼び出し最適化としておきます。)

.. code-block:: Clojure
  :linenos:

  (defn factorial2 [n]
    (loop [count n acc 1] 
      (if (zero? count)
        acc
        (recur (dec count) (* acc count)))))

``recur`` が呼び出されると  ``loop`` の部分まで戻って再帰される感じです。  ``loop`` 自体はラムダ式を引数の初期値とともに作成するらしいです。 



============================================
まとめ 
============================================

- Clojureがコンパイルされたあとにどんな感じになるんかちょっと調べたいですがどうするのがいいんだろうかという気分。javapとか使えば見られるんでしょうか？
  - ``clojure.asm`` とかあるらしい?

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

第1章ではClojureの関数型の部分についてJavaと比較するような形で書かれています。
最初は細かく書こうと思ったんですが、思ったよりボリューム満点だったので適当にClojureの部分だけ要約します。

============================================
再帰
============================================

Programming Clojureとか読んでると今更な感もあるんですが、触れられていました。

通常の再帰ではスタックがあふれるので、 ``recur`` を使って末尾再帰します。 ただし、 JVMは末尾呼び出し最適化をサポートしてないのでシュミレートしているだけのようです。('tail call optimazation'とあったので末尾呼び出し最適化としておきます。)

.. code-block:: Clojure
  :linenos:

  (defn factorial2 [n]
    (loop [count n acc 1]
      (if (zero? count)
        acc
        (recur (dec count) (* acc count)))))

相互再帰は ``trampoline`` でやる感じです。ただし、サンプルでは普通の相互再帰と、 ``letfn`` でローカルに関数を2つ作ってそれを相互再帰する方も紹介されていました。
普通に相互再帰すると関数呼び出しが ``trampoline`` 付きでの呼び出しになるのが普通に関数呼び出せば良くなるのがメリットみたいです。

.. code-block:: Clojure
  :linenos:

  ;; 使うときはtrampolineなしで普通に呼べば良い
  (defn my-even? [n]
    (letfn [(e? [n] (if (zero? n) true #(o? (dec n))))
            (o? [n] (if (zero? n) false #(e? (dec n))))]
      (trampoline e? n)))

  ;; trampolineはmy-evenの中に閉じ込められているのでそのまま使える
  (defn my-odd? [n]
    (not (my-even? n)))

============================================
高階関数
============================================

特に発見とかもなかったです。 ``filter`` の例が出ていました。

.. code-block:: Clojure
  :linenos:

  (def lst ["a" "b" "c" "d"])
  (filter #(= "a" %) lst)

それ以外にもコマンドパターンの比較があったりしました。

============================================
部分適用と合成関数
============================================

 ``partial`` を使った部分適用について触れられています。
部分適用とかカリー化とか誤用の元なので触れるのに勇気がいる・・・

.. code-block:: Clojure
  :linenos:

  (def twice (partial * 2))
  (map twice [1 2 3 4 5])

関数の合成の方は ``comp`` で出来ます。評価順は右から左って感じです。

.. code-block:: Clojure
  :linenos:

  ;; 2足してから2倍する
  (map (comp (partial * 2) (partial + 2)) [1 2 3 4 5])

============================================
遅延評価
============================================

もっと使わないと全然理解が甘い気がしてて恐縮ですが、
 ``map`` とかでも ``lazy sequence`` を返してくる点が触れられています。

.. code-block:: Clojure
  :linenos:

  ;; lazy-cat全く覚えてなかった
  ;; 素朴な使い方
  (lazy-cat [1 2 3] [4 5 6])

  ;; フィボナッチ ただしプログラミングClojureで紹介されている良くないパターン
  ;; map以下では自分自身が常に変更されて計算されていくイメージ
  ;; [1 1]のときはmapの引数は[1] [1]となり、2が計算される
  ;; 2が分かると[1 1 2]となり[1 1 2]と[1 2]となり3が計算される
  ;; 3が分かると[1 1 2 3]となり[1 1 2 3]と[1 2 3]となり5が計算される
  ;; 以下無限に続くものがmapの引数となるリスト
  (def fib-seq
    (lazy-cat [1 1] (map + (rest fib-seq) fib-seq)))



============================================
まとめ
============================================

- ほとんど復習でしたが、 ``trampoline`` の使い方とか参考になりました。

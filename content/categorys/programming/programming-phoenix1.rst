Programming Phoenix勉強その1
################################

:date: 2016-12-28 21:50
:tags: Elixir,Phoenix
:slug: programming-phoenix1
:summary: Programming Phoenixって本を読むその1

| 買ってあったけど読んでなかったので読みます.プログラミングElixirは原著の方も翻訳の方も一応読んでます.
| プログラミングElixirについては色々なところで書評なり見る気がするけど,こっちの方は余り見ない気がします.
|

.. raw:: html
  
  <div class="amazlet-box" style="margin-bottom:0px;"><div class="amazlet-image" style="float:left;margin:0px 12px 1px 0px;"><a href="http://www.amazon.co.jp/exec/obidos/ASIN/1680501453/zonuko-22/ref=nosim/" name="amazletlink" target="_blank"><img src="https://images-fe.ssl-images-amazon.com/images/I/41pPn50VnvL._SL160_.jpg" alt="Programming Phoenix: Productive, Reliable, Fast" style="border: none;" /></a></div><div class="amazlet-info" style="line-height:120%; margin-bottom: 10px"><div class="amazlet-name" style="margin-bottom:10px;line-height:120%"><a href="http://www.amazon.co.jp/exec/obidos/ASIN/1680501453/zonuko-22/ref=nosim/" name="amazletlink" target="_blank">Programming Phoenix: Productive, Reliable, Fast</a><div class="amazlet-powered-date" style="font-size:80%;margin-top:5px;line-height:120%">posted with <a href="http://www.amazlet.com/" title="amazlet" target="_blank">amazlet</a> at 17.04.16</div></div><div class="amazlet-detail">Chris Mccord Bruce Tate Jose Valim <br />Pragmatic Bookshelf <br />売り上げランキング: 3,667<br /></div><div class="amazlet-sub-info" style="float: left;"><div class="amazlet-link" style="margin-top: 5px"><a href="http://www.amazon.co.jp/exec/obidos/ASIN/1680501453/zonuko-22/ref=nosim/" name="amazletlink" target="_blank">Amazon.co.jpで詳細を見る</a></div></div></div><div class="amazlet-footer" style="clear: left"></div></div>
   
|
| ちなみに実際にコードを書くPart1のChapter2からやってきます.
| あとPhoenix自体は何回か触ってます.趣味で.
|

===================
前提
===================

- PostgreSQL9.5
- Elixir 1.3.2
- Phoenix Framework1.2.1

本より新し目のバージョンにしてるので,色々問題ありそうですが頑張る感じで行きます.

=================
初期構築
=================

プロジェクトテンプレートの生成としてはじめに以下のコマンドを入力します.

.. code-block:: shell
  :linenos:

  $ mix phoenix.new hello
  * creating hello/ config/ config.exs
    ...

  Fetch and install dependencies? [Yn] y
  * running mix deps.get
  * running npm

| これでカレントディレクトリにhelloってフォルダが掘られて,色々勝手に整備してくれる.
| 次に以下のコマンドでDB作ったりします.

.. code-block:: shell
  :linenos:

  $ cd hello
  hello $ mix ecto.create
  ==> connection
  Compiling 1 file （.ex）
  Generated connection app
  ...

| これで ``hello_dev`` とか言うデータベースができていればOKです.
| 出来てなければ, ``config/dev.exs`` ってファイルにDBとの接続設定があるので見直します.
|

========
起動
========

以下のコマンドでサーバー起動.

.. code-block:: shell
  :linenos:

  $ cd hello
  $ mix phoenix.server

| ``mix phoenix.server`` の部分は ``iex -S mix phoenix.server`` でもOK.こちらはIEXの内部でサーバーが起動する.
| ちなみにデフォルトでは ``localhost:4000`` で起動する.
|

===============
ルーティング
===============

特定のURLとのルーティングを行うには, ``web/router.exs`` に設定を書く.


.. code-block:: Elixir
  :linenos:

  defmodule Hello.Router do
    # 省略

    scope "/", Hello do
      pipe_through :browser # Use the default browser stack

      get "/hello", HelloController, :world  # 追加
      get "/", PageController, :index
    end

    # Other scopes may use custom stacks.
    # scope "/api", Hello do
    #   pipe_through :api
    # end
  end

| 見ればなんとなくわかると思いますが, ``get`` マクロに対して色々ルーティングの設定をします.
| この場合は ``/hello`` にアクセスが来たら ``HelloController`` （モジュール）の ``:world`` アクション（関数）を呼び出すようにしてます.
| ただ,この段階だと ``HelloController`` がないのでアクセスしてもエラー画面です.
| エラー画面が若干本と違ってたので貼っておきます.

.. image:: /images/Phoenix_error.jpg
  :alt: Quicksilver

|

Controller実装
==================

エラーを解消するために ``web/controllers/hello_controller.ex`` を以下の内容で作ります.

.. code-block:: Elixir
  :linenos:

  defmodule Hello.HelloController do
    use Hello.Web, :controller

    def world（conn, _param） do
      render conn, "world.html"
    end
  end

| ファイル名はController名をスネークケース,モジュール名は, （ ``scope`` で設定した名前） ``.`` （ ``get`` に設定したController名）で作ります.
| （ココらへんの理解が微妙に曖昧）
| で,また ``/hello`` にアクセスすると,今度はviewがないと怒られます。
|

View実装
================

| ``web/views/hello_view.ex`` を以下の内容で作ります.

.. code-block:: Elixir
  :linenos:

  defmodule Hello.HelloView do
    use Hello.Web, :view
  end

| で,今度はtemplateが無いって怒られるのでまた作ります.
|

Template実装
================

| ``web/templates/world.html.eex`` を以下の内容で作ります.

.. code-block:: html
  :linenos:

  <h1>From template: Hello world!</h1>

これで晴れて ``/hello`` にアクセスしても怒られなくなります.

=========================
Routing時のパラメータ
=========================

| 次に,ルーティング時にパラメータを渡す方法を実装します.
| （ ``/hoge/1/`` のような感じに）
| ``web/router.ex`` に上の方で追加したルーティング設定を修正します.

.. code-block:: Elixir
  :linenos:

  get "/hello/:name", HelloController, :world

| こうすると ``:name`` の部分が色々変えられてControllerに渡されてきます.
| なので,Controllerを以下のように変更して渡された値を取得できるようにします.

.. code-block:: Elixir
  :linenos:

  def world(conn, %{"name" => name}) do
    render conn, "world.html", name: name
  end

| パターンマッチにより渡されてきた値が ``name`` にバインドされます.
| パターンマッチについては本の中で解説されてますが,飛ばします.プログラミングElixirとかElixirのチュートリアルとか読んでもらえれば.
| 最後に,template側で渡された値を表示するようにしてあげれば完成.

.. code-block:: html
  :linenos:

  <h1>Hello <%= String.capitalize @name %>!</h1>

| ``<%= ～ %>`` の部分にElixirの関数が書けて, ``@name`` の部分にControllerから渡された値が入ってくるようです.
|

==============
まとめ
==============

| とりあえず今回はここまでとしておきます。
| かなり復習感ありましたが,基本的な部分はなんとなくわかったと思います。
| やっぱりRailsにかなり近くて,Railsやってた人はここらへんはあまり深く読まなくても良い気がします.
| あと名前付けとかのルールとかは追々という感じで調べていきたいです.

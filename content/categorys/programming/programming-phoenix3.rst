Programming Phoenix勉強その3
################################

:date: 2017-01-01 00:50
:tags: Elixir,Phoenix
:slug: programming-phoenix3
:related_posts: programming-phoenix3
:summary: Programming Phoenixって本を読むその3

| その3です。
| その2の続きです。
| 今回からChpater3です.
| このChapterではまず ``rumbl`` と呼ばれるアプリを作ります.
| ビデオにたいしてリアルタイムでコメントを付けられるアプリになる予定らしい.
|

====================
準備
====================

| Chapter1と同様に以下のコマンドでPhoenixの新しいプロジェクトを作成します.（詳細は割愛）
.. code-block:: shell
  :linenos:

  $ mix phoenix.new rumbl
  * creating rumbl/ config/ config.exs
    ...

  Fetch and install dependencies? [Yn] y
  * running mix deps.get
  * running npm

  $ cd rumbl
  rumbl $ mix ecto.create
  ==> connection
  Compiling 1 file （.ex）
  Generated connection app
  ...



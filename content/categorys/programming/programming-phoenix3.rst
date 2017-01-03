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


=====================================
Modelの追加
=====================================

| 実際はコマンドで自動生成されるものを手製で実装します.
| ``web/models/user.ex`` を以下の内容で実装します.

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.User do
    defstruct [:id, :name, :username, :password]
  endD

| これは ``id, name, username, password`` 構造体として持つUserモジュールです.

===============================
Repositoryの変更
===============================

| 現段階では,RepositoryはRDBからではなく独自にハードコーディングします.
| このようにすることで,データの概念とデータベースの概念が分離されていることがわかります.
| （ ``Repo`` と ``Model`` として）
| まず, ``lib/rumbl/repo.ex`` を以下のように変更します.
|

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.Repo do
    @moduledoc """
    In memory repository.
    """

    def all(Rumbl.User) do
      [%Rumbl.User{id: "1", name: "Jose", username: "josevalim", password: "elixir"},
      %Rumbl.User{id: "2", name: "Bruce", username: "redropids", password: "7longs"},
      %Rumbl.User{id: "3", name: "Chris", username: "chrismccord", password: "phx"}]
    end

    def all(_module), do: []

    def get(module, id) do
      Enum.find all(module), fn map -> map.id == id end
    end

    def get_by(module, params) do
      Enum.find all(module), fn map ->
        Enum.all?(params, fn {key, val} -> Map.get(map, key) == val end)
      end
    end
  end

| ``Ecto`` を使わないようにしたので, ``lib/rumbl.ex`` を編集して上記の ``repo.ex`` をプロセス管理対象から外します.
|

.. code-block:: Elixir
  :linenos:

  # Start the Ecto repository
  # supervisor(Rumbl.Repo, []), # これをコメントアウト

| 上手く行っているか試すにはコンソールでプロジェクトフォルダに移動して ``iex -S mix`` コマンドで ``iex`` を起動します.
|

.. code-block:: shell
  :linenos:

  rumbl $ iex -S mix
  Erlang/OTP 19 [erts-8.2] [source] [64-bit] [smp:4:4] [async-threads:10] [hipe] [kernel-poll:false] [dtrace]

  Compiling 7 files (.ex)
  Interactive Elixir (1.3.4) - press Ctrl+C to exit (type h() ENTER for help)
  iex(1)> alias Rumbl.User
  Rumbl.User
  iex(2)> alias Rumbl.Repo
  Rumbl.Repo
  iex(3)> Repo.all User
  [%Rumbl.User{id: "1", name: "Jose", password: "elixir", username: "josevalim"},
   %Rumbl.User{id: "2", name: "Bruce", password: "7longs", username: "redropids"},
   %Rumbl.User{id: "3", name: "Chris", password: "phx", username: "chrismccord"}]
  iex(4)> Repo.all Rumbl.Other
  []
  iex(5)> Repo.get User, "1"
  %Rumbl.User{id: "1", name: "Jose", password: "elixir", username: "josevalim"}
  iex(6)> Repo.get_by User, name: "Brunce"
  nil
  iex(7)> Repo.get_by User, name: "Bruce"
  %Rumbl.User{id: "2", name: "Bruce", password: "7longs", username: "redropids"}
  iex(8)>

========================================
Controllerの実装
========================================

| 上記で作成した ``Repository`` を扱う ``Controller`` を実装します.
| まず,専用のルーティング設定を ``web/router.ex`` に設定します.
|

.. code-block:: Elixir
  :linenos:

  scope "/", Rumbl do
    pipe_through :browser # Use the default browser stacks.

    get "/users", UserController, :index     # 追加
    get "/users/:id", UserController, :show  # 追加
    get "/", PageController, :index
  end

| みて分かる通り ``UserControler`` の ``index`` アクションと ``show`` アクションに対応するルーティング設定を行います.
| ``get`` マクロはHTTPメソッドのGETで呼び出されることを想定されています.
| 次に,設定したルーティングに対応する ``Controller`` を実装します.
|

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.UserController do
    use Rumbl.Web, :controller
  
    def index(conn, _params) do
      users = Repo.all(Rumbl.User)
      render conn, "index.html", users: users
    end
  end

| ``hello`` アプリで作成したものと対して変わらないと思います.
| 違いは ``Repo.all/1`` 関数でユーザ一覧を取ってきてることくらいだと思います.
| この時点でもまだ ``View`` がないとエラーになるので, ``View`` の実装をします.
|

====================
Viewの実装
====================

| ``View`` を以下の内容で実装します.
| 

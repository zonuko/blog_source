Programming Phoenix勉強その7
################################

:date: 2017-01-15 17:52
:tags: Elixir,Phoenix
:slug: programming-phoenix7
:related_posts: programming-phoenix6
:summary: Programming Phoenixって本を読むその7

| その7です。
| ここからchapter5です。認証周りをやるらしいです。
|

==================================
パスワードのハッシュ化
==================================

| まずはパスワードのハッシュ化を行います。必要なライブラリをインストールするために ``mix.exs`` に以下のように追記を行います。
| 

.. code-block:: Elixir
  :linenos:

    ...
  def application do
    [mod: {Rumbl, []},
     applications: [:phoenix, :phoenix_pubsub, :phoenix_html, :cowboy, :logger, :gettext,
                    :phoenix_ecto, :postgrex, :comeonin]] # comeoninを追加
  end
    ...
  defp deps do
    [{:phoenix, "~> 1.2.1"},
     {:phoenix_pubsub, "~> 1.0"},
     {:phoenix_ecto, "~> 3.0"},
     {:postgrex, ">= 0.0.0"},
     {:phoenix_html, "~> 2.6"},
     {:phoenix_live_reload, "~> 1.0", only: :dev},
     {:gettext, "~> 0.11"},
     {:cowboy, "~> 1.0"},
     {:comeonin, "~> 2.0"}] # 追加
  end

| ``application`` に対して追加しているのはこのアプリの依存ライブラリを書いているようです。
| ``comeonin`` とか言うライブラリを追加しています。 `リポジトリ <https://github.com/riverrun/comeonin>`_ を見るとそのまんまパスワードをハッシュ化してくれるライブラリだとわかります。
| ``mix deps.get`` で追加できたらモデルでこいつを使うように変更してやります。
|

.. code-block:: Elixir
  :linenos:

  def changeset(model, params \\ %{}) do
    model
    |> cast(params, [:name, :username]) # 更新予定のパラメータカラムを第三引数でとる(?)
    |> validate_required([:name, :username]) # このリストがcastが返すchangesetに存在するか検証
    |> validate_length(:username, min: 1, max: 20)
  end

  def registration_changeset(model, params) do
    model
    |> changeset(params)
    |> cast(params, [:password])
    |> validate_required([:password])
    |> validate_length(:password, min: 6, max: 100)
    |> put_pass_hash()
  end

  defp put_pass_hash(changeset) do
    case changeset do
      %Ecto.Changeset{valid?: true, changes: %{password: pass}} ->
        put_change(changeset, :password_hash, Comeonin.Bcrypt.hashpwsalt(pass))
      _ ->
        changeset
    end
  end

| ``Ecto`` の最新版を使っているので書籍と若干異なっています。新しい方の ``Ecto`` では ``cast/4`` は推奨されなくなっているようです。
| なので、 `Phoenixのガイド <http://www.phoenixframework.org/docs/ecto-models>`_ とか、 `Ectoのドキュメント <https://hexdocs.pm/ecto/Ecto.Changeset.html>`_ とかを見て適当に修正してます。（このやり方でいいか不安ですが・・・）
| また、 ``:empty`` もWarningになるので、空のハッシュに変えています。
| ついでに ``create`` アクションで ``User.changeset`` の部分を ``User.registration_changeset`` に変更します。
| ここまでやってMacだとOKでしたが、Windowsだとエラーになりました。
|

==================================
Windowsでのエラー（comeonin）
==================================

| Windowsから ``comeonin`` を使おうとするとコンパイルを促すエラーが出るので `ここ <https://github.com/riverrun/comeonin/wiki/Requirements>`_ を参考にコンパイルします。
| ちなみにVisualStudioインストールしてあったので最下部付近にあるVSインストール済みの場合の方法を取っています。

#. VSに付属している開発者コマンドプロンプトを起動します。
#. 開発者コマンドプロンプト上で以下のコマンドを実行しておきます。

.. code-block:: shell
  :linenos:

  > vcvarsall.bat amd64

#. ``vcvarsall.bat`` にパスが通ってない場合は、適当にフルパスで指定すればいいと思います。これを行わなくてもコンパイル自体は出来ますが、実行時にエラーになりました。（ ``vcvarsall.bat`` については `MSDN <https://msdn.microsoft.com/ja-jp/library/x4d2c09s.aspx>`_ ）
#. 本プロジェクト（ ``rumbl`` ）のディレクトリまで移動して以下のコマンドを実行します。

.. code-block:: shell
  :linenos:

  rumbl > mix deps.compile

| 自分の環境ではこれでうまくいきました。
|

==================================
Plugについて
==================================

| ``Plug`` を使ってログイン機能を作る前に ``Plug`` についてちょっと掘ります。

- ``Plug`` にはモジュールプラグと関数プラグの二種類が存在する。
- モジュールプラグは名前の通り幾つかの関数を集めたモジュールのプラグ
- 関数プラグは関数名をアトムとして指定したプラグ

| ログイン機能としてモジュールプラグを作成します。
|

モジュールプラグ
==================================

| モジュールプラグとして設定するモジュールには ``init/1`` 関数と ``call/2`` 関数が必要とされます。
| 以下は何もしないモジュールプラグの例です。

.. code-block:: Elixir
  :linenos:

  defmodule NothingPlug do
    def init(opts) do
      opts
    end

    def call(conn, _opts) do
      conn
    end
  end

| ``call`` 関数の引数を見るとわかりますが、モジュールプラグは ``conn`` を変換するようです。
|

Plug.Connについて(conn)
==================================

| ``Plug.Conn`` が持つフィールドについて見てみます。
| 書籍の方には色々書いてありますが割愛します。 `Plug.Connの公式ドキュメント <https://hexdocs.pm/plug/Plug.Conn.html>`_ を参照して下さい。ここではリクエストフィールドが持つものだけを見てみます。
|

- ``host``
    リクエストのホスト名 ex) www.pragprog.com

- ``method``
    リクエストのWebメソッド（GETとかPOSTとか）

- ``path_info``
    パスを分割したリスト

- ``req_headers``
    リクエストヘッダ

- ``scheme``
    プロトコル（httpとか）

| Webのリクエスト周りに関係するものが存在していることがわかります。
|

認証プラグの実装
=======================

| やっと認証用のプラグを実装します。
| ``controllers/auth.ex`` を以下の内容で実装します。
|

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.Auth do
    import Plug.Conn
  
    def init(opts) do
      # キーワードリストから:repoの箇所の値を取得する
      # 無ければexception(つまりは必須)
      Keyword.fetch!(opts, :repo)
    end
  
    def call(conn, repo) do
      user_id = get_session(conn, :user_id)
      user = user_id && repo.get(Rumbl.User, user_id)
      # assignでconnを変更する(importされた関数)
      # これによって:current_userがコントローラやビューで使えるようになる
      assign(conn, :current_user, user)
    end
  end

| コメント通りなので余り言うことはないです。
| ``init`` で ``repo`` を取得してそれが ``conn`` の第二引数に渡されるようです。セッションにあるユーザIDからユーザを取得しています。
| パイプラインの流れの一部として処理してほしいので ``router.ex`` を以下のように変更します。
| 

.. code-block:: Elixir
  :linenos:

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_flash
    plug :protect_from_forgery
    plug :put_secure_browser_headers
    plug Rumbl.Auth, repo: Rumbl.Repo # 追加
  end

アクセス制限の実装
=======================

| ``Plug`` は出来たのでアクセス制限とログインを作ります。ログインしない限りは ``:index`` アクションと ``:show`` アクションにアクセス出来ないようにします。
| ``user_controller.ex`` を以下のように変更します。
|

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.UserController do
    ...
    def index(conn, _params) do
      case authenticate(conn) do
        # 構造体connのhaltedメンバのパターンマッチによる振り分け
        %Plug.Conn{halted: true} = conn ->
          conn
        conn ->
          users = Repo.all(Rumbl.User)
          render conn, "index.html", users: users
      end
    end
    ...
    defp authenticate(conn) do
      # Plugで追加したassignの呼び出しが可能かどうか
      if conn.assigns.current_user do
        conn
      else
        conn
        |> put_flash(:error, "You must be logged in to access that page")
        |> redirect(to: page_path(conn, :index))
        |> halt()
      end
    end
  end

| 先程の ``Plug`` で変更した値を ``authenticate/1`` 関数で使っています。また、 ``:index`` アクションのアクセス時に ``authenticate`` 関数で認証済みかチェック掛けています。
|

``authenticate`` の関数プラグ化
======================================

| ``user_controller.ex`` の ``Rumbl.Web`` の直下のあたりに以下を追加します。
|

.. code-block:: Elixir
  :linenos:

  plug :authenticate when action in [:index, :show]

| また、 ``index`` アクションを ``case`` 文を使う以前のものに戻しておきます。 ``authenticate`` 関数も以下のように2引数にしておきます。
|

.. code-block:: Elixir
  :linenos:

  defp authenticate(conn, _opts) do
    # Plugで追加したassignの呼び出しが可能かどうか
    if conn.assigns.current_user do
      conn
    else
      conn
      |> put_flash(:error, "You must be logged in to access that page")
      |> redirect(to: page_path(conn, :index))
      |> halt()
    end
  end

| ``_opts`` を追加しただけです。関数 ``Plug`` 化したためです。 ``Plug`` をマクロ展開したときの例が出てますが割愛します。
|

ログインの実装
======================================



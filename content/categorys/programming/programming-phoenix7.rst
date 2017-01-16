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

| まずはパスワードのハッシュ化を行います。必要なライブラリをインストールするために ``mix.exs`` に以下のように追記をお行います。
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
| また、 ``:empty`` もWarningになるので、空の構造体に変えています。
| ここまでやってMacだとOKでしたが、Windowsだとエラーになりました。
|

==================================
Windowsでのエラー（Comeonin）
==================================

| Windowsから ``comeonin`` を使おうとするとコンパイルを促すエラーが出るので `ここ <https://github.com/riverrun/comeonin/wiki/Requirements>`_ を参考にコンパイルします。
| ちなみにVisualStudioインストールしてあったので最下部付近にあるVSインストール済みの場合の方法を取っています。

- VSに付属している開発者コマンドプロンプトを起動します。
- 開発者コマンドプロンプト上で以下のコマンドを実行しておきます。

.. code-block:: shell
  :linenos:

  > vcvarsall.bat amd64

- ``vcvarsall.bat`` にパスが通ってない場合は、適当にフルパスで指定すればいいと思います。これを行わなくてもコンパイル自体は出来ますが、実行時にエラーになりました。
  （ ``vcvarsall.bat`` については `ここ <https://msdn.microsoft.com/ja-jp/library/x4d2c09s.aspx>`_ ）
- 本プロジェクト（ ``rumbl`` ）のディレクトリまで移動して以下のコマンドを実行します。

.. code-block:: shell
  :linenos:

  rumbl > mix deps.compile

| 自分の環境ではこれでうまくいきました。

Programming Phoenix勉強その6
################################

:date: 2017-01-11 17:52
:tags: Elixir,Phoenix
:slug: programming-phoenix6
:related_posts: programming-phoenix5
:summary: Programming Phoenixって本を読むその6

| その6です。
| 実際にDBを操作するところからです。
|

=========================
新規ユーザ生成処理
=========================

| ``Rumbl.UserController`` に以下の関数を実装します。
|

.. code-block:: Elixir
  :linenos:

  def new(conn, _params) do
    changeset = User.changeset(%User{})
    render conn, "new.html", changeset: changeset
  end

| ``changeset`` 周りとかが謎めいていますが一旦置いときます。単に自分が今理解してないだけですが・・・
| DBの操作とそれ以外の検証とかエラーとかセキュリティとかを分離するのに役立つっぽいです。
| ``user.ex`` に上記で利用している ``User.changeset`` 関数を実装します。
|

.. code-block:: Elixir
  :linenos:

  def changeset(model, params \\ :empty) do
    model
    |> cast(params, ~w(name username), [])
    |> validate_length(:username, min: 1, max: 20)
  end

| ``Ecto`` を使う関数を定義しました。 ``cast`` で ``Ecto.changeset`` を生成してバリデーションチェックを掛けているようです。
|

=========================
前準備
=========================

| ``:new`` アクションを実装する前に前準備をします。
| 今まで書いてあったルーティング設定を消して以下を追加します。まぁ説明不要だと思います。
|

.. code-block:: Elixir
  :linenos:

  resouces "/users", UserController, only: [:index, :show, :new, :create]

=========================
テンプレート実装
=========================

| ``:new`` に対応するテンプレートを適当に作ります。
|

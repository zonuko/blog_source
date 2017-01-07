Programming Phoenix勉強その5
################################

:date: 2017-01-09 00:43
:tags: Elixir,Phoenix
:slug: programming-phoenix5
:related_posts: programming-phoenix4
:summary: Programming Phoenixって本を読むその5

| その5です。ここからChapter4です。
| ``Ecto`` を使って独自実装してた ``Repository`` を ``Postgres`` に置き換えていきます。
| まず ``lib/rumbl/repo.ex`` をもとに戻します。
|

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.Repo do
    use Ecto.Repo, otp_app: :rumbl
  end

| さらに ``lib/rumbl.ex`` でコメントアウトした部分をもとに戻します。
|

.. code-block:: Elixir
  :linenos:

  # Start the Ecto repository
  supervisor(Rumbl.Repo, []), # ここのコメントアウトを戻す

| まだ ``mix ecto.create`` をしてなければしておきます。
|

=========================
modelの実装
=========================

| 次に ``model`` の実装を行います。
| ``web/model/user.ex`` を以下の内容で実装します。
|

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.User do
    use Rumbl.Web, :model
  
    schema "users" do
      field :name, :string
      field :username, :string
      field :password, :string, virtual: true
      field :password_hash, :string
  
      timestamps
    end
  end

| ``ActiveRecord`` 使ったことがあればそんなに違和感なく受け入れられると思います。
| ``:virtual`` オプションは値として受け取るが、DBには保存しない値です。
| ここまで行って起動してみたら以下のような警告が出ました。
|

.. code-block:: shell
  :linenos:

  warning: variable "timestamps" does not exist and is being expanded to "timestamps()", 
  please use parentheses to remove the ambiguity or change the variable name
    web/models/user.ex:10

| ``timestamps`` が変数なのか ``timestamps/0`` の関数呼び出しか曖昧だと言われてるようです。
| 今回は ``timestamps/0`` の呼び出しなので ``timestamps`` の部分を ``timestamps()`` にすると警告がでなくなります。 `ここらへん <http://www.phoenixframework.org/docs/ecto-models>`_ を参考にしました。
|
| 最後に ``web/web.ex`` の ``model`` 関数を以下のように変更します。

.. code-block:: Elixir
  :linenos:

  def model do
    quote do
      use Ecto.Schema

      import Ecto
      import Ecto.Changeset
      import Ecto.Query, only: [from: 1, from: 2] # only以下を追加
    end
  end

|
